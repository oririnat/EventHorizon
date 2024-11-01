# EventHorizon

<p align="center">
  <img src="https://raw.githubusercontent.com/oririnat/EventHorizon/master/events-web-gui/src/assets/event_horizon_white.png" alt="Event Horizon Logo">
</p>


**EventHorizon** is a cloud-native, microservice-based intelligence platform for tracking and analyzing public GitHub events. Built with scalability and real-time processing in mind, EventHorizon leverages FastAPI, RabbitMQ, MariaDB, and Nginx to provide insightful, up-to-date information on GitHub activity. Users can view and analyze events, actor details, repository metrics, and more through a user-friendly Angular frontend.

**Fun fact**:
EventHorizon contains the creator name: **ori** :)

---

## 📖 Introduction

EventHorizon’s goal is to deliver real-time GitHub events. The platform continuously fetches, processes, and displays data on GitHub activity, allowing users to search by actor name, repository name, or event type, and explore trending repositories. 

This system features a distributed microservices architecture:
- **Event Fetcher Service**: Retrieves public events from GitHub.
- **Event Processor Service**: Processes and stores events in the database.
- **Event REST API Service**: Exposes the data via a RESTful API.
- **Angular Web GUI**: A web-based interface that provides easy access to real-time data.

By following best practices in containerization and service isolation, EventHorizon is an easily deployable, scalable, and maintainable solution suitable for continuous monitoring.

---

## 🚀 Microservice Architecture Overview

### **1. Event Fetcher Service**
The Event Fetcher Service periodically pulls public events from GitHub’s API and sends them to RabbitMQ for processing. It’s designed to handle a high volume of requests while avoiding rate limits through intelligent scheduling and error handling.

- **Language**: Python
- **Dependencies**: FastAPI, Pika (RabbitMQ client), Requests...
- **Key Feature**: Maintains real-time data flow by sending GitHub events to RabbitMQ.

### **2. Event Processor Service**
The Event Processor Service listens to messages from RabbitMQ, processes each event, and stores it in MariaDB. This service is optimized for concurrency and ensures data consistency.

- **Language**: Python
- **Dependencies**: SQLAlchemy, Pika, PyMySQL
- **Key Feature**: Ensures data persistence and efficient processing.

### **3. Event REST API Service**
The Event REST API Service provides a FastAPI-based RESTful interface, exposing endpoints to retrieve events, actors, and repository data. It features Swagger documentation for easy exploration of API capabilities.

Fill free to view the API documentation at: http://localhost:8000/docs
after running the docker-compose up command.

- **Language**: Python (FastAPI)
- **Dependencies**: FastAPI, SQLAlchemy
- **Key Feature**: Allows querying and filtering of events with real-time search functionality.

### **4. Angular Web GUI**
The Angular Web GUI presents a user-friendly interface for browsing and interacting with the data. Users can view the latest events, recent actors, trending repositories, and use search filters.

- **Language**: TypeScript (Angular)
- **Dependencies**: Angular CLI
- **Key Feature**: Responsive web interface with dynamic data from the REST API.

---

## 🛠️ Installation Guide

### Prerequisites

Ensure Docker and Docker Compose are installed on your system.


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/oririnat/EventHorizon.git
   cd EventHorizon
   ```

2. **Replace secrets in the docker-compose.yml file**:
   ```bash
   Change the environment variables in the docker-compose.yml file to your own values.
   Alternatively, get the file from the creator - ori.
   ```

3. **Make sure the .sh files are in LF format**:
    - If you are using Windows, you may need to convert the line endings of the `.sh` files to LF format.
    
    pay attention to the following files:
    - `events_fetcher_service/start_with_delay.sh`
    - `events_processor_service/start_with_delay.sh`
    - `events_rest_api_service/start_with_delay.sh`

    Follow these steps to convert the line endings:
    Open each `.sh` file in a code editor and convert the line endings to LF:
    Convert Line Endings to LF:
        - Use a code editor like Visual Studio Code or Notepad++ to open the script.
        - In Visual Studio Code: Go to the bottom-right corner, click on CRLF, and select LF.
        - In Notepad++: Go to Edit > EOL Conversion > Unix (LF).
   
4. **Build and Run the Services**:
   ```bash
    docker-compose up --build
    ```

5. **Access the Web GUI**:
    Open your browser and navigate to http://localhost:4200
    
6. **Access the API Documentation**:
    Open your browser and navigate to http://localhost:8000/docs

7. **Access the RabbitMQ Management Interface**:
    Open your browser and navigate to http://localhost:15672
    