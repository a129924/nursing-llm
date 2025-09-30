#!/bin/bash

# This script pulls the specified model from the Ollama repository.

# Load environment variables from .env file
if [ -f ../.env ]; then
    export $(cat ../.env | xargs)
fi

# Check if MODEL_NAME is set
if [ -z "$MODEL_NAME" ]; then
    echo "Error: MODEL_NAME is not set in the .env file."
    exit 1
fi

# Pull the model using Ollama
ollama pull "$MODEL_NAME"

echo "Model '$MODEL_NAME' has been pulled successfully."