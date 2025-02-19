```python
# Tôi sẽ giải thích chi tiết kiến trúc hệ thống theo từng tầng theo thứ tự từ trên xuống dưới:

# 1. 1.Client Layer  (Tầng Người Dùng)
# - Đây là tầng đầu tiên tiếp nhận các yêu cầu từ người dùng
# - Bao gồm Web Client và Mobile Client để hỗ trợ đa nền tảng
# - Sử dụng Global CDN để tối ưu việc phân phối nội dung trên phạm vi toàn cầu
# - Tích hợp DDoS Protection thông qua AWS Shield để bảo vệ hệ thống khỏi các cuộc tấn công từ chối dịch vụ

# 2. Tầng Bảo Mật (Security Layer)  
# - WAF (Web Application Firewall) bảo vệ ứng dụng khỏi các cuộc tấn công web phổ biến
# - API Gateway quản lý và kiểm soát các API endpoints
# - Auth Service xử lý xác thực người dùng sử dụng Lambda
# - Token Store lưu trữ các token xác thực an toàn trên S3

# 3. Tầng Xử Lý Dữ Liệu (Data Processing Layer)
# - Input Validator kiểm tra tính hợp lệ của dữ liệu đầu vào
# - Data Sanitizer làm sạch dữ liệu để tránh các mã độc
# - Schema Validator đảm bảo dữ liệu tuân thủ cấu trúc định nghĩa
# - Data Transformer chuyển đổi dữ liệu sang định dạng phù hợp

# 4. Tầng Điều Phối Tác Vụ (Task Orchestration Layer)
# - Task Manager quản lý và điều phối các tác vụ
# - LLM Orchestrator phân phối tác vụ cho các mô hình LLM phù hợp
# - Task Analyzer phân tích và phân loại các tác vụ
# - Sử dụng Task Database và Task Cache để tối ưu hiệu suất

# 5. Tầng Quản Lý Queue (Queue Management Layer)
# - Kafka Cluster đảm bảo xử lý message theo thứ tự và có khả năng mở rộng
# - Hệ thống 3 queue:
#   + Priority Queue cho các tác vụ ưu tiên cao
#   + Standard Queue cho các tác vụ thông thường
#   + Batch Queue cho xử lý hàng loạt
# - Dead Letter Queue xử lý các message thất bại

# 6. Tầng Quản Lý Tài Nguyên (Resource Management Layer)
# - Account Service quản lý thông tin và quyền hạn người dùng
# - Rate Limiter kiểm soát tần suất gọi API
# - Load Balancer phân phối tải đồng đều
# - Account Database và Cache lưu trữ và tối ưu truy xuất

# 7. Tầng Xử Lý LLM (LLM Processing Layer)
# - Auto Scaling Manager tự động điều chỉnh số lượng workers
# - Năm engine LLM chính: OpenAI, Claude, Gemini, DeepSeek, Qwen
# - Result Collector tổng hợp kết quả từ các engine
# - Result Cache lưu trữ tạm thời kết quả để tái sử dụng

# 8. Tầng Xử Lý Kết Quả (Result Processing Layer)
# - Result Merger kết hợp kết quả từ nhiều nguồn
# - Result Analyzer phân tích chất lượng kết quả
# - Final Processor xử lý cuối cùng trước khi trả về
# - Result Database lưu trữ kết quả lâu dài

# 9. Tầng Giám Sát (Monitoring Layer)
# - Metrics & Alerts theo dõi và cảnh báo về hiệu suất hệ thống
# - Log Aggregation tập hợp logs từ các thành phần
# - Distributed Tracing theo dõi luồng xử lý
# - Real-time Analytics phân tích dữ liệu thời gian thực
# - System Monitor giám sát tổng thể hệ thống

# 10. Tầng Độ Tin Cậy (Reliability Layer)
# - Backup Store sao lưu dữ liệu định kỳ
# - Recovery Manager quản lý quy trình phục hồi
# - Health Checker kiểm tra sức khỏe các thành phần

# Các Điểm Nổi Bật của Kiến Trúc:

# 1. Khả năng Mở Rộng
# - Thiết kế theo microservices
# - Auto-scaling tự động
# - Cấu trúc queue có thể mở rộng
# - Phân tán tải qua load balancer

# 2. Độ Tin Cậy
# - Nhiều lớp cache
# - Hệ thống backup đầy đủ
# - Xử lý lỗi với Dead Letter Queue
# - Giám sát và cảnh báo chủ động

# 3. Bảo Mật
# - Nhiều lớp bảo vệ (Shield, WAF)
# - Xác thực và phân quyền chặt chẽ
# - Mã hóa và quản lý token an toàn
# - Kiểm soát truy cập API

# 4. Hiệu Suất
# - Global CDN
# - Hệ thống cache nhiều tầng
# - Xử lý song song với nhiều queue
# - Tối ưu hóa truy vấn database

# Bạn có cần thêm thông tin chi tiết về bất kỳ tầng hoặc thành phần nào không?


from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, StatefulSet, Deploy
from diagrams.k8s.network import Service, Ingress
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS, ElastiCache
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.aws.network import APIGateway, CloudFront, ELB
from diagrams.aws.security import IAM, WAF, Shield
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR, Kinesis
from diagrams.aws.management import Cloudwatch, SystemsManager
from diagrams.aws.compute import AutoScaling, Lambda

# Định nghĩa màu sắc cho các luồng xử lý khác nhau
EDGE_COLORS = {
    "primary": "#1E88E5",    # Main flow
    "secondary": "#43A047",   # Queue processing
    "warning": "#FDD835",     # Monitoring
    "error": "#E53935",      # Error handling
    "info": "#00ACC1",       # Data flow
    "success": "#4CAF50"     # Successful processing
}

# Định nghĩa style cho các node
NODE_CONFIG = {
    "fontsize": "13",
    "width": "2.0",
    "height": "1.5"
}

with Diagram(
    "En-v2-[Enhanced Multi-LLM].Final Multi-LLM Processing System Architecture",
    show=True,
    direction="TB",
    graph_attr={
        "splines": "ortho",
        "nodesep": "0.8",
        "ranksep": "1.0",
        "fontsize": "20"
    }
):
    # Client & Entry Layer
    with Cluster("1.Client Layer \n (Tầng Người Dùng)"):
        shield = Shield("DDoS Protection \n(Shield)")
        client = React("Web Client")
        mobile = React("Mobile Client")
        cdn = CloudFront("Global CDN")
        
        [client, mobile] >> cdn >> shield

    # Security & Authentication
    with Cluster("2.Security Layer \n (Tầng Bảo Mật)"):
        waf = WAF("WAF \n (Tường lửa \n - bảo vệ ứng dụng \n khỏi các cuộc \n tấn công web \n phổ biến )")
        api_gateway = APIGateway("API Gateway \n (Công giao tiếp chính)")
        auth_service = Lambda("Auth Service \n (Dịch vụ Xác thực)")
        token_store = S3("Token Store \n (Kho Lưu trữ Token)")
        
        shield >> waf >> api_gateway
        api_gateway >> Edge(color=EDGE_COLORS["primary"]) >> auth_service
        auth_service - token_store

    # Data Validation & Processing
    with Cluster("3.Data Processing Layer \n (Tầng Xử Lý Dữ Liệu)"):
        input_validator = Pod("Input Validator \n (Kiểm tra Đầu vào)")
        sanitizer = Pod("Data Sanitizer \n (Làm sạch dữ liệu)")
        schema_validator = Pod("Schema Validator \n (Kiểm tra Schema)")
        data_transformer = Pod("Data Transformer \n (Dữ liệu chuyển đổi)")
        
        api_gateway >> input_validator >> sanitizer >> schema_validator >> data_transformer

    # Task Orchestration
    with Cluster("4.Task Orchestration Layer \n (Tầng Điều Phối Tác Vụ)"):
        task_manager = Server("Task Manager \n (Quản lí tác vụ)")
        orchestrator = Pod("LLM Orchestrator \n (Quản lý LLM)")
        task_analyzer = Pod("Task Analyzer \n (Phân tích các tác vụ)")
        task_db = RDS("Task Database \n (Cơ sở dữ liệu tác vụ)")
        task_cache = ElastiCache("Task Cache \n (Tác vụ Cache)")
        
        data_transformer >> task_manager >> orchestrator >> task_analyzer
        task_analyzer - task_db
        task_manager - task_cache

    # Message Queue System
    with Cluster("5.Queue Management Layer \n (Tầng Quản Lý Queue)"):
        kafka = Kafka("Kafka Cluster \n đảm bảo xử lý message theo thứ tự \n và có khả năng \n mở rộng")
        queues = [
            SQS("Priority Queue \n (tác vụ ưu tiên cao)"),
            SQS("Standard Queue \n (tác vụ thông thường)"),
            SQS("Batch Queue \n (Xử lý hàng loạt)")
        ]
        dlq = SQS("Dead Letter Queue \n (Xử lý các Message thât bại)")
        
        task_analyzer >> kafka >> Edge(color=EDGE_COLORS["secondary"]) >> queues
        kafka >> Edge(color=EDGE_COLORS["error"]) >> dlq

    # Account & Resource Management
    with Cluster("6.Resource Management Layer \n (Tầng Quản \n Lý Tài Nguyên)"):
        account_service = StatefulSet("Account Service \n (quản lý \n thông tin \n và quyền hạn người dùng)")
        rate_limiter = Pod("Rate Limiter \n (Kiểm soát \n tần xuất \n gọi API)")
        load_balancer = ELB("Load Balancer \n (Phân phối \n tải đồng đều)")
        account_db = RDS("Account Database \n (Thông tin \n lưu trữ tài khoản)")
        account_cache = ElastiCache("Account Cache \n (Tối ưu hóa \n truy xuất \n đến Account)")
        
        account_service >> rate_limiter >> load_balancer
        account_service - account_db
        account_service - account_cache

    # LLM Processing
    with Cluster("7.LLM Processing Layer \n (Tầng xử lí LLM)"):
        scaling_manager = AutoScaling("Auto Scaling Manager \n (Tự động điều chỉnh \n Số lượng workers)")
        llm_workers = [
            Deploy("OpenAI Engine"),
            Deploy("Claude Engine"),
            Deploy("Gemini Engine"),
            Deploy("DeepSeek Engine"),
            Deploy("Qwen Engine")
        ]
        result_collector = StatefulSet("Result Collector \n (Tổng hợp kết \n quả từ \n các engine)")
        result_cache = ElastiCache("Result Cache \n (Lưu trữ \n tạm thời \n kết quả \n để tái \n sử dụng)")
        
        queues >> load_balancer >> scaling_manager
        for worker in llm_workers:
            scaling_manager >> worker >> result_collector
        result_collector - result_cache

    # Result Processing
    with Cluster("8.Result Processing Layer \n (Tầng xử lý kết quả)"):
        merger = EMR("Result Merger \n (Kết hợp kết quả từ nhiều nguồn)")
        analyzer = Pod("Result Analyzer \n (Phân tích chất lượng kết quả)")
        final_processor = Pod("Final Processor \n (Xử lý cuối trước khi trả về)")
        result_db = RDS("Result Database \n (Lưu trữ kết quả lâu dài)")
        
        result_collector >> merger >> analyzer >> final_processor
        final_processor - result_db

    # System Monitoring
    with Cluster("9.Monitoring Layer \n (Tầng giám sát)"):
        metrics = Cloudwatch("Metrics & Alerts \n (Theo dõi \n và cảnh báo \n hiệu suất \n hệ thống)")
        logs = Cloudwatch("Log Aggregation \n (Tâp hợp logs \n từ các thành phần)")
        tracer = Pod("Distributed Tracing \n (Theo dõi \n luồng xử lý)")
        analytics = Kinesis("Real-time Analytics \n (Phân tích \n dũ liệu \n thời gian thực)")
        monitor = SystemsManager("System Monitor \n (Giám sát \n tổng thể \n hệ thống)")
        
        metrics >> monitor
        [logs, tracer] >> analytics >> monitor

    # Reliability & Recovery
    with Cluster("10. Reliability Layer \n (Tầng độ tin cậy)"):
        backup_store = S3("Backup Store \n (Sao lưu dữ liệu định kì)")
        recovery_manager = Pod("Recovery Manager \n (Quản lí quy trình phục hồi)")
        health_check = Pod("Health Checker \n (Kiểm tra \n sức khỏe \n của các thành phần)")
        
        [task_db, account_db, result_db] >> backup_store
        recovery_manager >> backup_store
        health_check >> monitor

    # System Feedback Loop
    final_processor >> Edge(color=EDGE_COLORS["success"]) >> task_manager

    # Monitoring Connections
    monitor >> Edge(color=EDGE_COLORS["warning"]) >> [
        task_manager,
        kafka,
        load_balancer,
        scaling_manager,
        result_collector
    ]
```