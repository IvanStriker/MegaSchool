from ultralytics import YOLO
import cv2
import supervision as sv

# Загрузка модели
model = YOLO('runs/detect/train/weights/best.pt')

# Загрузка изображения
image = cv2.imread("53.png")

# Выполнение детекции
results = model(image)[0]

# Вариант 1: Использовать правильный метод преобразования
detections = sv.Detections.from_ultralytics(results)

# Обработка обнаружений - detections теперь объект Detections, а не кортеж
for i in range(len(detections.xyxy)):
    bbox = detections.xyxy[i]  # Координаты bounding box
    confidence = detections.confidence[i]
    class_id = detections.class_id[i]

    # Рисуем bounding box
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Добавляем текстовую метку
    cv2.putText(image, f'{class_id}: {confidence:.2f}',
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2)
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
