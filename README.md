# AVERT-X: Adaptive Chaos Engineering + XAI 

A prototype implementation demonstrating **Adaptive Chaos Engineering with Explainable AI (XAI)** for microservice resilience analysis. This PoC aligns with the research direction described in the abstract document, focusing on failure injection, metric-driven degradation assessment, and explainability using XAI.

This project integrates:

* **Chaos Mesh** for controlled failure injection
* **Kubernetes** for microservice deployment
* **FastAPI** ML microservice (sentiment model)
* **Load generation** for traffic simulation
* **Metric logging** for system-level and model-level behavior
* **SHAP-based XAI analysis** to explain degradation patterns

---

## Project Brief

Modern microservices are highly dynamic and distributed, causing traditional manual resilience testing approaches to fail at scale. The proposed research introduces a conceptual framework for **Adaptive Chaos Engineering enhanced with XAI**, focusing on:

### 1. **Adaptive Failure Injection**

* Controlled chaos tailored to service topology
* Chaos Mesh used here as the failure injection engine (e.g., pod-kill, network latency)

### 2. **Metric Collection & Ranking**

* Logs model latency, confidence, errors as system-level and business-level indicators
* Metrics are compared before and during chaos to quantify degradation

### 3. **XAI-Based Explanatory Analysis**

* Uses SHAP to explain **which features/inputs** contribute most to degraded performance
* Makes failure impact transparent and traceable

This PoC demonstrates the *foundational pipeline* of such a system.

---

## Project Folder Structure

```
chaos-xai-poc/
├── app/
│   ├── main.py                # FastAPI ML microservice
│   ├── server.py              # Uvicorn entrypoint
│   └── requirements.txt       # App dependencies
│
├── load/
│   └── load_test.py           # Load generator simulating user traffic
│
├── chaos/
│   ├── pod_kill.yaml          # Chaos Mesh: periodic pod termination
│   ├── network_latency.yaml   # Chaos Mesh: network delay
│   └── notes.md               # RBAC/namespace notes
│
├── k8s/
│   ├── deployment.yaml        # ML API Kubernetes Deployment
│   └── service.yaml           # ClusterIP Service
│
├── analysis/
│   ├── shap_analysis.py       # XAI-based resilience interpretation
│   └── sample_requests.json   # (to be generated) sample logs for XAI
│
├── Dockerfile                 # Container image for ML microservice
├── README.md                  # (this document)
└── ...
```

---

## Role of Each File

### **app/main.py**

Implements a simple sentiment analysis microservice using DistilBERT. Logs latency, confidence, and request metadata—used as resilience metrics.

### **app/server.py**

Runs FastAPI using Uvicorn.

### **app/requirements.txt**

Dependencies like FastAPI, Transformers, PyTorch.

### **Dockerfile**

Builds the ML API container image.

### **k8s/deployment.yaml**

Deploys two replicas of the ML API with readiness probes.

### **k8s/service.yaml**

Exposes the ML API inside the cluster.

### **chaos/pod_kill.yaml**

Injects pod-kill failures every minute.

### **chaos/network_latency.yaml**

Adds 500ms latency + jitter every 2 minutes.

### **load/load_test.py**

Sends continuous traffic to ML API; records model behavior for comparison.

### **analysis/shap_analysis.py**

Runs XAI using SHAP to:

* identify important input features,
* compare behavior before vs during chaos,
* interpret performance degradation.

---

## Setup & Run Instructions

### **1. Build & Push Docker Image**

```
docker build -t <registry>/ml-api:latest .
docker push <registry>/ml-api:latest
```

Replace `<registry>` with Docker Hub or private registry.

---

### **2. Apply Kubernetes Manifests**

```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check pod status:

```
kubectl get pods -l app=ml-api
```

---

### **3. Deploy Chaos Experiments**

```
kubectl apply -f chaos/pod_kill.yaml
kubectl apply -f chaos/network_latency.yaml
```

Verify:

```
kubectl get podchaos
kubectl get networkchaos
```

---

### **4. Run Load Generator**

Inside cluster:

```
kubectl run -it loadgen --image=python:3.10 --restart=Never -- /bin/bash
```

Then:

```
pip install requests
python load/load_test.py --url http://ml-api-svc/predict --rate 2 --duration 120
```

Export logs to `analysis/sample_requests.json`.

---

### **5. Run XAI Analysis (SHAP)**

```
cd analysis
python shap_analysis.py
```

Generates:

* SHAP feature importance
* Explanation of degradation under chaos

