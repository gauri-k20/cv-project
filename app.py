import cv2
import numpy as np
from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

# Function for applying translation
def translate_image(img, tx, ty):
    rows, cols = img.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])  # Translation matrix
    translated_img = cv2.warpAffine(img, M, (cols, rows))
    return translated_img

# Function for applying rotation
def rotate_image(img, angle):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))
    return rotated_img

# Function for applying scaling
def scale_image(img, scale_x, scale_y):
    scaled_img = cv2.resize(img, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
    return scaled_img

# Function for applying shearing
def shear_image(img, shear_factor):
    rows, cols = img.shape[:2]
    M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
    sheared_img = cv2.warpAffine(img, M, (cols + int(shear_factor * rows), rows))
    return sheared_img

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    if request.method == 'POST':
        file = request.files['file']
        operation = request.form['operation']

        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

        if operation == 'translate':
            tx = int(request.form['tx'])
            ty = int(request.form['ty'])
            transformed_img = translate_image(img, tx, ty)
        elif operation == 'rotate':
            angle = float(request.form['angle'])
            transformed_img = rotate_image(img, angle)
        elif operation == 'scale':
            scale_x = float(request.form['scale_x'])
            scale_y = float(request.form['scale_y'])
            transformed_img = scale_image(img, scale_x, scale_y)
        elif operation == 'shear':
            shear_factor = float(request.form['shear_factor'])
            transformed_img = shear_image(img, shear_factor)

        # Save output
        output_file = 'output.jpg'
        cv2.imwrite(output_file, transformed_img)

        return send_file(output_file, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)
