import uuid
import time
import random
from typing import Dict, Any, List
from database import DatabaseManager
from resource_monitor import ResourceMonitor
from rate_limiter import RateLimiter

class LoadBalancer:
    def __init__(self):
        self.db = DatabaseManager()
        self.resource_monitor = ResourceMonitor()
        self.rate_limiter = RateLimiter()
        
        # Danh sách các worker/service LLM
        self.available_workers = {
            "openai": {"endpoint": "https://api.openai.com", "weight": 0.4},
            "claude": {"endpoint": "https://api.anthropic.com", "weight": 0.3},
            "gemini": {"endpoint": "https://generativelanguage.googleapis.com", "weight": 0.3}
        }
    
    def distribute_task(self, task: Dict[str, Any], account_id: uuid.UUID) -> Dict[str, Any]:
        """Phân phối task đến worker phù hợp"""
        # Lấy thông tin tài nguyên hiện tại
        current_resources = self.resource_monitor.monitor_resources()
        
        # Kiểm tra rate limit của tài khoản
        try:
            rate_limit_info = self._check_rate_limits(account_id, task)
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
        # Chọn worker phù hợp
        selected_worker = self._select_worker(current_resources, rate_limit_info)
        
        # Gán task cho worker
        result = self._assign_task(selected_worker, task)
        
        return result
    
    def _check_rate_limits(self, account_id: uuid.UUID, task: Dict[str, Any]) -> Dict[str, Any]:
        """Kiểm tra giới hạn sử dụng cho tài khoản"""
        # Xác định LLM provider từ task
        llm_provider = task.get("provider", self._suggest_provider())
        
        # Kiểm tra rate limit
        rate_limit_result = self.rate_limiter.check_limits(account_id, llm_provider)
        
        return {
            "provider": llm_provider,
            "remaining_limits": rate_limit_result["remaining_limits"]
        }
    
    def _suggest_provider(self) -> str:
        """Gợi ý nhà cung cấp LLM dựa trên trọng số"""
        providers = list(self.available_workers.keys())
        weights = [self.available_workers[p]["weight"] for p in providers]
        return random.choices(providers, weights=weights)[0]
    
    def _select_worker(self, resources: Dict[str, Any], rate_limit_info: Dict[str, Any]) -> str:
        """Chọn worker phù hợp nhất"""
        worker_scores = {}
        
        for provider, worker_info in self.available_workers.items():
            # Tính điểm dựa trên nhiều yếu tố
            score = self._calculate_worker_score(
                provider=provider,
                resources=resources,
                rate_limit_info=rate_limit_info
            )
            worker_scores[provider] = score
        
        # Chọn worker có điểm cao nhất
        selected_worker = max(worker_scores, key=worker_scores.get)
        return selected_worker
    
    def _calculate_worker_score(self, 
                                 provider: str, 
                                 resources: Dict[str, Any], 
                                 rate_limit_info: Dict[str, Any]) -> float:
        """Tính điểm cho mỗi worker"""
        # Kiểm tra health score của LLM service
        llm_health_score = resources.get(f"llm_{provider}", 0)
        
        # Kiểm tra giới hạn còn lại
        remaining_requests = rate_limit_info["remaining_limits"]["requests"]
        remaining_tokens = rate_limit_info["remaining_limits"]["tokens"]
        
        # Tính điểm kết hợp
        score = (
            llm_health_score * 0.4 +  # Trạng thái dịch vụ
            (remaining_requests / 60) * 30 +  # Giới hạn request
            (remaining_tokens / 40000) * 30   # Giới hạn tokens
        )
        
        return score
    
    def _assign_task(self, worker: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Gán task cho worker được chọn"""
        try:
            # Trong một hệ thống thực tế, bạn sẽ gọi API của worker
            # Ở đây chúng ta giả lập quá trình
            endpoint = self.available_workers[worker]["endpoint"]
            
            # Mô phỏng việc gửi task
            task_result = {
                "status": "success",
                "worker": worker,
                "endpoint": endpoint,
                "task_id": str(uuid.uuid4()),
                "estimated_tokens": task.get("estimated_tokens", 0)
            }
            
            # Cập nhật mức sử dụng
            self.rate_limiter.update_usage(
                task.get("account_id"), 
                worker, 
                task_result["estimated_tokens"]
            )
            
            return task_result
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Lỗi khi gán task: {str(e)}",
                "worker": worker
            }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Lấy trạng thái của một task"""
        # Trong hệ thống thực tế, bạn sẽ truy vấn trạng thái task từ database
        # Ở đây chúng ta giả lập
        query = """
        SELECT status, worker, created_at, completed_at 
        FROM task_logs 
        WHERE task_id = %s
        """
        try:
            result = self.db.execute_query(query, (task_id,)).fetchone()
            
            if result:
                return {
                    "task_id": task_id,
                    "status": result[0],
                    "worker": result[1],
                    "created_at": result[2],
                    "completed_at": result[3]
                }
            else:
                return {
                    "status": "not_found",
                    "message": "Không tìm thấy task"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def log_task(self, task_result: Dict[str, Any]):
        """Ghi log task"""
        try:
            log_query = """
            INSERT INTO task_logs 
            (task_id, account_id, worker, status, estimated_tokens, created_at) 
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            self.db.execute_query(log_query, (
                task_result.get("task_id"),
                task_result.get("account_id"),
                task_result.get("worker"),
                task_result.get("status", "pending"),
                task_result.get("estimated_tokens", 0)
            ))
        except Exception as e:
            print(f"Lỗi khi ghi log task: {e}")
