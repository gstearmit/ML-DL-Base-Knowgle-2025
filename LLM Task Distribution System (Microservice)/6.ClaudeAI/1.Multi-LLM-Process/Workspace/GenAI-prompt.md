### Hãy triển khai lần lượt 10 layer này trên môi trường kubenet , docker ,... qua file docker-compose.yml

### Let's deploy these 10 layers one by one on kubenet, docker,... via docker-compose.yml file.

### @enterprise_architecture_en.py Let's deploy these 10 layers one by one on kubenet, docker,... via docker-compose.yml file in to forder @Workspace to implement code.

### --------- Gen Prompt Project -------------
Hãy Làm các bước sau để triển khai hệ thống:
0. Tôi muốn triển khai hệ thống trên môi trường kubenet, docker,... qua file docker-compose.yml. Toàn bộ các service được triển khai trên các node khác nhau theo kiến trúc microservice. 
Toàn bộ code được triển khai bên trong thư muc enterprise-llm-system.
1. Tham chiếu thiết kế kiến trúc @Onpremis-implement/On-Premises Multi-LLM Processing System Architecture.md để triển khai code.
2.Viết code triển khai 7 flow cụ thể cho tôi . để tôi sử dụng được qua postman API tham chiếu @1.đánh số từ 1-15 cho các luồng xử lý quan trọng.md để triển khai code.
3.về database tham chiếu @v2.Database Schema Design.md để triển khai code.
4.Triển khai code theo kiến trúc sequence diagram đã phân tích @0.1.sequence diagram thể hiện 7 flow chính của hệ thống.md
5. Mỗi modules được triển khai độc lập , mỗi phần làm 1 nhiệm vụ riêng . Có ELK Stack , Jaeger , Grafana , MinIO , Keepalived , Kafka , Flink , Spring Boot , Docker , Kubernetes , Docker Compose , Postman , ... để monitor hệ thống , Tracing lỗi và logic của hệ thống để đảm bảo hệ thống hoạt đông thông suốt , không bị lỗi.
6.


### --------------
Khởi động lại hệ thống:

````bash
# Build các services
cd services/task-manager
./mvnw clean package
cd ../auth-service
./mvnw clean package
cd ../..

# Khởi động lại toàn bộ hệ thống
docker-compose down -v
docker-compose up -d

# Đợi services khởi động
sleep 30

# Khởi tạo Keycloak
./scripts/init-keycloak.sh
````