from diagrams import Diagram, Cluster, Edge
from diagrams.oci.network import LoadBalancer
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.auth import Oauth2Proxy as OAuth2
from diagrams.onprem.auth import Oauth2Proxy as JWT
from diagrams.onprem.network import Consul
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import MySQL
from diagrams.onprem.ci import Jenkins
from diagrams.custom import Custom

with Diagram("02_Fixed_Microservice_Architecture", show=False):
    # Tạo các icon custom bên trong with Diagram(...)
    logstash = Custom("Logstash", "./icons/logstash.png")
    kibana = Custom("Kibana", "./icons/kibana.png")
    metricbeat = Custom("Metricbeat", "./icons/metricbeat.png")
    filebeat = Custom("Filebeat", "./icons/filebeat.png")

    pinecone = Custom("Pinecone", "./icons/pinecone.png")
    chroma = Custom("Chroma", "./icons/chroma.png")
    weaviate = Custom("Weaviate", "./icons/weaviate.png")

    apache_jena = Custom("Apache Jena", "./icons/apachejena.png")
    rdf4j = Custom("RDF4J", "./icons/rdf4j.png")

    client = Server("Client")
    gateway = Server("API Gateway")
    gateway << [OAuth2("Authentication"), JWT("Authorization")]
    
    with Cluster("Services"):
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
    
    with Cluster("Monitoring"):
        monitoring = [Prometheus(), Grafana(), Jaeger()]
    
    with Cluster("Security"):
        security = [OAuth2("Auth"), JWT("Token Validation")]
    
    with Cluster("Infrastructure"):
        load_balancer = LoadBalancer("API Gateway LB")
    
    with Cluster("Logging Pipeline"):
        logging_pipeline = [Server("Graylog"), logstash, kibana, metricbeat, filebeat]
    
    with Cluster("Data Management"):
        vector_db = [pinecone, chroma, weaviate, Redis("Vector Store")]
        cache_cluster = [Redis("Cache"), Redis("Session"), Redis("Rate Limiting")]
    
    with Cluster("Knowledge Graph"):
        knowledge_graph = [apache_jena, rdf4j]
    
    # Connect components
    client >> gateway
    gateway >> task_manager
    task_manager >> orchestrator
    
    orchestrator >> kafka
    kafka >> [openai_worker, genmini_worker, claude_worker, deepseek_worker, qwen_worker]
    [openai_worker, genmini_worker, claude_worker, deepseek_worker, qwen_worker] >> orchestrator
    
    orchestrator >> rate_limiter >> load_balancer
    
    # Monitoring connections
    monitoring >> Edge(label="Metrics") >> orchestrator
    monitoring >> Edge(label="Metrics") >> kafka
    monitoring >> Edge(label="Metrics") >> gateway
    
    # Logging connections
    client >> Edge(label="Logs") >> logstash
    gateway >> Edge(label="Logs") >> logstash
    task_manager >> Edge(label="Logs") >> logstash
    orchestrator >> Edge(label="Logs") >> logstash
    kafka >> Edge(label="Logs") >> logstash
    
    # Data management
    for db in vector_db:
        for kg in knowledge_graph:
            db >> kg
    
    for cache in cache_cluster:
        gateway >> cache
        task_manager >> cache
    
    # CI/CD pipeline
    Jenkins("CI/CD") >> gateway

 
