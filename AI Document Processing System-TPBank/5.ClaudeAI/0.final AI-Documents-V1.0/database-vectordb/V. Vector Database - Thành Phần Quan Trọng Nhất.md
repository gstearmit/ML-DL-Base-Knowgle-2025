V. Vector Database - Thành Phần Quan Trọng Nhất

Vector Database là thành phần quan trọng nhất trong kiến trúc cơ sở dữ liệu của DocumentAI, vì nó cho phép tìm kiếm ngữ nghĩa và RAG, làm nền tảng cho khả năng hiểu và truy xuất thông tin thông minh từ tài liệu.

### 1. Cấu Trúc Vector và Metadata Chi Tiết

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

### 2. Ví Dụ Tìm Kiếm Nâng Cao

```python
async def semantic_search(query, filters=None, top_k=5):
    # Tạo embedding cho câu query
    query_embedding = await generate_embedding(query)
    
    # Xây dựng filter
    filter_dict = {}
    
    if filters:
        if 'document_types' in filters:
            filter_dict["document_type"] = {"$in": filters['document_types']}
        
        if 'user_id' in filters:
            filter_dict["user_id"] = filters['user_id']
            
        if 'date_range' in filters:
            filter_dict["created_at"] = {
                "$gte": filters['date_range']['start'],
                "$lte": filters['date_range']['end']
            }
        
        if 'entities' in filters:
            filter_dict["entities"] = {"$in": filters['entities']}
    
    # Thực hiện tìm kiếm
    results = pinecone_index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_dict
    )
    
    # Xử lý kết quả
    processed_results = []
    for match in results.matches:
        # Truy vấn nội dung đầy đủ từ PostgreSQL nếu cần
        chunk_content = await db.fetchval(
            """
            SELECT content FROM document_chunks
            WHERE document_id = $1 AND chunk_index = $2
            """,
            match.metadata['document_id'],
            match.metadata['chunk_index']
        )
        
        processed_results.append({
            "id": match.id,
            "score": match.score,
            "content": chunk_content,
            "document_id": match.metadata['document_id'],
            "document_name": match.metadata.get('document_name', 'Unknown'),
            "chunk_index": match.metadata['chunk_index'],
            "section": match.metadata.get('section', 'Unknown')
        })
    
    return processed_results
```

### 3. Quản Lý Hybrid Search

Kết hợp vector search với keyword search để cải thiện kết quả:

```python
async def hybrid_search(query, filters=None, top_k=5):
    # 1. Semantic search với vector
    vector_results = await semantic_search(query, filters, top_k=top_k*2)
    
    # 2. Keyword search trong PostgreSQL
    keywords = extract_keywords(query)
    if keywords:
        keyword_query = ' & '.join(keywords)
        
        # Tạo full-text search query
        keyword_results = await db.fetch(
            """
            SELECT 
                dc.document_id,
                dc.chunk_index,
                dc.content,
                d.filename as document_name,
                ts_rank_cd(to_tsvector('english', dc.content), to_tsquery('english', $1)) as rank
            FROM 
                document_chunks dc
            JOIN 
                documents d ON dc.document_id = d.id
            WHERE 
                to_tsvector('english', dc.content) @@ to_tsquery('english', $1)
            ORDER BY 
                rank DESC
            LIMIT $2
            """,
            keyword_query, top_k*2
        )
        
        # Convert to similar format as vector results
        processed_keyword_results = [{
            "id": f"{row['document_id']}_chunk_{row['chunk_index']}",
            "score": row['rank'],
            "content": row['content'],
            "document_id": row['document_id'],
            "document_name": row['document_name'],
            "chunk_index": row['chunk_index'],
            "source": "keyword"
        } for row in keyword_results]
        
        # 3. Merge results (hybrid approach)
        merged_results = merge_and_rank_results(vector_results, processed_keyword_results, top_k)
        return merged_results
    
    # Nếu không có keyword hữu ích, chỉ trả về vector results
    return vector_results[:top_k]
```

### 4. Reranking và Hybrid Retrieval

```python
def merge_and_rank_results(vector_results, keyword_results, top_k):
    # Create a dictionary to store all results with scores
    all_results = {}
    
    # Process vector results (semantic similarity)
    for result in vector_results:
        id = result["id"]
        all_results[id] = {
            **result,
            "semantic_score": result["score"],
            "keyword_score": 0,
            "final_score": result["score"] * 0.7  # Weight semantic score at 70%
        }
    
    # Process keyword results
    for result in keyword_results:
        id = result["id"]
        if id in all_results:
            # If already exists from semantic search, update scores
            all_results[id]["keyword_score"] = result["score"]
            all_results[id]["final_score"] += result["score"] * 0.3  # Weight keyword score at 30%
        else:
            # New result from keyword search
            all_results[id] = {
                **result,
                "semantic_score": 0,
                "keyword_score": result["score"],
                "final_score": result["score"] * 0.3  # Only keyword score
            }
    
    # Convert dictionary to list and sort by final score
    merged_list = list(all_results.values())
    merged_list.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Return top_k results
    return merged_list[:top_k]
```