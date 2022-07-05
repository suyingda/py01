import ast
import json
import os
import time

import gridfs
from bson.objectid import ObjectId
from bson import json_util
# from bson import ObjectId
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import pymongo

app = Flask(__name__, static_folder='save_file', static_url_path="/save_file")
# download
# app.default_config['JSONIFY_MINETYPE'] = "application/DragonFire"

# flask method=['get','post'] endpoint='h1'
# @app.route('/home/<id>')
# def index(id):
# CORS
CORS(app, resource=r'/*')

# connect mongo server
mongo = {}

absolute = os.path.dirname(__file__)
# 定义文件的保存路径和文件名尾缀
FOLDER = os.path.join(absolute, 'save_file')

from bson.objectid import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# print(type(ObjectId(bbb), bbb))

def returnType(data):
    return json_util.dumps({'data': data, 'message': 'success', 'code': 200})


def isAllowedFile(filename):
    pass


# 存储到mongodb
def save_file_to_mongo(content):
    with open(content, 'rb') as f:
        data = f.read()
        fs = gridfs.GridFS(mongo.demo, 'img')
        print(fs.put(data), '文件上传')
        # retrun fs.put(data)


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
    path = './save_file/' + _format[0] + t + '.' + _format[1]
    if fileData:
        fileData.save(path)
        # else:
        #     return 'We don\'t allow this file extension.'
    return json_util.dumps(
        {'data': '/save_file/' + _format[0] + t + '.' + _format[1], 'message': 'success', 'code': 200})


# @app.route("/download")
# def find():

@app.route("/download")
def download_file():
    file_path = os.path.join(FOLDER, '1.jpeg    ')
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "The downloaded file does not exist"


@app.route("/get_file")
def get_file():
    app.config["JSONIFY_MINETYPE"] = "application/DragonFire"
    return send_file("save_file/1.jpeg")


@app.route("/get_json")
def get_json():
    d = {
        "name": "Alexander.DSB.Li"
    }
    return jsonify(d)
    # return d


mongo = pymongo.MongoClient(host='localhost', port=27017, tz_aware=True)


def mongodb_init01():
    rows = mongo.hello.world.find()
    for r in rows:
        print(r)
    db = mongo.hello
    print(db)
    # 删除数据库
    print(mongo.drop_database('hello'))
    # 获取数据库
    print(mongo.list_database_names())
    # _db = mongo.list
    # 获取所有集合名称
    print(mongo.list.list_collection_names())
    # 获取所有集合对象
    print(mongo.list.list_collections())


@app.route("/components/delete", methods=['POST'])
def delete():
    props = eval(request.data)
    db = mongo.components
    if props['parentId']:
        db.list.delete_one({"_id": ObjectId(props['parentId'])})
        db.list_children.delete_many({"parent": ObjectId(props['parentId'])})
    elif props['childrenId']:
        db.list_children.delete_one({"_id": props['childrenId']})
        # return json_util.dumps({'message': 'success', 'code': 200})
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route("/components/list", methods=['GET'])
def list():
    db = mongo.components
    data = db.list.find()
    data_child = db.list_children.find()
    print(data, 'parent')
    print(data_child, 'child')
    dict = []
    result = db.list.aggregate(
        [{
            '$lookup': {
                "from": "list_children",
                "localField": "_id",
                "foreignField": "parent",
                "as": "children"
            }
        }]
    )
    for rc in result:
        temp = ast.literal_eval(JSONEncoder().encode(rc))
        dict.append(temp)

    return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})


# 插入数据
@app.route('/components/insert', methods=['POST'])
def insert():
    print('插入数据：', request.data, type(request.data))
    props = eval(request.data)
    db = mongo.components
    print(props)
    if '_id' in props:
        print(props, '插入子节点', ObjectId(props['_id']))
        data = {}
        data['parent'] = ObjectId(props['_id'])
        data["pageName"] = props['pageName']
        data["pageType"] = props['pageType']
        data["menuPath"] = props['menuPath']
        data["menuWeight"] = props['menuWeight']
        print(data, '子集插入')
        db.list_children.insert_one(data)
    else:
        print(props, 'insert')
        db.list.insert_one(props)

    return json_util.dumps({'message': 'success', 'code': 200})


@app.route('/components/search', methods=['POST'])
def search():
    print(request.data, 'search', type(request.data))
    props = eval(request.data)
    _id = ''
    try:
        _id = props["_id"]
    except:
        return 'Parameter _id cannot be empty'
    print(props, 'search')
    db = mongo.components
    data = db.list.find({"_id": ObjectId(_id)})
    dict = []
    for r in data:
        dict.append(ast.literal_eval(JSONEncoder().encode(r)))
        # print(dict)
    return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})


# page

def requestBase(files):
    url = "/upload"
    data = {
        "username": "ssm"
    }
    response = request.post(url, data=files)
    print("request:", response.text)


# 插入数据

@app.route('/components/head', methods=['POST'])
def insert_page():
    db = mongo.components
    props = eval(request.data)
    # if 'image' in props:
    #     requestBase(props['image'])
    db.page_module.save(props)
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route('/components/page/<string:name>', methods=['GET'])
def page(name):
    print(name)
    return 'page'


if __name__ == "__main__":
    mongodb_init01()
    app.run(host='0.0.0.0', port=3000)