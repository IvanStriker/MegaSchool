from ultralytics import YOLO
import cv2
import supervision as sv
import easyocr
import pytesseract
from PIL import Image

model = YOLO('runs/detect/train4/weights/best.pt')

image = cv2.imread("45 (1).png")

results = model(image)[0]

original = image.copy()

detections = sv.Detections.from_ultralytics(results)

ocr_reader = easyocr.Reader(['ru'])


#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Влад\Tesseract-OCR\tesseract.exe'

#print(pytesseract.image_to_string(Image.open('48.png')),1111111111111111111111111111222222222222222222222222222222222)

def get_res():

    res=[]

    for i in range(len(detections.xyxy)):
        bbox = detections.xyxy[i]
        class_id = detections.class_id[i]

        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if str(class_id)[0] == '3' or str(class_id)[0] == '8':
            for_text = original[y1-5:y2, x1:x2]
            text_results = ocr_reader.readtext(for_text)

            extracted_texts = []

            for (ocr_bbox, text, confidence) in text_results:
                if confidence >= 0.3:
                    extracted_texts.append(text)

            full_text = ' '.join(extracted_texts)
        else:
            full_text = ''

        result = {
            'coord': (x1,y1,x2,y2),
            'class': str(class_id)[0],
            'text': full_text,
        }
        res.append(result)

    return res

print(get_res())


