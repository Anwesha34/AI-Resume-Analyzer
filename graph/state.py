from typing import Any, Dict, List, Optional, TypedDict


class HiringState(TypedDict, total=False):
    resume_file: Any
    resume_text: str
    jd_text: str
    resume_chunks: List[str]
    relevant_resume_chunks: List[str]
    jd_requirements: List[str]
    extracted_skills: Dict[str, List[str]]
    structured_resume_data: Dict[str, Any]
    matched_skills: List[str]
    missing_skills: List[str]
    semantic_matches: List[Dict[str, Any]]
    evidence_mapping: List[Dict[str, str]]
    section_scores: Dict[str, float]
    overall_score: float
    graph_data: Dict[str, Any]
    improvement_actions: List[str]
    summary: str
    semantic_score: float
    skill_match_score: float
    llm_score: float
    error: Optional[str]
