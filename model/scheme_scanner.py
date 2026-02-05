from ultralytics import YOLO
import cv2
import supervision as sv
import easyocr
import os

curDir = os.path.dirname(os.path.abspath(__file__))
model = None


def prepareModel():
    global model
    model = YOLO(curDir + '/for_colab_3/runs/detect/train/weights/best.pt')


def scan(path: str):
    global model
    image = cv2.imread(path)
    results = model(image)[0]
    original = image.copy()
    detections = sv.Detections.from_ultralytics(results).with_nms(threshold=0.3)
    ocr_reader = easyocr.Reader(['ru', 'en'])
    return getTokens(image, original, detections, ocr_reader)


def getTokens(image, original, detections, ocr_reader):

    res=[]

    for i in range(len(detections.xyxy)):
        bbox = detections.xyxy[i]
        class_id = detections.class_id[i]
        x1, y1, x2, y2 = map(int, bbox)
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #if str(class_id)[0] == '3' or str(class_id)[0] == '8':

        h, w = image.shape[:2]
        for_text = original[max(y1-20, 0) : min(y2+20, h),
                            max(x1-20, 0) : min(x2+20, w)]
        if str(class_id)[0] == '4':
            for_text = cv2.rotate(for_text, cv2.ROTATE_90_CLOCKWISE)
            text_results = ocr_reader.readtext(for_text)
        else:
            text_results = ocr_reader.readtext(for_text)
        extracted_texts = []

        for (ocr_bbox, text, confidence) in text_results:
            if confidence >= 0.3:
                extracted_texts.append(text)

        full_text = ' '.join(extracted_texts)

        result = {
            'coord': (x1,y1,x2,y2),
            'class': str(class_id),
            'text': full_text,
        }
        res.append(result)

    return res

