import requests as req
from bs4 import BeautifulSoup as  bsoup
from dotenv import load_dotenv
from duckduckgo_search import DDGS as ddgs
from html2text  import HTML2Text
from time import sleep

load_dotenv()

class scraper:
    def crawl_companies(self, query:str, num_results:int=5)->list[str]:
        urls=[]
        try:
            response=ddgs().text(query,max_results=5)
            for r in response:
                url=r['href']
                urls.append(url)
                sleep(1)
        except Exception as e:
            print(e)
        return urls
    
    def scrape_companies(self, url:str)->str:
        response=req.get(url, timeout=2)  #Get the web page
        if response.status_code==200:
            output=bsoup(response.content, 'html.parser') #parse it into html.parser format
            #Convert to markdown format
            converter=HTML2Text()
            converter.ignore_links=False
            result=converter.handle(str(output))        
            return result
        else:
            print("Error Loading data", response.status_code)
            return False
    