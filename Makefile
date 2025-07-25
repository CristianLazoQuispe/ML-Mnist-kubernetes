# Makefile - Deploying ML-MNIST on Kubernetes
# This Makefile automates the build, push, deploy, test, load, metrics, logs, and clean operations for the ML-MNIST application on Kubernetes.
# In my case I use 3 nodes in Minikube, but you can use only one node if you want.
# It assumes you have Minikube and kubectl installed and configured.
# The application is built using Docker and deployed on a Kubernetes cluster.
# The application is a FastAPI service that classifies MNIST images using an ONNX model.

APP_IMAGE  = ml-mnist-kubernetes-ml-mnist-kube
TEST_IMAGE = ml-mnist-kubernetes-mnist-tester

.PHONY: build clean-images push deploy test open-ssh stress-test stress-test-thread metrics open-dashboard logs clean status build-compose test-compose stress-test-compose-thread run-compose logs-compose-service logs-compose-tester open-ssh

# Build de imágenes Docker
build:
	docker build -f docker/Dockerfile -t $(APP_IMAGE):latest .
	docker build -f docker/Dockerfile.tester -t $(TEST_IMAGE):latest .


clean-images:
# Try to remove images from Minikube nodes if they exist
    
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

open-ssh:
	kubectl exec -it mnist-test-job-v8mvk -- /bin/sh

# Simulation 2000 requests to MNIST service
stress-test:
	kubectl delete job mnist-load-generator-job || true
	kubectl apply -f k8s/load-generator-job.yaml
	kubectl logs job/mnist-load-generator-job

# Simulation 2000 requests to MNIST service in parallel (using threads)
stress-test-thread:
	kubectl delete job mnist-load-generator-thread-job || true
	kubectl apply -f k8s/load-generator-thread-job.yaml
	sleep 60
	kubectl logs job/mnist-load-generator-thread-job
# Show metrics and resource usage
metrics:
	minikube addons enable metrics-server
	kubectl top pods
	kubectl get hpa
# Show the dashboard of Minikube
open-dashboard:
	minikube dashboard

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

status:
# Check status
	kubectl get pods -o wide
	kubectl get svc
	kubectl top pods
	kubectl get hpa

############################################
# Build with Docker-compose

build-compose:
# Build the images
	docker compose build
test-compose:
# Run tests from tester (does not start anything if it fails)
	docker compose up --exit-code-from mnist-tester --abort-on-container-exit mnist-tester
stress-test-compose-thread:
# Run tests stress 
	python3 assets/load.py --url=http://localhost:8000/predict
run-compose:
# Run the MNIST service
	docker compose up -d ml-mnist-kube
# Run the MNIST tester
	docker compose up -d mnist-tester
logs-compose-service:
# Show logs of the MNIST service
	docker compose logs -f ml-mnist-kube
logs-compose-tester:
# Show logs of the MNIST tester
	docker compose logs -f mnist-tester
