from typing import List, Dict, Any, Iterable
from .models import Endpoint, Decision


def _labels_match(endpoint: Endpoint, selector: Dict[str, str]) -> bool:
    for k, v in selector.items():
        if endpoint.labels.get(k) != v:
            return False
    return True


def _get_match_labels(block: Dict[str, Any]) -> Dict[str, str]:
    if not block:
        return {}
    return block.get("matchLabels", {}) or {}


def _extract_policies(raw_policies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize minimal fields we care about."""
    normalized = []
    for p in raw_policies:
        spec = p.get("spec", {})
        ep_sel = _get_match_labels(spec.get("endpointSelector", {}))
        ingress = spec.get("ingress", []) or []
        norm_ingress = []
        for rule in ingress:
            from_eps = rule.get("fromEndpoints", []) or []
            from_selectors = [_get_match_labels(fe) for fe in from_eps]

            to_ports = []
            for tp in rule.get("toPorts", []) or []:
                for prt in tp.get("ports", []) or []:
                    port = int(prt.get("port", 0))
                    proto = prt.get("protocol", "TCP")
                    to_ports.append({"port": port, "protocol": proto})

            norm_ingress.append(
                {
                    "from_selectors": from_selectors,
                    "to_ports": to_ports,
                }
            )

        normalized.append(
            {
                "name": p.get("metadata", {}).get("name", "unknown"),
                "endpoint_selector": ep_sel,
                "ingress": norm_ingress,
            }
        )
    return normalized


def analyze_connectivity(
    endpoints: List[Endpoint],
    raw_policies: List[Dict[str, Any]],
    ports: Iterable[int],
) -> List[Decision]:
    """Very small subset of Cilium logic, good enough for demo."""
    policies = _extract_policies(raw_policies)
    ports = list(ports)
    decisions: List[Decision] = []

    for src in endpoints:
        for dst in endpoints:
            if src.name == dst.name:
                continue

            for port in ports:
                decision = "deny"
                reason = "no matching allow rule"

                for pol in policies:
                    # Destination must match endpointSelector
                    if not _labels_match(dst, pol["endpoint_selector"]):
                        continue

                    for idx, ing in enumerate(pol["Ingress"] if False else pol["ingress"]):
                        # fromEndpoints match?
                        from_ok = False
                        if not ing["from_selectors"]:
                            from_ok = True  # treat as any
                        else:
                            for sel in ing["from_selectors"]:
                                if _labels_match(src, sel):
                                    from_ok = True
                                    break
                        if not from_ok:
                            continue

                        # port match?
                        port_ok = False
                        for pinfo in ing["to_ports"]:
                            if pinfo["port"] == port:
                                port_ok = True
                                proto = pinfo["protocol"]
                                break
                        if not port_ok:
                            continue

                        decision = "allow"
                        reason = f"allowed by policy '{pol['name']}' ingress rule #{idx}"
                        break

                    if decision == "allow":
                        break

                decisions.append(
                    Decision(
                        src=src.name,
                        dst=dst.name,
                        port=port,
                        protocol="TCP",
                        decision=decision,
                        reason=reason,
                    )
                )

    return decisions

