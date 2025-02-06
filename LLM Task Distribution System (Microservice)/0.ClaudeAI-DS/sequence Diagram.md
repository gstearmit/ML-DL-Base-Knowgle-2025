@startuml

actor "Người dùng" as User
participant "API Gateway" as APIGW
participant "Task Manager Service" as TMS
participant "DeepSeek R1" as DSR1
participant "Kafka" as Kafka
participant "Worker Service" as WS
participant "LLM API" as LLM
participant "Result Aggregator Service" as RAS

User -> APIGW: Gửi yêu cầu
APIGW -> TMS: Chuyển yêu cầu
TMS -> DSR1: Gửi yêu cầu để chia nhỏ task
DSR1 -> TMS: Trả về danh sách task con
TMS -> Kafka: Đẩy task vào Kafka
Kafka -> WS: Phân phối task
WS -> LLM: Gọi API tương ứng
LLM -> WS: Trả kết quả
WS -> Kafka: Đẩy kết quả vào Kafka
Kafka -> RAS: Nhận kết quả
RAS -> DSR1: Gửi kết quả để đánh giá
DSR1 -> RAS: Trả kết quả cuối cùng
RAS -> APIGW: Trả kết quả
APIGW -> User: Trả kết quả cuối cùng

@enduml
