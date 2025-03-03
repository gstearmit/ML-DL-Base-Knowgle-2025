from typing import Dict, Any
from database import DatabaseManager
import time
import uuid

class RateLimiter:
    def __init__(self):
        self.db = DatabaseManager()
        self.limits = {
            "openai": {
                "requests_per_min": 60,
                "tokens_per_min": 40000,
                "concurrent_requests": 10
            },
            "claude": {
                "requests_per_min": 50,
                "tokens_per_min": 35000,
                "concurrent_requests": 8
            },
            "gemini": {
                "requests_per_min": 45,
                "tokens_per_min": 30000,
                "concurrent_requests": 6
            }
        }
        self.request_history = {}
    
    def check_limits(self, account_id: uuid.UUID, llm_provider: str) -> Dict[str, Any]:
        """Kiểm tra giới hạn sử dụng cho một tài khoản và nhà cung cấp LLM"""
        current_time = time.time()
        
        # Lấy thông tin quota từ database
        quota_query = """
        SELECT quota_type, current_usage, monthly_limit 
        FROM usage_quotas 
        WHERE user_id = %s AND quota_type = %s
        """
        result = self.db.execute_query(quota_query, (str(account_id), llm_provider)).fetchone()
        
        if not result:
            raise ValueError(f"Không tìm thấy quota cho account {account_id} và provider {llm_provider}")
        
        # Kiểm tra mức sử dụng hiện tại
        current_usage, monthly_limit = result[1], result[2]
        
        # Tính toán remaining limits
        remaining_limits = {
            "requests": self.limits[llm_provider]["requests_per_min"] - current_usage,
            "tokens": self.limits[llm_provider]["tokens_per_min"] - current_usage,
            "concurrent": self.limits[llm_provider]["concurrent_requests"]
        }
        
        # Kiểm tra và cập nhật lịch sử request
        if account_id not in self.request_history:
            self.request_history[account_id] = []
        
        # Loại bỏ các request cũ hơn 1 phút
        self.request_history[account_id] = [
            req for req in self.request_history[account_id] 
            if current_time - req['timestamp'] <= 60
        ]
        
        # Kiểm tra số lượng request trong 1 phút
        if len(self.request_history[account_id]) >= self.limits[llm_provider]["requests_per_min"]:
            raise Exception(f"Vượt quá giới hạn request cho {llm_provider}")
        
        # Ghi nhận request mới
        self.request_history[account_id].append({
            'timestamp': current_time,
            'provider': llm_provider
        })
        
        return {
            "status": "allowed",
            "remaining_limits": remaining_limits
        }
    
    def update_usage(self, account_id: uuid.UUID, llm_provider: str, tokens_used: int):
        """Cập nhật mức sử dụng tokens"""
        update_query = """
        UPDATE usage_quotas 
        SET current_usage = current_usage + %s 
        WHERE user_id = %s AND quota_type = %s
        """
        self.db.execute_query(update_query, (tokens_used, str(account_id), llm_provider))
    
    def reset_monthly_quotas(self):
        """Đặt lại quota hàng tháng"""
        reset_query = """
        UPDATE usage_quotas 
        SET current_usage = 0, reset_date = CURRENT_DATE 
        WHERE reset_date < CURRENT_DATE
        """
        self.db.execute_query(reset_query)
    
    def get_account_usage_summary(self, account_id: uuid.UUID) -> Dict[str, Any]:
        """Lấy tổng quan mức sử dụng của tài khoản"""
        query = """
        SELECT quota_type, current_usage, monthly_limit, reset_date
        FROM usage_quotas
        WHERE user_id = %s
        """
        results = self.db.execute_query(query, (str(account_id),)).fetchall()
        
        summary = {}
        for result in results:
            summary[result[0]] = {
                "current_usage": result[1],
                "monthly_limit": result[2],
                "reset_date": result[3],
                "usage_percentage": (result[1] / result[2]) * 100 if result[2] > 0 else 0
            }
        
        return summary
