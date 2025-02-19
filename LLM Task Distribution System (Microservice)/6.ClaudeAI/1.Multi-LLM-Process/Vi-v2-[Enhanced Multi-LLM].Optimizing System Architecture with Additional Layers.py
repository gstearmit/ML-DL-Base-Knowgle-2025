# Giải thích chi tiết kiến trúc hệ thống bằng tiếng Việt.

# Tổng Quan Kiến Trúc Hệ Thống Xử Lý Đa LLM:

# 1. Tầng Người Dùng (Client Layer)
# - Ứng dụng Khách hàng: Giao diện người dùng cuối để tương tác với hệ thống
# - CDN: Mạng phân phối nội dung, giúp tối ưu hóa việc truyền tải dữ liệu và giảm độ trễ

# 2. Tầng Bảo Mật (Security Layer)
# - API Gateway: Cổng giao tiếp chính cho mọi yêu cầu vào hệ thống
# - Tường lửa WAF: Bảo vệ chống lại các lỗ hổng bảo mật web phổ biến
# - Dịch vụ Xác thực: Quản lý việc xác thực và phân quyền người dùng
# - Kho lưu trữ Token: Lưu trữ an toàn các token xác thực

# 3. Tầng Kiểm Tra Dữ Liệu (Validation Layer)
# - Bộ Kiểm tra Đầu vào: Xác thực định dạng và dữ liệu của yêu cầu
# - Bộ Làm sạch Dữ liệu: Xử lý dữ liệu đầu vào để ngăn chặn tấn công injection
# - Bộ Kiểm tra Schema: Đảm bảo dữ liệu tuân theo cấu trúc đã định nghĩa

# 4. Tầng Quản Lý Tác Vụ (Task Management)
# - Quản lý Tác vụ: Điều phối việc thực thi các tác vụ
# - Phân tích Tác vụ: Phân tích và phân loại các tác vụ đầu vào
# - Cơ sở dữ liệu Tác vụ: Lưu trữ thông tin và trạng thái tác vụ
# - Điều phối DeepSeek: Quản lý việc định tuyến tác vụ cho DeepSeek

# 5. Tầng Hàng Đợi Tin Nhắn (Message Queue)
# - Kafka Broker: Hệ thống trung gian xử lý tin nhắn chính
# - Nhiều Hàng đợi: Cho phép xử lý song song và phân phối tải
# - Hàng đợi Dead Letter: Xử lý các tin nhắn thất bại

# 6. Tầng Quản Lý Tài Khoản (Account Management)
# - Dịch vụ Tài khoản: Quản lý tài khoản và quyền người dùng
# - Giới hạn Tốc độ: Kiểm soát tốc độ gọi API
# - Cân bằng Tải: Phân phối công việc giữa các worker
# - Cơ sở dữ liệu Tài khoản: Lưu trữ thông tin tài khoản
# - Redis Cache: Bộ nhớ đệm cho dữ liệu tài khoản thường xuyên truy cập

# 7. Tầng Xử Lý LLM (LLM Processing)
# - Nhiều Worker LLM: Xử lý tác vụ sử dụng các mô hình ngôn ngữ khác nhau
# - Bộ Thu thập Kết quả: Tổng hợp kết quả từ các worker
# - Bộ nhớ đệm Kết quả: Lưu trữ tạm kết quả để truy xuất nhanh

# 8. Tầng Xử Lý Kết Quả (Result Processing)
# - Trộn Kết quả: Kết hợp kết quả từ nhiều worker LLM
# - Phân tích Cuối cùng: Thực hiện phân tích cuối cùng trên kết quả đã trộn
# - Cơ sở dữ liệu Kết quả: Lưu trữ kết quả đã xử lý

# 9. Tầng Giám Sát (Monitoring)
# - Số liệu & Cảnh báo: Theo dõi hiệu suất hệ thống và kích hoạt cảnh báo
# - Tổng hợp Log: Tập trung hóa logs hệ thống
# - Theo dõi Phân tán: Theo dõi luồng yêu cầu qua hệ thống
# - Phân tích Thời gian thực: Phân tích hành vi hệ thống 

# 10. Tầng Chống Lỗi (Fault Tolerance)
# - Kho Sao lưu: Duy trì bản sao lưu hệ thống
# - Quản lý Phục hồi: Xử lý quy trình phục hồi hệ thống
# - Tự động Mở rộng: Tự động điều chỉnh phân bổ tài nguyên

# Ưu điểm Chính của Kiến trúc:

# 1. Tính Sẵn sàng Cao
# - Nhiều phiên bản worker cho mỗi LLM
# - Cơ chế chuyển đổi dự phòng tự động
# - Khả năng triển khai đa vùng

# 2. Khả năng Mở rộng
# - Mở rộng ngang các node worker
# - Phân phối tải qua hàng đợi
# - Bộ nhớ đệm nhiều tầng

# 3. Bảo mật
# - Phương pháp bảo mật nhiều lớp
# - Kiểm tra và làm sạch dữ liệu
# - Giới hạn tốc độ và kiểm soát truy cập

# 4. Hiệu suất
# - Sử dụng CDN cho phân phối nội dung
# - Chiến lược cache
# - Tối ưu hóa định tuyến tin nhắn


from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, StatefulSet, Deploy
from diagrams.k8s.network import Service, Ingress
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS, ElastiCache
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.security import IAM, WAF
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR, Kinesis
from diagrams.aws.management import Cloudwatch
from diagrams.aws.compute import AutoScaling

# Định nghĩa các biến màu sắc
EDGE_COLORS = {
    "primary": "#1E88E5",    # Xanh dương đậm
    "secondary": "#43A047",   # Xanh lá
    "warning": "#FDD835",     # Vàng
    "error": "#E53935",       # Đỏ
    "info": "#00ACC1"         # Xanh dương nhạt
}

with Diagram("Vi-v2-[Enhanced Multi-LLM].Optimizing System Architecture with Additional Layers", show=True, direction="TB"):
    # Tầng Client
    with Cluster("Tầng Người Dùng"):
        client = React("Ứng dụng Client")
        cdn = CloudFront("CDN")

    # Tầng Bảo Mật
    with Cluster("Tầng Bảo Mật"):
        waf = WAF("Web Application\nFirewall")
        api_gateway = APIGateway("API Gateway")
        auth = IAM("Dịch vụ Xác thực")
        token_store = S3("Kho Token")
        
        api_gateway >> Edge(color=EDGE_COLORS["primary"]) >> waf
        waf >> Edge(color=EDGE_COLORS["primary"]) >> auth
        auth - token_store

    # Tầng Kiểm Tra Dữ Liệu
    with Cluster("Tầng Validation"):
        validator = Pod("Kiểm tra\nĐầu vào")
        sanitizer = Pod("Làm sạch\nDữ liệu")
        schema = Pod("Kiểm tra\nSchema")
        
        validator >> Edge(color=EDGE_COLORS["info"]) >> sanitizer >> schema

    # Tầng Quản Lý Tác Vụ
    with Cluster("Tầng Quản Lý Tác Vụ"):
        task_manager = Server("Quản lý Tác vụ")
        orchestrator = Pod("DeepSeek\nOrchestrator")
        task_analyzer = Pod("Phân tích\nTác vụ")
        task_db = RDS("CSDL Tác vụ")
        task_cache = ElastiCache("Cache Tác vụ")
        
        task_manager >> orchestrator >> task_analyzer
        task_analyzer - task_db
        task_manager - task_cache

    # Tầng Message Queue
    with Cluster("Tầng Message Queue"):
        kafka = Kafka("Kafka Broker")
        queues = [
            SQS("Queue 1"),
            SQS("Queue 2"),
            SQS("Queue 3")
        ]
        dlq = SQS("Dead Letter\nQueue")
        
        kafka >> Edge(color=EDGE_COLORS["secondary"]) >> queues
        kafka >> Edge(color=EDGE_COLORS["error"]) >> dlq

    # Tầng Quản Lý Tài Khoản
    with Cluster("Tầng Quản Lý Tài Khoản"):
        account_service = StatefulSet("Dịch vụ\nTài khoản")
        rate_limiter = Pod("Giới hạn\nTốc độ")
        load_balancer = Service("Cân bằng\nTải")
        account_db = RDS("CSDL\nTài khoản")
        account_cache = ElastiCache("Cache\nTài khoản")
        
        account_service >> rate_limiter >> load_balancer
        account_service - account_db
        account_service - account_cache

    # Tầng Xử Lý LLM
    with Cluster("Tầng Xử Lý LLM"):
        llm_workers = [
            Deploy("OpenAI\nWorkers"),
            Deploy("Claude\nWorkers"),
            Deploy("Gemini\nWorkers"),
            Deploy("DeepSeek\nWorkers"),
            Deploy("Qwen\nWorkers")
        ]
        auto_scaling = AutoScaling("Tự động\nMở rộng")
        result_collector = StatefulSet("Thu thập\nKết quả")
        result_cache = ElastiCache("Cache\nKết quả")
        
        for worker in llm_workers:
            auto_scaling >> worker >> result_collector
        result_collector - result_cache

    # Tầng Xử Lý Kết Quả
    with Cluster("Tầng Xử Lý Kết quả"):
        merger = EMR("Trộn\nKết quả")
        final_analysis = Pod("Phân tích\nCuối cùng")
        result_db = RDS("CSDL\nKết quả")
        
        result_collector >> merger >> final_analysis
        final_analysis - result_db

    # Tầng Giám Sát
    with Cluster("Tầng Giám sát"):
        metrics = Cloudwatch("Metrics &\nCảnh báo")
        logs = Cloudwatch("Tập hợp\nLog")
        trace = Pod("Theo dõi\nPhân tán")
        analytics = Kinesis("Phân tích\nThời gian thực")
        
        [metrics, logs, trace] >> analytics

    # Tầng Fault Tolerance
    with Cluster("Tầng Fault Tolerance"):
        backup = S3("Kho\nSao lưu")
        recovery = Pod("Quản lý\nPhục hồi")
        
        [task_db, account_db, result_db] >> backup
        recovery >> backup

    # Kết nối các thành phần
    client >> cdn >> api_gateway
    schema >> task_manager
    task_analyzer >> kafka
    queues >> load_balancer
    load_balancer >> llm_workers
    final_analysis >> Edge(color=EDGE_COLORS["info"]) >> task_manager

    # Kết nối giám sát
    metrics >> Edge(color=EDGE_COLORS["warning"]) >> [
        task_manager,
        kafka,
        result_collector,
        account_service
    ]