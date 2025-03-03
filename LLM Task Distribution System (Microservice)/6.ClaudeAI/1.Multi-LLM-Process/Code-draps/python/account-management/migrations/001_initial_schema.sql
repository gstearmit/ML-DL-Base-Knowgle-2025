-- Tạo bảng resource_monitoring_logs
CREATE TABLE IF NOT EXISTS resource_monitoring_logs (
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    cpu_usage JSONB NOT NULL,
    memory_usage JSONB NOT NULL,
    network_status JSONB NOT NULL,
    llm_services_status JSONB NOT NULL
);

-- Tạo bảng task_logs
CREATE TABLE IF NOT EXISTS task_logs (
    task_id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    worker VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    estimated_tokens INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (account_id) REFERENCES accounts(user_id)
);

-- Tạo index để tăng tốc truy vấn
CREATE INDEX IF NOT EXISTS idx_task_logs_account_id ON task_logs(account_id);
CREATE INDEX IF NOT EXISTS idx_task_logs_worker ON task_logs(worker);
CREATE INDEX IF NOT EXISTS idx_task_logs_status ON task_logs(status);
CREATE INDEX IF NOT EXISTS idx_resource_monitoring_timestamp ON resource_monitoring_logs(timestamp);

-- Tạo bảng lưu trữ lịch sử rotation credentials
CREATE TABLE IF NOT EXISTS credential_rotation_history (
    rotation_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    old_api_key VARCHAR(255),
    new_api_key VARCHAR(255) NOT NULL,
    rotation_reason VARCHAR(100),
    rotated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

-- Tạo bảng lưu trữ cảnh báo hệ thống
CREATE TABLE IF NOT EXISTS system_alerts (
    alert_id UUID PRIMARY KEY,
    component VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    health_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'open'
);

-- Tạo index cho bảng alerts
CREATE INDEX IF NOT EXISTS idx_system_alerts_component ON system_alerts(component);
CREATE INDEX IF NOT EXISTS idx_system_alerts_severity ON system_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_system_alerts_status ON system_alerts(status);
