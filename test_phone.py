import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("models/teacher/best.pt")

# Stream from phone camera
url = "http://192.168.0.149:8080/video"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("❌ Could not open video stream.")
    exit()

print("📹 Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame")
        break

    # Run YOLO inference
    results = model(frame, conf=0.7, iou=0.45)

    # YOLO returns a list, take first result
    r = results[0]

    # Draw detections on frame
    annotated_frame = r.plot()

    # Display output
    cv2.imshow("YOLO Live", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
