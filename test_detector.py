import detector

output_directory = "webcam_slides"

my_detector = detector.Detector(device=0, outpath=output_directory)

print("webcam initialized successfully!")

my_detector.cap.release()