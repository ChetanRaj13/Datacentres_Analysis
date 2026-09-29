from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ProblemRecord(BaseModel):
    id: str = Field(..., description="Unique record identifier")
    source: str = Field(..., description="Data source name (reddit, hackernews, google_news, youtube)")
    url: str = Field(..., description="Traceable original URL")
    title: str = Field(..., description="Cleaned title")
    text: str = Field(..., description="Cleaned body or combined text")
    author_hash: str = Field(..., description="Anonymized author hash (no PII)")
    created_at: int = Field(default=0, description="Unix timestamp of creation")
    score: int = Field(default=0, description="Upvotes/likes/points")
    num_comments: int = Field(default=0, description="Number of comments")
    query: str = Field(default="", description="Search query/topic that retrieved this item")
    lang: str = Field(default="en", description="Language detected (en, hinglish, other)")
    
    # Enriched fields
    pain_score: float = Field(default=0.0, description="Calculated pain intensity score")
    theme: str = Field(default="Social impact", description="Sustainability / Environment / Social impact / Business")
    problem_statement: Optional[str] = Field(default=None, description="Extracted problem statement")
    cluster_id: Optional[int] = Field(default=None, description="Assigned problem cluster ID")

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise ValueError("Record id cannot be null or empty")
        return str(v).strip()

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise ValueError("Record text cannot be null or empty")
        return str(v).strip()
