[//]: # (get route params)
request.args.get('xxx')


[//]: # (渲染模版页面)
render_template(path.html)

修改模版路径 app = Flask(__name__,template_folder = r'c:\template')


[//]: # (mongodb createUser)
use admin 
db.createUser({user:'root',pwd:'ixd',roles:['root']})

[//]: # (验证是否创建成功)
db.auth('root','ixd')


[//]: # (启动mongo 使用安全模式运行)
mongod -f /mongodb/conf/mongo.conf --auth

bin ./mongo -uroot -pixd --authenticationDatabase=admin
