"""Tạo lại QR cho tên miền mới. Chạy: python generate_qr.py https://example.com"""
import sys
from pathlib import Path
from urllib.parse import urlsplit
import qrcode

if len(sys.argv) != 2:
    raise SystemExit('Cách chạy: python generate_qr.py https://ten-mien-cua-ban.vn')
base = sys.argv[1].rstrip('/')
parsed = urlsplit(base)
if parsed.scheme not in ('https', 'http') or not parsed.netloc or parsed.query or parsed.fragment:
    raise SystemExit('Nhập URL http/https hợp lệ, không có query hoặc fragment.')
folder = Path(__file__).resolve().parent
codes = ['DEMO-001', 'DEMO-002', 'DEMO-003']
links = {'invite': base + '/?view=invite'}
links.update({code: base + '/?view=checkin&code=' + code for code in codes})
for name, url in links.items():
    qr = qrcode.QRCode(box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(folder / (name + '.png'))
    print(name + '.png -> ' + url)
