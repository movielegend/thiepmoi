"""Tạo lại QR cho tên miền mới. Chạy: python generate_qr.py https://movielegend.github.io/thiepmoi/"""
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
import qrcode

base = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'https://movielegend.github.io/thiepmoi'
parsed = urlsplit(base)
if parsed.scheme not in ('https', 'http') or not parsed.netloc:
    raise SystemExit('Nhập URL http/https hợp lệ, không có query hoặc fragment.')

folder = Path(__file__).resolve().parent
links = {'invite': base}
for name, url in links.items():
    qr = qrcode.QRCode(box_size=12, border=4, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(folder / (name + '.png'))
    print(name + '.png -> ' + url)

# Gọi tạo lại thiệp mời chính thức
card_script = folder / 'create_invitation_card.py'
if card_script.exists():
    subprocess.run([sys.executable, str(card_script)], check=False)
