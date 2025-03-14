
# Use the Python 3.10.9-slim image as the base
FROM python:3.10.9-slim

RUN mkdir -p /app/models

WORKDIR /app

# Copy the Stable Diffusion model into the container
# (Assuming you have the model files on your local machine)
# This is done early so it has a lower chance of having layers invalidated during build, saving long up/download times.
COPY ./builder/models/* /app/models/


# Install system dependencies required by Stable Diffusion and the API
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && apt-get clean


# Install Python dependencies for Stable Diffusion and the API
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# Copy the requirements.txt file into the container
COPY ./builder/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
# RUN pip install torch torchvision torchaudio transformers diffusers flask  # Prior to requirements.txt

# Install diffusers with PyTorch support - Keeping this separate for now. The reqs file includes "diffusers".
# RUN #pip install "diffusers[torch]"  # This is now install in the reqs file, right after "diffusers" (we do both)

RUN pip install transformers
RUN pip install diffusers
RUN pip install diffusers[torch]


# Expose the API port
EXPOSE 5000

# Copy the API script into the container
COPY ./src/app.py /app/app.py

# Set the entrypoint to run the API when the container starts
CMD ["python", "app.py"]

