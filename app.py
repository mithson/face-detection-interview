from flask import Flask, request, render_template
import os
import cv2
import imutils

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    if file.filename == '':
        return 'No file selected'
    file.save(os.path.join('uploads', file.filename))
    image = cv2.imread(os.path.join('uploads', file.filename))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return render_template('index.html', message='No face detected. Please upload another image.')
    else:
        return render_template('index.html', message='Face detected. Image uploaded successfully.')
