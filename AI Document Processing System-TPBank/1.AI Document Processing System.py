from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Python

with Diagram("AI Document Processing System - Microservice Architecture", show=False):
    user = Users("User")
    gateway = Nginx("API Gateway")

    with Cluster("File Processing Cluster"):
        file_ingestion = Python("File Ingestion Service")
        doc_processing = Python("Document Processing Service")
    
    with Cluster("AI & Embedding Cluster"):
        ai_analysis = Python("Embedding & AI Analysis Service")
        agile_service = Python("Document Standardization Service")
    
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
