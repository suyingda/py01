from flask import Blueprint, jsonify, request
from common.mongo import mongo
from bson.objectid import ObjectId
import json
import ast
app = Blueprint('components', __name__, url_prefix='/components')
