


# 1. Construiste tu imagen con docker compose
# 2. Load
minikube image load ml-mnist-kubernetes-ml-mnist-kube:latest

# 3. Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# 4. Check status
kubectl get pods -o wide
kubectl get svc
kubectl top pods
kubectl get hpa
