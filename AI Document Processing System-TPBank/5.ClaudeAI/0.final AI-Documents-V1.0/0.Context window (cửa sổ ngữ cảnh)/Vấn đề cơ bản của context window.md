## Vấn đề cơ bản của context window
Mỗi mô hình LLM có một giới hạn vật lý về số lượng tokens có thể xử lý đồng thời. Giới hạn này tồn tại vì:

Giới hạn kiến trúc: Attention mechanism trong Transformer có độ phức tạp O(n²) với n là độ dài ngữ cảnh
Giới hạn bộ nhớ: Mỗi token yêu cầu lưu trữ trạng thái ẩn (hidden states)
Giới hạn huấn luyện: Mô hình chỉ được huấn luyện với độ dài context cụ thể