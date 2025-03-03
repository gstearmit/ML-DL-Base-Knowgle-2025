import uuid
import hashlib
import secrets
from typing import Dict, Any
from database import DatabaseManager
from datetime import datetime, timedelta

class AccountService:
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password: str) -> str:
        """Hàm mã hóa mật khẩu sử dụng SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_account(self, email: str, password: str, full_name: str = None) -> uuid.UUID:
        """Đăng ký tài khoản mới"""
        password_hash = self.hash_password(password)
        user_id = self.db.create_account(email, password_hash, full_name)
        
        # Tạo quota mặc định cho tài khoản
        self.db.create_usage_quota(user_id, 'openai', 100000)  # 100k tokens mỗi tháng
        self.db.create_usage_quota(user_id, 'claude', 80000)   # 80k tokens mỗi tháng
        self.db.create_usage_quota(user_id, 'gemini', 60000)   # 60k tokens mỗi tháng
        
        return user_id
    
    def generate_api_key(self, user_id: uuid.UUID, name: str = None) -> str:
        """Tạo API key mới cho người dùng"""
        permissions = {
            "openai": {"read": True, "write": True},
            "claude": {"read": True, "write": True},
            "gemini": {"read": True, "write": True}
        }
        return self.db.create_api_key(user_id, name, permissions)
    
    def manage_credentials(self):
        """Quản lý và rotation credentials"""
        # Lấy danh sách tài khoản hoạt động
        accounts = self._get_active_accounts()
        
        for account in accounts:
            # Kiểm tra hạn mức sử dụng
            usage = self._check_account_usage(account)
            
            # Rotation credentials nếu cần
            if self._need_rotation(account):
                self._rotate_credentials(account)
            
            # Cập nhật trạng thái
            self._update_account_status(account, usage)
    
    def _get_active_accounts(self):
        """Lấy danh sách tài khoản đang hoạt động"""
        query = "SELECT user_id, email FROM accounts WHERE status = 'active'"
        return self.db.execute_query(query).fetchall()
    
    def _check_account_usage(self, account):
        """Kiểm tra mức độ sử dụng của tài khoản"""
        user_id = account[0]
        query = """
        SELECT quota_type, current_usage, monthly_limit 
        FROM usage_quotas 
        WHERE user_id = %s
        """
        return self.db.execute_query(query, (user_id,)).fetchall()
    
    def _need_rotation(self, account):
        """Kiểm tra xem có cần rotation credentials không"""
        # Logic kiểm tra rotation dựa trên thời gian và mức độ sử dụng
        return True  # Tạm thời luôn trả về True để demo
    
    def _rotate_credentials(self, account):
        """Thực hiện rotation credentials"""
        try:
            # Tạo credentials mới
            new_api_key = self.generate_api_key(account[0], f"Rotated-{datetime.now()}")
            
            # Log lịch sử rotation
            self._log_rotation_history(account, new_api_key)
            
        except Exception as e:
            print(f"Lỗi rotation credentials: {e}")
    
    def _log_rotation_history(self, account, new_api_key):
        """Ghi lại lịch sử rotation"""
        # Thêm logic ghi log rotation vào database hoặc file log
        print(f"Rotated credentials for account: {account[1]}")
    
    def _update_account_status(self, account, usage):
        """Cập nhật trạng thái tài khoản dựa trên mức sử dụng"""
        for quota in usage:
            if quota[1] > quota[2]:  # current_usage > monthly_limit
                # Cập nhật trạng thái tài khoản nếu vượt quá giới hạn
                update_query = "UPDATE accounts SET status = 'suspended' WHERE user_id = %s"
                self.db.execute_query(update_query, (account[0],))
                break
