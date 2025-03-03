II. Vector Database (Pinecone/Weaviate)

Vector Database lưu trữ các embeddings (biểu diễn vector) của các đoạn văn bản, cho phép tìm kiếm ngữ nghĩa và RAG (Retrieval Augmented Generation).

### 1. Cấu Trúc Lưu Trữ trong Pinecone

Trong Pinecone, dữ liệu được tổ chức trong các chỉ mục (index) và namespace:

```python
# Định nghĩa cấu trúc Index
index_definition = {
    "name": "documentai-embeddings",
    "dimension": 1536,  # OpenAI ada-002 embedding dimension
    "metric": "cosine",  # Similarity metric
    "pods": 2,
    "pod_type": "p1.x1"  # Loại pod cho hiệu suất
}

# Vector metadata
vector_metadata = {
    "document_id": "b87a56e2-3e21-4c11-8f3c-c92d4c13823a",
    "chunk_id": "b87a56e2-3e21-4c11-8f3c-c92d4c13823a_chunk_0",
    "chunk_index": 0,
    "document_type": "brd",
    "token_count": 512,
    "user_id": "7f6d9e15-8a2d-47f8-b2e7-4da3510b1ec7",
    "created_at": "2023-12-01T10:15:23Z",
    "source": "documents/b87a56e2-3e21-4c11-8f3c-c92d4c13823a.pdf"
}
```

### 2. Ví Dụ Truy Vấn Pinecone

```python
# Tìm kiếm vectors tương tự
def search_similar_vectors(query_embedding, document_ids=None, top_k=5):
    # Cấu hình filter nếu cần giới hạn theo document_ids
    filter_config = None
    if document_ids:
        filter_config = {
            "document_id": {"$in": document_ids}
        }
    
    # Thực hiện tìm kiếm
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_config
    )
    
    return results
```

### 3. Cấu Trúc Weaviate (Lựa Chọn Thay Thế)

Nếu sử dụng Weaviate, dữ liệu được tổ chức theo schema hướng đối tượng:

```python
# Định nghĩa schema
document_chunk_class = {
    "class": "DocumentChunk",
    "vectorizer": "none",  # Sử dụng embeddings được tính toán bên ngoài
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The content of the document chunk"
        },
        {
            "name": "documentId",
            "dataType": ["string"],
            "description": "ID of the parent document"
        },
        {
            "name": "chunkIndex",
            "dataType": ["int"],
            "description": "Index of the chunk within document"
        },
        {
            "name": "documentType",
            "dataType": ["string"],
            "description": "Type of document (BRD, API spec, etc)"
        },
        {
            "name": "userId",
            "dataType": ["string"],
            "description": "Owner of the document"
        },
        {
            "name": "tokenCount",
            "dataType": ["int"],
            "description": "Number of tokens in the chunk"
        }
    ]
}
```