## I. PostgreSQL - Cơ Sở Dữ Liệu Quan Hệ

PostgreSQL được sử dụng để lưu trữ dữ liệu có cấu trúc, metadata, thông tin người dùng và trạng thái hệ thống.

### 1. Schema Chính

#### Bảng `users`
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB
);
```

#### Bảng `documents`
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    document_type VARCHAR(100),
    mime_type VARCHAR(100) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size BIGINT,
    status VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    summary TEXT,
    metadata JSONB,
    tags TEXT[],
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Indexes để tối ưu truy vấn
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_documents_document_type ON documents(document_type);
```

#### Bảng `document_chunks`
```sql
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER,
    embedding_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_document_chunks_document_id ON document_chunks(document_id);
```

#### Bảng `visualizations`
```sql
CREATE TABLE visualizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    visualization_type VARCHAR(100) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    parameters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_visualizations_document_id ON visualizations(document_id);
CREATE INDEX idx_visualizations_user_id ON visualizations(user_id);
```

#### Bảng `queries`
```sql
CREATE TABLE queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    response_text TEXT,
    document_ids UUID[] NOT NULL,
    embedding_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_queries_user_id ON queries(user_id);
CREATE INDEX idx_queries_created_at ON queries(created_at);
```

### 2. Transactions và Consistency

Để đảm bảo tính nhất quán của dữ liệu, DocumentAI sử dụng các transactions khi cần cập nhật nhiều bảng liên quan:

```python
async def update_document_status(document_id, status, summary=None, metadata=None):
    async with db.transaction():
        # Cập nhật document
        await db.execute(
            """
            UPDATE documents 
            SET status = $1, 
                summary = COALESCE($2, summary), 
                metadata = COALESCE($3, metadata),
                updated_at = CURRENT_TIMESTAMP,
                processed_at = CASE WHEN $1 = 'processed' THEN CURRENT_TIMESTAMP ELSE processed_at END
            WHERE id = $4
            """,
            status, summary, metadata, document_id
        )
        
        # Tạo lịch sử trạng thái
        await db.execute(
            """
            INSERT INTO document_status_history(document_id, status, metadata)
            VALUES ($1, $2, $3)
            """,
            document_id, status, metadata
        )
```
