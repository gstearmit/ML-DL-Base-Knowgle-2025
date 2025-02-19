from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.k8s.network import Service
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.aws.network import APIGateway
from diagrams.aws.security import IAM
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR

with Diagram("Multil-LLM Processing System Architecture", show=False, direction="TB"):
    # Client and API Gateway
    client = React("Client Application")
    api_gateway = APIGateway("API Gateway")
    
    # Authentication & Authorization
    with Cluster("Security Layer"):
        auth = IAM("Auth Service")
        token_store = S3("Token Store")
        auth - token_store

    # Task Management
    with Cluster("Task Management"):
        task_manager = Server("Task Manager")
        deepseek = Pod("DeepSeek R1\nOrchestrator")
        task_analyzer = Pod("Task Analyzer")
        task_db = RDS("Task Database")
        
        task_manager >> deepseek >> task_analyzer
        task_analyzer - task_db

    # Message Queue
    with Cluster("Message Queue"):
        kafka = Kafka("Kafka Broker")
        kafka_cluster = [
            SQS("Queue 1"),
            SQS("Queue 2"),
            SQS("Queue 3")
        ]
        kafka >> Edge(color="darkgreen") >> kafka_cluster

    # Account Management
    with Cluster("Account Management"):
        account_service = StatefulSet("Account Service")
        rate_limiter = Pod("Rate Limiter")
        load_balancer = Service("Load Balancer")
        account_db = RDS("Account DB")
        
        account_service >> rate_limiter >> load_balancer
        account_service - account_db

    # LLM Workers
    with Cluster("LLM Processing"):
        workers = [
            Pod("OpenAI Workers"),
            Pod("Claude Workers"),
            Pod("Gemini Workers"),
            Pod("DeepSeek Workers"),
            Pod("Qwen Workers")
        ]
        result_collector = StatefulSet("Result Collector")
        
        for worker in workers:
            worker >> result_collector

    # Result Processing
    with Cluster("Result Processing"):
        merger = EMR("Result Merger")
        final_analysis = Pod("Final Analysis")
        result_db = RDS("Result Database")
        
        result_collector >> merger >> final_analysis
        final_analysis - result_db

    # Connect components
    client >> api_gateway >> auth
    api_gateway >> task_manager
    task_analyzer >> kafka
    kafka >> load_balancer
    load_balancer >> workers
    final_analysis >> task_manager