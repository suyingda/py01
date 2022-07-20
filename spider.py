import time
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from common.mongo import mongo

url = 'http://intl-design-ui.woa.com/'
driver = webdriver.Chrome()


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
        get_href = get_href.replace('/', '__')
        # print(get_href,'get_hrefget_hrefget_href')
        child_href.append({
            'name': get_href,
            'href': r.get_attribute('href')
        })


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
def generate(_res, name):
    link_reg = '<link rel="stylesheet" href="/umi.css">'
    script_reg = '<script src="/umi.js"></script>'
    pre_http = 'http://intl-design-ui.woa.com/'
    link_res = _res.replace(link_reg, '<link rel="stylesheet" href="' + pre_http + 'umi.css">')
    # script_res = link_res.replace(script_reg, '<script src="' + pre_http + 'umi.js"></script>')
    script_res = link_res.replace(script_reg, '<script src="' + pre_http + 'umi.js"></script>')
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
for r in child_href:
    new_res = get_html_text(r['href'])
    print(r, 'namename')
    print(r['name'], 'namename')
    # 判断是否是存在name
    if r['name']:
        generate(new_res, r['name'] + '.html')


def connect_mongodb():
    db = mongo.intl_components
    r = db.data.find()
    for i in r:
        print(i)
    db.data.insert_one({"data": child_href})


time.sleep(10)
driver.quit()

connect_mongodb()
