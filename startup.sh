#!/bin/bash

echo "[1] Unsetting KUBECONFIG"
unset KUBECONFIG

echo "[2] Restoring kubeconfig from kind cluster"
mv ~/.kube/config ~/.kube/config.backup 2>/dev/null
kind get kubeconfig --name chaos-sockshop > ~/.kube/config

echo "[3] Setting context to kind-chaos-sockshop"
kubectl config use-context kind-chaos-sockshop

echo "[4] Showing namespaces"
kubectl get ns

echo "[5] Showing Chaos Mesh pods"
kubectl get pods -n chaos-mesh

echo "[6] Port-forward Chaos Mesh Dashboard on http://localhost:2333"
kubectl port-forward -n chaos-mesh svc/chaos-dashboard 2333:2333
