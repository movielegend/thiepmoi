import qrcode
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# URL đích chính thức trên GitHub Pages
TARGET_URL = "https://movielegend.github.io/thiepmoi/"

# Kích thước thiệp mời chuẩn sang trọng (1080 x 1620 px - tỉ lệ 2:3 hoàn hảo cho Story, Post và in ấn)
WIDTH = 1080
HEIGHT = 1620

# Tạo nền thiệp: Nền gradient tối sang trọng #131411 -> #1a1b16
card = Image.new("RGBA", (WIDTH, HEIGHT), (19, 20, 17, 255))
draw = ImageDraw.Draw(card)

# Tạo hiệu ứng chuyển sắc tinh tế (subtle radial/linear luxury dark glow)
for i in range(HEIGHT):
    # nhẹ nhàng tăng sắc độ ở giữa
    factor = 1.0 - (abs(i - HEIGHT // 2) / (HEIGHT // 2)) * 0.25
    r = int(18 * factor + 5)
    g = int(19 * factor + 5)
    b = int(16 * factor + 5)
    draw.line([(0, i), (WIDTH, i)], fill=(r, g, b, 255))

# Palette màu vàng kim champagne
GOLD_PRIMARY = (213, 183, 121, 255)   # #d5b779
GOLD_LIGHT = (244, 230, 196, 255)     # #f4e6c4
GOLD_DARK = (163, 133, 76, 255)       # #a3854c
TEXT_WHITE = (255, 255, 255, 255)
TEXT_MUTED = (185, 180, 168, 255)
BOX_BG = (26, 27, 23, 255)

# 1. Vẽ khung viền kép hoàng gia (Double luxury gold borders)
margin_outer = 40
draw.rectangle(
    [margin_outer, margin_outer, WIDTH - margin_outer, HEIGHT - margin_outer],
    outline=GOLD_DARK,
    width=2
)

margin_inner = 60
draw.rectangle(
    [margin_inner, margin_inner, WIDTH - margin_inner, HEIGHT - margin_inner],
    outline=GOLD_PRIMARY,
    width=3
)

# Họa tiết 4 góc nghệ thuật
corner_len = 36
for cx, cy, x_dir, y_dir in [
    (margin_inner, margin_inner, 1, 1),
    (WIDTH - margin_inner, margin_inner, -1, 1),
    (margin_inner, HEIGHT - margin_inner, 1, -1),
    (WIDTH - margin_inner, HEIGHT - margin_inner, -1, -1)
]:
    draw.line([(cx, cy + y_dir * 14), (cx + x_dir * corner_len, cy + y_dir * 14)], fill=GOLD_LIGHT, width=2)
    draw.line([(cx + x_dir * 14, cy), (cx + x_dir * 14, cy + y_dir * corner_len)], fill=GOLD_LIGHT, width=2)
    # Kim cương nhỏ ở góc
    draw.polygon([
        (cx + x_dir * 9, cy + y_dir * 5),
        (cx + x_dir * 13, cy + y_dir * 9),
        (cx + x_dir * 9, cy + y_dir * 13),
        (cx + x_dir * 5, cy + y_dir * 9)
    ], fill=GOLD_LIGHT)

# Load fonts hệ thống
font_georgia_bold = lambda sz: ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", sz)
font_georgia = lambda sz: ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", sz)
font_georgia_italic = lambda sz: ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", sz)
font_arial = lambda sz: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", sz)
font_arial_bold = lambda sz: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", sz)

def draw_centered_text(y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])

# Header & Tiêu đề
y = 110
y = draw_centered_text(y, "T R Â N   T R Ọ N G   K Í N H   M Ờ I", font_arial_bold(18), GOLD_PRIMARY) + 22

# Đường kẻ phân cách vàng hoa văn
line_w = 200
draw.line([(WIDTH//2 - line_w//2, y), (WIDTH//2 + line_w//2, y)], fill=GOLD_DARK, width=1)
draw.polygon([(WIDTH//2 - 5, y - 5), (WIDTH//2 + 5, y - 5), (WIDTH//2, y + 5)], fill=GOLD_LIGHT)
y += 32

y = draw_centered_text(y, "THE GOLDEN", font_georgia_bold(66), GOLD_LIGHT) + 12
y = draw_centered_text(y, "Y E A R   E N D   P A R T Y   2 0 2 6", font_arial_bold(22), GOLD_PRIMARY) + 18
y = draw_centered_text(y, "Một hành trình — Ngàn khoảnh khắc", font_georgia_italic(26), TEXT_MUTED) + 45

# 2. Khung thông tin sự kiện trang trọng (Thời gian, Địa điểm, Dresscode)
info_box_w = WIDTH - margin_inner * 2 - 90
info_box_h = 280
info_box_x = (WIDTH - info_box_w) // 2
info_box_y = y

draw.rounded_rectangle(
    [info_box_x, info_box_y, info_box_x + info_box_w, info_box_y + info_box_h],
    radius=14,
    fill=BOX_BG,
    outline=GOLD_PRIMARY,
    width=2
)

# Nội dung bên trong khung thông tin
info_y = info_box_y + 26

def draw_info_row(iy, label, val):
    lbl_font = font_arial_bold(13)
    val_font = font_georgia_bold(22)
    
    # Label
    bbox_lbl = draw.textbbox((0, 0), label, font=lbl_font)
    draw.text(((WIDTH - (bbox_lbl[2] - bbox_lbl[0])) // 2, iy), label, font=lbl_font, fill=GOLD_PRIMARY)
    iy += 22
    
    # Value
    bbox_val = draw.textbbox((0, 0), val, font=val_font)
    draw.text(((WIDTH - (bbox_val[2] - bbox_val[0])) // 2, iy), val, font=val_font, fill=TEXT_WHITE)
    return iy + 44

info_y = draw_info_row(info_y, "T H Ờ I   G I A N", "14H00 — Ngày 10 tháng 11 năm 2026")
info_y = draw_info_row(info_y, "Đ Ị A   Đ I Ể M", "Trường Đại học Thăng Long")
info_y = draw_info_row(info_y, "T R A N G   P H Ụ C   G Ợ I   Ý", "Đen & Vàng Champagne sang trọng")

y = info_box_y + info_box_h + 50

# 3. Tạo mã QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(TARGET_URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#121310", back_color="#ffffff").convert("RGBA")

# Resize QR Code (350x350 px)
qr_size = 350
qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

# Khung chứa QR màu trắng viền vàng
qr_box_padding = 22
qr_box_w = qr_size + qr_box_padding * 2
qr_box_h = qr_size + qr_box_padding * 2
qr_box_x = (WIDTH - qr_box_w) // 2
qr_box_y = y

draw.rounded_rectangle(
    [qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h],
    radius=18,
    fill=(255, 255, 255, 255),
    outline=GOLD_PRIMARY,
    width=3
)

card.paste(qr_img, (qr_box_x + qr_box_padding, qr_box_y + qr_box_padding), qr_img)

y = qr_box_y + qr_box_h + 24
y = draw_centered_text(y, "QUÉT MÃ ĐỂ MỞ THIỆP & XÁC NHẬN THAM DỰ", font_arial_bold(18), GOLD_LIGHT) + 8
y = draw_centered_text(y, "movielegend.github.io/thiepmoi", font_arial(14), TEXT_MUTED) + 30

# Footer
footer_y = HEIGHT - margin_inner - 80
draw_centered_text(footer_y, "BAN TỔ CHỨC", font_arial_bold(13), TEXT_MUTED)
draw_centered_text(footer_y + 24, "CÔNG TY TNHH THE GOLDEN", font_georgia_bold(19), GOLD_PRIMARY)

# Lưu ảnh chất lượng cao
output_path = Path(__file__).resolve().parent / "thiep-moi-the-golden.png"
card.convert("RGB").save(output_path, "PNG", quality=95)
print("Đã tạo thành công thiệp mời:", output_path)

# Tạo luôn phiên bản invite.png cập nhật URL mới
invite_qr = qrcode.QRCode(box_size=12, border=4, error_correction=qrcode.constants.ERROR_CORRECT_M)
invite_qr.add_data(TARGET_URL)
invite_qr.make(fit=True)
invite_qr.make_image(fill_color="black", back_color="white").save(Path(__file__).resolve().parent / "invite.png")
print("Đã cập nhật invite.png trỏ đến:", TARGET_URL)
