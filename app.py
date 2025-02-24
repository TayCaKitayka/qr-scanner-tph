import os
from flask import Flask, render_template, request, redirect, url_for
from pyzbar.pyzbar import decode
import cv2

app = Flask(__name__)

UPLOAD_DIR = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'supersecretkey'  # Для использования flash сообщений

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def handle_file():
    if 'file' not in request.files:
        return redirect(request.url)

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return redirect(request.url)

    if uploaded_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        qr_text = read_qr_code(file_path)
        return render_template('index.html', qr_content=qr_text, img_path=file_path)


def read_qr_code(img_path):
    img = cv2.imread(img_path)
    decoded_data = decode(img)

    if not decoded_data:
        return "No QR code detected."

    for obj in decoded_data:
        return obj.data.decode("utf-8")

    return "No QR code detected."


if __name__ == '__main__':
    app.run(debug=True)
