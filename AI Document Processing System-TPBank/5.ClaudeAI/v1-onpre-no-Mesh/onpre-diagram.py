from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis 
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper 
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.network import Kong
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker 
from diagrams.generic.storage import Storage as MinioStorage
from diagrams.saas.chat import Slack
from diagrams.aws.storage import S3 
from diagrams.gcp.ml import AIPlatform
from diagrams.custom import Custom


with Diagram("Onpremise AI Document Processing Architecture V1.0", show=True, direction="TB"):
    # Client Layer
    with Cluster("Client Layer"):
        web_app = Client("Web Application")
        mobile_app = Client("Mobile App")
        api_client = Client("API Client")
        
    # API Gateway Layer
    with Cluster("API Gateway Layer"):
        kong = Kong("Kong API Gateway")
        auth = Server("Authentication & Authorization")
        rate_limit = Server("Rate Limiter")
        api_docs = Server("API Documentation")
    
    # Connect clients to gateway
    web_app >> kong
    mobile_app >> kong
    api_client >> kong
    
    # Microservice Layer
    with Cluster("Microservice Layer"):
        doc_service = Server("Document Service")
        ocr_service = Server("OCR Service")
        ai_engine = Server("AI Engine Service")
        rag_service = Server("RAG Service")
        viz_service = Server("Visualization Service")
        export_service = Server("Export Service")
        vector_db_service = Server("Vector DB Service")
    
    # AI Models
    with Cluster("AI Models"):
        openai = Custom("OpenAI API\nGPT-4", "./../custom_icons/openai.png")
        claude = Custom("Anthropic API\nClaude 3", "./../custom_icons/claude.png")
        gemini = Custom("Google API\nGemini Pro", "./../custom_icons/gemini.png")
    
    # Database & Storage
    with Cluster("Database & Storage"):
        postgres = PostgreSQL("PostgreSQL")
        minio = MinioStorage("MinIO/S3")
        redis_cache = Redis("Redis Cache")
        vector_db = Custom("Google API\nGemini Pro", "./../custom_icons/vectordb.png")
    
    # Message Broker
    with Cluster("Message Broker"):
        kafka = Kafka("Apache Kafka")
        zookeeper = Zookeeper("ZooKeeper")
        
        kafka - Edge(color="red", style="dotted") - zookeeper
    
    # Monitoring & Logging
    with Cluster("Monitoring & Logging"):
        elk = Server("ELK Stack")
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        
        elk >> grafana
        prometheus >> grafana
    
    # Orchestration
    with Cluster("Orchestration"):
        celery = Server("Celery Workers")
        airflow = Airflow("Apache Airflow")
        
        airflow >> celery
    
    # Connect Gateway to Services
    kong >> doc_service
    kong >> ai_engine
    kong >> rag_service
    kong >> viz_service
    kong >> export_service
    
    # Service interconnections
    doc_service >> ocr_service
    doc_service >> kafka
    ocr_service >> doc_service
    
    ai_engine >> openai
    ai_engine >> claude
    ai_engine >> gemini
    ai_engine >> vector_db_service
    ai_engine >> kafka
    
    rag_service >> ai_engine
    rag_service >> vector_db_service
    rag_service >> doc_service
    
    viz_service >> ai_engine
    viz_service >> doc_service
    
    export_service >> ai_engine
    export_service >> doc_service
    
    vector_db_service >> vector_db
    
    # Services to Data
    doc_service >> postgres
    doc_service >> minio
    ai_engine >> minio
    viz_service >> minio
    export_service >> minio
    ocr_service >> minio
    ai_engine >> redis_cache
    rag_service >> redis_cache
    
    # Messaging connections
    kafka >> ai_engine
    kafka >> doc_service
    
    # Orchestration connections
    celery >> ai_engine
    celery >> doc_service
    celery >> ocr_service
    celery >> viz_service
    
    # Monitoring connections
    doc_service >> elk
    ai_engine >> elk
    rag_service >> elk
    viz_service >> elk
    export_service >> elk
    ocr_service >> elk
    vector_db_service >> elk