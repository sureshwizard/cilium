from typing import Dict, List, Optional
from pydantic import BaseModel


class Endpoint(BaseModel):
    name: str
    labels: Dict[str, str]


class Decision(BaseModel):
    src: str
    dst: str
    port: int
    protocol: str
    decision: str  # "allow" or "deny"
    reason: str


class Node(BaseModel):
    id: str
    labels: Dict[str, str]


class Edge(BaseModel):
    source: str
    target: str
    decision: str
    ports: List[str]


class GraphResult(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    decisions: List[Decision]


class AnalyzeRequest(BaseModel):
    endpoints_yaml: str
    policies_yaml: str
    ports: Optional[List[int]] = None

