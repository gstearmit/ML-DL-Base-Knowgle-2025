# Giải thích cách hoạt động của kiến trúc hệ thống

## Các lớp trong hệ thống

### 1. Lớp Client (Client Layer)
- **Web Application**: Giao diện người dùng trên web
- **Mobile App**: Ứng dụng di động
- **API Client**: Các ứng dụng bên thứ ba kết nối thông qua API

### 2. Lớp API Gateway
- **Kong API Gateway**: Cổng API trung tâm, điều hướng các yêu cầu đến các dịch vụ phù hợp
- **Authentication & Authorization**: Xác thực và phân quyền người dùng
- **Rate Limiter**: Giới hạn số lượng yêu cầu để tránh quá tải
- **API Documentation**: Tài liệu API cho nhà phát triển

### 3. Lớp Microservice
- **Document Service**: Quản lý tài liệu, lưu trữ và truy xuất
- **OCR Service**: Nhận dạng ký tự quang học, chuyển đổi hình ảnh thành văn bản
- **AI Engine Service**: Xử lý trung tâm trí tuệ nhân tạo
- **RAG Service**: Retrieval Augmented Generation - Tạo nội dung với hỗ trợ truy xuất thông tin
- **Visualization Service**: Tạo biểu đồ và trực quan hóa dữ liệu
- **Export Service**: Xuất dữ liệu sang nhiều định dạng khác nhau
- **Vector DB Service**: Quản lý cơ sở dữ liệu vector

### 4. Mô hình AI
- **OpenAI API (GPT-4)**: Mô hình ngôn ngữ lớn của OpenAI
- **Anthropic API (Claude 3)**: Mô hình ngôn ngữ lớn của Anthropic
- **Google API (Gemini Pro)**: Mô hình ngôn ngữ lớn của Google

### 5. Cơ sở dữ liệu và Lưu trữ
- **PostgreSQL**: Cơ sở dữ liệu quan hệ
- **MinIO/S3**: Lưu trữ đối tượng
- **Redis Cache**: Bộ nhớ đệm
- **Vector Database (Pinecone/Weaviate)**: Cơ sở dữ liệu lưu trữ vector nhúng

### 6. Message Broker
- **Apache Kafka**: Hệ thống xử lý dữ liệu theo luồng
- **ZooKeeper**: Điều phối và quản lý cấu hình cho Kafka

### 7. Giám sát và Ghi nhật ký
- **ELK Stack**: Elasticsearch, Logstash, Kibana cho phân tích nhật ký
- **Prometheus**: Thu thập và lưu trữ số liệu
- **Grafana**: Trực quan hóa số liệu và cảnh báo

### 8. Điều phối
- **Celery Workers**: Xử lý công việc bất đồng bộ
- **Apache Airflow**: Quản lý và lập lịch quy trình công việc

## Cách thức hoạt động

1. **Luồng yêu cầu từ người dùng**:
   - Người dùng tương tác qua Web App, Mobile App, hoặc API Client
   - Yêu cầu được gửi đến Kong API Gateway

2. **Xử lý tại API Gateway**:
   - Kong xác thực người dùng qua Authentication & Authorization
   - Rate Limiter kiểm soát số lượng yêu cầu
   - Kong định tuyến yêu cầu đến microservice thích hợp

3. **Xử lý tài liệu**:
   - Document Service nhận và lưu trữ tài liệu vào PostgreSQL và MinIO
   - Nếu cần OCR, tài liệu được gửi đến OCR Service để xử lý
   - Thông tin xử lý được gửi đến Kafka để các dịch vụ khác có thể sử dụng

4. **Xử lý AI và RAG**:
   - AI Engine Service kết nối với các mô hình OpenAI, Claude, Gemini
   - RAG Service truy xuất thông tin liên quan từ Vector Database
   - AI Engine lưu kết quả vào MinIO và lưu trữ đệm trong Redis

5. **Trực quan hóa và Xuất dữ liệu**:
   - Visualization Service tạo biểu đồ dựa trên dữ liệu từ AI Engine
   - Export Service chuyển đổi kết quả sang các định dạng khác nhau

6. **Xử lý bất đồng bộ**:
   - Các tác vụ nặng được gửi đến Celery Workers
   - Airflow lập lịch và quản lý quy trình công việc phức tạp

7. **Giám sát hệ thống**:
   - Tất cả các dịch vụ gửi nhật ký đến ELK Stack
   - Prometheus thu thập số liệu hiệu suất
   - Grafana hiển thị bảng điều khiển và cảnh báo

8. **Mở rộng dữ liệu**:
   - Kafka quản lý luồng dữ liệu giữa các dịch vụ
   - Redis cung cấp bộ đệm để cải thiện hiệu suất
   - Vector Database lưu trữ vector nhúng để tìm kiếm ngữ nghĩa

Đây là kiến trúc microservice hiện đại, có khả năng mở rộng cao, sử dụng các công nghệ AI tiên tiến để xử lý tài liệu với việc tích hợp RAG (Retrieval Augmented Generation) để cải thiện độ chính xác của các câu trả lời AI.