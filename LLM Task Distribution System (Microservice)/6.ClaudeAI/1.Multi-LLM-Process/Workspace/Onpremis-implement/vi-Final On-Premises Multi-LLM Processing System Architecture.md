```mermaid
graph TB
    subgraph "1. Tầng Người Dùng"
        WC[Web Client\nVue/React/Angular]
        MC[Mobile Client\niOS/Android]
        NGX[Nginx CDN Cluster]
        FW[Cisco/Palo Alto\nFirewall Cluster]
    end

    subgraph "2. Tầng Bảo Mật"
        WAF[ModSecurity WAF\nNginx Module]
        API[Kong API Gateway\nEnterprise]
        AUTH[Keycloak\nIdentity & Access]
        TS[MinIO\nToken Storage]
    end

    subgraph "3. Tầng Xử Lý Dữ Liệu"
        IV[Input Validator\nJSON Schema]
        DS[Data Sanitizer\nCustom Rules]
        SV[Schema Validator\nOpenAPI]
        DT[Data Transformer\nApache NiFi]
    end

    subgraph "4. Tầng Điều Phối Tác Vụ"
        TM[K8s Task Manager]
        LO[LLM Orchestrator\nCustom Service]
        TA[Task Analyzer\nML Model]
        TD[(PostgreSQL 15\nTask DB)]
        TC[(Redis 7\nTask Cache)]
    end

    subgraph "5. Tầng Quản Lý Queue"
        KF[Kafka 3.5\nCluster]
        PQ[RabbitMQ\nPriority Queue]
        SQ[RabbitMQ\nStandard Queue]
        BQ[RabbitMQ\nBatch Queue]
        DQ[RabbitMQ\nDead Letter Queue]
    end

    subgraph "6. Tầng Quản Lý Tài Nguyên"
        AS[Account Service\nSpring Boot]
        RL[HAProxy\nRate Limiter]
        LB[HAProxy\nLoad Balancer]
        AD[(PostgreSQL 15\nAccount DB)]
        AC[(Redis 7\nAccount Cache)]
    end

    subgraph "7. Tầng Xử Lý LLM"
        KS[K8s HPA\nAuto Scaling]
        OE[OpenAI Engine\nGPT-4]
        CE[Claude Engine\nAnthropic]
        GE[Gemini Engine\nGoogle]
        DE[DeepSeek Engine]
        QE[Qwen Engine\nAlibaba]
        RC[Result Collector\nCustom Service]
        RCH[(Redis 7\nResult Cache)]
    end

    subgraph "8. Tầng Xử Lý Kết Quả"
        RM[Result Merger\nCustom Service]
        RA[Result Analyzer\nML Model]
        FP[Final Processor\nApache Camel]
        RD[(PostgreSQL 15\nResult DB)]
    end

    subgraph "9. Tầng Giám Sát"
        MA[Prometheus\nMetrics Alert]
        LA[ELK Stack 8.x\nLog Analysis]
        DT[Jaeger\nDistributed Tracing]
        RT[Apache Flink\nStream Processing]
        SM[Grafana\nDashboards]
    end

    subgraph "10. Tầng Độ Tin Cậy"
        BS[MinIO\nBackup Storage]
        REM[Recovery Manager\nCustom Service]
        HC[Health Checker\nSpring Actuator]
        HA[High Availability\nKeepalived]
    end

    %% Data Flow Connections
    WC & MC --> NGX --> FW
    FW --> WAF --> API
    API --> AUTH
    AUTH <--> TS

    API --> IV --> DS --> SV --> DT
    DT --> TM --> LO --> TA
    TM <--> TD & TC

    TA --> KF --> PQ & SQ & BQ
    KF --> DQ

    AS --> RL --> LB
    AS <--> AD & AC

    LB --> KS --> OE & CE & GE & DE & QE --> RC
    RC <--> RCH

    RC --> RM --> RA --> FP
    FP <--> RD

    %% Monitoring Connections
    MA & LA & DT --> RT --> SM

    %% Backup and Recovery
    TD & AD & RD --> BS
    REM --> BS
    HC --> SM
    
    %% High Availability
    HA --> FW & LB & KF

```
I'll create an updated version of the diagram focusing purely on on-premises infrastructure, with clearer organization and detailed component relationships.



Các thay đổi chính trong phiên bản final này bao gồm:

1. Chi Tiết Hóa Công Nghệ:
   - Chỉ rõ phiên bản cụ thể: Redis 7, PostgreSQL 15, ELK Stack 8.x
   - Thêm framework/platform cụ thể: Spring Boot, Apache Camel, Apache NiFi

2. Tăng Cường High Availability:
   - Thêm Keepalived cho quản lý HA
   - Cluster hóa các thành phần quan trọng như Nginx, Firewall
   - Redundancy cho các service chính

3. Tối Ưu Luồng Xử Lý:
   - Tích hợp Apache NiFi cho data transformation
   - Sử dụng Apache Camel cho final processing
   - Tận dụng ML models cho task và result analysis

4. Cải Thiện Monitoring:
   - Tích hợp Spring Actuator cho health checking
   - Sử dụng Prometheus kết hợp Grafana
   - Jaeger cho distributed tracing

5. Bảo Mật Nâng Cao:
   - ModSecurity tích hợp như Nginx module
   - Keycloak cho identity management
   - Enterprise version của Kong API Gateway

Bạn cần thêm thông tin chi tiết về phần nào của kiến trúc không?