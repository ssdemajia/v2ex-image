import json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def read_password():
    with open('config.json') as fp:
        config = json.load(fp)
    return config['password']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS