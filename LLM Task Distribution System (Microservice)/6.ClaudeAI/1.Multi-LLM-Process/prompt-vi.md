### Tôi muốn bạn hỗ trợ tôi phần tích,  làm một plan (Hãy bổ sung và làm rõ thêm các ý nếu còn thiếu cho ý tưởng sau ) về 1 hệ thống như mô tả sau:
Hệ thống gần giống https://openrouter.ai/ 
idea:
Có n tài khoản gmail được tạo trước và tương ứng với nó có n tài khoản đã được đăng kí trước với các LLM sau :
   + Có n tài khoản OpenAI
   + có n tài khoản Genmini
   + Có n tài khoản Claude
   + Có n tài khoản DeepSeek
   + Có n tài khoản Qwen-2.5
   
để xử lý dự án lớn với n task cụ thể , đối với mỗi một yêu cầu cụ thể hãy :
  - Dùng 1 Mô hình ngôn ngữ lớn như DeepSeek R1 làm LLM chính có nhiệm vụ điều phối , chia task , làm rõ task nếu task chưa rõ.
  - Sau khi có danh sách Task hãy đẩy lần lượt các task qua Kafka lần lượt tới các Mô hình ngôn ngữ lơn sau :  để thực hiện đa tiến trình các task , 
    sau đó Merge kết quả n tiến trình trên để cho LLM DeepSeek R1 đánh giá task hoàn thành
  - Tôi muốn chạy song song , đa tiến trình , tự động cân bằng các lần gọi các task với giới hạn limit của mối mô hình ngôn ngữ lớn . 
  - sử dụng với n tài khoản gmail để gọi API LLM như OpenAI , Claude , Genmini ,.... 
  
Kết quả mong muốn :
  - Hãy dùng lib pip diagram python  trả về cho tôi 1 bản vẽ   Thiết kế Kiến trúc hệ thống (Microservice Architecture)
  - Dùng StartUML hãy vẽ biểu đồ Tuần tư từng luồng / flow mà bạn đã phân tích được.

  ## Res
  