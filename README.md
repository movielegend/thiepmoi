# THE GOLDEN — Thiệp Mời Year End Party 2026

Website thiệp mời điện tử sang trọng dành cho sự kiện **THE GOLDEN — Year End Party 2026**. Tối ưu hoàn hảo cho cả trình duyệt điện thoại di động (iOS / Android) và máy tính để bàn. Tích hợp tính năng gửi email xác nhận tham dự tự động kèm hình ảnh thiệp mời qua giao thức SMTP.

---

## 📌 Thông tin sự kiện
* **Thời gian:** 14H ngày 10 tháng 11 năm 2026
* **Địa điểm:** Trường Đại học Thăng Long
* **Trang phục gợi ý:** Đen & vàng champagne sang trọng

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Chuẩn bị môi trường
Yêu cầu máy tính đã cài đặt Python 3.6 trở lên.

Cài đặt thư viện tạo mã QR (nếu cần tạo lại QR):
```bash
python3 -m pip install "qrcode[pil]"
```

### 2. Cấu hình gửi Email (SMTP)
Sao chép tệp mẫu `email_config.json.example` thành `email_config.json`:
```bash
cp email_config.json.example email_config.json
```

Mở `email_config.json` và điền thông tin tài khoản Gmail của Ban Tổ Chức:
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "email-cua-ban@gmail.com",
  "smtp_password": "xxxx xxxx xxxx xxxx",
  "from_name": "THE GOLDEN — Ban Tổ Chức"
}
```
> **Lưu ý:** `smtp_password` là **Mật khẩu ứng dụng (App Password)** gồm 16 ký tự được tạo từ [Google Account Security](https://myaccount.google.com/apppasswords), không phải mật khẩu đăng nhập Gmail thông thường.

### 3. Khởi chạy máy chủ
Chạy lệnh sau trong thư mục dự án:
```bash
python3 server.py
```
* **Mở trên máy tính:** Truy cập [http://localhost:8080](http://localhost:8080)
* **Mở trên điện thoại di động:** Truy cập theo địa chỉ IP mạng nội bộ (Wi-Fi), ví dụ: `http://192.168.1.xxx:8080` hoặc quét mã QR trong file `invite.png`.

---

## 📁 Cấu trúc thư mục

* `index.html`: Giao diện thiệp mời điện tử đơn trang, form RSVP xác nhận tham dự và modal thông báo.
* `style.css`: Bộ phong cách thiết kế sang trọng với font chữ `Playfair Display`, `Montserrat` và `Lora`. Tối ưu responsive toàn diện cho mobile (tai thỏ, Dynamic Island, Home indicator).
* `app.js`: Xử lý logic giao diện, chuyển đổi trạng thái nút bấm động theo phản hồi tham dự, gọi API gửi email và hiển thị popup.
* `server.py`: Máy chủ HTTP phục vụ file tĩnh và xử lý `POST /api/send-email` gửi email HTML kèm ảnh thiệp mời qua Gmail SMTP.
* `email_config.json.example`: Tệp cấu hình SMTP mẫu an toàn để đẩy lên kho mã nguồn.
* `gala.webp`: Hình ảnh thiệp mời đính kèm trong email xác nhận.
* `thiep-moi-the-golden.png`: Ảnh thiệp mời điện tử hoàng gia độ phân giải cao kèm mã QR quét mở trang.
* `invite.png`: Mã QR truy cập thiệp mời trực tuyến.
* `create_invitation_card.py`: Script Python thiết kế và xuất file ảnh thiệp mời đồ họa cao cấp.
* `generate_qr.py`: Script Python để tạo lại mã QR khi thay đổi IP hoặc tên miền.

---

## 🔒 Bảo mật
* Tệp `email_config.json` và thư mục `sent_emails/` đã được khai báo trong `.gitignore` để tránh rò rỉ thông tin mật khẩu và dữ liệu khách mời lên GitHub.
