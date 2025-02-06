from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python 
from diagrams.custom import Custom
from diagrams.onprem.client import User

with Diagram("Microservice Architecture", show=False, direction="LR"):
    user = User("User")
    api_gateway = Nginx("API Gateway")
    task_manager = Python("Task Manager Service")
    kafka = Kafka("Kafka")
    worker = Python("Worker Service")
    result_aggregator = Python("Result Aggregator Service")
    load_balancer = Server("Load Balancer Service")
    auth_service = Python("Authentication Service")

    with Cluster("LLM APIs"):
        openai = Custom("OpenAI", "./../images/openai_icon.png")
        gemini = Custom("Gemini", "./../images/genmini_icon.png")
        anthropic = Custom("Anthropic", "./../images/claude_icon.png")
        deepseek = Custom("DeepSeek", "./../images/deepseek_icon.png")
        qwen = Custom("Qwen-2.5", "./../images/qwen_icon.png")

    user >> api_gateway >> task_manager >> kafka
    kafka >> worker >> openai
    kafka >> worker >> gemini
    kafka >> worker >> anthropic
    kafka >> worker >> deepseek
    kafka >> worker >> qwen
    worker >> kafka >> result_aggregator >> api_gateway >> user
    load_balancer - Edge(color="brown", style="dashed") - worker
    auth_service - Edge(color="blue", style="dashed") - worker