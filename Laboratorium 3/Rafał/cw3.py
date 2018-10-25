from flask import Flask
from flask import session
from flask import request

app = Flask(__name__)
app.secret_key = b'trol12345'

@app.route('/utnickir/zw3/')
def index():
    return "Jest dobrze"

@app.route('/utnickir/zw3/upload', methods=['POST'])
def upload():
    print(request.files)
    return "OK"