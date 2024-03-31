# running it is python app.py
from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = os.path.join('static', 'outputs')
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
    # Check if the input image is not None
    if image is None:
        return None

    # Convert the image to grayscale for denoising
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform NLM denoising
    # H defines the filter strength (more =  blurry, less = less filter)
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, h=50)

    return denoised_image

if __name__ == '__main__':
    app.run(debug=True)
