import cv2

device_id = 0 # Replace with your webcam's device ID if needed 
cap = cv2.VideoCapture(device_id)

if not cap.isOpened(): 
    print("Error: Unable to open webcam") 
    exit()

ret, frame = cap.read()

if not ret: 
    print("Error: Unable to read frame from webcam") 
    cap.release() 
    exit()

cv2.imshow("Webcam Test", frame) # Display the frame in a window 
cv2.waitKey(0) # Wait for a keypress 
cap.release() 
cv2.destroyAllWindows()