https://chatgpt.com/share/67a4be4c-5a9c-8001-a6e5-1cdcaeda0a19

### Issue Team Dev/BA/CR:
  Đối với 1 developer New/Senior thì với cả ngàn document tài liệu hệ thống của các modules Bank.
  Để đọc và xem hết thì cực kì vất vả --> nên viêc mantainer / Update tính năng khá mất thời gian.

# Prompt for AI Document Processing System

Tôi muốn bạn Hãy phần tích, xây dựng một plan hoàn chỉnh (Hãy bổ sung và làm rõ thêm các ý nếu còn thiếu cho ý tưởng bên dưới ) về 1 hệ thống AI như mô tả sau:
 Xây dựng Hệ thống tương tự như hệ thống https://notebooklm.google.com/
## idea: 
 input :
   + cho phép người dùng đính kèm lên các định dạng video cuộc họp , chốt tính năng, documents file : doc , docx , pdf , jpg , png , .mp4, ... : 
   trong đó toàn bộ tài liệu đính kèm đều mô tả các tài liệu BRD , BA , thiết kế kiến trúc hệ thống 
   , sơ đồ luồng , biểu đồ tuần tự , kiến trúc hệ thống database, sơ đồ thiết kế API ,...
   + Đối với các video file , documents file pdf ,... Tài liệu quá dài hãy áp dụng Context window (cửa sổ ngữ cảnh) là lượng văn bản tối đa mà mô hình LLM có thể xử lý trong một lần gọi. Để mở rộng context window vượt quá giới hạn mặc định của nhà cung cấp gốc, cho phép xử lý đầu vào dài hơn.
   Mỗi mô hình LLM có giới hạn context window nhất định (ví dụ: GPT-4 có 8K hoặc 32K tokens)
* vậy hãy áp dung "context expansion" có thể vượt qua giới hạn này. Hãy sử dụng kỹ thuật như phân đoạn, tóm tắt thông minh hoặc nén token để xử lý văn bản dài hơn.
   
 Output:
   + Tổng hợp, hỏi đáp các kiến thức liên quan đến các nguồn file input đã được đính kèm. 
   + Chuẩn hóa gợi ý lại các tài liệu theo chuẩn mới như Agile/scrum , Báo cáo tiến độ dự án dưới dạng Grant Chart, theo dõi chất lượng bug/Issue qua jira, ... để triển khai tiếp cho các phare khác của dự án.
   + Thêm tính năng gợi ý câu hỏi về tài liệu : Với mỗi tài liệu , video được upload , chunking xong thì đều có câu hỏi gợi ý , action liên quan đến nội dung file , video được tải lên nhằm mục đích làm rõ . giải thích thêm ,.... hoặc hành động liên quan đến nội dung, ....
   
    
  
## Kết quả mong muốn :
  - Hệ thống phải sử dụng các AI tiên tiến như OpenAI , Claude , Gemini để tổng hợp , phân tích , embeding , dùng vector database để lưu trữ hiểu các nghĩa của tài liệu.
  - Bổ sung làm rõ các Công Nghệ Chính được sử dụng trong dự án , một số công nghệ ví dụ như:
    Có sử dung thêm kafka để làm pub/sub
    | Layer           | Công Nghệ                  | Mục Đích                           |
    |-----------------|---------------------------|-----------------------------------|
    | Processing      | Apache NiFi, Tesseract    | Xử lý file đa định dạng           |
    | AI Core         | OpenAI GPT-4, Claude 3    | Phân tích semantic                 |
    | Vector DB       | Pinecone, Weaviate        | Lưu trữ embedding                 |
    | Orchestration   | LangChain, LlamaIndex     | Kết nối các thành phần AI         |
    | Visualization   | Diagram (Python), PlantUML| Tự động sinh diagram              |
    | Backend         | FastAPI, Celery           | Xây dựng API và xử lý bất đồng bộ |

  - Hãy làm rõ hơn về "context expansion" , kỹ thuật như phân đoạn, tóm tắt thông minh hoặc nén token để xử lý văn bản dài hơn  với vai trò với một kỹ sư AI có kinh nghiêm hơn 10 năm làm về AI và trải qua rất nhiều dự án lớn ứng dựng AI trong ngân hàng . theo cách dễ hiểu , có ví dụ minh họa , ảnh , mô hình,.. để minh chứng , giải thích clear hơn.
  - Về Technical AI Hãy Làm rõ cơ chế hoạt động và công nghệ OCR Cho documents file và file định đạng video.
  - Hãy dùng lib pip diagram python đưa cho tôi 1 bản vẽ Thiết kế Kiến trúc hệ thống final thông thể dự án theo kiến trúc Microservice Architecture.
  - Dùng mermaid vẽ sequence Diagram ,flow . Hãy vẽ top 15 biểu đồ Tuần tự từng luồng / flow quan trọng nhất.   
  - Hãy viết code dự án này từ đầu tới cuối cho tôi bằng ngôn ngữ python theo kiến trúc microservice , có tích hợp service Mesh , elk để monitor với khaí năng bài toán nâng cao nâng cao . Đặc biệt bỏ qua , không sử dụng công nghệ LangChain Orchestrator.
  


  ### --- Idea 3 : -------
Tôi muốn bạn  phần tích, xây dựng một plan hoàn chỉnh (Hãy bổ sung và làm rõ thêm các ý nếu còn thiếu cho ý tưởng bên dưới ) về 1 hệ thống AI như mô tả sau:
 Xây dựng Hệ thống tương tự như hệ thống https://notebooklm.google.com/
## idea: 
 input :
   + cho phép người dùng đính kèm lên các định dạng file : doc , docx , pdf , jpg , png , mp4, ... : 
   trong đó toàn bộ tài liệu đính kèm đều mô tả các tài liệu BRD , BA , thiết kế kiến trúc hệ thống 
   , sơ đồ luồng , biểu đồ tuần tự , kiến trúc hệ thống database, sơ đồ thiết kế API ,...
   
 Output:
   + Tổng hợp, hỏi đáp các kiến thức liên quan đến các nguồn file input đã được đính kèm. 
   + Chuẩn hóa gợi ý lại các tài liệu theo chuẩn mới như Agile/scrum , Báo cáo tiến độ dự án dưới dạng Grant Chart, theo dõi chất lượng bug/Issue qua jira, ... để triển khai tiếp cho các phare khác của dự án.
    
  
## Kết quả mong muốn :
  - Hệ thống phải sử dụng các AI tiên tiến như OpenAI , Claude , Gemini để tổng hợp , phân tích , embeding , dùng vector database để lưu trữ hiểu các nghĩa của tài liệu.
  - Bổ sung làm rõ các Công Nghệ Chính được sử dụng trong dự án ví dụ như:
    Có sử dung thêm kafka để làm pub/sub
    | Layer           | Công Nghệ                  | Mục Đích                           |
    |-----------------|---------------------------|-----------------------------------|
    | Processing      | Apache NiFi, Tesseract    | Xử lý file đa định dạng           |
    | AI Core         | OpenAI GPT-4, Claude 3    | Phân tích semantic                 |
    | Vector DB       | Pinecone, Weaviate        | Lưu trữ embedding                 |
    | Orchestration   | LangChain, LlamaIndex     | Kết nối các thành phần AI         |
    | Visualization   | Diagram (Python), PlantUML| Tự động sinh diagram              |
    | Backend         | FastAPI, Celery           | Xây dựng API và xử lý bất đồng bộ |

  - Hãy dùng draw.io theme AWS để đưa cho tôi 1 bản vẽ Thiết kế Kiến trúc hệ thống final thông thể dự án theo kiến trúc Microservice Architecture.
  - Dùng StartUML để vẽ top 20 sequence Diagram flow quan trọng nhất.  
  