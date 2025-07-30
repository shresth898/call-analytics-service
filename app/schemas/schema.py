from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CallBase(BaseModel):
    agent_id: str
    customer_id: str
    language: str
    start_time: datetime
    duration_seconds: int
    transcript: str


class CallCreate(CallBase):
    call_id: str

class CallOut(CallBase):
    call_id: str
    agent_talk_ratio: Optional[float] = None
    customer_sentiment_score: Optional[float] = None

    class Config:
        orm_mode = True


class CallListResponse(BaseModel):
    calls: List[CallOut]
    total: int

class CallRecommendationResponse(BaseModel):
    similar_calls: List[str]
    nudges: List[str]


class AgentAnalytics(BaseModel):
    agent_id: str
    average_sentiment: float
    average_talk_ratio: float
    total_calls: int

class AgentAnalyticsResponse(BaseModel):
    agents: List[AgentAnalytics]
