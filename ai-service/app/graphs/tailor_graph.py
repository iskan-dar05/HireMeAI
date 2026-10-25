import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from app.models.groq_client import get_groq

class State(TypedDict, total=False):
    content: dict
    job_description: str
    result: dict

def tailor_node(state: State) -> State:
    model = get_groq()
    prompt = (
        "Tailor the existing CV to the target job description. Preserve all facts and dates. "
        "Do not add skills or experience not supported by the original CV. Keep the same JSON structure. "
        "Return valid JSON only.\n\nExisting CV:\n" + json.dumps(state["content"], ensure_ascii=False) +
        "\n\nJob description:\n" + state["job_description"]
    )
    response = model.invoke([
        SystemMessage(content="You carefully tailor CV content without fabricating facts."),
        HumanMessage(content=prompt)
    ])
    text = response.content if isinstance(response.content, str) else json.dumps(response.content)
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    parsed = json.loads(text)
    if not isinstance(parsed, dict) or "personal_info" not in parsed:
        raise ValueError("Model returned invalid CV structure")
    return {"result": parsed}

graph = StateGraph(State)
graph.add_node("tailor", tailor_node)
graph.add_edge(START, "tailor")
graph.add_edge("tailor", END)
tailor_graph = graph.compile()

def tailor_cv(content: dict, job_description: str) -> dict:
    return {"content": tailor_graph.invoke({"content": content, "job_description": job_description})["result"]}
