from ultralytics import YOLO

model=YOLO("yolov8m.pt")
results = model.train(data='data.yaml', epochs=100, imgsz=640)