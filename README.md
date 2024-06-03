# tributary

# Sensor Streaming Backend

## Project Overview

This project is the backend for a sensor streaming system designed to provide real-time data from engine sensors to drivers. The system processes engine temperature data and exposes it via a Flask API connected to a Redis database. 

## Tech Stack

- **Flask**: A web framework for building the server that exposes the API.
- **Redis**: An in-memory datastore for fast data access.
- **Docker**: Used to run the Flask server and Redis instance in containers.
- **Docker Compose**: Used to manage multi-container Docker applications.

## API Endpoints

### /record
- **Description**: Records a new engine temperature reading to the database.
- **Method**: POST

### /collect
- **Description**: Collects the most current engine temperature from the database and calculates an average.
- **Method**: GET

## Setup Instructions

### Prerequisites

1. **IDE**: Ensure you have an appropriate IDE installed. We recommend [PyCharm](https://www.jetbrains.com/pycharm/).
2. **GitHub Repository**: Initialize a Git repository and host it on GitHub.
3. **Docker Desktop**: Install Docker Desktop. You can download it from [here](https://www.docker.com/products/docker-desktop).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/sensor-streaming-backend.git
   cd sensor-streaming-backend
