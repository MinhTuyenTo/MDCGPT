import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox
import google.generativeai as genai
import hashlib, os
import speech_recognition as sr
import threading
from gtts import gTTS
import pygame
import tempfile, time
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os,sys,gc
import tkinter as tk  
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageTk

# ========== CẤU HÌNH ==========
def resource_path(relative_path):
    """ Lấy đường dẫn đúng khi chạy file .exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

SERVICE_JSON = resource_path("D:\MDCGPT\service_account.json")


def typewriter_effect(widget, text, tag="ai", delay=10):
    """Hiển thị từng ký tự một để tránh đơ UI"""
    widget.configure(state="normal")
    widget.insert("end", "\nAI: ", tag)
    widget.configure(state="disabled")
    
    def write_char(i=0):
        if i < len(text):
            widget.configure(state="normal")
            widget.insert("end", text[i], tag)
            widget.see("end")
            widget.configure(state="disabled")
            widget.after(delay, write_char, i + 1)
    write_char()

def init_sheet():
    global sheet
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    SERVICE_FILE = os.path.join(BASE_DIR, "service_account.json")

    creds = Credentials.from_service_account_file(
        SERVICE_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1tLPU-SIjSQ8KOuVodsw79aZ3MPpd6jgXl9HSkm_8XZE").worksheet("users")
    return sheet
def get_parent_phone(student_name, student_class=None):
    """Truy xuất SĐT phụ huynh từ Sheet3"""
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        SERVICE_FILE = os.path.join(BASE_DIR, "service_account.json")

        creds = Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet3 = client.open_by_key("1tLPU-SIjSQ8KOuVodsw79aZ3MPpd6jgXl9HSkm_8XZE").worksheet("sodienthoai")
        data = sheet3.get_all_records()

        for row in data:
            name = str(row.get("Họ tên học sinh") or "").strip().lower()
            class_name = str(row.get("Lớp") or "").strip().lower()
            phone = str(row.get("SĐT phụ huynh") or "").strip()
            if student_name.lower() in name and (not student_class or student_class.lower() in class_name):
                return phone
        return None
    except Exception as e:
        print(f"[Lỗi đọc Sheet3]: {e}")
        return None

sheet = init_sheet()

def add_user_to_sheet(userid, password):
    global sheet
    try:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([userid, password, now])
        print(f"✅ Đã ghi {userid} ({password}) vào Google Sheet.")
    except Exception as e:
        print(f"[Lỗi ghi Google Sheet]: {e}")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

API_KEY = "AIzaSyBvlTttA6TqW2V9N14ZTHf2P8ROkBsnOZ4"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=(
        "Bạn là MĐC GPT - AI Tư vấn học đường trường THPT MẠC ĐĨNH CHI. "
        "Chỉ trả lời về các chủ đề liên quan đến học đường ở trường MẠC ĐĨNH CHI như: "
        "nội quy trường học, học tập các môn Toán, Lý, Hóa, Văn, Sử, Địa, Sinh, Anh,..., "
        "cách học hiệu quả, kỹ năng trong trường MẠC ĐĨNH CHI, cách ăn mặc khi đến trường. "
        "Nếu câu hỏi ngoài phạm vi trường THPT MẠC ĐĨNH CHI, hãy trả lời: "
        "'Xin lỗi, tôi chỉ hỗ trợ các vấn đề liên quan đến học đường tại trường MẠC ĐĨNH CHI.'\n"
        """
                    ĐOÀN XÃ CHƯ PĂH                                                      ĐOÀN TNCS HỒ CHÍ MINH                 
ĐOÀN TRƯỜNG THPT MẠC ĐĨNH CHI
                                    ***                 
                        Số: 01 /QC-ĐTN                                                         Chư Păh, ngày 20  tháng 8 năm 2025

QUY CHẾ
QUY ĐỊNH NỀ NẾP ĐỐI VỚI HỌC SINH

Căn cứ vào Điều lệ Đoàn TNCS Hồ Chí Minh;
Căn cứ vào Quy tắc ứng xử của trường THPT Mạc Đĩnh Chi;
              Căn cứ Quy chế thi đua giữa các lớp của trường THPT Mạc Đĩnh Chi
Đoàn trường thống nhất đưa ra quy chế sau:
I . MỤC ĐÍCH.
- Góp phần hình thành tác phong, thói quen học tập và sinh hoạt tích cực, nghiêm túc cho học sinh.
- Đảm bảo môi trường giáo dục có trật tự, an toàn, văn minh.
 	-  Nâng cao ý thức trách nhiệm và tinh thần tự giác của học sinh.
- Tạo thói quen tôn trọng kỷ luật, sống có tổ chức, biết tự quản và hỗ trợ lẫn nhau.
- Làm căn cứ để đánh giá, xếp loại thi đua tập thể và cá nhân trong năm học.
"""
"""
II. QUY ĐỊNH NỀ NẾP
A. ĐỒNG PHỤC
1. Áo, quần:
- Học sinh khi đến trường mặc áo sơ mi trắng, quần tây màu xanh, màu đen hoặc màu xanh đen một màu. Đối với học sinh nam phải bỏ áo trong quần. 
- Ngày thứ 5 đồng phục áo xanh thanh niên Việt Nam.
- Học sinh nữ: Đồng phục áo dài vào các ngày thứ 2, thứ 4 và các ngày lễ trong năm học (có thể mặc áo gi-lê màu trắng).
- Thực hiện nghiêm túc việc mặc áo khoác đồng phục của nhà trường , không được phép mặc áo khoác có màu. Nếu thời tiết lạnh, khi đoàn trường thông báo, học sinh có thể mặc các loại áo khoác khác.
2. Đầu tóc: Phải gọn gàng, không được nhuộm các màu (nếu nhuộm chỉ được nhuộm tóc màu đen). Học sinh không xăm chàm lên cơ thể.  
- Học sinh nam không để tóc dài, không cắt tóc ngắn quá 3 phân và cắt, kẻ tóc mai không phù hợp, không để đuôi tóc nhọn. Học sinh nam không được đeo hoa tai.
- Học sinh nữ không trang điểm, không đeo khuyên mũi, không sơn móng tay, móng chân.
3. Giày dép: Đi giày kín, giày bít, dép có quai hậu (quai hậu dép không dùng dây mảnh nhỏ, dây rời hoặc mang tính chất đối phó).
4. Bảng tên: Học sinh khi đến trường phải mang bảng tên (có dán hình 3 x 4 và đóng dấu hoặc in lôgô của nhà trường); không dán hình người khác, tranh ảnh hoặc viết vẽ lên bảng tên). 
"""
"""
B. CÁC QUY ĐỊNH KHÁC
1. Học sinh không được ra khỏi trường trong thời gian buổi học (trừ trường hợp giáo viên cho phép hoặc đã học xong môn học trái buổi ).
2. Cấm mang vũ khí, chất gây nổ, gây cháy; rượu bia, thuốc lá, chất kích thích vào trường.
3. Không đi xe đạp, xe máy trong khuôn viên sân trường.
4. Không tập trung đông người ở khu vực trước cổng trường.
5. Không sử dụng điện thoại trong khuôn viên  nhà trường
6. Không hút thuốc lá trong và ngoài nhà trường.
7. Giữ vệ sinh chung, bảo vệ tài sản nhà trường.
"""
"""
C. QUY ĐỊNH TRỪ ĐIỂM NỀ NẾP
Tổng điểm nề nếp tối đa: 60 điểm
1. Về đồng phục và tác phong
Học sinh không mang bảng tên, huy hiệu Đoàn (đối với đoàn viên) hoặc có các vi phạm về bảng tên, logo, quần áo đồng phục, áo khoác, giày dép không đúng quy định sẽ bị trừ 1 điểm cho mỗi học sinh vi phạm.
Học sinh nữ đi học nếu trang điểm, tô son môi, sơn móng tay hoặc móng chân, nhuộm tóc hay để các kiểu tóc không phù hợp với môi trường học đường sẽ bị trừ 2 điểm cho mỗi học sinh vi phạm.
Học sinh nam đeo hoa tai, nhuộm tóc, cắt hoặc uốn tóc không đúng quy định cũng sẽ bị trừ 2 điểm cho mỗi học sinh vi phạm.
2. Về vệ sinh trường lớp và bảo quản cơ sở vật chất
Nếu lớp không hoàn thành nhiệm vụ lao động thường xuyên hoặc định kỳ sẽ bị trừ 5 đến 10 điểm cho mỗi lớp.
Nếu không thực hiện nhiệm vụ: trừ 10 điểm/lớp.
Nếu có thực hiện nhưng kết quả không đạt yêu cầu: trừ 5 điểm/lớp.
Lớp học để bẩn như bảng không lau, có rác trong hộc bàn, dụng cụ vệ sinh như chổi, sọt rác để sai vị trí quy định sẽ bị trừ 5 điểm/lớp.
Khi ra khỏi lớp mà không tắt điện, quạt hoặc các thiết bị điện khác sẽ bị trừ 2 điểm/lớp.
Học sinh mang vũ khí, chất dễ cháy, chất nổ vào trường học sẽ bị xử lý nghiêm và trừ 15 điểm cho mỗi học sinh vi phạm.
Học sinh phá hoại tài sản trường, bẻ cây xanh, làm hư hại cơ sở vật chất hoặc tự ý di chuyển ghế đá trong khuôn viên trường sẽ bị trừ 10 điểm cho mỗi học sinh vi phạm.
Học sinh xả rác trong khuôn viên nhà trường hoặc mang rác thải nhựa vào trường sẽ bị trừ 2 điểm cho mỗi học sinh vi phạm.
3. Về nề nếp học tập và sinh hoạt
Nếu lớp không học các tiết giáo dục ngoài giờ lên lớp (NGLL), quốc phòng, hướng nghiệp, thể dục (với tỷ lệ trên 2/3 học sinh nghỉ không có lý do), hoặc không tham gia các hoạt động ngoại khóa, các cuộc thi trực tuyến (với tỷ lệ tham gia dưới 80% sĩ số), hoặc không tham gia mít tinh, hoạt động được phân công thì sẽ bị trừ 10 điểm/lớp.
Lớp không tổ chức sinh hoạt 15 phút đầu giờ, sinh hoạt sai chủ đề hoặc có hơn một nửa học sinh không tham gia sẽ bị trừ 5 điểm/lớp.
Vi phạm trong tiết chào cờ như: xuống sân chào cờ trễ quá 5 phút sau hiệu lệnh trống, lớp trực tuần không đảm bảo công tác chuẩn bị (văn nghệ, điều khiển chào cờ...), hoặc không thu dọn, đưa ghế chào cờ vào kho sau khi kết thúc buổi lễ sẽ bị trừ 5 điểm/lớp.
Lớp được phân công trực cổng trường nhưng không thực hiện nhiệm vụ, không đủ người trực tại các vị trí (cổng chính, cổng nhà thi đấu, khu vực nhà vệ sinh) hoặc để cờ đỏ trực không đúng tác phong, không nghiêm túc, tự ý đổi người trực sẽ bị trừ 5 điểm/lớp.
Học sinh đánh nhau hoặc có liên quan đến đánh nhau sẽ bị trừ 10 điểm cho mỗi học sinh vi phạm.
Học sinh sử dụng rượu, bia, hút thuốc lá, thuốc lá điện tử hoặc các chất kích thích khác trong khuôn viên trường hoặc khu vực trước cổng trường, hoặc đến trường khi trong người có mùi rượu, bia sẽ bị trừ 10 điểm cho mỗi học sinh vi phạm.
Học sinh gửi xe máy hoặc xe đạp trước cổng trường, đi xe máy hoặc xe đạp trong khuôn viên trường, không đội mũ bảo hiểm, hoặc chở ba khi đến trường sẽ bị trừ 10 điểm cho mỗi học sinh vi phạm.
Sử dụng điện thoại trong lớp khi chưa được giáo viên cho phép sẽ bị trừ 5 điểm cho mỗi học sinh vi phạm.
Học sinh leo trèo cổng trường, hàng rào sẽ bị trừ 5 điểm mỗi học sinh.
Học sinh ra ngoài cổng trường trong giờ học khi chưa được giáo viên hoặc nhà trường cho phép sẽ bị trừ 2 điểm mỗi học sinh.
Cúp tiết, bao gồm tiết chào cờ, tiết NGLL, hoặc tiết sinh hoạt 15 phút, sẽ bị trừ 2 điểm mỗi học sinh.
Học sinh vắng học trong các buổi ôn tập, ngoại khóa, mít tinh... nếu có phép sẽ bị trừ 0,5 điểm, nếu không có phép sẽ bị trừ 1 điểm cho mỗi học sinh.
Học sinh đi học trễ sau tiếng trống vào học sẽ bị trừ 1 điểm cho mỗi học sinh vi phạm.
Trong các buổi sinh hoạt hoặc hoạt động ngoại khóa, học sinh không nghiêm túc, bị giáo viên hoặc cán bộ lớp nhắc nhở sẽ bị trừ 1 điểm mỗi học sinh.
4. Về văn hóa ứng xử
Học sinh vi phạm quy định tại Điều 7 - Ứng xử của học sinh, Chương II, Bộ quy tắc ứng xử của trường THPT Mạc Đĩnh Chi sẽ bị trừ 10 điểm mỗi học sinh.
Cụ thể:
Đối với cán bộ quản lý, giáo viên, nhân viên: học sinh cần kính trọng, lễ phép, trung thực, chia sẻ và chấp hành các quy định. Không được bịa đặt, xúc phạm danh dự, nhân phẩm, hay có hành vi bạo lực.
Đối với học sinh khác: cần giao tiếp bằng ngôn ngữ đúng mực, thân thiện, trung thực, hợp tác, tôn trọng sự khác biệt. Không được nói tục, chửi bậy, miệt thị, gây mất đoàn kết, bịa đặt, lôi kéo bè phái hoặc phát tán thông tin làm ảnh hưởng đến danh dự của bạn khác.
Đối với cha mẹ và người thân: cần thể hiện sự kính trọng, lễ phép, trung thực và yêu thương.
Đối với khách đến trường: phải tôn trọng, lễ phép, có thái độ đúng mực.
Ngoài ra, học sinh vi phạm các quy định của Luật An ninh mạng, sử dụng điện thoại hoặc thiết bị quay phim, chụp ảnh để đăng tải hình ảnh, video không lành mạnh (như video đánh nhau hoặc các nội dung gây ảnh hưởng xấu đến uy tín và hoạt động giáo dục của nhà trường) sẽ bị trừ 15 điểm mỗi học sinh.video không tốt làm ảnh hưởng đến hoạt động giáo dục nhà trường (ví dụ như video đánh nhau…)	15đ /1 HS
*Lưu ý: 
- Đối với các học sinh vi phạm các lỗi có điểm trừ từ 5 điểm trở lên, các lớp lập danh sách nộp về đoàn trường vào ngày thứ 7 hàng tuần, để theo dõi và có biện pháp xử lý kịp thời.
- Đối với từng hoạt động phong trào trong năm học, Đoàn trường sẽ có kế hoạch riêng.
- Đối với HS vi phạm trật tự an toàn giao thông, vi phạm pháp luật Nhà nước thì sẽ xem xét đưa lên hội đồng kỉ luật của nhà trường.
"""
"""
QUY ĐỊNH CỘNG ĐIỂM THI ĐUA
1. Cộng điểm thi đua hàng tuần
Căn cứ vào kết quả xếp loại thi đua hàng tuần do nhà trường công bố:
Nếu lớp đạt danh hiệu “Lớp chọn” (đạt 100 điểm thi đua trong tuần) sẽ được cộng thêm 2 điểm cho lớp trong tuần đó.
Nếu lớp đạt danh hiệu “Lớp cơ bản” (đạt 98 điểm thi đua trong tuần) cũng được cộng 2 điểm cho lớp trong tuần đó.
→ Như vậy, mỗi tuần lớp có thể được cộng tối đa 2 điểm vào tổng điểm nề nếp tùy theo kết quả xếp loại.
2. Cộng điểm khi tham gia phong trào do Đoàn tổ chức
Đối với tập thể lớp:
Khi lớp tham gia các phong trào, hoạt động do Tỉnh đoàn phát động, tùy theo mức độ hoàn thành và kết quả đạt được, lớp có thể được cộng tối đa 10 điểm/lớp.
Khi lớp tham gia các phong trào, hoạt động do Xã đoàn hoặc Phường đoàn tổ chức, lớp sẽ được cộng tối đa 5 điểm/lớp.
Đối với cá nhân học sinh:
Học sinh tích cực tham gia, đạt thành tích hoặc có đóng góp nổi bật trong các phong trào của Đoàn (ở cấp trường, xã hoặc tỉnh) sẽ được cộng thêm 5 điểm cho mỗi cá nhân.
"""
"""
D. QUY ĐỊNH TRỪ ĐIỂM SỔ ĐẦU BÀI
Điểm tối đa cho mỗi tiết học: 10 điểm
Trong quá trình giảng dạy, giáo viên bộ môn căn cứ vào thái độ học tập, ý thức kỷ luật và nền nếp của học sinh trong từng tiết để chấm điểm sổ đầu bài. Các lỗi vi phạm cụ thể bị trừ điểm như sau:
Học sinh vắng học không có lý do sẽ bị trừ 1 điểm cho mỗi học sinh.
Học sinh vắng học có lý do (có giấy phép hợp lệ) sẽ bị trừ 0,5 điểm cho mỗi học sinh.
Học sinh vào lớp trễ mà không xin phép trước sẽ bị trừ 0,5 điểm cho mỗi học sinh.
Học sinh mặc đồng phục không đúng quy định (thiếu bảng tên, sai trang phục, không gọn gàng, không đi giày dép đúng quy định...) sẽ bị trừ 2 điểm cho mỗi học sinh.
Học sinh sử dụng ngôn ngữ ứng xử không phù hợp hoặc thực hiện các hành vi bị cấm theo điều lệ nhà trường (như nói tục, gây gổ, xúc phạm người khác...) sẽ bị trừ 2 điểm cho mỗi học sinh.
Lớp học không tập trung, nói chuyện riêng nhiều, không tích cực phát biểu xây dựng bài, hoặc có kết quả học tập dưới trung bình trong tiết học sẽ bị trừ 3 điểm cho tập thể lớp.
Nếu lớp không có khăn lau bảng, để lớp học bẩn, bàn ghế không ngay ngắn, đồ dùng học tập không gọn gàng, phòng học không sạch sẽ, thì sẽ bị trừ 2 điểm cho lớp.
Học sinh không học bài cũ, không soạn bài, không làm bài tập theo yêu cầu của giáo viên, hoặc làm việc riêng trong giờ học sẽ bị trừ 1 điểm cho mỗi học sinh vi phạm.
Học sinh sử dụng điện thoại trong giờ học khi chưa được giáo viên cho phép sẽ bị trừ 2 điểm cho mỗi học sinh vi phạm.
Học sinh cúp tiết, bỏ học tiết đó không lý do sẽ bị trừ 2 điểm cho mỗi học sinh vi phạm.
Lưu ý quan trọng:
Đối với học sinh bị bệnh dài ngày (từ 5 ngày trở lên), hoặc mắc bệnh xã hội cần điều trị, giáo viên bộ môn vẫn thực hiện trừ điểm theo quy định. Tuy nhiên, vào cuối tuần, nếu học sinh có giấy phép hợp lệ (như giấy nhập viện, giấy ra viện, giấy xét nghiệm...) thì sẽ được xem xét điều chỉnh trong tổng hợp điểm thi đua.
Giáo viên khi nhận xét trong sổ đầu bài phải phù hợp với số điểm đã cho. Không được chấm điểm tùy ý hoặc ghi nhận xét chung chung như: “Được”, “Tạm”, “Bình thường”.
Chấm điểm học tốt: mỗi tiết học tốt được đánh giá theo hai mức là Đạt hoặc Không đạt.
Chỉ khi tiết học đạt từ 9 điểm trở lên mới được xếp loại Đạt.
Cách tính điểm thi đua hàng tuần
Tổng điểm thi đua của mỗi lớp trong tuần được tính tối đa là 100 điểm, bao gồm hai phần chính:
Điểm nề nếp:
Tối đa 60 điểm.
Nếu có vi phạm, điểm nề nếp được tính theo công thức:
→ Điểm nề nếp = 60 - Tổng điểm vi phạm.
Điểm sổ đầu bài:
Lấy tổng điểm của tất cả các tiết học trong tuần, chia trung bình cộng, rồi nhân hệ số 4.
Tối đa 40 điểm.
Đối với tuần đăng ký học tốt:
Điểm nề nếp: tối đa 60 điểm, tính tương tự như trên (60 - điểm vi phạm).
Điểm sổ đầu bài: lấy trung bình các tiết trong tuần nhân hệ số 3, tối đa 30 điểm.
Điểm học tốt: tối đa 10 điểm, tính riêng như sau:
Mỗi lớp đăng ký 5 tiết học tốt trong 1 tuần.
Mỗi tiết đạt yêu cầu được cộng 2 điểm/tiết.
Mỗi tiết không đạt sẽ bị trừ 2 điểm/tiết.
"""
"""
III.KHEN THƯỞNG.
1 Khen thưởng.
  Căn cứ vào điểm thi đua, Đoàn trường khen thưởng cho các Chi đoàn có điểm thi đua từ cao xuống thấp ( số lượng tùy vào tình hình thực tế) và không có học sinh vi phạm kỷ luật từ khiển trách trở lên 
IV. TỔ CHỨC THỰC HIỆN.
Đoàn trường và các bộ phận có liên quan chủ động phối hợp, triển khai tổ chức thực hiện tốt quy chế. Công tác bình xét thi đua, khen thưởng được tổ chức một năm 1 lần vào cuối năm học.
"""
"""
	 TM.BCH ĐOÀN TRƯỜNG
Nơi nhận:                                                                                          BÍ THƯ
- GVCN, Ban cán sự lớp;
- Lưu VP Đoàn trường.	
					
									   Thái Thị Thu Hà
                                       """
    )
)


chat = model.start_chat()

# ========== HÀM HỖ TRỢ ==========

def hash_password(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_users_from_sheet():
    global sheet
    """Đọc toàn bộ danh sách tài khoản từ Google Sheet"""
    try:
        records = sheet.get_all_records()
        users = {}
        for r in records:
            userid = str(r.get("userid") or r.get("name") or "").strip()
            pw = str(r.get("password") or "").strip()
            if userid and pw:
                users[userid] = pw
        

        return users
    except Exception as e:
        print(f"[Lỗi load users từ Google Sheet]: {e}")
        return {}

def save_user_to_sheet(userid, password):
    global sheet
    """Thêm user mới vào Google Sheet"""
    try:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sheet.append_row([userid, hash_password(password), now])
        print(f"✅ Đã thêm {userid} vào Google Sheet.")
    except Exception as e:
        print(f"[Lỗi ghi Google Sheet]: {e}")

def update_password_in_sheet(userid, new_password):
    """Cập nhật mật khẩu trên Google Sheet (nếu cần sau này)"""
    try:
        records = sheet.get_all_records()
        for i, row in enumerate(records, start=2):  # dòng 1 là header
            if str(row.get("userid") or row.get("name")) == userid:
                sheet.update_cell(i, 2, hash_password(new_password))
                print(f"Đã cập nhật mật khẩu cho {userid}")
                return
    except Exception as e:
        print(f"[Lỗi cập nhật mật khẩu Google Sheet]: {e}")

def save_last_user(username):
    with open("last_user.txt", "w", encoding="utf-8") as f:
        f.write(username)

def load_last_user():
    if os.path.exists("last_user.txt"):
        with open("last_user.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def logout_user():
    if os.path.exists("last_user.txt"):
        os.remove("last_user.txt")
        
# ========== ỨNG DỤNG ==========
class MDCGPTApp:
    def start_playback_for_text(self, text):
        """Phát âm thanh từ văn bản (chạy trong luồng riêng để không treo UI)"""
        if not text:
            messagebox.showinfo("Thông báo", "Không có nội dung để phát.")
            return

        def play_audio_thread():
            try:
                # Tạo file âm thanh tạm
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts = gTTS(text=text, lang="vi")
                    tts.save(tmp.name)
                    tmp_path = tmp.name

                # Phát âm thanh
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()

                # Đợi đến khi phát xong (vẫn song song với UI)
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                pygame.mixer.quit()
                os.remove(tmp_path)
            except Exception as e:
                print(f"[Lỗi phát âm thanh]: {e}")
                messagebox.showerror("Lỗi âm thanh", str(e))

        # Chạy phát âm thanh trong luồng riêng
        threading.Thread(target=play_audio_thread, daemon=True).start()
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PHẦN MỀM MDC_BOT")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Icon cửa sổ
        if os.path.exists("assets/logoMDC.ico"):
            self.root.iconbitmap("assets/logoMDC.ico")

        self.username = load_last_user() or None
        self.load_images()
        self.show_welcome_screen() if not self.username else self.show_main_screen()
    def load_images(self):
        try:
            self.bg_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/welcomepng.png")).resize((900, 600), Image.Resampling.LANCZOS))
            self.logo1_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/logotruong.png")).resize((130, 130), Image.Resampling.LANCZOS))
            self.logo2_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/logodoan.png")).resize((110, 110), Image.Resampling.LANCZOS))
        except Exception as e:
            print(f"[Lỗi tải hình]: {e}")
            self.bg_photo = self.logo1_photo = self.logo2_photo = None
    # ========== MÀN HÌNH CHÀO ==========
    def show_welcome_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        # Tạo Canvas
        canvas = ctk.CTkCanvas(self.root, width=900, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Load và hiển thị background
        try:
            self.bg_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/welcomepng.png")).resize((900, 600), Image.Resampling.LANCZOS))
            canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tải được background.png\n{e}")
            return

        # Tạo 2 vùng click trong suốt (không dùng Button)
        # Vùng ĐĂNG NHẬP: x=300→600, y=280→350 (tọa độ đúng nút xanh)
        login_zone = canvas.create_rectangle(
            336, 210, 562, 274,
            fill="", outline="", tags="login_zone"
        )

        # Vùng ĐĂNG KÝ: x=300→600, y=380→450 (tọa độ đúng nút xanh lá)
        register_zone = canvas.create_rectangle(
            336, 307, 562, 373,
            fill="", outline="", tags="register_zone"
        )


        def on_click_login(e):
            self.show_login_screen()

        def on_click_register(e):
            self.show_register_screen()

        # Gắn sự kiện
        canvas.tag_bind("login_zone", "<Button-1>", on_click_login)
        canvas.tag_bind("register_zone", "<Button-1>", on_click_register)

        # (Tùy chọn) Nếu bạn muốn hoàn toàn không có hiệu ứng hover nào cả:
        # → Xóa 4 hàm on_enter/on_leave và chỉ để lại on_click
    # ========== ĐĂNG NHẬP ==========
 
    def show_login_screen(self):
        for w in self.root.winfo_children():
            w.destroy()
        #Canvas
        canvas = ctk.CTkCanvas(self.root, width=900, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        # Background
        try:
            self.login_bg_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/loginpng.png")).resize((900, 600), Image.Resampling.LANCZOS))
            canvas.create_image(0, 0, image=self.login_bg_photo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không load được login.png!\n{e}")
            return

        # ================= Ô TÊN – TRONG SUỐT 100% =================
        entry_user = tk.Entry(
            self.root,
            font=("Arial", 18),
            fg="#003087",              # màu chữ
            bg="#f7f6f4",                # nền trắng (nhưng sẽ bị ảnh nền che → trong suốt)
            relief="flat",             # không viền
            highlightthickness=0,
            insertbackground="#003087" # con trỏ gõ
        )
        entry_user.place(x=152, y=218, width=650, height=40)
        entry_user.insert(0, "")  # để trống

        # ================= Ô MẬT KHẨU – TRONG SUỐT 100% =================
        entry_pass = tk.Entry(
            self.root,
            font=("Arial", 18),
            fg="#003087",
            bg="#f7f6f4",
            relief="flat",
            highlightthickness=0,
            show="*",
            insertbackground="#003087"
        )
        entry_pass.place(x=210, y=300, width=600, height=40)

        # === TẠO 2 VÙNG CLICK BẰNG CANVAS CREATE_RECTANGLE ===
        # Nút ĐĂNG NHẬP
        login_rect = canvas.create_rectangle(
            378, 375, 521, 412,   # tọa độ chính xác nút "Đăng nhập" trong ảnh
            fill="", outline="", tags="login_btn"
        )

        # Nút QUAY LẠI
        back_rect = canvas.create_rectangle(
            378, 421, 521, 459,   # tọa độ nút "Quay lại"
            fill="", outline="", tags="back_btn"
        )

        def on_click_login(e):
            self.do_login(entry_user.get(), entry_pass.get())
        def on_click_back(e):
            self.show_welcome_screen()

        # Gắn sự kiện
        canvas.tag_bind("login_btn", "<Button-1>", on_click_login)
        canvas.tag_bind("back_btn", "<Button-1>", on_click_back)
        # Focus + Enter
        entry_user.focus()
        self.root.bind("<Return>", lambda e: self.do_login(entry_user.get(), entry_pass.get()))
    def do_login(self, username, password):
            if not username or not password:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tên và mật khẩu!")
                return

            users = load_users_from_sheet()
            if not users:
                messagebox.showerror("Lỗi", "Không tải được dữ liệu người dùng!")
                return

            hashed = hash_password(password)
            if username in users and users[username] == hashed:
                self.username = username
                save_last_user(username)
                messagebox.showinfo("Thành công", f"Chào mừng {username} quay lại!")
                self.show_main_screen()
            else:
                messagebox.showerror("Sai thông tin", "Tên người dùng hoặc mật khẩu không đúng!")
    # ========== ĐĂNG KÝ ==========
    def show_register_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        # === Canvas + Background đăng ký ===
        canvas = ctk.CTkCanvas(self.root, width=900, height=600, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        try:
            self.register_bg_photo = ImageTk.PhotoImage(Image.open(resource_path("assets/registerpng.png")).resize((900, 600), Image.Resampling.LANCZOS))
            canvas.create_image(0, 0, image=self.register_bg_photo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tìm thấy ảnh đăng ký!\n{e}")
            return

        # ================= 3 Ô NHẬP DÙNG tk.Entry =================
        entry_user = tk.Entry(self.root, font=("Arial", 18), fg="#003087", bg="#f7f6f4",
                            relief="flat", highlightthickness=0, insertbackground="#003087")
        entry_user.place(x=152, y=218, width=650, height=40)
        entry_user.focus()

        entry_pass1 = tk.Entry(self.root, font=("Arial", 18), fg="#003087", bg="#f7f6f4",
                            relief="flat", highlightthickness=0, show="*", insertbackground="#003087")
        entry_pass1.place(x=212, y=298, width=600, height=40)

        entry_pass2 = tk.Entry(self.root, font=("Arial", 18), fg="#003087", bg="#f7f6f4",
                            relief="flat", highlightthickness=0, show="*", insertbackground="#003087")
        entry_pass2.place(x=307, y=378, width=500, height=40)

        # === 2 NÚT CLICK VÔ HÌNH – KHÔNG HOVER, KHÔNG HIỆU ỨNG ===
        btn_register = canvas.create_rectangle(378, 440, 521, 479, fill="", outline="", tags="register")
        btn_back     = canvas.create_rectangle(378, 498, 521, 537, fill="", outline="", tags="back")

        # Chỉ giữ click – không hover, không viền, không fill
        canvas.tag_bind("register", "<Button-1>", lambda e: self.do_register(
            entry_user.get().strip(), entry_pass1.get(), entry_pass2.get()
        ))
        canvas.tag_bind("back", "<Button-1>", lambda e: self.show_welcome_screen())

        # Nhấn Enter = Đăng ký
        self.root.bind("<Return>", lambda e: self.do_register(
            entry_user.get().strip(), entry_pass1.get(), entry_pass2.get()
        ))
    def do_register(self, username, pass1, pass2):
        username = username.strip()
        if not username or not pass1 or not pass2:
            messagebox.showwarning("Thiếu", "Vui lòng nhập đầy đủ!")
            return
        if pass1 != pass2:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp!")
            return
        if len(pass1) < 4:
            messagebox.showwarning("Yếu", "Mật khẩu phải ≥ 4 ký tự!")
            return

        users = load_users_from_sheet()
        if username in users:
            messagebox.showerror("Lỗi", "Tên người dùng đã tồn tại!")
            return

        save_user_to_sheet(username, pass1)
        messagebox.showinfo("Thành công", f"Đăng ký thành công: {username}")
        self.show_login_screen()
    # ========== GIAO DIỆN CHÍNH ==========
    def show_main_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        # --- Tiêu đề ứng dụng (giữa màn hình) ---
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.pack(fill="x", pady=(10, 10))  # 10px khoảng cách dưới

        ctk.CTkLabel(
            title_frame,
            text="MDC BOT V1.1",
            font=("Arial", 20, "bold"),
            text_color="#1b5e20"
        ).pack(side="top", pady=5)

        # --- Nút người dùng góc phải ---
        display_name = self.username if len(self.username) <= 20 else self.username[:17] + "..."
        self.user_button = ctk.CTkButton(
            self.root,
            text=display_name,
            width=180,          # cố định 180px là đủ đẹp
            height=38,
            corner_radius=19,
            fg_color="#1e88e5",
            hover_color="#1565c0",
            font=("Arial", 13, "bold"),
            command=self.show_user_menu
        )
        self.user_button.place(relx=1.0, x=-20, y=15, anchor="ne")

        # --- Khung chat ---
        chat_frame = ctk.CTkFrame(self.root)
        chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Thanh trên của khung chat (Clear | ... | 🔊 Nghe âm thanh | Search | Save)
        top_bar = ctk.CTkFrame(chat_frame, fg_color="transparent")
        top_bar.pack(fill="x")

        # Clear bên trái
        ctk.CTkButton(top_bar, text="Clear", command=self.clear_chat, width=80, fg_color="#c62828").pack(side="left", padx=5, pady=5)

        # Nút phát âm thanh ở cạnh phải (sẽ dùng self.last_ai_text)
        self.speak_button_top = ctk.CTkButton(
            top_bar,
            text="🔊 Nghe âm thanh",
            width=140,
            fg_color="#00897b",
            hover_color="#00695c",
            command=lambda: threading.Thread(target=self.start_playback_for_text, args=(getattr(self, "last_ai_text", ""),)).start()
        )
        self.speak_button_top.pack(side="right", padx=5, pady=5)

        # Search và Save bên phải (sau speak_button)
        ctk.CTkButton(top_bar, text="Search", command=self.search_in_chat, width=80, fg_color="#ffb300").pack(side="right", padx=5, pady=5)
        ctk.CTkButton(top_bar, text="Save", command=self.save_chat, width=80, fg_color="#4caf50").pack(side="right", padx=5, pady=5)



        # Khung hiển thị chat
        self.chat_box = ctk.CTkTextbox(chat_frame, wrap="word", font=("Arial", 13))
        self.chat_box.pack(fill="both", expand=True)
        self.chat_box.configure(state="disabled")
        self.chat_box.tag_config("user", foreground="#1a73e8")
        self.chat_box.tag_config("ai", foreground="#2e7d32")

        # Khung nhập tin nhắn
        bottom = ctk.CTkFrame(self.root, corner_radius=15)
        bottom.pack(fill="x", padx=20, pady=15)

        self.entry = ctk.CTkTextbox(bottom, height=50, wrap="word")
        self.entry.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        self.entry.bind("<Control-Return>", self.send_message)

        # Nút micro 🎤
        self.mic_button = ctk.CTkButton(
            bottom,
            text="🎤",
            width=50,
            fg_color="#ff7043",
            command=self.start_voice_input
        )
        self.mic_button.pack(side="right", padx=5, pady=15)


        # Nút gửi
        ctk.CTkButton(bottom, text="Gửi (Ctrl+Enter)",
                    command=self.send_message).pack(side="right", padx=5, pady=15)


        # --- Giữ nút người dùng luôn ở góc phải khi resize ---
        def reposition_user_button(event=None):
            self.user_button.place(relx=1.0, x=-20, y=15, anchor="ne")

        self.root.bind("<Configure>", reposition_user_button)


    # ========== XỬ LÝ CHAT ==========
    def send_message(self, event=None):
        user_text = self.entry.get("1.0", "end").strip()
        if not user_text:
            return
        self.entry.delete("1.0", "end")

        self.chat_box.configure(state="normal")
        if self.chat_box.get("1.0", "end-1c").strip():
            self.chat_box.insert("end", f"\nBạn: {user_text}", "user")
        else:
            self.chat_box.insert("end", f"Bạn: {user_text}", "user")

        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

        threading.Thread(target=self.get_ai_response, args=(user_text,)).start()

    def get_ai_response(self, text):
            try:
                lower_text = text.lower().strip()

                # ===================================================================
                # 1. TRA SỐ ĐIỆN THOẠI PHỤ HUYNH – ƯU TIÊN CAO NHẤT
                # ===================================================================
                if any(k in lower_text for k in ["sđt", "sdt", "số điện thoại", "phụ huynh", "bố mẹ"]):
                    import re
                    class_match = re.search(r'lớp\s*([0-9]{1,2}[A-Za-z][0-9]?)', text, re.IGNORECASE)
                    name_match = re.search(r'(?:bố|mẹ|phụ huynh|của|học sinh)\s+([^\d]+?)(?=lớp|$)', text, re.IGNORECASE)
                    if not name_match:
                        name_match = re.search(r'^([A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ][^\d]+)', text)

                    student_name = name_match.group(1).strip().title() if name_match else None
                    student_class = class_match.group(1).upper().replace(" ", "") if class_match else None

                    if student_name and student_class:
                        phone = get_parent_phone(student_name, student_class)
                        ai_text = f"Số điện thoại phụ huynh của {student_name} lớp {student_class}:\n{phone}" if phone else f"Không tìm thấy số điện thoại phụ huynh của {student_name} lớp {student_class}."
                    else:
                        ai_text = "Vui lòng nhập đúng định dạng, ví dụ:\nSĐT phụ huynh Nguyễn Hoàng Bảo Anh lớp 11A1"

                    self.last_ai_text = ai_text
                    self.root.after(0, lambda: typewriter_effect(self.chat_box, ai_text, "ai", delay=15))
                    return

                # ===================================================================
                # 2. CHỈ GHI NHẬN VI PHẠM KHI: CÓ TÊN HOẶC "LỚP" + TỪ KHÓA VI PHẠM
                # → Tránh hiểu nhầm câu hỏi thành lệnh ghi vi phạm!
                # ===================================================================
                import re

                # Kiểm tra có chứa tên học sinh HOẶC cụm "lớp XX" không → mới coi là ghi nhận vi phạm
                has_name = bool(re.search(r'[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ]', text))
                has_class = bool(re.search(r'lớp\s*[0-9]{1,2}[A-Za-z][0-9]?', text, re.IGNORECASE))
                has_violation_keyword = any(k in lower_text for k in [
                    "vắng", "đồng phục", "hút thuốc", "đi học trễ", "đánh nhau", "điện thoại", "xả rác",
                    "trang điểm", "rượu bia", "phá hoại", "nói tục", "an ninh mạng", "không tắt", "lớp bẩn"
                ])

                # Chỉ xử lý vi phạm nếu: là cờ đỏ + có tên/lớp + có từ khóa vi phạm
                if is_codo(self.username) and (has_name or has_class) and has_violation_keyword:
                    result = self.handle_violation_record(text)
                    self.last_ai_text = result
                    self.root.after(0, lambda: typewriter_effect(self.chat_box, result, "ai"))
                    return

                # ===================================================================
                # 3. MỌI TRƯỜNG HỢP KHÁC → ĐỂ GEMINI TRẢ LỜI BÌNH THƯỜNG (QUAN TRỌNG NHẤT!)
                # ===================================================================
                response = chat.send_message(text)
                ai_text = response.text.strip()
                self.last_ai_text = ai_text
                self.root.after(0, lambda: typewriter_effect(self.chat_box, ai_text, "ai", delay=15))

            except Exception as e:
                error_msg = f"Đã xảy ra lỗi: {str(e)}"
                self.last_ai_text = error_msg
                self.root.after(0, lambda: typewriter_effect(self.chat_box, error_msg, "ai"))


    def clear_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.chat_box.configure(state="disabled")

    def save_chat(self):
        chat_history = self.chat_box.get("1.0", "end").strip()
        if not chat_history: return
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if f:
            with open(f, "w", encoding="utf-8") as file: file.write(chat_history)
            messagebox.showinfo("Lưu", f"Đã lưu vào {f}")

    def search_in_chat(self):
        kw = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa:")
        if not kw: return
        self.chat_box.tag_remove("highlight", "1.0", "end")
        i = "1.0"
        while True:
            i = self.chat_box.search(kw, i, nocase=1, stopindex="end")
            if not i: break
            end = f"{i}+{len(kw)}c"
            self.chat_box.tag_add("highlight", i, end)
            i = end
        self.chat_box.tag_config("highlight", background="yellow", foreground="black")

    # ========== MENU NGƯỜI DÙNG ==========
    def show_user_menu(self):
        menu = ctk.CTkToplevel(self.root)
        menu.title("Tài khoản")
        menu.geometry("250x200")
        ctk.CTkLabel(menu, text=f"Tài khoản: {self.username}", font=("Arial", 15, "bold")).pack(pady=15)
        ctk.CTkButton(menu, text="Đổi mật khẩu", width=150,
                      command=lambda:[menu.destroy(), self.show_change_password()]).pack(pady=8)
        ctk.CTkButton(menu, text="Đăng xuất", width=150, fg_color="#c62828",
                      hover_color="#8e0000", command=lambda:[menu.destroy(), self.username_logout()]).pack(pady=8)

    def show_change_password(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Đổi mật khẩu")
        win.geometry("400x300")

        ctk.CTkLabel(win, text="Đổi mật khẩu", font=("Arial", 20, "bold")).pack(pady=20)
        old_pw = ctk.CTkEntry(win, placeholder_text="Mật khẩu hiện tại", show="*")
        old_pw.pack(pady=10, padx=60, fill="x")
        new_pw = ctk.CTkEntry(win, placeholder_text="Mật khẩu mới", show="*")
        new_pw.pack(pady=10, padx=60, fill="x")
        cf_pw = ctk.CTkEntry(win, placeholder_text="Nhập lại mật khẩu mới", show="*")
        cf_pw.pack(pady=10, padx=60, fill="x")

        def confirm():
            users = load_users_from_sheet()
            if users[self.username] != hash_password(old_pw.get().strip()):
                return messagebox.showerror("Lỗi", "Mật khẩu hiện tại không đúng.")
            if new_pw.get().strip() != cf_pw.get().strip():
                return messagebox.showerror("Lỗi", "Mật khẩu mới không khớp.")
            update_password_in_sheet(self.username, new_pw.get().strip())
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
            win.destroy()

        ctk.CTkButton(win, text="Xác nhận", command=confirm).pack(pady=20)

    def username_logout(self):
        logout_user()
        self.username = None
        self.show_welcome_screen()

    def start_voice_input(self):
        if hasattr(self, "listening") and self.listening:
            # Nếu đang nghe → hủy
            self.listening = False
            self.mic_button.configure(text="🎤", fg_color="#ff7043")
            self.entry.delete("1.0", "end")
            self.entry.insert("end", "[Đã hủy ghi âm]")
            return

        # Bắt đầu ghi âm
        self.listening = True
        self.mic_button.configure(text="🟥 Đang nghe", fg_color="#d32f2f")
        threading.Thread(target=self._voice_to_text, daemon=True).start()

    def _voice_to_text(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        try:
            with mic as source:
                self.entry.delete("1.0", "end")
                self.entry.insert("end", "[Hãy nói vào micro...]")
                self.entry.update()
                recognizer.adjust_for_ambient_noise(source)

                # Nghe trong khi cờ listening = True
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)

            if not self.listening:
                return  # Nếu người dùng hủy giữa chừng thì thoát

            self.entry.delete("1.0", "end")
            self.entry.insert("end", "[Đang xử lý...]")
            self.entry.update()

            text = recognizer.recognize_google(audio, language="vi-VN")
            self.entry.delete("1.0", "end")
            self.entry.insert("end", text)

        except sr.WaitTimeoutError:
            self.entry.delete("1.0", "end")
            self.entry.insert("end", "")
            messagebox.showwarning("Hết thời gian", "Không phát hiện giọng nói.")
        except sr.UnknownValueError:
            self.entry.delete("1.0", "end")
            messagebox.showwarning("Không nhận diện được", "Không nghe rõ giọng nói, vui lòng thử lại.")
        except sr.RequestError:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến máy chủ nhận diện giọng nói.")
        finally:
            self.listening = False
            self.mic_button.configure(text="🎤", fg_color="#ff7043")
    def run(self): self.root.mainloop()

    def start_playback_for_text(self, text):
        """
        Bắt đầu quy trình: đổi nút -> tạo tệp TTS -> phát -> dọn dẹp.
        Chạy trong một thread để không block UI.
        """
        # Nếu không có nội dung
        if not text or text.strip() == "":
            messagebox.showinfo("Thông báo", "Chưa có nội dung AI để phát.")
            return

        # Nếu đang phát rồi thì ignore (hoặc dừng và sẽ chơi lại) - ở đây ta dừng trước
        if getattr(self, "playing_audio", False):
            # nếu đang phát, dừng trước
            self.stop_playback()
            return

        # cập nhật UI: chuyển sang "Đang xử lí âm thanh"
        try:
            self.speak_button_top.configure(text="Đang xử lí âm thanh", state="disabled")
        except Exception:
            pass

        def _worker(t):
            try:
                # sanitize text: loại ký tự * gây lỗi
                safe_text = t.replace("*", " ").strip()

                # tạo file tạm an toàn (không close rồi hệ điều hành xóa)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tmp_path = tmp.name
                tmp.close()

                # tạo tts
                tts = gTTS(text=safe_text, lang='vi')
                tts.save(tmp_path)

                # chuẩn bị playback: đặt trạng thái playing
                self.playing_audio = True
                self.current_audio_path = tmp_path

                # cập nhật UI: đã sẵn sàng -> cho phép dừng
                def set_to_stop():
                    try:
                        self.speak_button_top.configure(text="Dừng Nghe", state="normal",
                                                        command=self.stop_playback)
                    except Exception:
                        pass
                self.root.after(0, set_to_stop)

                # khởi tạo pygame mixer nếu chưa khởi
                try:
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                except Exception:
                    # try init anyway
                    pygame.mixer.init()

                # nếu đang có âm thanh đang chạy thì dừng
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                except Exception:
                    pass

                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()

                # đợi play xong hoặc user dừng (kiểm tra playing_audio)
                while getattr(self, "playing_audio", False) and pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                # nếu user dừng sớm, dừng music
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                except Exception:
                    pass

            except Exception as e:
                # hiển thị lỗi nhẹ
                print("[Lỗi play_ai_voice]:", e)
                self.root.after(0, lambda: messagebox.showerror("Lỗi phát âm thanh", str(e)))
            finally:
                # dọn dẹp file tạm
                try:
                    if hasattr(self, "current_audio_path") and os.path.exists(self.current_audio_path):
                        os.remove(self.current_audio_path)
                except Exception:
                    pass

                # reset trạng thái playing
                self.playing_audio = False
                self.current_audio_path = None

                # đưa nút về trạng thái ban đầu (khi hoàn tất)
                def reset_button():
                    try:
                        # khôi phục command và text
                        self.speak_button_top.configure(text="🔊 Nghe âm thanh", state="normal",
                                                        command=lambda: threading.Thread(target=self.start_playback_for_text, args=(getattr(self, "last_ai_text", ""),)).start())
                    except Exception:
                        pass
                self.root.after(0, reset_button)

        # start worker thread
        threading.Thread(target=_worker, args=(text,), daemon=True).start()


    def stop_playback(self):
        """Dừng phát âm thanh đang chạy (gọi từ nút Dừng Nghe)."""
        # đặt flag false để worker thoát vòng chờ
        self.playing_audio = False
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception:
            pass

        # cập nhật nút tức thì
        try:
            self.speak_button_top.configure(text="🔊 Nghe âm thanh", state="normal",
                                            command=lambda: threading.Thread(target=self.start_playback_for_text, args=(getattr(self, "last_ai_text", ""),)).start())
        except Exception:
            pass
    def handle_violation_record(self, raw_text):
        """Xử lý ghi nhận vi phạm (cá nhân + tập thể) – trả về nội dung phản hồi cho AI"""
        import re
        text = raw_text.strip()
        lower_text = text.lower()

        # === BƯỚC 1: Tìm lớp (bắt buộc) ===
        class_match = re.search(r'lớp\s*([0-9]{1,2}[A-Za-z]\d?)', text, re.IGNORECASE)
        if not class_match:
            return "Không tìm thấy thông tin lớp.\nVui lòng ghi rõ lớp bị vi phạm (ví dụ: lớp 11A1)."

        student_class = class_match.group(1).upper().replace(" ", "")

        # === BƯỚC 2: Xác định là vi phạm TẬP THỂ hay CÁ NHÂN ===
        collective_indicators = [
            "lớp bẩn", "bảng không lau", "rác trong hộc", "chổi sọt", "không tắt điện", "không tắt quạt",
            "không tắt máy chiếu", "không tổ chức sinh hoạt", "sinh hoạt 15 phút", "không sinh hoạt đầu giờ",
            "không tham gia chào cờ", "trễ chào cờ", "không dọn ghế", "cả lớp ra khỏi", "cả lớp cúp",
            "trực cổng không nghiêm", "không trực cổng", "không lao động", "lao động qua loa"
        ]

        is_collective = any(indicator in lower_text for indicator in collective_indicators)

        if is_collective:
            # ——————— VI PHẠM TẬP THỂ ———————
            desc = re.sub(r'lớp\s*' + re.escape(class_match.group(1)), '', text, flags=re.IGNORECASE)
            desc = re.sub(r'\s+', ' ', desc).strip()
            if desc.lower().startswith("lớp"):
                desc = desc[4:].strip()
            violation_desc = desc.capitalize() if desc else "Vi phạm nề nếp tập thể"

            # Ghi vào sheet
            record_violation(f"LỚP {student_class}", student_class, violation_desc)

            return (f"ĐÃ GHI NHẬN VI PHẠM TẬP THỂ\n\n"
                    f"Lớp: {student_class}\n"
                    f"Lỗi: {violation_desc}\n"
                    f"Cờ đỏ: {self.username}\n\n"
                    f"Đã cập nhật bảng theo dõi nề nếp.")

        else:
            # ——————— VI PHẠM CÁ NHÂN ———————
            # Bắt tên học sinh (rất linh hoạt)
            name_pattern = re.compile(
                r'(?:bạn|học sinh)?\s*([A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ][^,.\d]*?)\s*(?=lớp|hút|trễ|đồng|vắng|cúp|đánh|điện|trang|xả|rượu|phá|nói|đeo|không|ra|đi|để|vi|đăng|quay|chia|an)',
                re.IGNORECASE
            )
            name_match = name_pattern.search(text)

            if not name_match:
                return "Không nhận diện được tên học sinh.\nVí dụ đúng:\n• Nguyễn Văn Nam lớp 11A1 hút thuốc\n• Bảo Anh 10A3 đi trễ"

            full_name = name_match.group(1).strip()
            # Chuẩn hóa tên (viết hoa chữ cái đầu mỗi từ)
            full_name = re.sub(r'\b\w', lambda m: m.group().upper(), full_name)

            # Loại bỏ tên + lớp ra khỏi câu để lấy mô tả vi phạm
            desc = re.sub(re.escape(full_name), '', text, flags=re.IGNORECASE)
            desc = re.sub(r'lớp\s*' + re.escape(class_match.group(1)), '', desc, flags=re.IGNORECASE)
            desc = re.sub(r'bạn|học sinh|\s+', ' ', desc).strip()
            violation_desc = desc.capitalize() if desc else "Vi phạm nề nếp"

            # Ghi vào sheet
            record_violation(full_name, student_class, violation_desc)

            return (f"ĐÃ GHI NHẬN VI PHẠM CÁ NHÂN\n\n"
                    f"Học sinh: {full_name}\n"
                    f"Lớp: {student_class}\n"
                    f"Lỗi: {violation_desc}\n"
                    f"Cờ đỏ: {self.username}\n\n"
                    f"Đã cập nhật bảng theo dõi nề nếp.")


# ====================== VI PHẠM NỀ NẾP - TỰ ĐỘNG GHI SHEET2 ======================
def init_violation_sheet():
    """Khởi tạo sheet vi phạm (Sheet2)"""
    global violation_sheet
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        SERVICE_FILE = os.path.join(BASE_DIR, "service_account.json")

        creds = Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key("1tLPU-SIjSQ8KOuVodsw79aZ3MPpd6jgXl9HSkm_8XZE")
        violation_sheet = spreadsheet.worksheet("codo")  # Tên sheet của bạn
        return violation_sheet
    except Exception as e:
        print(f"[Lỗi khởi tạo Sheet vi phạm]: {e}")
        return None

# Khởi tạo ngay khi chạy chương trình
violation_sheet = init_violation_sheet()
# ====================== PHÂN QUYỀN CỜ ĐỎ TỰ ĐỘNG (KHÔNG CẦN SHEET) ======================
import re

def is_codo(username):
    """
    Kiểm tra username có phải cờ đỏ không
    Quy tắc: bắt đầu bằng 'codo' + 2 số lớp (10/11/12) + a + 1 số (1-9)
    Ví dụ: codo10a1, codo11a5, codo12a9 → True
    """
    if not username:
        return False
    username = str(username).strip().lower()
    pattern = r'^codo(10|11|12)a[1-9]$'    # chính xác 100% theo quy ước của bạn
    return bool(re.match(pattern, username))
# Danh sách lỗi và dòng tương ứng trong Sheet (cực kỳ quan trọng!)
VIOLATION_MAPPING = {
    # Dòng 2-10
    "vắng có phép": 2,
    "vắng không phép": 3,
    "đồng phục": 4,
    "cúp tiết": 5,
    "đi học trễ": 6,
    "điện thoại": 7,
    "lớp học để bẩn": 8,
    "bảng không lau": 8,
    "rác trong hộc bàn": 8,
    "chổi sọt để sai": 8,
    "không mang bảng tên": 9,
    "huy hiệu đoàn": 9,

    # Dòng 10-19
    "uống rượu": 10,
    "hút thuốc": 10,
    "rượu bia": 10,
    "chất kích thích": 10,
    "trang điểm": 11,
    "sơn móng tay": 11,
    "nhuộm tóc": 11,
    "đeo hoa tai": 12,
    "đánh nhau": 14,
    "quay clip": 14,
    "tung lên mạng": 14,
    "không tắt điện": 15,
    "không tắt quạt": 15,
    "không tắt máy chiếu": 15,
    "vũ khí": 16,
    "chất dễ cháy": 16,
    "chất nổ": 16,
    "phá hoại": 17,
    "bẻ cây": 17,
    "vẽ bậy": 17,
    "làm hư bàn ghế": 17,
    "xả rác": 18,
    "mang rác nhựa": 18,

    # Dòng 19-27
    "không tham gia ngll": 19,
    "không học ngll": 19,
    "ngoại khóa": 19,
    "thể dục": 19,
    "hướng nghiệp": 19,
    "không tổ chức sinh hoạt": 20,
    "sinh hoạt 15 phút": 20,
    "sinh hoạt sai chủ đề": 20,
    "chào cờ": 21,
    "trễ chào cờ": 21,
    "không chuẩn bị chào cờ": 21,
    "không dọn ghế": 21,
    "ra khỏi trường không phép": 22,
    "cúp tiết": 22,          # trùng dòng 5 nhưng cúp cả lớp thì nặng hơn
    "không nghiêm túc": 23,
    "bị nhắc nhở": 23,
    "thiếu lễ phép": 24,
    "xúc phạm": 25,
    "nói tục": 26,
    "chửi bậy": 26,
    "gây mất đoàn kết": 26,
    "lôi kéo bè phái": 26,
    "an ninh mạng": 27,
    "đăng tải video": 27,
    "chia sẻ nội dung không lành mạnh": 27,
}

def record_violation(full_student_name, student_class, violation_text):
    """Ghi nhận vi phạm vào Sheet2 - ghi đầy đủ họ tên"""
    global violation_sheet
    if not violation_sheet:
        return "Lỗi: Không kết nối được Sheet vi phạm."

    try:
        # Xác định cột của lớp
        headers = violation_sheet.row_values(1)
        class_col = None
        for idx, h in enumerate(headers):
            if h.strip().upper() == student_class.upper():
                class_col = idx + 1
                break
        if not class_col:
            return f"Không tìm thấy cột lớp {student_class}"

        # Tìm dòng lỗi phù hợp
        violation_row = None
        lower_violation = violation_text.lower()
        for keyword, row in VIOLATION_MAPPING.items():
            if keyword in lower_violation:
                violation_row = row
                break

        if not violation_row:
            violation_row = 10  # mặc định dòng hút thuốc/rượu bia nếu không rõ

        # Tăng số lượng vi phạm
        current_val = violation_sheet.cell(violation_row, class_col).value or "0"
        new_val = int(float(current_val)) + 1
        violation_sheet.update_cell(violation_row, class_col, new_val)

        # GHI CHI TIẾT VÀO DÒNG 32: DÙNG HỌ TÊN ĐẦY ĐỦ
        detail_row = 32
        current_details = violation_sheet.cell(detail_row, class_col).value or ""
        today = datetime.now().strftime("%d/%m")

        # Tạo dòng ghi chi tiết mới - dùng tên đầy đủ
        new_detail = f"{full_student_name.strip()} {violation_text.strip()} - {today}"

        # Nếu đã có nội dung cũ thì xuống dòng
        updated_details = current_details + ("\n" if current_details else "") + new_detail
        violation_sheet.update_cell(detail_row, class_col, updated_details)

        return f"Đã ghi nhận vi phạm của {full_student_name} lớp {student_class}: {violation_text}"
    except Exception as e:
        print(f"[Lỗi ghi vi phạm]: {e}")
        return "Có lỗi khi ghi nhận vi phạm."

# ========== CHẠY ỨNG DỤNG ==========
if __name__ == "__main__":
    app = MDCGPTApp()
    app.run()
