from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.integration import SQS
from diagrams.onprem.queue import Kafka
from diagrams.onprem.client import User
from diagrams.generic.device import Mobile
from diagrams.custom import Custom

with Diagram("System Design for Task Dispatcher & LLM Aggregator", show=False):
    user = User("Người dùng")

    with Cluster("API Gateway"):
        gateway = ECS("API Gateway")
    
    with Cluster("Task Coordination"):
        coordinator = Custom("LLM DeepSeek R1\n(Task Coordinator & Evaluator)", "./../images/llm_icon.png")
    
    with Cluster("Message Queue"):
        kafka = Kafka("Kafka Cluster")
    
    with Cluster("Task Processors"):
        openai = Custom("OpenAI Connector", "./../images/openai_icon.png")
        genmini = Custom("Genmini Connector", "./../images/genmini_icon.png")
        claude = Custom("Claude Connector", "./../images/claude_icon.png")
        deepseek = Custom("DeepSeek Connector", "./../images/deepseek_icon.png")
        qwen = Custom("Qwen-2.5 Connector", "./../images/qwen_icon.png")
    
    with Cluster("Result Merger"):
        merger = ECS("Result Merger")
    
    # Flow connections
    user >> gateway >> coordinator
    coordinator >> kafka

    # Kafka đẩy task tới các connector song song
    kafka >> Edge(label="Task 1") >> openai
    kafka >> Edge(label="Task 2") >> genmini
    kafka >> Edge(label="Task 3") >> claude
    kafka >> Edge(label="Task 4") >> deepseek
    kafka >> Edge(label="Task 5") >> qwen

    # Các connector gửi kết quả về merger
    openai >> merger
    genmini >> merger
    claude >> merger
    deepseek >> merger
    qwen >> merger

    # Merger gửi kết quả tổng hợp về coordinator
    merger >> coordinator

    # Coordinator gửi kết quả cuối cùng về gateway và sau đó tới người dùng
    coordinator >> gateway >> user
