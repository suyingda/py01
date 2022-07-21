from flask import Blueprint, jsonify, request
from common.mongo import mongo
from bson.objectid import ObjectId
import json
import ast

app = Blueprint('intl-components', __name__, url_prefix='/intl-components')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, ObjectId):
            print(str(o))
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/find", methods=['GET'])
def intl_find():
    # props = eval(request.data)
    db = mongo.intl_components
    result = db.data.find()
    dict = []
    for rc in result:
        print(rc)
        temp = ast.literal_eval(JSONEncoder().encode(rc))
        dict.append(temp)
    return jsonify({'message': 'success', "data": dict, 'code': 200})
