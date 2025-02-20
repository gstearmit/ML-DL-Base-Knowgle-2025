from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx, HAProxy
from diagrams.onprem.security import Vault
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka, RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.programming.framework import Spring, React
from diagrams.onprem.analytics import Spark
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.custom import Custom 

# Định nghĩa màu sắc cho các luồng xử lý
EDGE_COLORS = {
    "primary": "#1E88E5",    # Luồng chính
    "secondary": "#43A047",   # Xử lý queue
    "warning": "#FDD835",     # Giám sát
    "error": "#E53935",       # Xử lý lỗi
    "info": "#00ACC1",        # Luồng dữ liệu
    "success": "#4CAF50"      # Xử lý thành công
}

# Cấu hình style cho nodes
NODE_CONFIG = {
    "fontsize": "13",
    "width": "2.0",
    "height": "1.5"
}

with Diagram(
    "Final On-Premises Multi-LLM System Architecture",
    show=True,
    direction="TB",
    graph_attr={
        "splines": "ortho",
        "nodesep": "0.8",
        "ranksep": "1.0",
        "fontsize": "20"
    }
):
    # 1. Tầng Người Dùng
    with Cluster("1. Tầng Người Dùng"):
        web_client = React("Web Client\nVue/React")
        mobile_client = React("Mobile Client\niOS/Android")
        nginx_cdn = Nginx("Nginx CDN Cluster")
        firewall = Firewall("Firewall Cluster\nPalo Alto")
        
        [web_client, mobile_client] >> nginx_cdn >> firewall

    # 2. Tầng Bảo Mật
    with Cluster("2. Tầng Bảo Mật"):
        modsec = Server("ModSecurity WAF")
        kong = Server("Kong API Gateway")
        keycloak = Server("Keycloak IAM")
        minio_token = Custom("MinIO Token Store\nHigh Availability", "./icons/minio.png")
        
        firewall >> modsec >> kong
        kong >> Edge(color=EDGE_COLORS["primary"]) >> keycloak
        keycloak - minio_token

    # 3. Tầng Xử Lý Dữ Liệu
    with Cluster("3. Tầng Xử Lý Dữ Liệu"):
        validator = Pod("Input Validator\nJSON Schema")
        sanitizer = Pod("Data Sanitizer")
        schema = Pod("Schema Validator\nOpenAPI")
        transformer = Pod("Data Transformer\nApache NiFi")
        
        kong >> validator >> sanitizer >> schema >> transformer

    # 4. Tầng Điều Phối Tác Vụ
    with Cluster("4. Tầng Điều Phối Tác Vụ"):
        task_mgr = StatefulSet("K8s Task Manager")
        llm_orch = Pod("LLM Orchestrator")
        task_analyzer = Pod("Task Analyzer\nML Model")
        task_db = PostgreSQL("PostgreSQL 15\nTask DB")
        task_cache = Redis("Redis 7\nTask Cache")
        
        transformer >> task_mgr >> llm_orch >> task_analyzer
        task_analyzer - task_db
        task_mgr - task_cache

    # 5. Tầng Quản Lý Queue
    with Cluster("5. Tầng Quản Lý Queue"):
        kafka = Kafka("Kafka 3.5 Cluster")
        rmq_priority = RabbitMQ("Priority Queue")
        rmq_standard = RabbitMQ("Standard Queue")
        rmq_batch = RabbitMQ("Batch Queue")
        rmq_dlq = RabbitMQ("Dead Letter Queue")
        
        task_analyzer >> kafka >> Edge(color=EDGE_COLORS["secondary"]) >> [rmq_priority, rmq_standard, rmq_batch]
        kafka >> Edge(color=EDGE_COLORS["error"]) >> rmq_dlq

    # 6. Tầng Quản Lý Tài Nguyên
    with Cluster("6. Tầng Quản Lý Tài Nguyên"):
        account_svc = Spring("Account Service")
        rate_limit = HAProxy("Rate Limiter")
        load_bal = HAProxy("Load Balancer")
        account_db = PostgreSQL("PostgreSQL 15\nAccount DB")
        account_cache = Redis("Redis 7\nAccount Cache")
        
        account_svc >> rate_limit >> load_bal
        account_svc - account_db
        account_svc - account_cache

    # 7. Tầng Xử Lý LLM
    with Cluster("7. Tầng Xử Lý LLM"):
        k8s_scaling = Pod("K8s HPA\nAuto Scaling")
        llm_engines = [
            Docker("OpenAI Engine"),
            Docker("Claude Engine"),
            Docker("Gemini Engine"),
            Docker("DeepSeek Engine"),
            Docker("Qwen Engine")
        ]
        collector = StatefulSet("Result Collector")
        result_cache = Redis("Redis 7\nResult Cache")
        
        [rmq_priority, rmq_standard, rmq_batch] >> load_bal >> k8s_scaling
        for engine in llm_engines:
            k8s_scaling >> engine >> collector
        collector - result_cache

    # 8. Tầng Xử Lý Kết Quả
    with Cluster("8. Tầng Xử Lý Kết Quả"):
        merger = Spark("Result Merger")
        result_analyzer = Pod("Result Analyzer")
        final_proc = Pod("Final Processor")
        result_db = PostgreSQL("PostgreSQL 15\nResult DB")
        
        collector >> merger >> result_analyzer >> final_proc
        final_proc - result_db

    # 9. Tầng Giám Sát
    with Cluster("9. Tầng Giám Sát"):
        prom = Prometheus("Prometheus\nMetrics")
        elastic = Server("ELK Stack 8.x")
        jaeger = Server("Jaeger Tracing")
        flink = Spark("Apache Flink")
        grafana = Grafana("Grafana Dashboards")
        
        prom >> grafana
        [elastic, jaeger] >> flink >> grafana

    # 10. Tầng Độ Tin Cậy
    with Cluster("10. Tầng Độ Tin Cậy"):
        backup = Custom("MinIO Backup", "./icons/minio.png")
        recovery = Pod("Recovery Manager")
        health = Spring("Health Checker")
        keepalived = Server("Keepalived HA")
        
        [task_db, account_db, result_db] >> backup
        recovery >> backup
        health >> grafana
        keepalived >> [firewall, load_bal, kafka]

    # System Feedback Loop
    final_proc >> Edge(color=EDGE_COLORS["success"]) >> task_mgr

    # Monitoring Connections
    grafana >> Edge(color=EDGE_COLORS["warning"]) >> [
        task_mgr,
        kafka,
        load_bal,
        k8s_scaling,
        collector
    ]