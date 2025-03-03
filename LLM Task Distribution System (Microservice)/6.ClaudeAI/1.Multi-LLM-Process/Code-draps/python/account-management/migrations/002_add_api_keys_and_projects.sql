-- Migration: Thêm bảng api_keys và cập nhật quy trình tạo project

-- Tạo bảng api_keys nếu chưa tồn tại
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

-- Tạo function để tự động sinh API key
CREATE OR REPLACE FUNCTION generate_unique_api_key() 
RETURNS UUID AS $$
BEGIN
    RETURN gen_random_uuid();
END;
$$ LANGUAGE plpgsql;

-- Tạo trigger để tự động tạo API key khi tạo project
CREATE OR REPLACE FUNCTION create_project_api_key()
RETURNS TRIGGER AS $$
DECLARE
    new_api_key UUID;
BEGIN
    -- Kiểm tra xem API key đã tồn tại chưa
    IF NEW.api_key IS NULL THEN
        new_api_key := generate_unique_api_key();
        
        -- Chèn API key mới
        INSERT INTO api_keys (
            key_id, 
            user_id, 
            api_key, 
            name, 
            status, 
            permissions
        ) VALUES (
            new_api_key,
            NEW.user_id,
            new_api_key::text,
            CONCAT('Project API Key for ', NEW.project_name),
            'active',
            '{"default_access": true}'::jsonb
        );
        
        -- Cập nhật project với API key mới
        NEW.api_key := new_api_key;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tạo trigger cho bảng projects
CREATE TRIGGER ensure_project_api_key
BEFORE INSERT ON projects
FOR EACH ROW
EXECUTE FUNCTION create_project_api_key();

-- Index để tối ưu truy vấn
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_api_key ON api_keys(api_key);
