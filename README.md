🚀 Magic Cilium Policy Lab
Visual Simulator & Explainer for CiliumNetworkPolicy
Live Demo → https://cilium.admnwizard.com/web/
Built for eBPF Summit Hackathon 2025
Magic Cilium Policy Lab is a lightweight visual analyzer that simulates who can talk to whom under CiliumNetworkPolicy rules. It transforms complex YAML into a simple, interactive graph and human-readable decisions.
________________________________________
🌟 Features
•	🧩 Simulates Cilium Network Policies
•	🔍 Label-based traffic evaluation (Cilium-style)
•	📊 Clear allow/deny decision table
•	🕸️ Network graph visualization
•	📦 No cluster required — fully offline
•	⚡ FastAPI backend + simple HTML/JS UI
•	🔐 HTTPS-ready (your deployment uses SSL via NGINX)
________________________________________
🧰 Architecture
Magic Cilium follows a lightweight, clear architecture:
┌──────────────────────────┐
│         Web UI           │
│  YAML input fields       │
│  Run Analysis button     │
│  Graph + Decisions view  │
└─────────────┬────────────┘
              │ POST /api/analyze
              ▼
┌──────────────────────────┐
│     FastAPI Backend      │
│  Parses YAML (PyYAML)    |
│  Matches labels/ports    │
│  Simulates Cilium rules  │
└─────────────┬────────────┘
              │ JSON graph/decisions
              ▼
┌──────────────────────────┐
│   Browser Graph Renderer │
│  Draws nodes/edges       │
│  Shows ALLOW/DENY table  │
└──────────────────────────┘
Components
•	Frontend:
o	Static HTML, CSS, JS
o	Sends YAML to API
o	Renders graph + decisions
•	Backend:
o	Python + FastAPI
o	YAML parsing
o	Label + ingress rule matching
o	Port-based evaluation
•	Deployment:
o	Uvicorn on port 4089
o	NGINX SSL reverse-proxy
o	Public URL: https://cilium.admnwizard.com/web/
________________________________________
🧪 How to Test the UI
Visit → https://cilium.admnwizard.com/web/
This is the simplest way to test Magic Cilium.
You will see:
•	Endpoints YAML
•	Policy YAML
•	Run Analysis button
•	A Decisions Table
•	A Graph Visualization
1️⃣ Paste this into Endpoints YAML
endpoints:
  - name: frontend
    labels:
      app: frontend
      k8s:io.kubernetes.pod.namespace: shop
  - name: backend
    labels:
      app: backend
      k8s:io.kubernetes.pod.namespace: shop
  - name: database
    labels:
      app: database
      k8s:io.kubernetes.pod.namespace: shop
2️⃣ Paste this into Policy YAML
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "frontend-to-backend"
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "80"
              protocol: "TCP"
3️⃣ Click Run Analysis
4️⃣ Check the Decisions Table
You will see:
Source	Dest	Port	Decision	Reason
frontend	backend	80	ALLOW	allowed by policy
frontend	backend	443	DENY	no matching allow rule
all other combinations			DENY	no matching allow rule
5️⃣ Check the Graph
•	🟢 Green edges = ALLOW
•	🔴 Red edges = DENY
Example:
•	ALLOW frontend → backend (80/TCP)
•	DENY frontend → backend (443/TCP)
This gives a clear picture of “who can talk to whom”.
________________________________________
🧪 Example Scenarios
Add a second policy:
---
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "deny-to-database"
spec:
  endpointSelector:
    matchLabels:
      app: database
  ingress:
    - fromEndpoints:
        - matchLabels:
            k8s:io.kubernetes.pod.namespace: shop
      toPorts:
        - ports:
            - port: "80"
              protocol: "TCP"
Rerun → Graph updates automatically.
________________________________________
🔧 Local Installation
git clone https://github.com/yourname/magic-cilium
cd magic-cilium

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 4089
Open:
http://localhost:4089/web/
________________________________________
🖥️ Production Deployment (Your Server)
Location:
/home/sureshwizard/projects/liveprojects/selium
Running via systemd
ExecStart=/home/sureshwizard/projects/liveprojects/selium/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 4089
SSL URL
https://cilium.admnwizard.com/web/
NGINX handles:
•	SSL termination
•	Proxy to port 4089
•	Redirect HTTP → HTTPS
________________________________________
📚 What the Engine Supports
•	endpointSelector.matchLabels
•	ingress.fromEndpoints.matchLabels
•	ingress.toPorts[].ports[]
•	protocol: TCP
•	Implicit deny (when no rules match)
Perfect for:
•	Kubernetes
•	Cilium beginners
•	Policy debugging
•	Learning how label-based identity works
________________________________________
📈 Roadmap
•	Egress support
•	L7 HTTP rules
•	Multi-policy evaluation
•	Import from kubectl
•	Advanced graph visualization
•	Export to PDF/Markdown
________________________________________
🏷️ License
Open Source — Apache 2.0
________________________________________
👤 Author
AI & Code with Suresh
#aicodewithsuresh
https://cilium.admnwizard.com/web/

