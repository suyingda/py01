import pymongo

mongo = {}

# connect mongo
mongo = pymongo.MongoClient(
    # 用户名
    username='root',
    # 密码
    password='ixd',
    # 需要用户名和密码进行身份认证的数据库
    # authSource='admin',
    host='localhost', port=27017, tz_aware=True)
