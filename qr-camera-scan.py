import cv2
from pyzbar.pyzbar import decode

# Initialize the camera
cap = cv2.VideoCapture(0)  # '0' is usually the default value for the primary camera

x = None  # This will hold the data from the QR code

# Keep looking for QR codes until one is found
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Decode QR codes in the frame
    decoded_objects = decode(frame)

    for obj in decoded_objects:
        # Store the decoded data in x
        x = obj.data.decode()
        print("QR Code detected! It says: ", x)
        cv2.putText(frame, x, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        break  # Break out of the loop after storing the data

    if x is not None:
        # If x has data, break the loop
        break

    # Display the resulting frame
    cv2.imshow('QR Code Scanner', frame)

    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

# You can use x here for further processing
print("The url stored in the QR-Code is: ", x)
