import qrcode

url = "https://arirodriguez001.github.io/rafa-qr/"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_rafa_2026.png")
print(f"QR generado para: {url}")
