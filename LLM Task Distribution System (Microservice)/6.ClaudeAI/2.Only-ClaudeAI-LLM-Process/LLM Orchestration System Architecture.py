from diagrams import Diagram, Cluster
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Client
from diagrams.onprem.analytics import Spark
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Internet
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker

with Diagram("LLM Orchestration System Architecture", show=False, direction="TB"):
    # External Client
    client = Client("Client Application")
    
    # API Gateway & Load Balancer
    with Cluster("API Layer"):
        api = Nginx("API Gateway")
        lb = Nginx("Load Balancer")
    
    # Authentication & Token Management
    with Cluster("Authentication"):
        auth_db = PostgreSQL("Account DB")
        token_mgmt = Server("Token Manager")
        cache = Redis("Token Cache")
    
    # Main Orchestrator
    with Cluster("Orchestration Layer"):
        orchestrator = Server("DeepSeek R1\nOrchestrator")
        task_analyzer = Server("Task Analyzer")
        task_queue = Server("Task Queue")
    
    # Message Broker
    with Cluster("Message Broker"):
        kafka = Kafka("Kafka Cluster")
    
    # Worker Services
    with Cluster("Worker Services"):
        workers = [Docker("Worker 1"),
                  Docker("Worker 2"),
                  Docker("Worker 3")]
    
    # LLM Integration
    with Cluster("LLM Services"):
        llm_services = [
            Internet("Claude AI"),
            Internet("GPT API"),
            Internet("Other LLMs")
        ]
    
    # Result Processing
    with Cluster("Result Processing"):
        aggregator = Spark("Result Aggregator")
        result_db = PostgreSQL("Results DB")
    
    # Monitoring
    with Cluster("Monitoring"):
        metrics = Grafana("Metrics & Monitoring")
    
    # Connect components
    client >> api
    api >> lb
    lb >> auth_db
    lb >> token_mgmt
    token_mgmt >> cache
    
    lb >> orchestrator
    orchestrator >> task_analyzer
    task_analyzer >> task_queue
    task_queue >> kafka
    
    kafka >> workers
    for worker in workers:
        worker >> llm_services
        worker >> metrics
    
    workers >> aggregator
    aggregator >> result_db
    result_db >> orchestrator
    
    orchestrator >> api