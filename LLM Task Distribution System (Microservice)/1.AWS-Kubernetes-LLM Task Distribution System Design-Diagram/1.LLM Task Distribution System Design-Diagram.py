from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS as RDSPostgreSQL
from diagrams.aws.network import ELB, Route53
from diagrams.aws.storage import S3
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.storage import PV, PVC
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python 
from diagrams.onprem.client import User
from diagrams.custom import Custom
from diagrams.generic.database import SQL
# LLM Task Distribution System - Hệ thống Phân phối Task LLM (Microservice)
with Diagram("LLM Task Distribution System (Microservice)", show=False):
    user = User("Người dùng")

    with Cluster("Hạ tầng Cloud (ví dụ: AWS/Kubernetes)"):
        api_gateway = Ingress("API Gateway (Nginx/Kong)")

        with Cluster("Task Processors"):
            openai = Custom("OpenAI", "./../images/openai_icon.png")
            genmini = Custom("Gemini", "./../images/genmini_icon.png")
            anthropic = Custom("Anthropic", "./../images/claude_icon.png")
            deepseek = Custom("DeepSeek", "./../images/deepseek_icon.png")
            qwen = Custom("Qwen-2.5", "./../images/qwen_icon.png")

        with Cluster("Task Orchestration"):
            deepseek_r1 = Pod("DeepSeek R1 Service")

        kafka_cluster = Kafka("Kafka Cluster")
        task_queue = Kafka("Task Queue")
        result_queue = Kafka("Result Queue")

        with Cluster("LLM Consumers"):
            openai_consumer = [Pod("OpenAI Consumer") for _ in range(3)]
            gemini_consumer = [Pod("Gemini Consumer") for _ in range(2)]
            claude_consumer = [Pod("Claude Consumer") for _ in range(2)]
            deepseek_consumer = [Pod("DeepSeek Consumer") for _ in range(2)]
            qwen_consumer = [Pod("Qwen-2.5 Consumer") for _ in range(2)]

        account_db = SQL("Account Database") # Optional, có thể dùng config file cho MVP

    user >> api_gateway >> deepseek_r1
    deepseek_r1 >> task_queue
    task_queue >> openai_consumer
    task_queue >> gemini_consumer
    task_queue >> claude_consumer
    task_queue >> deepseek_consumer
    task_queue >> qwen_consumer

    openai_consumer >> result_queue << gemini_consumer
    claude_consumer >> result_queue
    deepseek_consumer >> result_queue
    qwen_consumer >> result_queue

    result_queue >> deepseek_r1
    deepseek_r1 >> api_gateway >> user

    # Kết nối đến LLM providers (biểu tượng minh họa)
    openai_consumer >> Edge(label="OpenAI API") >> openai
    gemini_consumer >> Edge(label="Gemini API") >> genmini
    claude_consumer >> Edge(label="Claude API") >> anthropic
    deepseek_consumer >> Edge(label="DeepSeek API") >> deepseek
    qwen_consumer >> Edge(label="Qwen-2.5 API") >> qwen

    # Kết nối đến Account Database (optional)
    openai_consumer >> account_db
    gemini_consumer >> account_db
    claude_consumer >> account_db
    deepseek_consumer >> account_db
    qwen_consumer >> account_db