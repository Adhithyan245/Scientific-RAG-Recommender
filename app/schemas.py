from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class RecommendationRequest(BaseModel):
    research_objective: str
    sample_type: str
    domain: str
    sensitivity: Optional[str] = None
    resolution: Optional[str] = None
    constraints: Optional[str] = None
    debug: Optional[bool] = False

class RecommendationItem(BaseModel):
    instrument: str
    reasoning: str
    alternatives: List[str]
    limitations: str
    score: float

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    confidence: float
    confidence_explanation: str
    warnings: List[str]
    debug_info: Optional[Dict[str, Any]] = None
