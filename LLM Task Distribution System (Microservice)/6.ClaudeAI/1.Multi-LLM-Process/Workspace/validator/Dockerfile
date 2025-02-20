FROM openjdk:17-slim

WORKDIR /app

# Cài đặt các công cụ cần thiết
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy các file cần thiết
COPY validator.jar .
COPY application.properties .

# Kiểm tra sự tồn tại của file JAR
RUN test -f validator.jar || echo "validator.jar not found!"

# Cấp quyền thực thi
RUN chmod +x validator.jar

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Command để chạy ứng dụng
CMD ["sh", "-c", "echo 'Waiting for dependencies...' && sleep 10 && java -jar validator.jar"] 