-- Create accounts table first since other tables reference it
CREATE TABLE IF NOT EXISTS accounts (
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

CREATE INDEX IF NOT EXISTS idx_accounts_email ON accounts(email);

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys (
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

CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_api_key ON api_keys(api_key);

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
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

CREATE UNIQUE INDEX IF NOT EXISTS idx_projects_name_user ON projects(user_id, project_name);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_priority ON projects(priority);

-- Create project_members table
CREATE TABLE IF NOT EXISTS project_members (
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

CREATE UNIQUE INDEX IF NOT EXISTS idx_project_members_unique ON project_members(project_id, user_id);

-- Create project_activity_log table
CREATE TABLE IF NOT EXISTS project_activity_log (
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

CREATE INDEX IF NOT EXISTS idx_project_activity_project_id ON project_activity_log(project_id);

-- Create tasks table with updated schema
CREATE TABLE IF NOT EXISTS tasks (
    task_id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    user_id UUID NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 1,
    status VARCHAR(50) NOT NULL CHECK (
        status IN (
            'pending',
            'in_queue',
            'processing',
            'completed',
            'failed',
            'cancelled',
            'paused',
            'retrying'
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

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);

-- Create task_history table
CREATE TABLE IF NOT EXISTS task_history (
    history_id UUID PRIMARY KEY,
    task_id UUID NOT NULL,
    status_from VARCHAR(20),
    status_to VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by UUID,
    reason TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

CREATE INDEX IF NOT EXISTS idx_task_history_task_id ON task_history(task_id);
