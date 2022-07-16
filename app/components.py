from flask import Blueprint, jsonify, request
from common.mongo import mongo
from bson.objectid import ObjectId
import json
import ast
app = Blueprint('components', __name__, url_prefix='/components')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/test2')
def test2():
    return 'hello'


@app.route("/delete", methods=['POST'])
def delete():
    props = eval(request.data)
    db = mongo.components
    if 'parentId' in props:
        db.list.delete_one({"_id": ObjectId(props['parentId'])})
        db.list_children.delete_many({"parent": ObjectId(props['parentId'])})
    elif 'childrenId' in props:
        db.list_children.delete_one({"_id": ObjectId(props['childrenId'])})
        # return jsonify({'message': 'success', 'code': 200})
    return jsonify({'message': 'success', 'code': 200})


@app.route("/update", methods=['POST'])
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
    return jsonify({'message': 'success', 'code': 200})


@app.route("/overview", methods=['GET'])
def overview():
    db = mongo.components
    dict = []
    res = db.list.aggregate([
        {
            "$lookup": {
                "from": "list_children",
                "localField": "_id",
                "foreignField": "parentId",
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
                "addType": {"$first": "$addType"},
                "pageName": {"$first": "$pageName"},
                "menuPath": {"$first": "$menuPath"},
                "menuWeight": {"$first": "$menuWeight"},
                # "pageType": {"$ifNull": ["$pageType", 's']},
                "pageType": {'$first': "$pageType"},
                # "pageType": {'$cond': [{"$eq": [{"$type": "$pageType"}, "missing"]}, 0, 1]},
                "children": {"$push": "$children"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "addType": 1,
                "pageName": 1,
                "menuPath": {"$ifNull": ["$menuPath", '请联系管理员']},
                "menuWeight": 1,
                "pageType": {"$ifNull": ["$pageType", '请联系管理员']},
                "children": {
                    "$filter": {"input": "$children", "as": "a", "cond": {"$ifNull": ["$$a._id", False]}}
                }
            }
        },
        {"$sort": {"menuWeight": 1}}
    ])
    print(res)
    for rc in res:
        print('111', rc)
        if rc:
            temp = ast.literal_eval(JSONEncoder().encode(rc))
            dict.append(temp)

    # print(dict2)
    return jsonify({'data': dict, 'message': 'success', 'code': 200})


@app.route("/list", methods=['GET'])
def list():
    db = mongo.components
    dict = []
    result = db.list.aggregate(
        [{
            '$lookup': {
                "from": "list_children",
                "localField": "_id",
                "foreignField": "parentId",
                "as": "children"
            },

        }, {"$sort": {"date": -1}}]
    )
    # print(result, 'list')
    for rc in result:
        print(rc)
        temp = ast.literal_eval(JSONEncoder().encode(rc))
        dict.append(temp)

    return jsonify({'data': dict, 'message': 'success', 'code': 200})


# 插入数据
@app.route('/insert', methods=['POST'])
def insert():
    # print('插入数据：', request.data, type(request.data))
    props = eval(request.data)
    db = mongo.components
    print(props)
    if 'parentId' in props:
        # print(props, '插入子节点', ObjectId(props['_id']))
        data = {}
        data['parentId'] = ObjectId(props['parentId'])
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

    return jsonify({'message': 'success', 'code': 200})


@app.route('/search', methods=['POST'])
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
    return jsonify({'data': dict, 'message': 'success', 'code': 200})


# 插入数据

@app.route('/head/add', methods=['POST'])
def insert_page():
    props = eval(request.data)
    db = mongo.components
    dict = {}
    parentId = props.get('parentId')
    headBackground = props.get('headBackground')
    title = props.get('title')
    desc = props.get('desc')
    overViewIcon = props.get('overViewIcon')
    if headBackground:
        dict['parentId'] = ObjectId(parentId)
    if headBackground:
        dict['headBackground'] = headBackground
    else:
        dict['headBackground'] = ''
    if title:
        dict['title'] = title
    else:
        dict['title'] = ''
    if desc:
        dict['desc'] = desc
    else:
        dict['desc'] = ''
    if overViewIcon:
        dict['overViewIcon'] = overViewIcon
    else:
        dict['overViewIcon'] = ''
    if parentId:
        # dict = (ast.literal_eval(JSONEncoder().encode(r)))
        db.page_head.update_one({'parentId': ObjectId(parentId)}, {"$set": dict}, upsert=True)
    else:
        db.page_head.insert_one(dict)
    return jsonify({'message': 'success', 'code': 200})


@app.route('/head', methods=['POST'])
def headaa():
    # print(request.data, 'head', type(request.data))
    props = eval(request.data)
    # 根据父类Id查询
    parentId = props.get('parentId')
    if parentId:
        db = mongo.components
        data = db.page_head.find_one({"parentId": ObjectId(parentId)})
        # print(data)
        if data:
            dict = ast.literal_eval(JSONEncoder().encode(data))
            return jsonify({'data': dict, 'message': 'success', 'code': 200})
        else:
            return jsonify({'data': {}, 'message': 'success', 'code': 200})

        # dict = ast.literal_eval(JSONEncoder().encode(r))
        # print(dict)
    else:
        return 'Parameter parentId cannot be empty'


# page content
@app.route('/content/add', methods=['POST'])
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
    return jsonify({'message': 'success', 'code': 200})


@app.route('/content', methods=['POST'])
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
    return jsonify({'data': dict, 'message': 'success', 'code': 200})
