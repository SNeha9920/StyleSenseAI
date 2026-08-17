from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class SkinScore(BaseModel):
    name: str
    score: Optional[float] = None


class SkinAnalysisStartResponse(BaseModel):
    analysis_id: int
    youcam_task_id: str
    status: str


class SkinAnalysisResultResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    status: str

    image_url: Optional[str] = None

    skin_health_score: Optional[float] = None
    hydration_score: Optional[float] = None
    texture_score: Optional[float] = None
    brightness_score: Optional[float] = None
    acne_score: Optional[float] = None

    skin_type: Optional[str] = None
    skin_tone: Optional[str] = None

    concerns: List[str] = []

    # AI-generated content
    ai_summary: Optional[str] = None
    ai_recommendation: Optional[str] = None

    # AI skincare plan
    recommended_routine: Optional[Dict[str, Any]] = None
    recommended_ingredients: Optional[List[Any]] = None
    recommended_products: Optional[List[Any]] = None

    analyzed_at: Optional[datetime] = None

    raw_result: Optional[Dict[str, Any]] = None


class SkinAnalysisHistoryItem(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int

    skin_health_score: Optional[float] = None
    hydration_score: Optional[float] = None
    texture_score: Optional[float] = None
    brightness_score: Optional[float] = None
    acne_score: Optional[float] = None

    ai_summary: Optional[str] = None

    analyzed_at: datetime


class SkinAnalysisHistoryResponse(BaseModel):

    analyses: List[SkinAnalysisHistoryItem]

    total: int