import os,shutil;
import glob;

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
    print(FOLDER_PATH);
    if os.path.exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)
        os.mkdir(FOLDER_PATH)
    return render_template('index.html',form_route="/upload");

@app.route("/upload", methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        image_file = request.files['img_file']
        if image_file:
            if os.path.exists( FOLDER_PATH):
                shutil.rmtree(FOLDER_PATH)
                os.mkdir(FOLDER_PATH)
            
            image_file.save(os.path.join(FOLDER_PATH, secure_filename(image_file.filename)))
            return redirect(url_for('run_prediction'));
        
        return render_template('index.html',form_route="/upload",upload_state='error')
    

@app.route("/predict", methods=['GET','POST'])
def run_prediction():
    if os.path.exists( FOLDER_PATH):
        uploads = glob.glob(os.path.join(FOLDER_PATH, '*'));
        image_file = uploads[0];
        file_name = os.path.basename(image_file);
    if request.method == 'POST':
        prediction = predict(image_file);
        image_url = url_for('static',filename=f'/uploads/{file_name}');
        return render_template('index.html',image_file=file_name,image_url=image_url,prediction=prediction)
    if request.method == 'GET':
        
        return render_template('index.html',form_route="/predict", upload_state='success',image_file=file_name)
        
    


if __name__ == '__main__':
    app.run('0.0.0.0',port=5100,debug=True);