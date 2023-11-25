import qrcode

# The URL you want to encode
url = 'http://127.0.0.1:5000/cylinder_info/28C-d2ae1dd5-196d-48b4-87ea-69474caaca72'

# Creating the QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Adding the URL to the QR code
qr.add_data(url)
qr.make(fit=True)

# Creating an image from the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Saving the image
img.save("generated_qr_codes/cylinder_tag.png")
