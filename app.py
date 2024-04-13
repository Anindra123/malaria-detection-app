import os,shutil;
import glob;
import PIL ;
from PIL import Image;
from flask import Flask;
from flask import render_template, request, redirect, url_for;
from werkzeug.utils import secure_filename
from main import predict



app = Flask(__name__) # creating the instance of flask class
image_file = None
FOLDER_NAME = 'uploads'
FOLDER_PATH = os.path.join(os.getcwd(),'static',FOLDER_NAME);

@app.route("/")
def init():
    if os.path.exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)
        os.mkdir(FOLDER_PATH)
    return render_template('index.html',form_route="/upload");

@app.route("/upload", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        image_file = request.files['img_file']
        
        if image_file:
            try:
                im = Image.open(image_file);
                
                if os.path.exists( FOLDER_PATH):
                    shutil.rmtree(FOLDER_PATH)
                    os.mkdir(FOLDER_PATH)

                im.save(os.path.join(FOLDER_PATH, secure_filename(image_file.filename)))
                return {
                    "status" : "success",
                    "message" : url_for('static',filename=f'uploads/{image_file.filename}'),
                }
            except:
                return {
                    "status" : "error",
                    "message" : "Not a valid image type",
                }
        else:
            return {
                    "status" : "error",
                    "message" : "File uploaded is invalid",
            }

@app.route("/predict", methods=['POST'])
def run_prediction():
    if os.path.exists( FOLDER_PATH):
        uploads = glob.glob(os.path.join(FOLDER_PATH, '*'));
        image_file = uploads[0];
        
    if request.method == 'POST':
        try:
            prediction = predict(image_file);
            return{
                "status":"success",
                "message" : prediction,
            }
        except:
            return{
                "status" : "error",
                "message" : "Error running prediction on image"
            }
        
        
    
        
    


if __name__ == '__main__':
    app.run('0.0.0.0',port=5100,debug=True);