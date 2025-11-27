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
