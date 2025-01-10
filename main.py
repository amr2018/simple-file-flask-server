from flask import Flask, send_file, make_response
from werkzeug.utils import secure_filename
import os
import socket
import pyqrcode

def make_qr_code():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        image_as_str = pyqrcode.QRCode(content=local_ip).png_as_base64_str(scale=5)
        html_img = '<img src="data:image/png;base64,{}">'.format(image_as_str)
        return html_img
    except:
        return "<h2> Error :( </h2>"

app = Flask(__name__)

def get_all_files():
    html = ""
    dir = 'my files/'
    for file_name in os.listdir(dir):
        html += f"<a href = '/file/{file_name}'>{file_name}</a>"

    return html


@app.route('/', methods = ['GET'],)
def home():
    return {'msg': 'Hello, world'}

@app.route('/myfiles', methods = ['GET'])
def show_files():
    return f"""{make_qr_code()}
    <h3>Open from any device</h3>
    <h1>My Files</h1></br>{get_all_files()}"""

@app.route('/file/<string:file>', methods = ['GET'])
def download(file):
    dir = 'my files/'
    file = secure_filename(file)
    file_path = os.path.join(dir, file)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    
    return make_response(f'file [{file}] is not found :(')




app.run(host='0.0.0.0', port=80, debug=True)
