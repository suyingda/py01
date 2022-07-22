# import time
# from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from common.mongo import mongo

from bson.objectid import ObjectId

url = 'http://intl-design-ui.woa.com/'
option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(chrome_options=option)


# driver = webdriver.Chrome()


def get_html_text(_url):
    driver.get(_url)
    return driver.page_source


# time.sleep(3)

res = get_html_text(url)
# print(res)
# 获取元素标签
elements = driver.find_elements(By.CLASS_NAME, '__dumi-default-menu-list')
# print(elements)
child_href = []
for e in elements:
    aaaa = e.find_elements(By.TAG_NAME, 'a')
    for r in aaaa:
        print('我是啥', r.text, r.tag_name, r.get_attribute('href'))
        get_href = r.get_attribute('href')
        get_href = get_href.replace('http://intl-design-ui.woa.com/', '')
        temp_line = get_href
        get_href = get_href.replace('/', '__')
        split_str = get_href.split('__')
        # resolve_path = get_href.replace('__', '/')
        # for c_r in child_href:
        # print(get_href,'get_hrefget_hrefget_href')
        collect_dict = {
            'label': r.text,
            'name': get_href,
            'href': r.get_attribute('href'),
            'page': f'/{temp_line}.html',
        }
        if split_str and len(split_str) > 1:
            print('split_str', split_str)
            collect_dict['parent'] = split_str[0]
        child_href.append(collect_dict)

# child_href

for index in range(len(child_href)):
    # for r, index in enumerate(child_href):
    # print(index, 'xx')
    r = child_href[index]
    if 'parent' in r:
        for rr in child_href:
            if rr['name'] == r['parent']:
                if 'children' not in rr:
                    rr['children'] = []
                rr['children'].append(r)
                # del child_href[index]

#
# for e in child:
#     print('我是啥', e.text)
# print(child)
# elements.click()
# time.sleep(5)
# scroll
# driver.execute_script('window.scrollTo(0,document.body.scrollHeight')
# driver.quit()
#
# res = request.urlopen(url)
#
# print(res)
# # print(res.read())
#
# text = res.read().decode('utf-8')
#
# print(res.geturl())
# print(res.getcode())
#
css_path = 'css'
js_path = 'js'


def generate(_res, name):
    link_reg = '<link rel="stylesheet" href="/umi.css">'
    script_reg = '<script src="/umi.js"></script>'
    pre_http = 'http://intl-design-ui.woa.com/'
    _dome = '/~demos/'
    # _res = _res.replace(_dome, 'http://intl-design-ui.woa.com/~demos/')
    link_res = _res.replace(link_reg, '<link rel="stylesheet" href="' + pre_http + 'umi.css">'
                                                                                   '<link rel="stylesheet" href="/get_file/' + css_path + '">')
    # script_res = link_res.replace(script_reg, '<script src="' + pre_http + 'umi.js"></script>')
    script_res = link_res.replace(script_reg,
                                  '<script src="' + pre_http + 'umi.js"></script><script src="/get_file/' + js_path + '"></script>')

    # print(_res, '有东西？')
    if not name:
        name = 'default.html'
    with open('./templates/' + name, 'w', encoding='utf-8') as fp:
        fp.write(script_res)


# generate(res, 'index.html')
#
# #
# # request.urlretrieve('url', 'xx.png')
#
# # 伪造
# path = 'http://www.baidu.com/'
# rs = request.Request(url=path)
# _t = request.urlopen(rs)
# print(_t.read().decode('utf-8'))
filter_data = []
for r in child_href:
    new_res = get_html_text(r['href'])
    # print(r, 'namename')
    # print(r['name'], 'namename')
    # 判断是否是存在name
    if r['name']:
        if 'parent' not in r:
            filter_data.append(r)
        generate(new_res, r['name'] + '.html')


def connect_mongodb():
    db = mongo.intl_components
    rrr = db.data.find()
    # print('数据库', rrr)
    templates_dict = {}
    for i in rrr:
        templates_dict = i
    # print('templates_dict', templates_dict)
    if "_id" in templates_dict:
        # print('666666', templates_dict['_id'])
        db.data.update_one({'_id': ObjectId(templates_dict['_id'])}, {"$set": {"data": filter_data}})
        # db.data.update_one({"_id": ObjectId(templates_dict['_id'])}, {"$set": filter_data})
        print('存在')
    else:
        db.data.insert_one({"data": filter_data})
        print('不存在')

    #


# time.sleep(10)
driver.quit()

connect_mongodb()
