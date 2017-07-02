from flask import request, render_template, request, send_from_directory, redirect, flash, url_for
from flask_app import app
import os
from processes import dog_breed_guesser_from_path
import base64
import io
from PIL import Image
from werkzeug.utils import secure_filename
from time import sleep

UPLOAD_FOLDER = 'C:\\Users\\zfeng\\Documents\\GitHub\\dog_project\\tmp\\'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_location)
            result = dog_breed_guesser_from_path(file_location)

            return render_template('image_upload.html',
                                    filename=filename, test_result=result)
            # return render_template('image_upload.html', test_result=result)
    return render_template('image_upload.html', test_result=None)


@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
