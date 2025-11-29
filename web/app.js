async function runAnalysis() {
  const endpoints = document.getElementById("endpoints").value;
  const policies = document.getElementById("policies").value;

  const res = await fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      endpoints_yaml: endpoints,
      policies_yaml: policies,
      ports: [80, 443],
    }),
  });

  if (!res.ok) {
    alert("Error running analysis");
    return;
  }

  const data = await res.json();
  renderDecisions(data.decisions);
  renderGraph(data);
}

function renderDecisions(decisions) {
  const container = document.getElementById("decisions");
  if (!decisions.length) {
    container.textContent = "No decisions.";
    return;
  }
  let html = "<table><thead><tr>";
  html += "<th>Source</th><th>Dest</th><th>Port</th><th>Protocol</th><th>Decision</th><th>Reason</th>";
  html += "</tr></thead><tbody>";
  for (const d of decisions) {
    const cls = d.decision === "allow" ? "badge-allow" : "badge-deny";
    html += `<tr>
      <td>${d.src}</td>
      <td>${d.dst}</td>
      <td>${d.port}</td>
      <td>${d.protocol}</td>
      <td class="${cls}">${d.decision.toUpperCase()}</td>
      <td>${d.reason}</td>
    </tr>`;
  }
  html += "</tbody></table>";
  container.innerHTML = html;
}

function renderGraph(graph) {
  const container = document.getElementById("graph");
  container.innerHTML = "";

  const nodesDiv = document.createElement("div");
  for (const n of graph.nodes) {
    const el = document.createElement("div");
    el.className = "node";
    el.textContent = n.id;
    nodesDiv.appendChild(el);
  }

  const edgesDiv = document.createElement("div");
  for (const e of graph.edges) {
    const el = document.createElement("div");
    el.className = "edge";
    const cls = e.decision === "allow" ? "badge-allow" : "badge-deny";
    el.innerHTML = `<span class="${cls}">${e.decision.toUpperCase()}</span> ${e.source} → ${e.target} (${e.ports.join(", ")})`;
    edgesDiv.appendChild(el);
  }

  container.appendChild(nodesDiv);
  container.appendChild(edgesDiv);
}

document.getElementById("run").addEventListener("click", runAnalysis);

// preload examples if you want
fetch("/examples/endpoints.yaml").catch(()=>{});

