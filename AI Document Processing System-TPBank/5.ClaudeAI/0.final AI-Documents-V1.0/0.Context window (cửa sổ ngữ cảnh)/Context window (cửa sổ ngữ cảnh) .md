#### Context window (cửa sổ ngữ cảnh) 

OpenRouter: 
Context window (cửa sổ ngữ cảnh) là lượng văn bản tối đa mà mô hình LLM có thể xử lý trong một lần gọi. OpenRouter cung cấp tính năng mở rộng context window vượt quá giới hạn mặc định của nhà cung cấp gốc, cho phép xử lý đầu vào dài hơn.
mô tả:
* Mỗi mô hình LLM có giới hạn context window nhất định (ví dụ: GPT-4 có 8K hoặc 32K tokens)
* OpenRouter cung cấp công nghệ "context expansion" có thể vượt qua giới hạn này
* Họ sử dụng kỹ thuật như phân đoạn, tóm tắt thông minh hoặc nén token để xử lý văn bản dài hơn.
Hãy làm rõ hơn về "context expansion" , kỹ thuật như phân đoạn, tóm tắt thông minh hoặc nén token để xử lý văn bản dài hơn  với vai trò teachnical AI có kịnh nghiêm hơn 10 năm làm AI , LLM theo cách dễ hiểu , có ví dụ minh họa , ảnh , mô hình,.. để minh chứng , giải thích clear hơn

### ----------
# Context Expansion: Kỹ thuật mở rộng cửa sổ ngữ cảnh trong LLM

Với tư cách là một chuyên gia AI có kinh nghiệm lâu năm, tôi sẽ giải thích sâu hơn về các kỹ thuật "context expansion" mà OpenRouter và các nền tảng tương tự sử dụng để vượt qua giới hạn context window.

## Vấn đề cơ bản của context window

Mỗi mô hình LLM có một giới hạn vật lý về số lượng tokens có thể xử lý đồng thời. Giới hạn này tồn tại vì:

1. **Giới hạn kiến trúc**: Attention mechanism trong Transformer có độ phức tạp O(n²) với n là độ dài ngữ cảnh
2. **Giới hạn bộ nhớ**: Mỗi token yêu cầu lưu trữ trạng thái ẩn (hidden states)
3. **Giới hạn huấn luyện**: Mô hình chỉ được huấn luyện với độ dài context cụ thể

## Các kỹ thuật Context Expansion

### 1. Phân đoạn thông minh (Chunking)

**Cách hoạt động:**
- Chia văn bản đầu vào thành các đoạn nhỏ hơn (chunks) có kích thước phù hợp với context window
- Xử lý từng chunk riêng biệt
- Kết hợp kết quả một cách thông minh

**Ví dụ minh họa:**

```
Văn bản 100K tokens
  ↓
[Chunk 1: 0-32K] → LLM → Kết quả 1
[Chunk 2: 32K-64K] → LLM → Kết quả 2 
[Chunk 3: 64K-96K] → LLM → Kết quả 3
[Chunk 4: 96K-100K] → LLM → Kết quả 4
  ↓
Thuật toán kết hợp thông minh
  ↓
Kết quả tổng hợp
```

![Minh họa Chunking](./Phân%20đoạn%20thông%20minh%20(Chunking).png)

### 2. Phân tầng và tóm tắt (Hierarchical Processing)

**Cách hoạt động:**
- Tóm tắt từng phần của tài liệu thành phiên bản ngắn gọn
- Tạo "bản đồ" tài liệu với cấu trúc phân cấp
- Khi cần thông tin chi tiết, truy xuất lại phần cụ thể đó

**Ví dụ minh họa:**

```
Văn bản dài → [Tóm tắt chung] + [Các tóm tắt chi tiết mỗi phần]

Khi cần trả lời:
1. Đầu tiên sử dụng tóm tắt chung để định hướng
2. Xác định phần cụ thể cần thông tin chi tiết 
3. Truy xuất và xử lý phần đó
```

![Minh họa Hierarchical Processing](./2.%20Phân%20tầng%20và%20tóm%20tắt%20(Hierarchical%20Processing).png

### 3. Nén token và embedding (Compression)

**Cách hoạt động:**
- Sử dụng thuật toán nén để giảm số lượng tokens cần thiết
- Áp dụng kỹ thuật trích xuất thông tin quan trọng
- Sử dụng embedding để biểu diễn thông tin dưới dạng vector đặc trưng 

**Phương pháp nén:**
- **Syntactic compression**: Loại bỏ từ không cần thiết, rút gọn cú pháp
- **Semantic compression**: Giữ lại ý nghĩa nhưng viết lại ngắn gọn hơn
- **Token-level compression**: Tối ưu hóa cách tokenize văn bản

![Minh họa Token Compression](./2.%20Phân%20tầng%20và%20tóm%20tắt%20(Hierarchical%20Processing).png)

### 4. Retrieval Augmented Generation (RAG)

**Cách hoạt động:**
- Lưu trữ toàn bộ văn bản dưới dạng vector trong cơ sở dữ liệu vector
- Khi nhận câu hỏi, truy xuất chỉ những phần liên quan nhất
- Chỉ đưa vào context window những phần thực sự cần thiết

**Ví dụ minh họa:**

```
1. Chia tài liệu 100K tokens thành 100 đoạn
2. Tính vector embedding cho mỗi đoạn và lưu vào vector DB
3. Khi có câu hỏi, tìm 5-10 đoạn liên quan nhất
4. Chỉ đưa những đoạn này vào LLM để xử lý
```

![Minh họa RAG](https://i.postimg.cc/85v18vfd/rag-diagram.png)

### 5. Cơ chế Attention hiệu quả

**Cách hoạt động:**
- Sử dụng các biến thể của cơ chế attention giảm độ phức tạp từ O(n²) xuống O(n log n) hoặc O(n)
- Áp dụng các kỹ thuật như Sparse Attention, Flash Attention, hoặc Linear Attention
- Cho phép xử lý nhiều tokens hơn với cùng tài nguyên tính toán

**Ví dụ về các kỹ thuật:**
- **Local Attention**: Chỉ quan tâm đến tokens gần nhau
- **Sparse Attention**: Chú ý có chọn lọc đến các tokens quan trọng
- **Sliding Window**: Di chuyển cửa sổ attention qua văn bản dài

![Minh họa Efficient Attention](https://i.postimg.cc/MTgRQb2h/efficient-attention.png)

## Ví dụ cụ thể về Context Expansion trên OpenRouter

Giả sử bạn cần phân tích một tài liệu pháp lý 150K tokens với GPT-4 (giới hạn 32K):

```python
# Phương pháp thông thường - SẼ BỊ LỖI
response = openai.chat.completions.create(
    model="openai/gpt-4",
    messages=[
        {"role": "user", "content": "Phân tích tài liệu pháp lý: " + legal_document_150k_tokens}
    ]
)

# Phương pháp với OpenRouter Context Expansion
response = openai.chat.completions.create(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-...",
    model="openai/gpt-4-turbo",
    messages=[
        {"role": "user", "content": "Phân tích tài liệu pháp lý: " + legal_document_150k_tokens}
    ],
    context_window_expanded=True,
    additional_params={
        "expansion_strategy": "chunking_with_overlap",  # Chiến lược mở rộng
        "chunk_size": 24000,  # Kích thước mỗi chunk
        "chunk_overlap": 4000  # Phần chồng lấp giữa các chunks
    }
)
```

## Ưu và nhược điểm của Context Expansion

**Ưu điểm:**
- Xử lý được tài liệu dài vượt xa giới hạn mô hình
- Giữ được context toàn cầu trong cả tài liệu lớn
- Tiết kiệm chi phí so với việc nâng cấp lên mô hình có context window lớn hơn

**Nhược điểm:**
- Độ chính xác có thể giảm ở một số trường hợp phức tạp
- Thời gian xử lý thường lâu hơn
- Có thể gặp vấn đề với tài liệu cần liên kết thông tin từ nhiều phần xa nhau

## Tương lai của Context Expansion

Các nghiên cứu mới nhất đang tập trung vào:
- Mô hình có khả năng xử lý hàng triệu tokens (như Claude 3 Opus với 200K tokens)
- Kiến trúc "recurrent" cho phép nhớ lâu dài mà không bị giới hạn bởi kích thước cửa sổ cố định
- Kỹ thuật "reasoning recycling" - tái sử dụng suy luận từ các đoạn trước

Context expansion là một lĩnh vực đang phát triển nhanh chóng, và các kỹ thuật được áp dụng ngày càng tinh vi hơn để cung cấp trải nghiệm mượt mà cho người dùng, giúp họ làm việc với các tài liệu dài mà không cần quan tâm đến giới hạn kỹ thuật của mô hình.