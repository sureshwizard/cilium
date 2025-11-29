from typing import List, Dict
from .models import Endpoint, Decision, Node, Edge, GraphResult


def build_graph(endpoints: List[Endpoint], decisions: List[Decision]) -> GraphResult:
    nodes = [Node(id=e.name, labels=e.labels) for e in endpoints]

    # Combine decisions into edges
    edge_map: Dict[tuple, Edge] = {}

    for d in decisions:
        key = (d.src, d.dst, d.decision)
        label = f"{d.port}/{d.protocol}"
        if key not in edge_map:
            edge_map[key] = Edge(
                source=d.src,
                target=d.dst,
                decision=d.decision,
                ports=[label],
            )
        else:
            if label not in edge_map[key].ports:
                edge_map[key].ports.append(label)

    edges = list(edge_map.values())
    return GraphResult(nodes=nodes, edges=edges, decisions=decisions)

