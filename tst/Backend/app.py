from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import cv2

app = Flask(__name__, static_folder='../frontend', static_url_path='')

model = YOLO('yolov8n.pt')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/output.jpg')
def output_image():
    return send_from_directory('.', 'output.jpg')

@app.route('/process-image', methods=['POST'])
def process_image():
    image_file = request.files['image']
    image_path = 'input.jpg'
    output_path = 'output.jpg'
    image_file.save(image_path)

    results = model(image_path)
    result = results[0]

    img = cv2.imread(image_path)
    count = 0

    for box in result.boxes:
        count += 1
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imwrite(output_path, img)

   
    thermal_defects = [2, 1, 0, 3]
    surface_defects = [1, 0, 2, 0]
    risk_levels = [1, 1, 2]
    nose_defect = {
        'severity': 'high',
        'type': 'تصادم'
    }

    return jsonify({
        'count': count,
        'image': '/output.jpg',
        'thermal_defects': thermal_defects,
        'surface_defects': surface_defects,
        'risk_levels': risk_levels,
        'nose_defect': nose_defect
    })

if __name__ == '__main__':
    app.run(debug=True)
