import qrcode
import uuid
import pandas as pd

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


if __name__ ==  '__main__':
    
    myList = pd.read_csv('TestNumbers.csv')
    print(myList.shape)
    
    print(myList.head())
    
    #1. Create QR Code
    myText = myList.iloc[0,0]
    create_qr_code(myText)
    
    #2. Removed used QR Code Value from CSV
    myList = myList.iloc[1:]
    myList.to_csv('TestNumbers.csv', index=False)
        
    print("Complete! Your QR-Code is in the generated_qr_codes folder.")