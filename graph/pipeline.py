from langgraph.graph import END, StateGraph

from agents.evidence_mapping import evidence_mapping_agent
from agents.graph_data import graph_data_agent
from agents.llm_reasoning import llm_reasoning_agent
from agents.parser import parser_agent
from agents.scoring import scoring_agent
from agents.semantic_matching import semantic_matching_agent
from agents.skill_extraction import skill_extraction_agent
from graph.state import HiringState


def _route_after_parser(state):
    return "error" if state.get("error") else "continue"


def build_graph():
    workflow = StateGraph(HiringState)

    workflow.add_node("parser", parser_agent)
    workflow.add_node("skill_extraction", skill_extraction_agent)
    workflow.add_node("semantic_matching", semantic_matching_agent)
    workflow.add_node("evidence_mapping", evidence_mapping_agent)
    workflow.add_node("llm_reasoning", llm_reasoning_agent)
    workflow.add_node("scoring", scoring_agent)
    workflow.add_node("graph_data", graph_data_agent)

    workflow.set_entry_point("parser")
    workflow.add_conditional_edges(
        "parser",
        _route_after_parser,
        {
            "error": END,
            "continue": "semantic_matching",
        },
    )
    workflow.add_edge("semantic_matching", "evidence_mapping")
    workflow.add_edge("evidence_mapping", "skill_extraction")
    workflow.add_edge("skill_extraction", "llm_reasoning")
    workflow.add_edge("llm_reasoning", "scoring")
    workflow.add_edge("scoring", "graph_data")
    workflow.add_edge("graph_data", END)

    return workflow.compile()


def run_pipeline(resume_file, jd_text):
    graph = build_graph()
    return graph.invoke({
        "resume_file": resume_file,
        "jd_text": jd_text,
    })
