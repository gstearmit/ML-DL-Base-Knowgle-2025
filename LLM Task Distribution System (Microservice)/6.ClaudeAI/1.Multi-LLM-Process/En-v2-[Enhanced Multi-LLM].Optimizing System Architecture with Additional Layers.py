from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, StatefulSet, Deploy
from diagrams.k8s.network import Service, Ingress
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS, ElastiCache
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.aws.network import APIGateway, CloudFront, ELB
from diagrams.aws.security import IAM, WAF, Shield
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR, Kinesis
from diagrams.aws.management import Cloudwatch, SystemsManager
from diagrams.aws.compute import AutoScaling, Lambda

# Định nghĩa màu sắc cho các luồng xử lý khác nhau
EDGE_COLORS = {
    "primary": "#1E88E5",    # Main flow
    "secondary": "#43A047",   # Queue processing
    "warning": "#FDD835",     # Monitoring
    "error": "#E53935",      # Error handling
    "info": "#00ACC1",       # Data flow
    "success": "#4CAF50"     # Successful processing
}

# Định nghĩa style cho các node
NODE_CONFIG = {
    "fontsize": "13",
    "width": "2.0",
    "height": "1.5"
}

with Diagram(
    "En-v2-[Enhanced Multi-LLM].Final Multi-LLM Processing System Architecture",
    show=True,
    direction="TB",
    graph_attr={
        "splines": "ortho",
        "nodesep": "0.8",
        "ranksep": "1.0",
        "fontsize": "20"
    }
):
    # Client & Entry Layer
    with Cluster("Entry Layer"):
        shield = Shield("DDoS Protection")
        client = React("Web Client")
        mobile = React("Mobile Client")
        cdn = CloudFront("Global CDN")
        
        [client, mobile] >> cdn >> shield

    # Security & Authentication
    with Cluster("Security Layer"):
        waf = WAF("WAF")
        api_gateway = APIGateway("API Gateway")
        auth_service = Lambda("Auth Service")
        token_store = S3("Token Store")
        
        shield >> waf >> api_gateway
        api_gateway >> Edge(color=EDGE_COLORS["primary"]) >> auth_service
        auth_service - token_store

    # Data Validation & Processing
    with Cluster("Data Processing Layer"):
        input_validator = Pod("Input Validator")
        sanitizer = Pod("Data Sanitizer")
        schema_validator = Pod("Schema Validator")
        data_transformer = Pod("Data Transformer")
        
        api_gateway >> input_validator >> sanitizer >> schema_validator >> data_transformer

    # Task Orchestration
    with Cluster("Task Orchestration Layer"):
        task_manager = Server("Task Manager")
        orchestrator = Pod("LLM Orchestrator")
        task_analyzer = Pod("Task Analyzer")
        task_db = RDS("Task Database")
        task_cache = ElastiCache("Task Cache")
        
        data_transformer >> task_manager >> orchestrator >> task_analyzer
        task_analyzer - task_db
        task_manager - task_cache

    # Message Queue System
    with Cluster("Queue Management Layer"):
        kafka = Kafka("Kafka Cluster")
        queues = [
            SQS("Priority Queue"),
            SQS("Standard Queue"),
            SQS("Batch Queue")
        ]
        dlq = SQS("Dead Letter Queue")
        
        task_analyzer >> kafka >> Edge(color=EDGE_COLORS["secondary"]) >> queues
        kafka >> Edge(color=EDGE_COLORS["error"]) >> dlq

    # Account & Resource Management
    with Cluster("Resource Management Layer"):
        account_service = StatefulSet("Account Service")
        rate_limiter = Pod("Rate Limiter")
        load_balancer = ELB("Load Balancer")
        account_db = RDS("Account Database")
        account_cache = ElastiCache("Account Cache")
        
        account_service >> rate_limiter >> load_balancer
        account_service - account_db
        account_service - account_cache

    # LLM Processing
    with Cluster("LLM Processing Layer"):
        scaling_manager = AutoScaling("Auto Scaling Manager")
        llm_workers = [
            Deploy("OpenAI Engine"),
            Deploy("Claude Engine"),
            Deploy("Gemini Engine"),
            Deploy("DeepSeek Engine"),
            Deploy("Qwen Engine")
        ]
        result_collector = StatefulSet("Result Collector")
        result_cache = ElastiCache("Result Cache")
        
        queues >> load_balancer >> scaling_manager
        for worker in llm_workers:
            scaling_manager >> worker >> result_collector
        result_collector - result_cache

    # Result Processing
    with Cluster("Result Processing Layer"):
        merger = EMR("Result Merger")
        analyzer = Pod("Result Analyzer")
        final_processor = Pod("Final Processor")
        result_db = RDS("Result Database")
        
        result_collector >> merger >> analyzer >> final_processor
        final_processor - result_db

    # System Monitoring
    with Cluster("Monitoring Layer"):
        metrics = Cloudwatch("Metrics & Alerts")
        logs = Cloudwatch("Log Aggregation")
        tracer = Pod("Distributed Tracing")
        analytics = Kinesis("Real-time Analytics")
        monitor = SystemsManager("System Monitor")
        
        metrics >> monitor
        [logs, tracer] >> analytics >> monitor

    # Reliability & Recovery
    with Cluster("Reliability Layer"):
        backup_store = S3("Backup Store")
        recovery_manager = Pod("Recovery Manager")
        health_check = Pod("Health Checker")
        
        [task_db, account_db, result_db] >> backup_store
        recovery_manager >> backup_store
        health_check >> monitor

    # System Feedback Loop
    final_processor >> Edge(color=EDGE_COLORS["success"]) >> task_manager

    # Monitoring Connections
    monitor >> Edge(color=EDGE_COLORS["warning"]) >> [
        task_manager,
        kafka,
        load_balancer,
        scaling_manager,
        result_collector
    ]