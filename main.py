import os
from common.path import FILE_PATH
import gridfs
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from common.mongo import mongo
from gevent import pywsgi

import common.config as _config

from app.components import app as components_bp
from app.common import app as common_bp

app = Flask(__name__, static_folder='save_file', static_url_path="/save_file")
app.config.from_object(_config)
# 导入蓝图结构
app.register_blueprint(common_bp)
app.register_blueprint(components_bp)
# download
# app.default_config['JSONIFY_MINETYPE'] = "application/DragonFire"
# routers.routers(app)
# flask method=['get','post'] endpoint='h1'
# @app.route('/home/<id>')
# def index(id):
# CORS
CORS(app, resource=r'/*')


# 存储到mongodb
def save_file_to_mongo(content):
    with open(content, 'rb') as f:
        data = f.read()
        fs = gridfs.GridFS(mongo.demo, 'img')
        print(fs.put(data), '文件上传')
        # retrun fs.put(data)


# @app.route("/download")
# def find():


@app.route("/get_file")
def get_file():
    app.config["JSONIFY_MINETYPE"] = "application/DragonFire"
    return send_file("save_file/1.jpeg")


@app.route('/components/page/<string:name>', methods=['GET'])
def page(name):
    print(name)
    return 'page'


# clear unnecessary
def delete_file(file_path, name):
    path = file_path + name
    if os.path.exists(path):
        os.remove(path)
        print('delete ', path)
    else:
        print("The file does not exist")


def unnecessary():
    file_path = FILE_PATH
    # path = file_path + _format[0] + t + '.' + _format[1]
    list = os.listdir(file_path)  # 列出文件夹下所有的目录与文件
    # print(list, '7777')
    db = mongo.components
    data = db.page_content.find()
    data_head = db.page_head.find()
    dict = ''
    for r in data:
        dict = dict + str(r)
    for r in data_head:
        dict = dict + str(r)
    # print(dict, 'data')

    for r in list:
        if r not in dict:
            delete_file(file_path, r)
            print("不在")
        # else:


if __name__ == "__main__":
    unnecessary()
    print('successful')
    server = pywsgi.WSGIServer(('0.0.0.0', 3000), app)
    server.serve_forever()

    # app.run(host='0.0.0.0', port=3000)
