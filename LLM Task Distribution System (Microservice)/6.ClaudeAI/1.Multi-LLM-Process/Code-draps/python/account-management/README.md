# Dịch Vụ Quản Lý Tài Khoản & Tài Nguyên

## Mô Tả

Dịch vụ quản lý tài khoản và tài nguyên cho hệ thống LLM (Large Language Model) phân tán. Cung cấp các chức năng:

- Quản lý tài khoản người dùng
- Kiểm soát rate limiting
- Giám sát tài nguyên hệ thống
- Cân bằng tải giữa các dịch vụ LLM

## Các Thành Phần Chính

1. `account_service.py`: Quản lý vòng đời tài khoản
   - Đăng ký tài khoản
   - Tạo API key
   - Quản lý và rotation credentials

2. `rate_limiter.py`: Kiểm soát giới hạn sử dụng
   - Theo dõi mức sử dụng tokens
   - Giới hạn số lượng request
   - Quản lý quota hàng tháng

3. `resource_monitor.py`: Giám sát tài nguyên hệ thống
   - Thu thập metrics CPU, memory, network
   - Theo dõi trạng thái dịch vụ LLM
   - Tính toán health score
   - Cảnh báo khi tài nguyên thấp

4. `load_balancer.py`: Cân bằng tải động
   - Phân phối task giữa các dịch vụ LLM
   - Chọn worker dựa trên tài nguyên và giới hạn
   - Theo dõi trạng thái task

## Cấu Hình Môi Trường

Sử dụng biến môi trường sau:

- `DB_HOST`: Địa chỉ máy chủ cơ sở dữ liệu
- `DB_NAME`: Tên cơ sở dữ liệu
- `DB_USER`: Tên người dùng cơ sở dữ liệu
- `DB_PASSWORD`: Mật khẩu cơ sở dữ liệu

## Cài Đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy migrations (nếu có)
python manage_db.py migrate
```

## Sử Dụng

```python
from account_service import AccountService
from rate_limiter import RateLimiter
from load_balancer import LoadBalancer

# Đăng ký tài khoản
account_service = AccountService()
user_id = account_service.register_account("user@example.com", "password123")

# Tạo API key
api_key = account_service.generate_api_key(user_id)

# Kiểm tra giới hạn sử dụng
rate_limiter = RateLimiter()
rate_limit_info = rate_limiter.check_limits(user_id, "openai")

# Phân phối task
load_balancer = LoadBalancer()
task = {
    "account_id": user_id,
    "provider": "openai",
    "estimated_tokens": 1000
}
result = load_balancer.distribute_task(task, user_id)
```

## Giám Sát & Logging

- Metrics hệ thống được lưu trong bảng `resource_monitoring_logs`
- Log task được lưu trong bảng `task_logs`

## Chiến Lược Rate Limiting

- Giới hạn request/phút cho từng nhà cung cấp LLM
- Theo dõi mức sử dụng tokens
- Tự động đình chỉ tài khoản khi vượt quá giới hạn

## Chiến Lược Cân Bằng Tải

- Chọn worker dựa trên:
  1. Trạng thái tài nguyên
  2. Giới hạn request còn lại
  3. Trọng số của từng dịch vụ

## Bảo Mật

- Mật khẩu được hash bằng SHA-256
- Rotation API key định kỳ
- Kiểm tra và giới hạn quyền truy cập

## Mở Rộng

Dịch vụ được thiết kế linh hoạt để dễ dàng mở rộng:
- Thêm nhà cung cấp LLM mới
- Điều chỉnh chiến lược rate limiting
- Tích hợp các dịch vụ giám sát bổ sung

## Ghi Chú Phát Triển

- Đảm bảo bảo mật và hiệu suất
- Thường xuyên kiểm tra và điều chỉnh ngưỡng giới hạn
- Theo dõi và phân tích log để cải thiện hệ thống
