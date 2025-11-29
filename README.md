🚀 Magic Cilium Policy Lab
Visual Simulator & Explainer for CiliumNetworkPolicy
URL: https://cilium.admnwizard.com/web/
Magic Cilium Policy Lab is a lightweight, visual tool that helps developers, DevOps engineers, and platform teams understand who can talk to whom under Cilium Network Policies.
CiliumNetworkPolicy is powerful but often difficult to reason about. Magic Cilium solves this by simulating traffic between endpoints, applying Cilium-style identity-based rules, and showing the results in a visual, easy-to-understand format.
________________________________________
🌟 Features
•	🔍 Simulate Cilium Network Policies without a Kubernetes cluster
•	👁️ Visual graph of allowed & denied connections
•	📄 Human-readable explanations for each traffic decision
•	🧩 Supports:
o	endpointSelector.matchLabels
o	ingress.fromEndpoints.matchLabels
o	ingress.toPorts.ports[].port
o	protocol: TCP
•	🧪 Offline analysis — works in any environment
•	🖥️ Minimal backend (FastAPI) + simple web UI
•	📦 Deployable on any Linux server (your instance runs on AlmaLinux + NGINX + SSL)
________________________________________
🧰 Architecture
User Input YAML → FastAPI Backend → Cilium-like Rule Engine → JSON → Web UI → Graph + Decisions
Components
•	Backend: Python 3 + FastAPI
•	Simulation Engine: Matches Cilium ingress rules (labels + ports)
•	Frontend: Lightweight HTML/JS UI
•	Visualization: Custom graph renderer (no external JS frameworks)
________________________________________
🔧 Installation (Local Dev)
1. Clone the repo
git clone https://github.com/yourname/magic-cilium-policy-lab.git
cd magic-cilium-policy-lab
2. Create virtual environment
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run backend
uvicorn app.main:app --host 0.0.0.0 --port 4089
Open the UI:
http://localhost:4089/web/
________________________________________
📦 Server Deployment (AlmaLinux)
On the production server at:
/home/sureshwizard/projects/liveprojects/selium
The app runs as a systemd service:
[Service]
ExecStart=/home/sureshwizard/projects/liveprojects/selium/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 4089
NGINX reverse-proxy + SSL is configured at:
https://cilium.admnwizard.com/web/
________________________________________
🧪 Example Usage
▶️ Endpoints YAML
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
▶️ Policy YAML
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
✔️ Result (Decision Summary)
•	frontend → backend:80 → ALLOW
•	frontend → backend:443 → DENY
•	all other combinations → DENY
✔️ Visual Graph
•	Green → Allowed
•	Red → Denied
•	Ports labeled on edges
________________________________________

🧪 How to Test the UI
URL: https://cilium.admnwizard.com/web/
Magic Cilium Policy Lab runs directly in your browser — no installation needed.
Follow these steps to run your first analysis:
________________________________________
1️⃣ Open the UI
Visit:
👉 https://cilium.admnwizard.com/web/
You will see:
•	Endpoints YAML (left box)
•	Policy YAML (right box)
•	Run Analysis button
•	Decisions Table
•	Graph Visualization
________________________________________
2️⃣ Paste Endpoint Definitions
Copy this into the Endpoints YAML box:
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
This defines three logical workloads with Kubernetes-style labels.
________________________________________
3️⃣ Paste a Cilium Network Policy
Copy this into the Policy YAML box:
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
This policy means:
frontend → backend on port 80/TCP is allowed.
Everything else is denied.
________________________________________
4️⃣ Click "Run Analysis"
The backend will:
•	Parse your YAML
•	Match labels using a Cilium-like evaluator
•	Simulate traffic on ports 80 and 443
•	Determine allow / deny
•	Return results as JSON
•	Render a visual graph
________________________________________
5️⃣ View the Results
✅ Decisions Table
You will see entries like:
Source	Dest	Port	Decision	Reason
frontend	backend	80	ALLOW	matched policy
frontend	backend	443	DENY	no matching rule
backend	database	80	DENY	no matching rule
Every source → destination → port is evaluated.
________________________________________
6️⃣ View the Graph
You will see:
•	Circles for each endpoint
•	Green edges for allowed traffic
•	Orange/red for denied traffic
•	Port numbers on each edge
Example:
•	🟢 ALLOW frontend → backend (80/TCP)
•	🔴 DENY backend → database (80/TCP, 443/TCP)
This gives a clear, human-friendly picture of "who can talk to whom".
________________________________________
7️⃣ Try More Scenarios (Optional)
You can experiment by:
•	Adding additional policies
•	Changing labels
•	Breaking policies intentionally
•	Creating deny-only policies
•	Testing namespace scoping
Example deny-policy:
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "deny-database"
spec:
  endpointSelector:
    matchLabels:
      app: database
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: backend
      toPorts:
        - ports:
            - port: "80"
              protocol: "TCP"
________________________________________
🎉 Testing Done!
_________________________________________________________________________________
🔍 How It Works
Magic Cilium evaluates:
1.	Which endpoints match the destination endpointSelector
2.	Which sources match fromEndpoints
3.	Whether the traffic port/protocol matches toPorts
4.	Everything else becomes implicitly denied
This approximates how Cilium generates eBPF rules inside the kernel’s datapath.
________________________________________
✨ Why This Project?
CiliumNetworkPolicy is extremely powerful but complex. Developers often struggle to understand what the YAML really means. Magic Cilium helps teams visualize, simulate, and explain policies — without needing a cluster.
Built for:
•	eBPF Summit Hackathon
•	Cilium developers
•	Kubernetes learners
•	DevOps & networking engineers
________________________________________
📚 Future Roadmap
•	Integration with real Kubernetes clusters
•	Auto-load pods via kubectl
•	Full L7 HTTP rule support
•	Egress policy support
•	Hubble flow correlation
•	Exportable reports (Markdown / PDF)
________________________________________
🏷️ License
Open Source — Apache 2.0 (recommended)
________________________________________
👤 Author
AI & Code with Suresh
#aicodewithsuresh
https://cilium.admnwizard.com/web/


