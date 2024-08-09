from flask import Flask, request, redirect, url_for, render_template
import os
import pickle
import keras
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

app = Flask(__name__)

# Set up a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained model
regpredict = pickle.load(open("Prediction.pkl", "rb"))

@app.route('/')
def home_1():
    return render_template('upload.html', animal=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
   
        img = image.load_img(file_path, target_size=(64, 64))
        img_array = img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        # testimg = np.vstack([IA])
        ans = round(regpredict.predict(img_array)[0][0])
        
        if ans == 0:
            animal = "Cat"
        else:
            animal = "Dog"
        
        return render_template('upload.html', animal=animal)
   
    return 'Invalid file format'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    # Implement your own secure filename logic or use a library
    return filename

if __name__ == '__main__':
    app.run(debug=True)
