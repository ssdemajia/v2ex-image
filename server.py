from flask import Flask, jsonify, render_template, make_response, send_from_directory
from flask import request
import os
import re
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__, template_folder='template')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), "upload")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# DOMAIN = "www.dowob.cn/image"
DOMAIN = "127.0.0.1:8989/image"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
def index():
    lists = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', file_list=lists)


@app.route('/upload', methods=["POST"])
def upload_image():
    form = request.form
    key = form['key']
    name = form['name']
    data = request.files
    file = data['uploadFile']
    if key != 'shaoshuai':
        return jsonify({'state': 1})
    if file:
        if name and re.match(r'^([a-zA-Z][a-zA-Z0-9_]*)$', name):
            if name.rfind('.') != -1:
                filename = name
            else:
                filename = name.rsplit('.', 1)[0] + '.' + file.filename.rsplit('.', 1)[1]
        elif allowed_file(file.filename):
            filename = file.filename
        else:
            return jsonify({
                'state': 2
            })
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({
            'state': 0,
            'url': request.url.rsplit('/', 1)[0] + '/image/' + filename
        })
    return jsonify({'state': 3})


@app.route('/image/<image_id>', methods=["GET"])
def get_image(image_id):
    image_path = os.path.join(UPLOAD_FOLDER, image_id)
    if not os.path.exists(image_path):
        return 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_id)


@app.route('/delete/<image>')
def delete(image):
    image_path = os.path.join(UPLOAD_FOLDER, image)
    if os.path.exists(image_path):
        os.unlink(image_path)
    return jsonify({
        'state': 0
    })
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8989', debug=True)