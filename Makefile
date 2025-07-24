# Makefile - Deploying ML-MNIST on Kubernetes
# This Makefile automates the build, push, deploy, test, load, metrics, logs, and clean operations for the ML-MNIST application on Kubernetes.

APP_IMAGE  = ml-mnist-kubernetes-ml-mnist-kube
TEST_IMAGE = ml-mnist-kubernetes-tester

.PHONY: build push deploy test load metrics logs clean

# Build de imágenes Docker
build:
	docker build -f docker/Dockerfile -t $(APP_IMAGE):latest .
	docker build -f docker/Dockerfile.tester -t $(TEST_IMAGE):latest .

# Push docker images to Minikube
push:
	minikube image load $(APP_IMAGE):latest
	minikube image load $(TEST_IMAGE):latest
# Verify images are loaded
	minikube image ls | grep $(APP_IMAGE)
	minikube image ls | grep $(TEST_IMAGE)

	minikube ssh --node minikube docker images
	minikube ssh --node minikube-m02 docker images
	minikube ssh --node minikube-m03 docker images

# Deploy in Kubernetes
deploy:
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/hpa.yaml

# Deploy test job (MNIST Tester)
test:
	kubectl apply -f k8s/test-job.yaml
	kubectl wait --for=condition=complete --timeout=60s job/mnist-test-job
	kubectl logs job/mnist-test-job

# kubectl exec -it mnist-test-job-v8mvk -- /bin/sh


# Simulation 200 requests to MNIST service
load:
	kubectl apply -f k8s/load-generator.yaml

# Show metrics and resource usage
metrics:
	kubectl top pods
	kubectl get hpa

# show logs of the MNIST pods
logs:
	kubectl get pods -o wide
	kubectl logs -l app=mnist --tail=50

	kubectl describe pod mnist-deployment-7fc5f6fbb7-kzrtw

# Clean up resources (optional)
clean:
	kubectl delete deployment mnist-deployment || true
	kubectl delete service mnist-service || true
	kubectl delete hpa mnist-hpa || true
	kubectl delete job load-generator || true
	kubectl delete job mnist-test-job || true
