import qrcode
import uuid

### 1. setup ###
generate_uuid = str(uuid.uuid4())
# The URL you want to encode
url = 'http://127.0.0.1:5000/cylinder_info/5C-9839826c-1816-44ef-ab97-c91c5bb47c53'
#or
unique_token = generate_uuid  #using this right now not url variable



### 2. generate QR code ###
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
img.save("generated_qr_codes/NEW_QR_CODE.png")
