#!/bin/bash

# Start Ollama in the background
ollama serve &

# Give Ollama time to initialize
sleep 3

# Pull the required model (replace with actual model name if needed)
ollama pull llama3.2:1b  # Example using llama3 8B model

# Run the Python application
python3 main.py