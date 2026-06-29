from pydantic import BaseModel
from typing import Optional


class SubredditCreate(BaseModel):
    name: str
    is_nsfw: bool = False
    category: Optional[str] = None
    manual_blocked: bool = False
    manual_allowed: bool = False
    confidence: float = 1.0
    source: str = "manual"
    description: Optional[str] = None


class SubredditUpdate(BaseModel):
    is_nsfw: Optional[bool] = None
    category: Optional[str] = None
    manual_blocked: Optional[bool] = None
    manual_allowed: Optional[bool] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    description: Optional[str] = None


class SubredditResponse(BaseModel):
    name: str
    is_nsfw: bool
    category: Optional[str] = None
    manual_blocked: bool
    manual_allowed: bool
    confidence: float
    source: str
    description: Optional[str] = None


class StatsResponse(BaseModel):
    total_subreddits: int
    nsfw_subreddits: int
    manual_blocked: int
    allowed: int