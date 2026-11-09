#!/usr/bin/env python3
"""
THE GOLDEN — Web Server with Confirmation Email Support.
Serves static files and handles POST /api/send-email.
"""
import os
import sys
import json
import smtplib
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

PORT = 8080
BASE_DIR = Path(__file__).resolve().parent
SENT_EMAILS_DIR = BASE_DIR / "sent_emails"
SENT_EMAILS_DIR.mkdir(exist_ok=True)
CONFIG_FILE = BASE_DIR / "email_config.json"

def load_email_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Lỗi đọc email_config.json:", e)
    return {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", 587)),
        "smtp_user": os.getenv("SMTP_USER", ""),
        "smtp_password": os.getenv("SMTP_PASSWORD", ""),
        "from_name": os.getenv("FROM_NAME", "THE GOLDEN — Ban Tổ Chức")
    }

def build_html_email(name, phone, department, note):
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin: 0; padding: 0; background-color: #11120f; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #f4f0e6; }}
    .email-container {{ max-width: 600px; margin: 30px auto; background-color: #1a1b16; border-radius: 12px; border: 1px solid #d5b779; overflow: hidden; }}
    .header {{ background: linear-gradient(135deg, #2b2516, #161713); padding: 35px 30px; text-align: center; border-bottom: 1px solid rgba(213, 183, 121, 0.4); }}
    .brand {{ font-size: 24px; letter-spacing: 5px; font-weight: bold; color: #ffffff; margin: 0; font-family: Georgia, serif; }}
    .brand-sub {{ font-size: 9px; letter-spacing: 3px; color: #d5b779; margin-top: 6px; text-transform: uppercase; }}
    .content {{ padding: 35px 30px; line-height: 1.7; font-size: 15px; color: #e8e2d4; }}
    .greeting {{ font-size: 18px; font-weight: bold; color: #d5b779; margin-bottom: 16px; font-family: Georgia, serif; }}
    .card-info {{ background: #24251e; border: 1px solid rgba(213, 183, 121, 0.3); border-radius: 8px; padding: 22px; margin: 25px 0; }}
    .info-row {{ margin-bottom: 14px; }}
    .info-row:last-child {{ margin-bottom: 0; }}
    .info-label {{ font-size: 11px; letter-spacing: 1.5px; color: #d5b779; font-weight: bold; text-transform: uppercase; margin-bottom: 3px; }}
    .info-value {{ font-size: 16px; font-weight: bold; color: #ffffff; font-family: Georgia, serif; }}
    .invitation-image {{ margin: 25px 0; text-align: center; }}
    .invitation-image img {{ max-width: 100%; border-radius: 8px; border: 1px solid rgba(213, 183, 121, 0.5); }}
    .footer {{ background-color: #12130e; padding: 25px; text-align: center; font-size: 12px; color: #8c897e; border-top: 1px solid rgba(255, 255, 255, 0.08); }}
    .footer strong {{ color: #d5b779; letter-spacing: 2px; }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <div class="brand">THE GOLDEN</div>
      <div class="brand-sub">YEAR END PARTY 2026</div>
    </div>
    <div class="content">
      <div class="greeting">Kính gửi {name},</div>
      <p>Ban tổ chức trân trọng cảm ơn bạn đã xác nhận tham dự đêm tiệc <strong>THE GOLDEN · Year End Party 2026</strong>. Sự hiện diện của bạn là niềm vinh hạnh to lớn và sẽ góp phần tạo nên một đêm tiệc trọn vẹn, đáng nhớ!</p>
      
      <div class="card-info">
        <div class="info-row">
          <div class="info-label">Thời gian</div>
          <div class="info-value">14H ngày 10 tháng 11 năm 2026</div>
        </div>
        <div class="info-row">
          <div class="info-label">Địa điểm</div>
          <div class="info-value">Trường Đại học Thăng Long</div>
        </div>
        <div class="info-row">
          <div class="info-label">Trang phục gợi ý</div>
          <div class="info-value">Đen &amp; vàng champagne</div>
        </div>
        {f'<div class="info-row"><div class="info-label">Phòng ban</div><div class="info-value">{department}</div></div>' if department else ''}
      </div>

      <div class="invitation-image">
        <img src="cid:invitation_cup" alt="Tấm thiệp mời THE GOLDEN">
      </div>

      <p>Mong sớm được đón tiếp bạn tại buổi tiệc!</p>
      <p style="margin-top: 25px;">Trân trọng,<br><strong>Ban tổ chức THE GOLDEN</strong></p>
    </div>
    <div class="footer">
      <strong>THE GOLDEN</strong> · Nhìn lại hành trình. Gắn kết để vươn xa.<br>
      <small style="margin-top: 5px; display: block;">Email này được gửi tự động để xác nhận đăng ký tham dự Year End Party 2026.</small>
    </div>
  </div>
</body>
</html>"""

def send_real_email(to_email, name, phone, department, note, config):
    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = f"[THE GOLDEN] Xác nhận tham dự Year End Party 2026 — {name}"
        msg["From"] = f'{config["from_name"]} <{config["smtp_user"]}>'
        msg["To"] = to_email

        html_content = build_html_email(name, phone, department, note)
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(html_content, "html", "utf-8"))

        # Đính kèm ảnh thiệp mời chính thức hoặc gala.webp dưới dạng CID để hiển thị trực tiếp trong thư
        card_path = BASE_DIR / "thiep-moi-the-golden.png"
        gala_path = BASE_DIR / "gala.webp"
        attach_path = card_path if card_path.exists() else gala_path
        if attach_path.exists():
            with open(attach_path, "rb") as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header("Content-ID", "<invitation_cup>")
            img.add_header("Content-Disposition", "inline", filename=attach_path.name)
            msg.attach(img)

        # Gửi qua SMTP
        server = smtplib.SMTP(config["smtp_server"], int(config["smtp_port"]))
        server.ehlo()
        server.starttls()
        user = str(config["smtp_user"]).strip()
        pwd = str(config["smtp_password"]).replace(" ", "").strip()
        server.login(user, pwd)
        server.sendmail(user, [to_email], msg.as_string())
        server.quit()
        print(f"Đã gửi email thực tế đến {to_email}")
        return True, "Email đã được gửi thành công đến hộp thư của bạn."
    except Exception as e:
        print(f"Lỗi gửi email qua SMTP: {e}")
        return False, str(e)

class GoldenServerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/send-email":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
            except Exception:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            name = data.get("name", "")
            email = data.get("email", "")
            phone = data.get("phone", "")
            department = data.get("department", "")
            note = data.get("note", "")
            attend = data.get("attend", "yes")

            config = load_email_config()
            is_smtp_ready = bool(config.get("smtp_user") and config.get("smtp_password"))
            email_sent = False
            msg_text = ""

            # Chỉ gửi khi chọn tham dự và có email
            if attend == "yes" and email:
                if is_smtp_ready:
                    ok, msg_text = send_real_email(email, name, phone, department, note, config)
                    email_sent = ok
                else:
                    msg_text = "Hệ thống đã chuẩn bị email xác nhận hoàn chỉnh."

                # Lưu bản ghi email vào thư mục sent_emails
                timestamp = int(os.times().system * 1000)
                safe_name = "".join(c for c in name if c.isalnum() or c in " _-") or "guest"
                filename = SENT_EMAILS_DIR / f"{safe_name}_{email}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(build_html_email(name, phone, department, note))

            response_data = {
                "success": True,
                "emailSent": email_sent,
                "smtpConfigured": is_smtp_ready,
                "message": msg_text,
                "data": {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "attend": attend
                }
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
            return

        return super().do_POST()

def run():
    os.chdir(BASE_DIR)
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, GoldenServerHandler)
    print(f"THE GOLDEN Server đang chạy tại http://0.0.0.0:{PORT} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDừng server.")
        httpd.server_close()

if __name__ == "__main__":
    run()
