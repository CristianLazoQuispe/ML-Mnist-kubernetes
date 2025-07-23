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
