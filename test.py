import cv2
import detector
print(cv2.__version__)

output_directory = "webcam_slides"

my_detector = detector.Detector(device=0, outpath=output_directory)
print("webcam")

my_detector.cap.release()