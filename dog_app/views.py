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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
            result = dog_breed_guesser_from_path('tmp/image.jpg')

            # return redirect(url_for('uploaded_file',
            #                         filename=filename, test_result=result))
            return render_template('image_upload.html', test_result=result)
    return render_template('image_upload.html', test_result=None)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     result=None
#     if request.method == 'POST':
#         file_b64 = request.form['b64file']
#         print("requested")
#         if file_b64:
#             # Decode the image
#             file = base64.b64decode(file_b64)
#             img = Image.open(io.BytesIO(file))
#             img.save('tmp/imge.jpg')
#             print("image saved")
#             result = dog_breed_guesser_from_path('tmp/imge.jpg')
#     return render_template('image_upload.html', test_result=result)

@app.route('/show/<test_result>/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('show_image.html', filename=filename, test_result=test_result)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
