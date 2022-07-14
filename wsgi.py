
# 访问测试报告
from flask import Flask
from gevent import pywsgi

app = Flask(__name__)


@app.route('/report', methods=['get'])
def index():
    return 'hello world'


server = pywsgi.WSGIServer(('0.0.0.0', 3001), app)
server.serve_forever()
