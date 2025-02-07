from diagrams import Diagram
from diagrams.aws.database import Aurora
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Weaviate
from diagrams.generic.general import Client

with Diagram("AI-Powered Document Intelligence Platform Architecture", show=True):
    user = Client("User")

    # Data Ingestion
    data_ingestion = Server("Data Ingestion (NiFi, Tesseract)")
    file_storage = S3("File Storage (S3)")

    # AI Core
    ai_core = Server("AI Core (OpenAI, Claude)")
    vector_db = Weaviate("Vector Database (Weaviate)")

    # Orchestration
    orchestration = Server("Orchestration (LangChain, LlamaIndex)")

    # Backend
    backend = Server("Backend (FastAPI, Celery)")
    queue = Kafka("Message Queue (Kafka)")
    database = Aurora("Relational DB (Aurora)")

    # Visualization
    visualization = Server("Visualization (Diagram, PlantUML)")

    # Connections
    user >> data_ingestion >> file_storage
    file_storage >> ai_core
    ai_core >> vector_db
    vector_db >> orchestration
    orchestration >> backend
    backend >> queue
    backend >> database
    orchestration >> visualization
    user >> backend