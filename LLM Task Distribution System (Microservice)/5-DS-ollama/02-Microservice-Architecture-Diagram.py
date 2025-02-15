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
from diagrams.elastic.elasticsearch import Logstash, Kibana
from diagrams.elastic.beats import Metricbeat, Filebeat
from diagrams.custom import Custom
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress as IngressController

# Định nghĩa các dịch vụ chưa có
Pinecone = lambda: Custom("Pinecone", "./icons/pinecone.png")
Chroma = lambda: Custom("Chroma", "./icons/chroma.png")
Weaviate = lambda: Custom("Weaviate", "./icons/weaviate.png")
ApacheJena = lambda: Custom("Apache Jena", "./icons/apachejena.png")
RDF4J = lambda: Custom("RDF4J", "./icons/rdf4j.png")

with Diagram("02_Microservice_Architecture", show=False):
    client = Server("Client")
    gateway = Server("API Gateway")

    with Cluster("Authentication & Authorization"):
        auth = OAuth2("Authentication")
        token_validation = JWT("Authorization")
        gateway << auth
        gateway << token_validation

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
        prometheus = Prometheus()
        grafana = Grafana()
        jaeger = Jaeger()

    with Cluster("Infrastructure"):
        load_balancer = LoadBalancer("API Gateway LB")
        ingress = IngressController("Ingress Controller")

    with Cluster("Logging Pipeline"):
        logstash = Logstash()
        kibana = Kibana()
        metricbeat = Metricbeat()
        filebeat = Filebeat()

    with Cluster("Data Management"):
        vector_db = [
            Pinecone(),
            Chroma(),
            Weaviate(),
            Redis("Vector Store")
        ]
        cache_cluster = [
            Redis("Cache"),
            Redis("Session"),
            Redis("Rate Limiting")
        ]

    with Cluster("Knowledge Graph"):
        knowledge_graph = [
            ApacheJena(),
            RDF4J()
        ]

    # Connect components
    client >> gateway
    gateway >> task_manager
    task_manager >> orchestrator

    orchestrator >> kafka
    kafka >> [openai_worker, genmini_worker, claude_worker, deepseek_worker, qwen_worker]
    [openai_worker, genmini_worker, claude_worker, deepseek_worker, qwen_worker] >> orchestrator

    orchestrator >> rate_limiter >> load_balancer >> ingress

    # Monitoring connections
    prometheus >> Edge(label="Metrics") >> orchestrator
    prometheus >> Edge(label="Metrics") >> kafka
    prometheus >> Edge(label="Metrics") >> gateway

    # Tracing connections
    jaeger >> Edge(label="Span Context") >> client
    jaeger >> Edge(label="Span Context") >> gateway
    jaeger >> Edge(label="Span Context") >> task_manager
    jaeger >> Edge(label="Span Context") >> orchestrator

    # Logging connections
    client >> Edge(label="Logs") >> logstash
    gateway >> Edge(label="Logs") >> logstash
    task_manager >> Edge(label="Logs") >> logstash
    orchestrator >> Edge(label="Logs") >> logstash
    kafka >> Edge(label="Logs") >> logstash
    openai_worker >> Edge(label="Logs") >> logstash
    genmini_worker >> Edge(label="Logs") >> logstash
    claude_worker >> Edge(label="Logs") >> logstash
    deepseek_worker >> Edge(label="Logs") >> logstash

    # Data management
    orchestrator >> vector_db
    task_manager >> vector_db
    gateway >> cache_cluster
    task_manager >> cache_cluster

    # Knowledge graph integration
    [db >> kg for db in vector_db for kg in knowledge_graph]

    # CI/CD pipeline
    jenkins = Jenkins("CI/CD")
    jenkins >> gateway
