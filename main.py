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
    # _p = os.path.abspath('/save_file/')
    # print(_p)

    file_path = '/Users/apple/Desktop/py-server/py01/save_file/'
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

    return json_util.dumps(
        {'data': _path, 'message': 'success', 'code': 200})


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


# connect mongo
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
    if 'parentId' in props:
        db.list.delete_one({"_id": ObjectId(props['parentId'])})
        db.list_children.delete_many({"parent": ObjectId(props['parentId'])})
    elif 'childrenId' in props:
        db.list_children.delete_one({"_id": ObjectId(props['childrenId'])})
        # return json_util.dumps({'message': 'success', 'code': 200})
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route("/components/update", methods=['POST'])
def update():
    props = eval(request.data)
    db = mongo.components
    if 'parentId' in props:
        _id = props['parentId']
        # print(props, 'update data')
        dict = {}
        addType = props.get('addType')
        pageName = props.get('pageName')
        menuPath = props.get('menuPath')
        menuWeight = props.get('menuWeight')
        pageType = props.get('pageType')
        if addType:
            dict['addType'] = addType
        if pageName:
            dict['pageName'] = pageName
        if menuPath:
            dict['menuPath'] = menuPath
        if menuWeight:
            dict['menuWeight'] = menuWeight
        if pageType:
            dict['pageType'] = pageType
        print(dict, '更改')
        db.list.update_one({'_id': ObjectId(_id)}, {"$set": dict})
    elif 'childrenId' in props:
        _id = props['childrenId']
        dict = {}
        addType = props.get('addType')
        pageName = props.get('pageName')
        menuPath = props.get('menuPath')
        menuWeight = props.get('menuWeight')
        pageType = props.get('pageType')
        if addType:
            dict['addType'] = addType
        if pageName:
            dict['pageName'] = pageName
        if menuPath:
            dict['menuPath'] = menuPath
        if menuWeight:
            dict['menuWeight'] = menuWeight
        if pageType:
            dict['pageType'] = pageType

        db.list_children.update_one({'_id': ObjectId(_id)}, {"$set": dict})
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route("/components/overview", methods=['GET'])
def overview():
    db = mongo.components
    dict = []
    res = db.list.aggregate([
        {
            "$lookup": {
                "from": "list_children",
                "localField": "_id",
                "foreignField": "parent",
                "as": "children"
            }

        },
        {
            "$unwind": {
                "path": "$children",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "page_content",
                "localField": "children._id",
                "foreignField": "parentId",
                "as": "children.pageContent",
            }
        },
        {
            "$unwind": {
                "path": "$children",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "page_head",
                "localField": "children._id",
                "foreignField": "parentId",
                "as": "children.pageHead",
            }
        },
        {
            "$group": {
                "_id": "$_id",
                # "name": {"$first": "$name"},
                "addType": {"$first": "$addType"},
                "pageName": {"$first": "$pageName"},
                "menuPath": {"$first": "$menuPath"},
                "menuWeight": {"$first": "$menuWeight"},
                "children": {"$push": "$children"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "addType": 1,
                "pageName": 1,
                "menuPath": 1,
                "menuWeight": 1,
                # "name": 1,
                "children": {
                    "$filter": {"input": "$children", "as": "a", "cond": {"$ifNull": ["$$a._id", False]}}
                }
            }
        }
    ])
    print(res)
    for rc in res:
        print(rc)
        temp = ast.literal_eval(JSONEncoder().encode(rc))
        dict.append(temp)

    # print(dict2)
    return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})


@app.route("/components/list", methods=['GET'])
def list():
    db = mongo.components
    dict = []
    result = db.list.aggregate(
        [{
            '$lookup': {
                "from": "list_children",
                "localField": "_id",
                "foreignField": "parent",
                "as": "children"
            },

        }, {"$sort": {"date": -1}}]
    )
    # print(result, 'list')
    for rc in result:
        print(rc)
        temp = ast.literal_eval(JSONEncoder().encode(rc))
        dict.append(temp)

    return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})


# 插入数据
@app.route('/components/insert', methods=['POST'])
def insert():
    # print('插入数据：', request.data, type(request.data))
    props = eval(request.data)
    db = mongo.components
    print(props)
    if 'parent' in props:
        # print(props, '插入子节点', ObjectId(props['_id']))
        data = {}
        data['parent'] = ObjectId(props['parent'])
        type = props.get('type')
        addType = props.get('addType')
        pageName = props.get('pageName')
        pageType = props.get('pageType')
        menuPath = props.get('menuPath')
        menuWeight = props.get('menuWeight')
        if type:
            data['type'] = type
        if addType:
            data['addType'] = addType
        if pageName:
            data['pageName'] = pageName
        if pageType:
            data['pageType'] = pageType
        if menuPath:
            data['menuPath'] = menuPath
        if menuWeight:
            data['menuWeight'] = menuWeight
        # print(data, '子集插入')
        db.list_children.insert_one(data)
    else:
        print(props, 'insert')
        db.list.insert_one(props)

    return json_util.dumps({'message': 'success', 'code': 200})


@app.route('/components/search', methods=['POST'])
def search():
    print(request.data, 'search', type(request.data))
    props = eval(request.data)
    # pageName = ''
    # try:
    #     pageName = props["pageName"]
    # except:
    #     return 'Parameter pageName cannot be empty'
    print(props, 'search')
    db = mongo.components
    # data = db.list.find({"pageName": {'$regex': pageName}})
    data = db.list.find({"pageName": {"$regex": props['pageName']}})
    # data_child = db.list_children.find({"pageName": {"$regex": "^'{0}'".format(props['pageName'])}})
    data_child = db.list_children.find({"pageName": {"$regex": props['pageName']}})
    print(data)
    dict = []
    for r in data:
        print(r)
        dict.append(ast.literal_eval(JSONEncoder().encode(r)))
    for r in data_child:
        print(r)
        dict.append(ast.literal_eval(JSONEncoder().encode(r)))
    # print(dict)
    print(dict)
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

@app.route('/components/head/add', methods=['POST'])
def insert_page():
    props = eval(request.data)
    db = mongo.components
    dict = {}
    headBackground = props.get('headBackground')
    title = props.get('title')
    desc = props.get('desc')
    overViewIcon = props.get('overViewIcon')
    if headBackground:
        dict['headBackground'] = headBackground
    if title:
        dict['title'] = title
    if desc:
        dict['desc'] = desc
    if overViewIcon:
        dict['overViewIcon'] = overViewIcon
    if '_id' in props:
        # dict = (ast.literal_eval(JSONEncoder().encode(r)))
        db.page_head.update_one({'parent': ObjectId(props['_id'])}, {"$set": dict}, upsert=True)
    else:
        db.page_head.insert_one(props)
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route('/components/head', methods=['POST'])
def headaa():
    # print(request.data, 'head', type(request.data))
    props = eval(request.data)
    # 根据父类Id查询
    parentId = props.get('parentId')
    if parentId:
        db = mongo.components
        data = db.page_head.find_one({"parentId": parentId})
        # print(data)
        if data:
            dict = ast.literal_eval(JSONEncoder().encode(data))
            return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})
        else:
            return json_util.dumps({'data': {}, 'message': 'success', 'code': 200})

        # dict = ast.literal_eval(JSONEncoder().encode(r))
        # print(dict)
    else:
        return 'Parameter parentId cannot be empty'


# page content
@app.route('/components/content/add', methods=['POST'])
def aaaa():
    props = eval(request.data)
    db = mongo.components
    if '_id' in props:
        print(props, 'update')
        # find
        data = db.page_content.find({'_id': ObjectId(props['_id']), "type": props['type']})
        #
        dict = {}
        for r in data:
            dict = r
            # dict = (ast.literal_eval(JSONEncoder().encode(r)))
        print(dict, 'xx', props)
        db.page_content.update_one(dict, {"$set": {
            # '_id': ObjectId(props['_id']),
            # 'type': props['type'],
            'data': props['data'],

        }})
    else:
        db.page_content.insert_one(props)
    return json_util.dumps({'message': 'success', 'code': 200})


@app.route('/components/content', methods=['POST'])
def content():
    print(request.data, 'content', type(request.data))
    props = eval(request.data)
    id = ''
    try:
        id = props["id"]
    except:
        return 'Parameter self id cannot be empty'
    print(props, 'page_head')
    db = mongo.components
    data = db.page_content.find_one({"id": id, "type": props['type']})
    dict = []
    if data:
        dict = ast.literal_eval(JSONEncoder().encode(data))
    print(data, '查询content')

    # for r in data:
    # dict = r
    # dict = ast.literal_eval(JSONEncoder().encode(r))
    # print(dict)
    return json_util.dumps({'data': dict, 'message': 'success', 'code': 200})


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
    file_path = '/Users/apple/Desktop/py-server/py01/save_file/'
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
    print(dict, 'data')

    for r in list:
        if (r in dict):
            print("在")
        else:
            delete_file(file_path, r)
            print("不在")
    # for r in :
    #     print(str(r))


if __name__ == "__main__":
    unnecessary()
    mongodb_init01()
    app.run(host='0.0.0.0', port=3000)
