from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import Aurora, ElastiCache, RDS
from diagrams.aws.network import ELB, VPC
from diagrams.aws.storage import S3
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import Ingress, SVC
from diagrams.k8s.storage import PV, PVC
from diagrams.onprem.client import User
from diagrams.onprem.database import Postgresql, Mongodb
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka, Rabbitmq 
from diagrams.onprem.monitoring import Grafana, Prometheus, Sentry
from diagrams.programming.language import Python 
from diagrams.aws.analytics import Analytics
from diagrams.saas.chat import Slack
from diagrams.onprem.vcs import Github
from diagrams.custom import Custom 
from diagrams.saas.identity import Auth0
from diagrams.elastic.elasticsearch import Elasticsearch

with Diagram("Project Insights AI Microservice", show=False):
    user = User("Người dùng")
    
    api_gateway = EC2("API Gateway (FastAPI)")

    doc_processing_svc = EC2("Document Processing Service (NiFi, Textract)")
    ai_core_svc = EC2("AI Core Service (GPT-4, Claude)")
    vector_db_svc = EC2("Vector DB Service (Pinecone)")
    output_gen_svc = EC2("Output Generation Service (Python)")
    user_svc = EC2("User Service (FastAPI)")
    task_queue = Rabbitmq("Task Queue (RabbitMQ)")
    cache = Redis("Cache (Redis)")
    db = Postgresql("Database (PostgreSQL)")
    nosql_db = Mongodb("NoSQL DB (MongoDB - optional)")
    search_index = Elasticsearch("Search Index (Elasticsearch)")
    monitoring = Prometheus("Prometheus")
    grafana = Grafana("Grafana")
    sentry = Sentry("Sentry")
    jira = Custom("Jira Integration", "./../images/jira-icon.png")
    external_ai = [Analytics("Google Document AI"), Analytics("OpenAI"), Analytics("Claude"), Analytics("Gemini")]


    user >> api_gateway >> user_svc >> db
    user >> api_gateway >> doc_processing_svc >> task_queue
    task_queue >> doc_processing_svc >> ai_core_svc >> vector_db_svc >> search_index >> db
    user >> api_gateway >> ai_core_svc >> vector_db_svc >> db
    
    user >> api_gateway >> jira

    monitoring - grafana
    monitoring - sentry
    [doc_processing_svc, ai_core_svc, vector_db_svc, output_gen_svc, user_svc, api_gateway] >> monitoring

    ai_core_svc >> external_ai

    visualization = [Diagram("Diagram (Python)"), Diagram("PlantUML"), Diagram("Mermaid")]
    user >> api_gateway >> output_gen_svc >> db >> visualization