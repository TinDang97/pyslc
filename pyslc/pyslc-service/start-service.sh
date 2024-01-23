#!/bin/bash

# Start the FastAPI server
uvicorn app.api.v1.server:app --host 0.0.0.0 --port 8000
