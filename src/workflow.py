from typing import Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI as gemini
from langgraph.checkpoint.memory import MemorySaver
from .models import CompanyAnalysis,Companyinfo,ResearchState
from .prompts import DeveloperToolsPrompts
from .scrape import scraper

class Workflow:
    def __init__(self):
        self.llm=gemini(model="gemini-2.5-flash", temperature=.7)
        self.prompts=DeveloperToolsPrompts()
        self.scrape=scraper()
        self.workflow=self.__build_workflow()
    
    def __build_workflow(self):
        graph=StateGraph(ResearchState)
        graph.add_node("extract_tools", self.__extract_tools_step)
        graph.add_node("research", self.__research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()
    
    def __extract_tools_step(self,state:ResearchState)->dict[str,Any]:
        print(f"Finding articles about {state.query}")
        
        article_query=f"{state.query} tools comparision best alternatives"
        all_content=""
        search_results=self.scrape.crawl_companies(article_query)
        
        for result in search_results:
            data=self.scrape.scrape_companies(result)
            if data:
                all_content+data[:1500]+"\n\n"
            
        messages=[
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(query=state.query,content=all_content))
        ]
        
        try:
            response=self.llm.invoke(messages)
            tool_names=[
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print(f"Extracted Tools: {tool_names}")
            return {"extracted_tools": tool_names}
        except Exception as e:
            print(e)
            return {"extracted_tools:",[] }
    
    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )
            
    def __research_step(self,state:ResearchState)->dict[str,Any]:
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            print("⚠️ No extracted tools found, falling back to direct search")
            search_results = self.scrape.crawl_companies(state.query, num_results=4)
            tool_names = [
                result
                for result in search_results
            ]
        else:
            tool_names = extracted_tools[:4]

        print(f"🔬 Researching specific tools: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            tool_search_results = self.scrape.crawl_companies(tool_name + " official site", num_results=1)

            if tool_search_results:
                result = tool_search_results
                url = result.get("url", "")

                company = Companyinfo(
                    name=tool_name,
                    description=result,
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                scraped = self.scrape.scrape_companies(url)
                if scraped:
                    content = scraped
                    analysis = self._analyze_company_content(company.name, content)

                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities

                companies.append(company)

        return {"companies": companies}
    
    def _analyze_step(self, state: ResearchState) -> dict[str, Any]:
        print("Generating recommendations")

        company_data = ", ".join([
            company.model_dump_json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}

    def run(self, query: str) -> ResearchState:
        search_results = self.scrape.crawl_companies(query, num_results=3)
        initial_state = ResearchState(query=query,search_results=search_results)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)