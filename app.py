import os
import shutil
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import pytesseract
import cv2

app = Flask(__name__)
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(carplate_img)
    return carplate_img

def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]
    return carplate_img

def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

@app.route('/')
def index():
    return 'hello bro'



@app.route('/file', methods=['POST'])
def upload_img():
    # for filename in os.listdir(UPLOAD_FOLDER):
    #     file_path = os.path.join(UPLOAD_FOLDER, filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))

    if 'file1' not in request.files:
        return 'there is no file1 in form!'
    file1 = request.files['file1']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    return jsonify({'number': path})
    carplate_img_rgb = open_img(img_path=path)
    carplate_haar_cascade = cv2.CascadeClassifier('./haar_cascades/haarcascade_russian_plate_number.xml')
    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)
    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    plt.axis('off')
    plt.imshow(carplate_extract_img_gray, cmap='gray')

    autonumber = str(pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
    return jsonify({'number': autonumber})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
