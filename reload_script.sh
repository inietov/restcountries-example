#! /bin/bash

podman build -f ./Containerfile -t fastapi_env:v1
podman run --rm --name FastAPI_dev -p 8080:8080 fastapi_env:v1
