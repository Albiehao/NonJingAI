from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8n.pt")

def detect(image_np):
    results = model(image_np)

    output = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = model.names[cls]

            output.append({
                "class": name,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })

    return output