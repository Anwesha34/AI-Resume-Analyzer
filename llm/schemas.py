from typing import Dict, List

from pydantic import BaseModel, Field


class SkillValidation(BaseModel):
    resume_skills: List[str] = Field(default_factory=list)
    jd_skills: List[str] = Field(default_factory=list)

    class Config:
        extra = "forbid"


class ReasoningOutput(BaseModel):
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    improvement_actions: List[str] = Field(default_factory=list)
    summary: str
    llm_score: float = Field(ge=0, le=100)

    class Config:
        extra = "forbid"


class ScoringOutput(BaseModel):
    section_scores: Dict[str, float] = Field(default_factory=dict)

    class Config:
        extra = "forbid"


class GraphDataOutput(BaseModel):
    score_distribution: Dict[str, float] = Field(default_factory=dict)
    skill_match: Dict[str, int] = Field(default_factory=dict)
    category_scores: Dict[str, float] = Field(default_factory=dict)
    gap_analysis: Dict[str, int] = Field(default_factory=dict)

    class Config:
        extra = "forbid"
