import qrcode
import uuid
import pandas as pd


def create_qr_code(y, index):
    # Creating the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Adding the data to the QR code
    qr.add_data(y)
    qr.make(fit=True)

    # Creating an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Saving the image with a unique file name using the index
    file_name = f'qr-{index}-{y}.png'
    route = f'generated_qr_codes/{file_name}'
    img.save(route)


if __name__ == '__main__':

    myList = pd.read_csv('TestNumbers.csv')
    print(myList.shape)

    print(myList.head())

    # Generate QR codes for the first 10 rows
    for i in range(min(10, len(myList))):
        myText = myList.iloc[i, 0]
        create_qr_code(myText, i)

    # Remove the used rows from the CSV after generating QR Codes
    myList = myList.iloc[10:] if len(myList) >= 10 else pd.DataFrame()
    myList.to_csv('TestNumbers.csv', index=False)

    print("Complete! Your QR-Codes are in the generated_qr_codes folder.")
