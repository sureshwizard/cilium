import yaml
from typing import List, Dict, Any
from .models import Endpoint


def parse_endpoints_from_yaml(yaml_text: str) -> List[Endpoint]:
    data = yaml.safe_load(yaml_text) or {}
    items = data.get("endpoints", [])
    endpoints = []
    for item in items:
        endpoints.append(
            Endpoint(
                name=item["name"],
                labels=item.get("labels", {}),
            )
        )
    return endpoints


def parse_policies_from_yaml(yaml_text: str) -> List[Dict[str, Any]]:
    """
    We keep policies as raw dicts. For demo we assume:
    - apiVersion: cilium.io/v2
    - kind: CiliumNetworkPolicy
    - spec:
        endpointSelector:
          matchLabels: {...}   # for destination
        ingress:
        - fromEndpoints:
          - matchLabels: {...} # for source
          toPorts:
          - ports:
            - port: "80"
              protocol: "TCP"
    """
    docs = list(yaml.safe_load_all(yaml_text)) or []
    return docs

