import requests

# Function to send email content to the API
def send_email_to_api(email_content):
    response = requests.post("http://localhost:8000/api/analyze", json={"email_content": email_content})
    response_data = response.json()

    # Safely access the keys
    sentiment = response_data.get("sentiment", "No sentiment data")
    summary = response_data.get("summary", "No summary data")
    reply = response_data.get("reply", "No reply data")

    print("====================== MAIL ANALYSIS RESULT ======================")
    print("I. SENTIMENT\n", sentiment, "\n")
    print("II. SUMMARY\n", summary, "\n")
    print("III. MAIL REPLY\n", reply, "\n")
    print("==================================================================")

# Trigger the function
if __name__ == "__main__":
    mail_content = \
"""
Chủ đề: Phản hồi về dịch vụ giám sát an toàn thông tin SOC

Kính gửi đội ngũ Viettel Cyber Security,

Chúng tôi, Công ty Chứng khoán ABCXYZ, muốn gửi lời cảm ơn đến đội ngũ chuyên gia của Viettel Cyber Security vì đã cung cấp dịch vụ giám sát an toàn thông tin SOC chuyên nghiệp trong thời gian qua.

Sau thời gian sử dụng dịch vụ, chúng tôi nhận thấy:

Hiệu quả giám sát vượt trội: Hệ thống SOC của Viettel đã phát hiện và cảnh báo kịp thời các mối đe dọa tiềm tàng, giúp ABCXYZ có thể ứng phó nhanh chóng, đảm bảo hệ thống hoạt động ổn định và an toàn.
Hỗ trợ tận tâm: Đội ngũ chuyên gia của Viettel luôn sẵn sàng hỗ trợ 24/7, đưa ra những tư vấn sát sao và phù hợp với tình hình thực tế của chúng tôi.
Báo cáo chất lượng: Các báo cáo phân tích chi tiết và rõ ràng đã mang lại cái nhìn sâu sắc về tình hình an ninh mạng của công ty.
Tuy nhiên, chúng tôi mong muốn Viettel Cyber Security có thể cải thiện thêm ở một số điểm:

Tăng cường tích hợp công cụ phân tích mối đe dọa nâng cao để nhận diện các nguy cơ tinh vi hơn.
Rút ngắn thời gian phản hồi trong các tình huống khẩn cấp để tối ưu hóa hiệu quả bảo vệ.
Chúng tôi đánh giá cao sự hợp tác và chuyên nghiệp của Viettel Cyber Security và mong tiếp tục đồng hành trong việc xây dựng hệ thống an ninh mạng vững chắc.

Trân trọng,
Hoang Trang Quang Giang Nghia (Mr.)
Công ty ABCXYZ
Điện thoại: 0979123456
"""
    send_email_to_api(mail_content)
    
    
