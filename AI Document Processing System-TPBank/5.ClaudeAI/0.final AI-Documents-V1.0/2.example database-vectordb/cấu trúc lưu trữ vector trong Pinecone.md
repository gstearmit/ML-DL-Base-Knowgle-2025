1. Cấu Trúc Vector và Metadata Chi Tiết

Chi tiết về cấu trúc lưu trữ vector trong Pinecone:

```
{
  "id": "doc123_chunk_7",  // Vector ID (document_id + chunk_index)
  "values": [0.1, 0.2, ..., 0.5],  // Embedding vector (1536 dimensions)
  "metadata": {
    // Document metadata
    "document_id": "doc123",
    "document_name": "System Architecture.pdf",
    "document_type": "architecture",
    "user_id": "user456",
    
    // Chunk metadata
    "chunk_id": "chunk789",
    "chunk_index": 7,
    "token_count": 512,
    "page_number": 12,
    "section": "Database Design",
    
    // Content metadata (helps with filtering)
    "contains_diagram": true,
    "contains_code": false,
    "programming_languages": ["SQL"],
    "entities": ["PostgreSQL", "Vector Database", "MinIO"],
    "created_at": "2024-03-01T14:32:10Z",
    "language": "en"
  }
}
```