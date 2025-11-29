from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .models import AnalyzeRequest, GraphResult
from .parser import parse_endpoints_from_yaml, parse_policies_from_yaml
from .engine import analyze_connectivity
from .graph import build_graph

app = FastAPI(title="Magic Cilium Policy Lab")

# Allow browser front-end on same host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static web UI
app.mount("/web", StaticFiles(directory="web", html=True), name="web")


@app.get("/")
def root():
    return {"message": "Magic Cilium Policy Lab API. Open /web for the UI."}


@app.post("/api/analyze", response_model=GraphResult)
def analyze(req: AnalyzeRequest):
    endpoints = parse_endpoints_from_yaml(req.endpoints_yaml)
    policies = parse_policies_from_yaml(req.policies_yaml)

    ports = req.ports or [80]
    decisions = analyze_connectivity(endpoints, policies, ports)
    graph = build_graph(endpoints, decisions)
    return graph

