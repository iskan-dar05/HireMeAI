import json
from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from app.models.groq_client import get_groq

class CVOutput(BaseModel):
    personal_info: dict[str, Any]
    experience: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    certifications: list[dict[str, Any]] = Field(default_factory=list)

class State(TypedDict, total=False):
    input_data: dict
    content: dict
    error: str

def generate_node(state: State) -> State:
    model = get_groq()
    structured = model.with_structured_output(CVOutput)
    data = state["input_data"]
    messages = [
        SystemMessage(content=(
            "You are a professional CV writer. Produce accurate, ATS-friendly CV content. "
            "Never invent employers, degrees, dates, metrics, certifications, skills, or achievements. "
            "Improve wording while preserving facts. Use the provided job description to prioritize relevant "
            "truthful details. Missing information must remain missing, not be fabricated. Return the required schema."
        )),
        HumanMessage(content="Input profile and job description:\n" + json.dumps(data, ensure_ascii=False))
    ]
    result = structured.invoke(messages)
    return {"content": result.model_dump()}

def build_graph():
    graph = StateGraph(State)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "generate")
    graph.add_edge("generate", END)
    return graph.compile()

cv_generation_graph = build_graph()

def generate_cv(input_data: dict) -> dict:
    result = cv_generation_graph.invoke({"input_data": input_data})
    return {"content": result["content"]}
