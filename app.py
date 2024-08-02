from flask import Flask, request, redirect, url_for, render_template
import os
import pickle
import keras
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array,array_to_img
import numpy as np
app = Flask(__name__)

# Set up a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
regpredict=pickle.load(open("Prediction.pkl","rb"))
@app.route('/')
def home_1():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    # if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
   
#      
    Image=image.load_img(file_path,target_size=(64,64))
    picture=image.img_to_array(Image)
    picture=picture/255
    IA = np.expand_dims(picture,axis=0)
    testimg = np.vstack([IA])
    ans=round(regpredict.predict(testimg)[0][0])
    if ans==0:
        image_1="Cat"
    else:
        image_1="Dog"
    return render_template('upload.html',ans="The predicted image is {}".format(image_1))
   
#     # return 'Invalid file format'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    # Implement your own secure filename logic or use a library
    return filename


if __name__ == '__main__':
    app.run(debug=True)
