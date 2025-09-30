# README.md

# Ollama Docker Project

This project provides a Docker setup for running the Ollama model. It includes a Docker Compose configuration to manage the services and a script to pull the specified model from the Ollama repository.

## Project Structure

- **docker/**: Contains scripts and configurations related to Docker.
  - **pull_model.sh**: Script to pull the specified model from the Ollama repository.
  
- **docker-compose.yml**: Defines the services, networks, and volumes for the Docker application.

- **.env**: Contains environment variables used in the `docker-compose.yml` file.

- **data/models/**: Directory to store models pulled from Ollama. This will be mounted as a volume in the Docker container to persist model data.

## Prerequisites

- Docker and Docker Compose must be installed on your machine.

## Setup Instructions

1. Clone the repository to your local machine.

2. Navigate to the project directory:

   ```bash
   cd path/to/your/project/server
   ```

3. Configure the environment variables in the `.env` file as needed. This may include model names, ports, and other configurations.

4. To pull the model, you can either:
   - Run the `pull_model.sh` script:

     ```bash
     ./docker/pull_model.sh
     ```

   - Or, ensure the model is specified in the `docker-compose.yml` file under the Ollama service configuration.

5. Start the Docker containers using Docker Compose:

   ```bash
   docker-compose up
   ```

## Usage

Once the containers are running, you can access the Ollama service as specified in the `docker-compose.yml` file. Make sure to check the logs for any output or errors.

## Notes

- Ensure that the `data/models` directory has the appropriate permissions for Docker to read and write model files.
- Refer to the documentation for Ollama for more details on using the models and any additional configurations that may be required.