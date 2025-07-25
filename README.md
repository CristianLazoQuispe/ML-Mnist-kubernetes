# ML-Mnist-kubernetes


mnist-fastapi-k8s/
├── app/
│   ├── api/
│   │   └── endpoints.py         # FastAPI endpoints
│   ├── adapter/
│   │   ├── model_runner.py      # ONNX runner con GPU fallback
│   │   └── preprocess.py        # Imagen -> tensor (1,1,28,28)
│   ├── config/
│   │   └── settings.py          # Config global, carga ONNX
│   └── main.py                  # arranque FastAPI
├── core/
│   ├── domain.py                # Esquemas Pydantic, negocio
│   └── service.py               # Interfaz de predicción
├── client/
│   └── send_images.py           # Script de carga extrema
├── assets/
│   ├── model.onnx               # Modelo ONNX (MNIST)
│   └── test_images/            # JPGs de prueba
│       ├── digit_0.jpg
│       ├── digit_1.jpg
│       └── ...
├── docker/
│   └── Dockerfile               # Python + ONNX GPU/CPU fallback
├── k8s/
│   ├── deployment.yaml          # GPU-aware + autoscaling
│   ├── service.yaml
│   └── hpa.yaml
├── requirements.txt
└── README.md




E:\Education\Kubernetes\ML-Mnist-kubernetes>python assets/load.py --url http://mnist.local/predict
Starting load test with 2000 requests...

=== Load Test Summary ===
Total Requests: 2000
Successes: 1994
Failures: 6
Total Time: 26.32 seconds

Response Time (in seconds):
  Mean:    0.6249
  StdDev:  0.1608
  Min:     0.1798
  Max:     1.3226


E:\Education\Kubernetes\ML-Mnist-kubernetes>docker compose up -d ml-mnist-kube
[+] Running 1/1
 ✔ Container ml-mnist-kube  Started                                                                                                                                              11.8s 

E:\Education\Kubernetes\ML-Mnist-kubernetes>python assets/load.py --url http://localhost:8000/predict
Starting load test with 2000 requests...

=== Load Test Summary ===  
Total Requests: 2000       
Successes: 1984
Failures: 16
Total Time: 112.93 seconds 

Response Time (in seconds):
  Mean:    2.7775
  StdDev:  0.5752
  Min:     0.7564
  Max:     5.0416
