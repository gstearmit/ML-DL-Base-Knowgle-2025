from diagrams import Diagram, Cluster, Node, Edge
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
from diagrams.elastic.elasticsearch import Logstash, Kibana
from diagrams.elastic.beats import Metricbeat, Filebeat
from diagrams.custom import Custom
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress as IngressController

with Diagram("02_Microservice_Architecture", show=False) as diag:
    client = Server("Client")
    gateway = Server("API Gateway") << (OAuth2("Authentication"), JWT("Authorization"))
    
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
    
    monitoring = Cluster("Monitoring") << (
        Prometheus(),
        Grafana(),
        Jaeger()
    )
    
    security = Cluster("Security") << (
        OAuth2("Auth"),
        JWT("Token Validation")
    )
    
    with Cluster("Infrastructure"):
        load_balancer = LoadBalancer("API Gateway LB")
        ingress = IngressController("Ingress Controller")
        
    logging_pipeline = Cluster("Logging Pipeline") << (
        Server("Graylog"),
        Logstash,
        Kibana,
        Metricbeat,
        Filebeat
    )
    
    with Cluster("Data Management"):
        vector_db = Cluster("Vector DB") << (
            Pinecone(),
            Chroma(),
            Weaviate(),
            Redis("Vector Store")
        )
        
        cache_cluster = Cluster("Cache") << (
            Redis("Cache"),
            Redis("Session"),
            Redis("Rate Limiting")
        )
        
    with Cluster("Knowledge Graph"):
        knowledge_graph = Cluster("Knowledge Graph") << (
            ApacheJena(),
            RDF4J()
        )
    
    # Connect components
    client >> gateway
    gateway >> task_manager
    task_manager >> orchestrator
    
    orchestrator >> kafka
    kafka >> openai_worker
    kafka >> genmini_worker
    kafka >> claude_worker
    kafka >> deepseek_worker
    kafka >> qwen_worker
    
    [openai_worker, genmini_worker, claude_worker,
     deepseek_worker, qwen_worker] >> orchestrator
    
    orchestrator >> rate_limiter >> load_balancer >> ingress
    
    # Monitoring connections
    monitoring.connect_to(orchestrator, Edge("Metrics"))
    monitoring.connect_to(kafka, Edge("Metrics"))
    monitoring.connect_to(gateway, Edge("Metrics"))
    
    # Tracing connections
    jaeger.connect_to(client, Edge("Span Context"))
    jaeger.connect_to(gateway, Edge("Span Context"))
    jaeger.connect_to(task_manager, Edge("Span Context"))
    jaeger.connect_to(orchestrator, Edge("Span Context"))
    
    # Security components
    gateway << (security)
    
    # Logging connections
    client.log(logstash)
    gateway.log(logstash)
    task_manager.log(logstash)
    orchestrator.log(logstash)
    kafka.log(logstash)
    openai_worker.log(logstash)
    genmini_worker.log(logstash)
    claude_worker.log(logstash)
    deepseek_worker.log(logstash)
    
    # Data management
    vector_db << (orchestrator, task_manager)
    cache_cluster << (gateway, task_manager)
    
    # Knowledge graph integration
    knowledge_graph << vector_db
    
    # CI/CD pipeline
    Jenkins("CI/CD") >> gateway

diag.view()