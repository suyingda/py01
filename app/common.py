from flask import Blueprint, request, jsonify, send_file
from common.path import FILE_PATH
from common.mongo import mongo

import os
import time

app = Blueprint('common', __name__, url_prefix='')

absolute = os.path.dirname(__file__)
# 定义文件的保存路径和文件名尾缀
FOLDER = os.path.join(absolute, 'save_file')


@app.route('/upload', methods=['POST'])
def upload():
    # if request.method == 'POST':
    print(request.files, 'file')
    # _array_files = [0]?
    r = request.files
    print(type(request.files))
    fileData = {}
    for i in r.items():
        print(type(i), i)
        print(i[1])
        fileData = i[1]

    print(fileData, fileData.filename, 'upload file')
    _format = ['default', 'png']
    if fileData.filename:
        _format = fileData.filename.split('.')

    t = str(round(time.time() * 1000))
    # _p = os.path.abspath('/save_file/')
    # print(_p)

    file_path = FILE_PATH
    path = file_path + _format[0] + t + '.' + _format[1]
    list = os.listdir(file_path)  # 列出文件夹下所有的目录与文件
    print(list, '7777')
    db = mongo.components
    exit_data = db.upload.find_one({"filename": _format[0]})
    print(exit_data)

    _path = '/save_file/' + _format[0] + t + '.' + _format[1]
    # if exit_data:
    #     return json_util.dumps(
    #         {'data': exit_data['path'], 'message': 'already existed', 'code': 200})
    # else:
    #     db.upload.insert_one({"filename": _format[0], "path": _path})
    print(_format[0], 'xxxx')
    if fileData:
        fileData.save(path)

    return jsonify({'data': _path, 'message': 'upload success', 'code': 200})


@app.route("/download")
def download_file():
    file_path = os.path.join(FILE_PATH, '01color1657696841589.png')
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"
