#### -------------
Tổng hợp các keywords cần chuẩn bị cho việc học , kiến thức liên quan đến mô tả sau :
Chúng tôi đang tìm kiếm một AI Engineer có kinh nghiệm vững vàng trong việc phát triển và triển khai các mô hình Machine Learning, MLOps, và LLM (Large Language Models) để xây dựng các giải pháp AI Agent và Document Understanding cho khách hàng trong ngành healthcare tại Mỹ. Vị trí này yêu cầu khả năng làm việc độc lập, tinh thần lãnh đạo, và khả năng xây dựng và dẫn dắt đội ngũ kỹ thuật mạnh mẽ.
Trách nhiệm chính:
• Xây dựng và triển khai các mô hình AI (LLM, NLP, và Document Understanding) cho các ứng dụng trong ngành healthcare.
• Xây dựng và quản lý các pipeline MLOps để triển khai và duy trì các mô hình Machine Learning trong môi trường sản xuất.
• Phát triển và tối ưu hóa các hệ thống AI Agent để hỗ trợ quy trình chăm sóc sức khỏe thông minh.
• Xây dựng và triển khai các giải pháp AI giải quyết các vấn đề phức tạp trong việc xử lý và hiểu các tài liệu y tế.
• Dẫn dắt và xây dựng đội ngũ kỹ thuật, bao gồm việc huấn luyện và mentoring các thành viên trong nhóm.
• Làm việc chặt chẽ với các nhóm khác (data science, engineering, product) để đảm bảo các giải pháp AI được triển khai hiệu quả và đáp ứng nhu cầu kinh doanh.
• Tương tác trực tiếp với khách hàng để hiểu rõ yêu cầu và giải pháp phù hợp trong ngành healthcare.

####### ----------------
Kể ra ngày thường xài Axolotl finetune LLM cứ như cơm bữa, file config y chang mọi khi mà hôm nay model nó phất cờ khởi nghĩa, cứ generate chữ như suối không thèm dừng 😅 
Tưởng mình config sai chỗ nào, ngồi train tới 20 cái model như người điên, cuối cùng đầu hàng reverse code về commit cũ từ 2 tháng trước của Axolotl. Voila, phép màu xuất hiện, chạy ngon như... cái máy đáng lẽ nó phải ngon từ đầu 🙃🙃🙃
Bài học: Đôi khi để tiến lên phía trước, ta phải... lùi lại 2 tháng 


##### ----------------------------

Gần đây mình đang thử nghiệm một pipeline post-training khá thú vị cho LLM. 
Pipeline này tập trung vào việc cải thiện chất lượng model thông qua "đấu đối kháng" và học từ thất bại. 
Để làm được việc này, mình đã implement Offline Arena, phiên bản Offline của Chatbot Arena để làm data huấn luyện.

📋 Setup:
- Base model: Qwen2.5-7B
- Đối thủ: Llama3.1-70B và Phi-4
- Judge: Qwen2.5-72B-Instruct
🔄 Pipeline gồm 3 vòng lặp, mỗi vòng có 3 giai đoạn:
1️⃣ SFT (Supervised Fine-tuning):
- Cho model "đấu" với đối thủ
- Thu thập cases thua
- Train lại với câu trả lời của đối thủ
2️⃣ DPO (Direct Preference Optimization):
- Model SFT mới tiếp tục "đấu"
- Cases thua → data preferences
- Train DPO
3️⃣ PPO:
- Model DPO đấu tiếp
- Train Reward Model từ kết quả
- Train PPO với RM mới
💰 Chi phí: ~$12,000 (bao gồm data + training) cho model 7B
🎯 Kết quả rất mãn nhãn! Điểm MT-Bench và IFEval của mô hình cho kết quả ngang hoặc hơn các mô hình lớn hơn như Llama3.3-70B


https://www.facebook.com/hqmpd

#### ------------------------

ffmpeg -i input.mp4 -c copy -ss 00:00:10 -to 00:00:30 output.mp4

ffmpeg -i C:\Users\BOSS\Downloads\Video_2025-01-18_142425.mp4 -c copy -ss 00:00:00 -to 00:15:00 output-Video_2025-01-18_142425.mp4


#### ----------------------

LLM Post-training sẽ là chiến trường khốc liệt nhất của năm 2025 👀
Hôm trước dân mạng bàn tán liệu "Pre-training đã chết" hay chưa? Thật ra pre-training là một mảnh đất vẫn còn rất nhiều đất diễn mà mọi người chưa nghĩ tới. Ví dụ như bạn hoàn toàn có thể sử dụng dữ liệu từ bộ FineWeb/FineWebEdu vốn có chất lượng rất cao, và sử dụng chúng để làm retrieval cho các data có chất lượng cao tương đương trong mớ hàng chục TB text data trong CommonCrawl. Thậm chí bạn có thể dụng LLM để viết lại toàn bộ dữ liệu Web để chúng trở thành dữ liệu dạng conditional & controllable 100%. 
Tuy nhiên, chi phí và tài nguyên trong việc nghiên cứu các kĩ thuật mới trong pre-training gần như chỉ có các phòng lab từ các ông lớn là có cơ hội tiếp xúc nhiều (riêng team Phi-4 của Microsoft đã dùng hơn 4,000 GPUs, đó là gấp đôi số lượng GPUs của một tập đoàn lớn ở Việt Nam vừa mua, chưa kể các team khác như Orca hay WizardLM)
Trong khi đó, post-training đang trở thành một "chiến trường" sôi động với rào cản tham gia thấp hơn nhiều so với pre-training. Các công ty vừa và nhỏ, thậm chí các nhóm nghiên cứu độc lập, đều có thể tham gia vào lĩnh vực này với chi phí và tài nguyên phần cứng vừa phải. Post-training cho phép các mô hình được tinh chỉnh để phục vụ các nhiệm vụ và lĩnh vực cụ thể, từ đó tạo ra giá trị khác biệt trên thị trường. Đây cũng chính là thứ tạo nên o1 hay các mô hình "suy nghĩ" như QwQ-32B-Preview, DeepSeek-v3 đang gây bão.
Một vài kĩ thuật phổ biến nhất trong Post-training hiện nay:
- Model merging: việc sử dụng merging cả trong và sau quá trình post-training đều cho thấy hiệu quả trong việc tránh overfit lẫn tiết kiệm tài nguyên training.
- DPO/PPO/KTO/etc.: còn gọi là "preference learning", thường được sử dụng với mục đích làm alignment. Cho mô hình tuân thủ theo một chính sách, ghi nhớ nào đó.
- Knowledge distillation: Kỹ thuật này cho phép chuyển giao kiến thức từ mô hình lớn (teacher) sang mô hình nhỏ hơn (student), giúp tối ưu hóa kích thước mô hình mà vẫn duy trì được phần lớn hiệu năng. KD trên LLMs hiện tại chủ yếu dựa trên synthetic data.
Một trong những mô hình đã làm post-training rất ấn tượng đó là Qwen. Nếu bạn hỏi Qwen một câu hỏi chính trị mang tính nhạy cảm, nếu hỏi bằng tiếng Việt, nó sẽ đưa ra câu trả lời mà một người Việt Nam muốn nghe và tương tự với tiếng Trung Quốc. Không bàn đến tính đúng sai của câu trả lời vì đây là một câu hỏi nhạy cảm, và mang tính cảm quan cũng như các kiến thức và nguồn thông tin mỗi người dân được tiếp cận, nhưng nếu đứng góc độ của một người muốn sử dụng mô hình này vào các sản phẩm global, thì nó đã global-ready 🙂
Cuối tuần rồi chạy một thử nghiệm nho nhỏ kết hợp cả 3 kĩ thuật trên, kết quả ra được một mô hình 7B cho kết quả gần ngang ngửa các mô hình 32B/70B 😎Có open-source hay không thì phải xin đã😆