# running it is python app.py
from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img = cv2.imread(filepath)
            # Apply NLM denoising (you can replace this with your actual NLM denoising function)
            denoised_img = perform_nlm_denoising(img)
            output_filename = 'denoised_' + filename
            output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            cv2.imwrite(output_filepath, denoised_img)
            return render_template('result.html', filename=output_filename)
    return redirect(url_for('index'))

def perform_nlm_denoising(image):
    # Your NLM denoising logic here (use OpenCV's cv2.fastNlMeansDenoising)
    # Replace this placeholder function with your actual implementation
    # For example:
    # denoised_image = cv2.fastNlMeansDenoising(image, None, h=10)
    # return denoised_image
    pass

if __name__ == '__main__':
    app.run(debug=True)
