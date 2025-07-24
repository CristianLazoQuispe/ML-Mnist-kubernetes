


# 1. Construiste tu imagen con docker compose
# 2. La cargas a Minikube
minikube image load ml-mnist-kubernetes-ml-mnist-kube:latest

# 3. Aplicar manifiestos
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# 4. Ver estado
kubectl get pods -o wide
kubectl get svc
kubectl top pods
kubectl get hpa

# Y si quieres simular carga:
kubectl apply -f k8s/load-generator.yaml