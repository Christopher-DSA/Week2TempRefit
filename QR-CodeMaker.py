import qrcode
import uuid

def create_qr_code(y):
    # Creating the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Adding the URL to the QR code
    qr.add_data(y)
    qr.make(fit=True)

    # Creating an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Saving the image
    file_name = 'qr-'+y+'.png'
    route = 'generated_qr_codes/'+file_name
    img.save(route)


#Always choose option 2 unless you have a special use case.
if __name__ ==  '__main__':
    Choice = input("\nCustom Data or Unique Token?(1 or 2)[if unsure, choose 2]: ")
    print(Choice)
    
    if Choice == '1':
        create_qr_code(Choice)
    elif Choice == '2':
        generate_uuid = str(uuid.uuid4())
        unique_token = generate_uuid
        create_qr_code(unique_token)
        print("Complete! Your file is in the generated_qr_codes folder.")
    else:   
        print("Invalid Choice")
        exit()