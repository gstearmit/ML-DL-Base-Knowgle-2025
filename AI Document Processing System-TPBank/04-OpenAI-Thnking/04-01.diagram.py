from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.queue import Kafka
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL

with Diagram("AI Document Processing System Architecture", show=False):
    # Người dùng và Frontend
    user = User("Người dùng")
    with Cluster("Frontend"):
        ui = Custom("Web UI", "./icons/ui.png")
    
    # Backend Microservices
    with Cluster("Backend Microservices"):
        upload_service = Server("File Upload Service")
        processing_service = Server("File Processing Service\n(Apache NiFi, Tesseract)")
        ai_core = Server("AI Analysis Service\n(OpenAI GPT-4, Claude 3, Gemini)")
        vector_db = Custom("Vector DB\n(Pinecone, Weaviate)", "./icons/database.png")
        orchestration = Server("Orchestration Service\n(LangChain, LlamaIndex)")
        visualization = Server("Visualization Service\n(Diagram, PlantUML)")
        backend_api = Server("Backend API Service\n(FastAPI, Celery)")
        db = PostgreSQL("Metadata DB")
    
    # Messaging hệ thống
    kafka = Kafka("Kafka Pub/Sub")
    
    # Flow dữ liệu
    user >> ui >> upload_service
    upload_service >> kafka
    kafka >> processing_service
    processing_service >> ai_core
    ai_core >> vector_db
    ai_core >> orchestration
    orchestration >> visualization
    visualization >> backend_api
    ai_core >> backend_api
    backend_api >> db
    user << backend_api
