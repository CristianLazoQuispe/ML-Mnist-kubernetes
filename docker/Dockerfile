FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# onnx runtime errors
ENV LD_LIBRARY_PATH=/opt/conda/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH

# Set default timezone to UTC or allow override
ARG CONTAINER_TIMEZONE=Etc/UTC
ENV CONTAINER_TIMEZONE=${CONTAINER_TIMEZONE}

# Fix time sync issue and install tzdata properly
RUN apt-get update 

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/${CONTAINER_TIMEZONE} /etc/localtime && \
    echo ${CONTAINER_TIMEZONE} > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Install system packages in one go (to reduce layers)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libxrender-dev \
    libgl1-mesa-glx libglib2.0-0 libgtk2.0-dev \
    python3-opencv git curl wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install jupyterlab
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY core core
COPY assets assets

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "app.main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]


#docker compose build
#docker compose up