import os
# from re import template
from string import Template
from flask import Flask, send_file, request, jsonify
# from werkzeug.utils import secure_filename
# from flask_cors import CORS
import time

app = Flask(__name__)
absolute = os.path.dirname(__file__)
# CORS(app)
app.debug = True
# 定义文件的保存路径和文件名尾缀
FOLDER = os.path.join(absolute, 'save_file')
HOST = "localhost"
PORT = 8080
UPLOAD = 'upload'
app.config['UPLOAD'] = UPLOAD
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'xls', 'xlsx', 'jpeg', 'jpg'])


# 进行文件类型判断的函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 默认访问
@app.route('/')
def index():
    html = Template(
        """
    <!DOCTYPE html>
    <html>
        <body style='padding-left:30px;'>
          <a href='http://localhost:8080/download'>下载</a>
          <br>
          <a href='http://localhost:8080/upload'>上传</a>
        </body>
    </html>
    """
    )
    html = html.substitute()
    return html


# 下载
@app.route("/download")
def download_file():
    file_path = os.path.join(FOLDER, 'test.md')
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"


# 上传
@app.route('/upload', methods=['post'])
def upload_file():
    file_dir = os.path.join(basedir, app.config['UPLOAD'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['test_file']
    if f and allowed_file(f.filename):
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        return jsonify({"state": 200, "data": "上传成功"})
    else:
        return jsonify({"state": 500, "errmsg": "上传失败"})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
