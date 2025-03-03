import psutil
import time
import json
import socket
import uuid
from typing import Dict, Any
from database import DatabaseManager

class ResourceMonitor:
    def __init__(self):
        self.db = DatabaseManager()
        self.metrics_history = []
        self.llm_services = ["openai", "claude", "gemini"]
    
    def monitor_resources(self) -> Dict[str, Any]:
        """Thu thập metrics hệ thống"""
        metrics = {
            "timestamp": time.time(),
            "cpu": self._get_cpu_metrics(),
            "memory": self._get_memory_metrics(),
            "network": self._get_network_metrics(),
            "llm_services": self._get_llm_metrics()
        }
        
        # Lưu lịch sử metrics
        self.metrics_history.append(metrics)
        
        # Giữ lại 100 điểm metrics gần nhất
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)
        
        # Tính toán health score
        health_scores = self._calculate_health_scores(metrics)
        
        # Cập nhật trạng thái tài nguyên
        self._update_resource_status(metrics, health_scores)
        
        return metrics
    
    def _get_cpu_metrics(self) -> Dict[str, float]:
        """Lấy metrics về CPU"""
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
            "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
    
    def _get_memory_metrics(self) -> Dict[str, float]:
        """Lấy metrics về bộ nhớ"""
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }
    
    def _get_network_metrics(self) -> Dict[str, Any]:
        """Lấy metrics về mạng"""
        try:
            # Lấy địa chỉ IP của máy
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            
            # Thống kê network I/O
            net_io = psutil.net_io_counters()
            
            return {
                "hostname": hostname,
                "ip_address": ip_address,
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_llm_metrics(self) -> Dict[str, Any]:
        """Lấy metrics về các dịch vụ LLM"""
        llm_metrics = {}
        
        for service in self.llm_services:
            # Lấy tổng số lượng request và tokens sử dụng
            query = """
            SELECT 
                COUNT(*) as total_requests, 
                SUM(current_usage) as total_tokens 
            FROM usage_quotas 
            WHERE quota_type = %s
            """
            result = self.db.execute_query(query, (service,)).fetchone()
            
            llm_metrics[service] = {
                "total_requests": result[0] if result else 0,
                "total_tokens": result[1] if result else 0
            }
        
        return llm_metrics
    
    def _calculate_health_scores(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Tính toán health score cho từng thành phần"""
        health_scores = {
            "cpu": max(0, 100 - metrics["cpu"]["usage_percent"]),
            "memory": max(0, 100 - metrics["memory"]["percent"]),
            "network": 100 if metrics["network"].get("ip_address") else 0
        }
        
        # Tính health score cho LLM services
        for service, service_metrics in metrics["llm_services"].items():
            # Giả sử health score dựa trên mức độ sử dụng tokens
            health_scores[f"llm_{service}"] = max(0, 100 - (service_metrics["total_tokens"] / 1000000 * 100))
        
        return health_scores
    
    def _update_resource_status(self, metrics: Dict[str, Any], health_scores: Dict[str, float]):
        """Cập nhật trạng thái tài nguyên"""
        # Lưu metrics vào database hoặc file log
        try:
            log_query = """
            INSERT INTO resource_monitoring_logs 
            (timestamp, cpu_usage, memory_usage, network_status, llm_services_status) 
            VALUES (%s, %s, %s, %s, %s)
            """
            self.db.execute_query(log_query, (
                metrics["timestamp"],
                json.dumps(metrics["cpu"]),
                json.dumps(metrics["memory"]),
                json.dumps(metrics["network"]),
                json.dumps(metrics["llm_services"])
            ))
        except Exception as e:
            print(f"Lỗi khi lưu resource monitoring logs: {e}")
        
        # Kiểm tra và cảnh báo nếu health score thấp
        for component, score in health_scores.items():
            if score < 20:  # Ngưỡng cảnh báo
                self._send_alert(component, score)
    
    def _send_alert(self, component: str, health_score: float):
        """Gửi cảnh báo khi health score thấp"""
        # Trong một hệ thống thực tế, bạn có thể:
        # 1. Gửi email
        # 2. Gửi thông báo qua Slack/Telegram
        # 3. Tạo ticket trong hệ thống quản lý sự cố
        print(f"CẢNH BÁO: Thành phần {component} có health score thấp: {health_score}")
    
    def get_resource_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Lấy lịch sử metrics trong một khoảng thời gian"""
        # Truy vấn lịch sử metrics từ database
        query = """
        SELECT * FROM resource_monitoring_logs 
        WHERE timestamp >= NOW() - INTERVAL '%s hours'
        ORDER BY timestamp DESC
        """
        results = self.db.execute_query(query, (hours,)).fetchall()
        
        return [
            {
                "timestamp": result[0],
                "cpu": json.loads(result[1]),
                "memory": json.loads(result[2]),
                "network": json.loads(result[3]),
                "llm_services": json.loads(result[4])
            } for result in results
        ]
