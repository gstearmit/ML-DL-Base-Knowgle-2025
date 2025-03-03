IV. Tích Hợp Giữa Các Cơ Sở Dữ Liệu

Việc tích hợp giữa các cơ sở dữ liệu là quan trọng để đảm bảo tính nhất quán và hiệu suất:

### 1. Liên Kết PostgreSQL và Vector Database

```python
# Thêm một chunk mới vào cả PostgreSQL và Vector Database
async def add_document_chunk(document_id, chunk_index, content, embedding):
    # 1. Thêm vào PostgreSQL
    db_result = await db.fetchrow(
        """
        INSERT INTO document_chunks(document_id, chunk_index, content, token_count)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """,
        document_id, chunk_index, content, len(content.split())
    )
    chunk_id = db_result['id']
    
    # 2. Thêm vào Vector Database
    vector_id = f"{document_id}_chunk_{chunk_index}"
    
    # Truy vấn metadata
    metadata = await db.fetchrow(
        """
        SELECT d.document_type, d.user_id, d.created_at
        FROM documents d
        WHERE d.id = $1
        """,
        document_id
    )
    
    # Lưu vector embedding
    pinecone_index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "document_id": str(document_id),
                    "chunk_id": str(chunk_id),
                    "chunk_index": chunk_index,
                    "document_type": metadata['document_type'],
                    "user_id": str(metadata['user_id']),
                    "created_at": metadata['created_at'].isoformat()
                }
            }
        ]
    )
    
    # 3. Cập nhật reference trong PostgreSQL
    await db.execute(
        """
        UPDATE document_chunks
        SET embedding_id = $1
        WHERE id = $2
        """,
        vector_id, chunk_id
    )
    
    return chunk_id, vector_id
```

### 2. Xử Lý Sự Cố và Khôi Phục

```python
# Kiểm tra và sửa chữa dữ liệu không đồng bộ
async def verify_and_repair_embeddings():
    # 1. Tìm các chunks không có embedding_id
    missing_embedding_chunks = await db.fetch(
        """
        SELECT id, document_id, chunk_index, content
        FROM document_chunks
        WHERE embedding_id IS NULL
        """
    )
    
    for chunk in missing_embedding_chunks:
        # Tạo embedding
        embedding = await generate_embedding(chunk['content'])
        
        # Thêm vào vector database và cập nhật PostgreSQL
        await add_embedding_for_chunk(
            chunk['id'],
            chunk['document_id'],
            chunk['chunk_index'],
            embedding
        )
    
    # 2. Kiểm tra vector không có liên kết trong SQL
    # (Triển khai tùy thuộc vào cách cụ thể của vector DB)
```