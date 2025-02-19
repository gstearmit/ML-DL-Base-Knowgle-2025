# Schema Database cho Hệ thống Multi-LLM

## 1. Project Database

### projects
```sql
CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    api_key UUID NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    settings JSONB,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id),
    FOREIGN KEY (api_key) REFERENCES api_keys(key_id)
);

CREATE UNIQUE INDEX idx_projects_name_user ON projects(user_id, project_name);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_priority ON projects(priority);
```

### project_members
```sql
CREATE TABLE project_members (
    member_id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    permissions JSONB,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

CREATE UNIQUE INDEX idx_project_members_unique ON project_members(project_id, user_id);
```

### project_activity_log
```sql
CREATE TABLE project_activity_log (
    log_id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    user_id UUID NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

CREATE INDEX idx_project_activity_project_id ON project_activity_log(project_id);
```

## 2. Task Database

### tasks
```sql
CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    user_id UUID NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 1,
    status VARCHAR(50) NOT NULL CHECK (
        status IN (
            'pending',        -- Chờ xử lý
            'in_queue',      -- Đang trong hàng đợi
            'processing',    -- Đang xử lý
            'completed',     -- Hoàn thành
            'failed',        -- Thất bại
            'cancelled',     -- Đã hủy
            'paused',        -- Tạm dừng
            'retrying'       -- Đang thử lại
        )
    ),
    input_data JSONB NOT NULL,
    output_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    deadline TIMESTAMP WITH TIME ZONE,
    assigned_worker_id UUID,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    parent_task_id UUID,
    execution_order INTEGER,
    metadata JSONB,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id)
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### task_history
```sql
CREATE TABLE task_history (
    history_id UUID PRIMARY KEY,
    task_id UUID NOT NULL,
    status_from VARCHAR(20),
    status_to VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by UUID,
    reason TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

CREATE INDEX idx_task_history_task_id ON task_history(task_id);
```

## 2. Account Database

### accounts
```sql
CREATE TABLE accounts (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    account_type VARCHAR(20) DEFAULT 'standard',
    verification_status BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_accounts_email ON accounts(email);
```

### api_keys
```sql
CREATE TABLE api_keys (
    key_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    permissions JSONB,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_api_key ON api_keys(api_key);
```

### usage_quotas
```sql
CREATE TABLE usage_quotas (
    quota_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    quota_type VARCHAR(50) NOT NULL,
    monthly_limit INTEGER NOT NULL,
    current_usage INTEGER DEFAULT 0,
    reset_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

CREATE INDEX idx_usage_quotas_user_id ON usage_quotas(user_id);
```

## 3. Result Database

### results
```sql
CREATE TABLE results (
    result_id UUID PRIMARY KEY,
    task_id UUID NOT NULL,
    engine_type VARCHAR(50) NOT NULL,
    output_data JSONB NOT NULL,
    confidence_score FLOAT,
    processing_time INTEGER,
    token_usage JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

CREATE INDEX idx_results_task_id ON results(task_id);
CREATE INDEX idx_results_engine_type ON results(engine_type);
```

### result_feedback
```sql
CREATE TABLE result_feedback (
    feedback_id UUID PRIMARY KEY,
    result_id UUID NOT NULL,
    user_id UUID NOT NULL,
    rating INTEGER,
    feedback_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (result_id) REFERENCES results(result_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id)
);

CREATE INDEX idx_result_feedback_result_id ON result_feedback(result_id);
```

## 4. Backup Store

### backup_metadata
```sql
CREATE TABLE backup_metadata (
    backup_id UUID PRIMARY KEY,
    backup_type VARCHAR(50) NOT NULL,
    source_database VARCHAR(50) NOT NULL,
    backup_path VARCHAR(255) NOT NULL,
    size_bytes BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    checksum VARCHAR(255),
    retention_period INTEGER
);

CREATE INDEX idx_backup_metadata_type ON backup_metadata(backup_type);
CREATE INDEX idx_backup_metadata_created_at ON backup_metadata(created_at);
```

### backup_history
```sql
CREATE TABLE backup_history (
    history_id UUID PRIMARY KEY,
    backup_id UUID NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20),
    error_message TEXT,
    performed_by UUID,
    FOREIGN KEY (backup_id) REFERENCES backup_metadata(backup_id)
);

CREATE INDEX idx_backup_history_backup_id ON backup_history(backup_id);
```

Các điểm chính trong thiết kế schema:

1. Sử dụng UUID làm khóa chính để đảm bảo tính duy nhất trên toàn hệ thống phân tán
2. Tích hợp timestamp với timezone để hỗ trợ người dùng toàn cầu
3. Sử dụng JSONB cho dữ liệu có cấu trúc động
4. Thiết lập các foreign key để đảm bảo tính toàn vẹn dữ liệu
5. Tạo các index phù hợp để tối ưu hiệu suất truy vấn
6. Theo dõi lịch sử thay đổi cho các bảng quan trọng
7. Hỗ trợ đa dạng loại tác vụ và engine LLM
8. Tích hợp hệ thống phân quyền và quota
9. Lưu trữ metadata cho hệ thống backup