from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Python

with Diagram("AWS TPBank - AI Document Processing System - Microservice Architecture", show=False):
    user = Users("User")
    gateway = Nginx("API Gateway")

    with Cluster("File Processing Cluster Service"):
        file_ingestion = ECS("File Ingestion")      # File Ingestion Service
        doc_processing = ECS("Document Processing") # Document Processing Service
    
    with Cluster("AI & Embedding Cluster Service"):
        ai_analysis = ECS("Embedding & AI Analysis")
        agile_service = ECS("Document Standardization")
    
    vector_db = Dynamodb("Vector Database")
    mq = SQS("Message Queue")
    
    # Flow connections
    user >> gateway
    gateway >> file_ingestion
    file_ingestion >> doc_processing
    doc_processing >> ai_analysis
    ai_analysis >> vector_db
    ai_analysis >> agile_service
    agile_service >> gateway
    mq >> ai_analysis
