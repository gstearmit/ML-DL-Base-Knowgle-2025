from diagrams import Diagram, Cluster
from diagrams.oci.network import LoadBalancer
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server

with Diagram("Microservice Architecture", show=False):
    client = Server("Client")
    gateway = Server("API Gateway")
    task_manager = Server("Task Manager")
    orchestrator = Server("DeepSeek R1 (Orchestrator)")
    rate_limiter = Server("Rate Limiter / Account Manager")
    
    kafka = Kafka("Kafka Broker")
    
    with Cluster("LLM Worker Services"):
        openai_worker = Server("OpenAI Worker")
        genmini_worker = Server("Genmini Worker")
        claude_worker = Server("Claude Worker")
        deepseek_worker = Server("DeepSeek Worker")
        qwen_worker = Server("Qwen-2.5 Worker")
    
    client >> gateway >> task_manager >> orchestrator
    orchestrator >> kafka
    kafka >> openai_worker
    kafka >> genmini_worker
    kafka >> claude_worker
    kafka >> deepseek_worker
    kafka >> qwen_worker
    
    # Các worker gửi kết quả về hợp nhất và đánh giá
    openai_worker >> orchestrator
    genmini_worker >> orchestrator
    claude_worker >> orchestrator
    deepseek_worker >> orchestrator
    qwen_worker >> orchestrator
    
    # Đường truyền quản lý giới hạn và cân bằng tải
    orchestrator >> rate_limiter
    rate_limiter >> LoadBalancer("Load Balancer")
    
    # Thư viện vẽ sơ đồ
    with Cluster("ELK Stack"):
        logstash = Server("Logstash")
        kibana = Server("Kibana")
        metricbeat = Server("Metricbeat")
        filebeat = Server("Filebeat")
    
    logstash >> kibana
    logstash >> metricbeat
    logstash >> filebeat    
    
    # Thư viện vẽ biểu đồ
    with Cluster("Visualisation"):
        startuml = Server("StartUML")
        mermaid = Server("Mermaid")
        diagram = Server("Diagram")
        plantuml = Server("PlantUML")
    
    startuml >> mermaid
    mermaid >> diagram
    diagram >> plantuml
    
    # Thư viện vẽ cơ sở dữ liệu
    with Cluster("Vector DB"):
        pinecone = Server("Pinecone")
        chroma = Server("Chroma")
        weaviate = Server("Weaviate")
        redis = Server("Redis")
    
    pinecone >> chroma
    chroma >> weaviate
    weaviate >> redis
    