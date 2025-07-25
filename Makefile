# Makefile - Deploying ML-MNIST on Kubernetes
# This Makefile automates the build, push, deploy, test, load, metrics, logs, and clean operations for the ML-MNIST application on Kubernetes.
# In my case I use 3 nodes in Minikube, but you can use only one node if you want.
# It assumes you have Minikube and kubectl installed and configured.
# The application is built using Docker and deployed on a Kubernetes cluster.
# The application is a FastAPI service that classifies MNIST images using an ONNX model.

APP_IMAGE  = ml-mnist-kubernetes-ml-mnist-kube
TEST_IMAGE = ml-mnist-kubernetes-mnist-tester

.PHONY: build push deploy test load metrics logs clean load-thread clean-images

# Build de imágenes Docker
build:
	docker build -f docker/Dockerfile -t $(APP_IMAGE):latest .
	docker build -f docker/Dockerfile.tester -t $(TEST_IMAGE):latest .


clean-images:
    
	minikube ssh --node minikube -- docker rmi $(TEST_IMAGE):latest  || true
	minikube ssh --node minikube-m02 -- docker rmi $(TEST_IMAGE):latest  || true
	minikube ssh --node minikube-m03 -- docker rmi $(TEST_IMAGE):latest  || true


	minikube ssh --node minikube -- docker rmi $(APP_IMAGE):latest  || true
	minikube ssh --node minikube-m02 -- docker rmi $(APP_IMAGE):latest  || true
	minikube ssh --node minikube-m03 -- docker rmi $(APP_IMAGE):latest  || true

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


# Simulation 2000 requests to MNIST service
load:
	kubectl delete job mnist-load-generator-job
	kubectl apply -f k8s/load-generator-job.yaml
	kubectl logs job/mnist-load-generator-job
load-thread:
	kubectl delete job mnist-load-generator-thread-job
	kubectl apply -f k8s/load-generator-thread-job.yaml
	kubectl logs job/mnist-load-generator-thread-job
# Show metrics and resource usage
metrics:
	minikube addons enable metrics-server
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
	kubectl delete job mnist-load-generator-job || true
	kubectl delete job mnist-load-generator-thread-job || true
	kubectl delete job mnist-test-job || true
