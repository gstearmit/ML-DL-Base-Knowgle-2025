from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User, Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper 
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.network import Istio, Ambassador
from diagrams.onprem.aggregator import Fluentd 
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana
from diagrams.elastic.beats import Metricbeat, Filebeat 
from diagrams.generic.storage import Storage as MinioStorage
from diagrams.generic.compute import Rack
from diagrams.generic.place import Datacenter
from diagrams.generic.network import Subnet
from diagrams.custom import Custom
   
# Create the diagram
with Diagram("DocumentAI Architecture with Istio Service Mesh", show=True, direction="TB", filename="document_ai_architecture"):
    
    # Users/Clients
    user = User("Người dùng")
    
    # Client Layer
    with Cluster("Client Layer"):
        web_ui = Client("Web UI")
        mobile_app = Client("Mobile App")
        api_client = Client("API Client")
        clients = [web_ui, mobile_app, api_client]
    
    # Istio Service Mesh
    with Cluster("Istio Service Mesh"):
        ingress = Ambassador("Ingress Gateway")
        
        # Control Plane
        with Cluster("Control Plane"):
            istiod = Istio("Istiod\n(Pilot, Mixer, Citadel)")
            policy = Server("Policy Enforcement")
            telemetry = Server("Telemetry Collection")
            control_plane = [istiod, policy, telemetry]
        
        # Data Plane (Envoy Sidecars)
        with Cluster("Data Plane (Envoy Sidecars)"):
            api_gw_sidecar = Istio("API Gateway Sidecar")
            doc_sidecar = Istio("Document Service Sidecar")
            ai_sidecar = Istio("AI Engine Sidecar")
            rag_sidecar = Istio("RAG Service Sidecar")
            viz_sidecar = Istio("Visualization Sidecar")
            export_sidecar = Istio("Export Service Sidecar")
            ocr_sidecar = Istio("OCR Service Sidecar")
            vector_db_sidecar = Istio("Vector DB Sidecar")
            
            sidecars = [
                api_gw_sidecar, doc_sidecar, ai_sidecar, rag_sidecar,
                viz_sidecar, export_sidecar, ocr_sidecar, vector_db_sidecar
            ]
        
        # Application Services
        with Cluster("Application Services"):
            api_gateway = Server("API Gateway Service")
            doc_service = Server("Document Service")
            ai_engine = Server("AI Engine Service")
            rag_service = Server("RAG Service")
            viz_service = Server("Visualization Service")
            export_service = Server("Export Service")
            ocr_service = Server("OCR Service")
            vector_db_service = Server("Vector DB Service")
            
            services = [
                api_gateway, doc_service, ai_engine, rag_service,
                viz_service, export_service, ocr_service, vector_db_service
            ]
    
    # External Services
    with Cluster("External Services"):
        # Using Custom for external AI services 
        openai = Custom("OpenAI API\nGPT-4", "./custom_icons/openai.png")
        claude = Custom("Anthropic API\nClaude 3", "./custom_icons/claude.png")
        gemini = Custom("Google API\nGemini Pro", "./custom_icons/gemini.png")
        external_services = [openai, claude, gemini]
    
    # Data Layer
    with Cluster("Data Layer"):
        postgres = PostgreSQL("PostgreSQL")
        minio = MinioStorage("MinIO/S3")
        redis_cache = Redis("Redis Cache")
        vector_db = Custom("\n Vector Database \nPinecone/Weaviate", "./custom_icons/vectordb.png")
        data_stores = [postgres, minio, redis_cache, vector_db]
    
    # Messaging
    with Cluster("Messaging"):
        kafka = Kafka("Apache Kafka")
        zookeeper = Zookeeper("ZooKeeper")
        messaging = [kafka, zookeeper]
    
    # Observability
    with Cluster("Observability"):
        prometheus = Prometheus("Prometheus\nMetrics")
        jaeger = Jaeger("Jaeger\nTracing")
        kiali = Custom("Kiali\nService Mesh\nVisualization", "./custom_icons/kiali.png") 
        grafana = Grafana("Grafana\nDashboards")
        
        # ELK Stack
        with Cluster("ELK Stack"):
            elasticsearch = Elasticsearch("Elasticsearch")
            kibana = Kibana("Kibana")
            fluentd = Fluentd("Fluentd")
            elk = [elasticsearch, kibana, fluentd]
        
        observability = [prometheus, jaeger, kiali, grafana]
    
    # Define connections
    
    # User to clients
    user >> Edge(color="black") >> clients
    
    # Clients to Ingress
    for client in clients:
        client >> Edge(color="black") >> ingress
    
    # Ingress to API Gateway Sidecar
    ingress >> Edge(color="orange") >> api_gw_sidecar
    
    # Sidecar to service connections
    api_gw_sidecar - Edge(color="orange") - api_gateway
    doc_sidecar - Edge(color="orange") - doc_service
    ai_sidecar - Edge(color="orange") - ai_engine
    rag_sidecar - Edge(color="orange") - rag_service
    viz_sidecar - Edge(color="orange") - viz_service
    export_sidecar - Edge(color="orange") - export_service
    ocr_sidecar - Edge(color="orange") - ocr_service
    vector_db_sidecar - Edge(color="orange") - vector_db_service
    
    # Service Mesh Control
    for sidecar in sidecars:
        istiod >> Edge(color="orange", style="dashed") >> sidecar
    
    # Service Communication through sidecars
    api_gw_sidecar - Edge(color="orange") - doc_sidecar
    api_gw_sidecar - Edge(color="orange") - ai_sidecar
    api_gw_sidecar - Edge(color="orange") - rag_sidecar
    api_gw_sidecar - Edge(color="orange") - viz_sidecar
    api_gw_sidecar - Edge(color="orange") - export_sidecar
    
    doc_sidecar - Edge(color="orange") - ocr_sidecar
    doc_sidecar - Edge(color="orange") - ai_sidecar
    
    ai_sidecar - Edge(color="orange") - vector_db_sidecar
    ai_sidecar - Edge(color="orange") - doc_sidecar
    
    rag_sidecar - Edge(color="orange") - ai_sidecar
    rag_sidecar - Edge(color="orange") - vector_db_sidecar
    
    # External Connections
    ai_engine >> Edge(color="blue") >> external_services
    rag_service >> Edge(color="blue") >> external_services
    
    # Database Connections
    doc_service >> Edge(color="purple") >> postgres
    doc_service >> Edge(color="purple") >> minio
    vector_db_service >> Edge(color="purple") >> vector_db
    ai_engine >> Edge(color="purple") >> minio
    viz_service >> Edge(color="purple") >> minio
    
    # Messaging
    kafka - Edge(color="red") - doc_service
    kafka - Edge(color="red") - ai_engine
    zookeeper - Edge(color="red") - kafka
    
    # Redis Caching
    redis_cache - Edge(color="purple") - api_gateway
    redis_cache - Edge(color="red") - rag_service
    redis_cache - Edge(color="red") - ai_engine
    
    # Observability
    for sidecar in sidecars:
        sidecar >> Edge(color="pink", style="dotted") >> jaeger
        sidecar >> Edge(color="pink", style="dotted") >> prometheus
    
    istiod >> Edge(color="pink", style="dotted") >> kiali
    prometheus >> Edge(color="pink", style="dotted") >> grafana
    jaeger >> Edge(color="pink", style="dotted") >> grafana
    
    for service in services:
        service >> Edge(color="pink", style="dotted") >> fluentd
    
    fluentd >> elasticsearch >> kibana




 