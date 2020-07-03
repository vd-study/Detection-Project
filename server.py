import os
from yolo_detector import *
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = 'static/downloand'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file_get():
    if 'file' not in request.files:
        return 'Нейронная сеть не может обрабатывать несуществующий файл'
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return 'Нейронная сеть не может обрабатывать пустой файл'
        if file and allowed_file(file.filename):
            list_picture = []
            nows = time.time()
            picture_name = str(nows)+'.jpg'
            print(picture_name)
            filename = secure_filename(picture_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            yolo_generated = get_picture_from_server(UPLOAD_FOLDER, picture_name)
            list_picture.append(yolo_generated)
            list_picture.append('downloand/arrow.jpg')
            list_picture.append('downloand/'+picture_name)
            for name in list_picture:
                print(name)
            return render_template('get_image.html', image_names=list_picture)
        else:
            return 'Данный сайт и нейросеть работают с фотографиями формата: png,jpg,jpeg'

    return 'Ооо, вы из Хогвартса , как попали сюда, рассказываете..'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def info_to_user():
    return render_template('upload.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=4567)
