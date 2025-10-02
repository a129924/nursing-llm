FROM ollama/ollama:latest

# install curl (assumes Debian/Ubuntu base)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
