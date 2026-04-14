from pydantic import BaseModel
from typing import Any
from typing import Optional

class Companyinfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: list[str] = []
    competitors: list[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: list[str] = []
    integration_capabilities: list[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent    

  
class ResearchState(BaseModel):
    query:str
    extracted_tools:list[str]=[]
    companies:list[Companyinfo]=[]
    analysis:Optional[str]=None
    search_results:list[str,Any]


class CompanyAnalysis(BaseModel):
    pricing_model:str #free, freemium, premium, unknown
    api_available:Optional[bool]=None
    is_open_source:Optional[bool]=None
    description:str=""
    language_support:list[str]=[]
    integration_capabailties:list[str]=[]
    tech_stack:list[str]=[]