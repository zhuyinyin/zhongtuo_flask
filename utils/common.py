# -*- coding:utf-8 -*-
"""常用公共函数库,各种杂项处理"""


def numerics(num, min=0, max=0):
    """
    数字整形，整形成指定范围内的数字
    :param num：[str|int] 要整形的变量，字符或数字
    :param min：[int] 最小值，当数字小于该值时或非数字时返回该值
    :param max：[int] 最大值，当数字大于该值时返回该值，为0 时不限制最大值
    :return: [int|float]
    """
    from re import compile
    if isinstance(num, str):
        r = int(num) if compile(r'^[-+]?[0-9]+$').match(num) else float(num) if compile(r'^[-+]?[0-9]+.[0-9]+$').match(
            num) else 0
    elif isinstance(num, (int, float)):
        r = num
    else:
        r = 0
    return min if r < min else (max if (r > max != 0) else r)


def alert(msg='', act=3):
    """
    JS弹出窗口
    静态方法
    Example：Main.alert('操作成功！',2) | Main.alert('确定后跳到首页！','http://www.itzyy.top')| Main.alert('','../')
    :param msg: [str] 需要弹出的消息内容，为空时不弹出，直接跳转
    :param act：[str] 弹窗确定后的动作：0不作任何处理，1停留在当前页并刷新，2返回上一页并刷新，3后退不刷新，4关闭当前窗口，其它为跳转页URL
    """
    js = '<script language="javascript">%s%s</script>'
    s1 = ('alert("%s");' % msg.replace('\"', '\\"')) if msg else ''
    if act == 0:
        s2 = ''
    elif act == 1:
        s2 = 'location=location;'  # 刷新当前页
    elif act == 2:
        s2 = 'location.replace(document.referrer);'  # 返回上一页并刷新，新窗口有效
    elif act == 3:
        s2 = 'history.back(-1);'  # 返回上一页且不刷新，当前窗口有效
    elif act == 4:
        s2 = 'window.opener=null; window.open("","_self"); window.close();'  # 部分浏览器必须是新窗口打开时有效
    else:
        s2 = 'location = "%s";' % act
    return js % (s1, s2)


def str_shift(word, grade=0, expression=''):
    """
    过滤字符特殊字符
    :param word: [str] 要检查的字符串
    :param grade: [int] 要过滤的字符，0过滤特殊字符[\'\"\\/&*]，1保留数字，2保留大小写字母，
    3保留大小写字母数字及下(中)划线，9自定义过滤,需要配合 self.shift(word,9,'"//*.$$$',r'[.$]*')
    :param expression: [str] 自定义过滤规则
    :return [str]

    """
    import re  # 正则
    if grade == 0:
        r = re.sub(r'[\'\"\\/&*]', '', word)
    elif grade == 1:
        r = re.sub(r'[^0-9]', '', word)
    elif grade == 2:
        r = re.sub(r'[^A-Za-z]', '', word)
    elif grade == 3:
        r = re.sub(r'[^A-Za-z0-9_-]', '', word)
    else:
        r = re.sub(expression, '', word)
    return r


def str_escape(value):
    """
    转义特殊字符
    用于SQL等，将 " 转义为 \"
    :param value: [str]
    :return:
    """
    value = str(value)
    value = value.replace('\\', '\\\\')
    value = value.replace('\0', '\\0')
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\032', '\\Z')
    value = value.replace("'", "\\'")
    value = value.replace('"', '\\"')
    return value


def str_replace(find, old=[], new=None):
    """
    批量/多次替换, 支持列表替换
    :param find: [str] 要替换的字符串
    :param old: [list] 要查找的字符串, 必须是列表
    :param new: [list|str] 替换后的新字符串, 可以是列表或字符
    :Example: str_replace('abcd',['a','c'],['E',9])  |  tr_replace('abcd',['a','c'],'M'
    :return: [str]
    """
    if not isinstance(old, list): old = [old]
    for i, rep in enumerate(old):
        if isinstance(new, (str, int)):
            find = find.replace(str(rep), str(new))
        else:
            find = find.replace(str(rep), str(new[i]))
    return find


def str_between(word, start='', flag=0, end=''):
    """
    截取指定的字符串
    :param word: [str] 要处理的字符串
    :param start: [str] 开始字符串, 为空时从开头截取, 特殊字符请使用 \ 转义, 如: start='\('  end='\)'
    :param flag:0 取 start 之前的字符，不包含 start [start首次出现以前]
                1 取 start 与 end 之间的字符，不包含 start 和 end [start与end首次出现]
                2 取 start 与 end 之间的字符，包含 start 和 end [start与end首次出现]
                3 取 start 之后的字符，不包含 start [start首次出现之后]
                4 取 start 与 end 之间的字符，不包含 start 和 end [start首次出现,end最后一次出现]
    :param end: [str] 结束字符串
    :return: [str]
    """
    import re

    if flag == 0:
        r = re.findall(r'' + '([\s\S]+?)' + start, word)
        r = r[0] if r else ''
    elif flag == 3:
        r = re.findall(r'' + start + '([\s\S]*)', word)
        r = r[0] if r else ''
    elif flag in (1, 2, 4):
        r = re.findall(r'' + start + '([\s\S]*)' + end, word) if flag == 4 else re.findall(
            r'' + start + '([\s\S]+?)' + end, word)
        if r:
            r = r[0]
            if flag == 2: r = '%s%s%s' % (start, r, end)
        else:
            r = ''
    return r


def str_cutting(string, length=1, dot=' ...'):
    """
    从开头截取指定长度的字符串
    自动计算中、英文长度
    通常用于标题、内容摘要等前部分截取
    :param string: 需要开始的字符串
    :param length: 长度，字节，一个汉字按两字节计算
    :param dot: 被截取后是否添加后缀
    :return: [str]
    str_cutting('广东凯格科技有限公司 / GuangDong Kyger Technology Co., Ltd.', 51)
    str_cutting('GuangDong Kyger Technology Co., Ltd. / 广东凯格科技有限公司', 51)
    """
    i = p = 0
    while True:
        if p < length and i < len(string):
            if u'\u4e00' <= string[i] <= u'\u9fff':
                p += 2
            else:
                p += 1
            i += 1
        else:
            break
    return string[:i] + dot if string != string[:i] else string


def str_random(length=6, letter=3, numeric=1):
    """
    随机生成字符串, 注意 numeric 和 letter 不能同时为0
    :param length: [int] 生成的字符串长度
    :param letter: [int] 字母大小写, 0不含字母, 1大写, 2小写字母, 3大小写字母同时
    :param numeric: [1|0] 是否有数字, 0不含数字, 1含数字
    :return:
    """
    import random
    str1 = '0123456789'
    str2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str3 = 'abcdefghijklmnopqrstuvwxyz'
    salt = str = ''
    if numeric: str = str1
    if letter == 1:
        str += str2
    elif letter == 2:
        str += str3
    elif letter == 3:
        str += str2 + str3
    if str:
        for i in range(length): salt += random.choice(str)
        return salt
    else:
        return ''


def html_escape(exam, quote=True):
    """
    转义HTML标签符
    类似PHP htmlspecialchars 函数，将 <>&"' 转义成 &amp; &lt; &gt;
    :param exam: [str|list|dict] 要转义的字符或数组
    :param quote: 是否转义单/双引号
    :return: [str|list|dict]
    html_escape(["<a href=''>Test</a>", '<b>OK</b>'])
    html_escape('<a href="test">Test</a>')
    html_escape({'a': '<a>Test</a>', 'b': '<b>OK</b>'})
    """

    def escape(exam, quote):
        s = exam.replace("&", "&amp;")  # Must be done first!
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        if quote:
            s = s.replace('"', "&quot;")
            s = s.replace("'", "&#x27;")
        return s

    if isinstance(exam, list):
        r = []
        for v in exam: r.append(escape(v, quote))
    elif isinstance(exam, dict):
        r = {}
        for k, v in exam.items():
            if isinstance(v, str):
                r.update({k: escape(v, quote)})
            else:
                r.update({k: v})

    elif isinstance(exam, str):
        r = escape(exam, quote)
    else:
        r = exam
    return r


def strip_tags(string, allowed_tags=''):
    """
    剥去 HTML、XML 标签
    :param string: 要检查的字符串
    :param allowed_tags: 允许的标签。这些标签不会被删除。多个标签用逗号隔开
    :return: [str]
    strip_tags('<a href="#">Test</a><img src="" />', 'img,br')  # Test<img src="" />
    strip_tags('<a href="#">Test</a><img src="" />')  # Test
    strip_tags(get_contents('http://www.itzyy.top'))
    """
    import re
    string = str(string)
    if allowed_tags != '':
        # 允许的标签列表
        allowed_tags = allowed_tags.split(',')
        allowed_tags_pattern = ['</?' + allowed_tag + '[^>]*>' for allowed_tag in allowed_tags]
        all_tags = re.findall(r'<[^>]+>', string, re.I)
        not_allowed_tags = []
        tmp = 0
        for tag in all_tags:
            for pattern in allowed_tags_pattern:
                rs = re.match(pattern, tag)
                if rs:
                    tmp += 1
                else:
                    tmp += 0
            if not tmp: not_allowed_tags.append(tag)
            tmp = 0
        for not_allowed_tag in not_allowed_tags:
            string = re.sub(re.escape(not_allowed_tag), '', string)
    else:
        # 没有保留标签，清除全部 HTML 标签
        string = re.sub(r'<[^>]*?>', '', string)
    return string


def nl2br(string, is_xhtml=True):
    """
    将换行符转HTML换行，\n 转 <br>
    字符串中的每个新行（\n）之前插入 HTML 换行符（<br> 或 <br />）
    类似 PHP 同名方法
    :param string: 要转义的字符串
    :param is_xhtml: XHTML 语法规范
    :return:
    """

    if is_xhtml:
        return string.replace('\n', '<br />\n')
    else:
        return string.replace('\n', '<br>\n')


def url_query2dict(deal):
    """
    URL字符串解析, URL <-> dict 互转
    将 /?action=del&id=1&id=2&id=6 解析成 {'action':'del','id':[1,2,6]}
    或将 {'id': 50, 'page': 3, 'ie': 'utf-8'} 转换成 id=50&page=3&ie=utf-8
    支持复选框名称最后[] 自动转成list name="checkboxName[]"
    将URL字符串解析成字典,出现 checkbox[] 字段多选或同一对象多个值时自动转成 list 形式
    :param deal: [str|dict] 需要解析的URL 或 Cookie 等，类似 m=product&id=41&action=del 之类的字串, 为 dict 时反向转换
    :return: [str|dict]
    :Example: url_query2dict('index/?action=del&id=1&id=2&id=6')
    :Example: url_query2dict({'id': 50, 'page': 3, 'ie': 'utf-8'})
    """
    r = {}
    from urllib.parse import parse_qs, urlencode
    if isinstance(deal, dict):
        r = urlencode(deal)
    elif isinstance(deal, str):
        t = deal if '?' not in deal else str_between(deal, r'\?', 3)  # 截取 ? 以后字串
        t = parse_qs(t, True)  # 允许 空值
        for k, v in t.items():  # 转成一维
            if k[-2:] != '[]':  # 判断是否按复选框处理
                r[k] = v[0] if len(v) == 1 else v  # 将 [] 转成 str,只取第一个元素
            else:  # 处理name名称中最后含[]的复选框
                r[k[:-2]] = v  # 去掉Name中最后的"[]"符号
    else:
        r = ''
    return r


def url_escape(path=''):
    """
    路径或URL转义
    将 \ 转义为 /
    :param str path: 需要转义的路径或URL
    :return str url：E:\python\kgcms
    """
    return path.replace("\\", '/').replace('//', '/')


def url_code(url='', act=0):
    """
    对URL进行编/解码处理
    :param url: [str] http://www.itzyy.top/?name=隔三秋
    :param act: [int] 0解码、1编码

    """
    from urllib import parse
    return parse.quote(url) if act else parse.unquote(url)


def url_analysis(url, reverse=False):
    """
    URL 解析，将URL中的请求目录路径按LIST的形式返回
    :Example：http://www.itzyy.top/product/58   # ['product','58']
    :param url: [str] 需要解析URL
    :param reverse: [bool] 反向解析,将数组转路径,为 True 时 url 请填写 List
    :return []: 按目录结构以列表的形式返回 # ['product','58']
    """
    if reverse:
        return '/'.join(url)
    else:
        from re import sub
        url = sub(r'^(http://|https://)(.*?)(/)', '', url, 1)  # 过滤掉域名
        url = url.split('?')
        url = url[0]

        r = []
        for k, v in enumerate(url.split('/')):
            r.append(v)
            if k > 20: break  # 限制过多层级目录
        return r


def url_parse(url, ret='__ALL__'):
    """
    URL 拆分, 获取URL中的域名,/协议/目录/query等
    :param url: 需要拆分的 URL : https://www.itzyy.top/path;pid?id=8#ok
    :param ret: [str] 返回数据结果
            __ALL__: 全部 (scheme='https', netloc='www.itzyy.top', path='/path', params='pid', query='id=8', fragment='ok')
            scheme : 网络协议 http|https
            netloc : 服务器位置/域名 www.itzyy.top
            path : 目录路径 /path
            params : 可选参数 pid
            query : 连接符（&）连接键值对 id=8
            fragment : 页面中的锚点 ok
    :return: dict|str  ret为__ALL__时返回dict, 否则返回str
    """
    from urllib.parse import urlparse
    r = urlparse(url)
    r = {
        'scheme': r.scheme,
        'netloc': r.netloc,
        'path': r.path,
        'params': r.params,
        'query': r.query,
        'fragment': r.fragment,
    }
    return r if ret == '__ALL__' else r[ret]


def url_update(url, update={}, deld=None):
    """
    URL中的参数修改/删除、类似PHP版中的 durl 方法
    :param url: [str] 需要处理的 URL，一般为：self.kg['server']['WEB_URL']
    :param update: [dict] 需要修改的 GET 变量和值，存在则修改、无则添加：{'ad':25, 'result':'ok'}
    :param deld: [list|str] 需要删除的GET参数名 ['action', 'id'] 或 'id'
    :return: [str] 处理后的URL
    :Example：   url_update('http://www.x.com/a.php?id=8&a=9', {'a': 2}, ['id', 'action'])
                url_update('http://www.x.com/a.php?id=8&a=9', {'a': 2}, 'id')
    """
    urls = url_query2dict(url)  # str 转 dict
    urls.update(update)  # 添加或修改
    # 删除
    if deld is not None:
        if not isinstance(deld, list): deld = [deld]
        for k in deld:
            try:
                del urls[k]
            except:
                pass
    urls = url_query2dict(urls)  # dict 转 str
    if '?' in url: urls = '%s?%s' % (str_between(url, r'\?'), urls)
    return urls


def url_absolute(url):
    """
    相对路径转绝对路径，相对于项目根目录
    print(url_absolute('temp/kgcms_version.json'))
    print(url_absolute('E:/python/kgcms/temp/kgcms_version.json'))
    """
    url = url_escape(url)
    from os import path
    P = url_escape(path.dirname(path.dirname(__file__)))  # 物理路径
    if P not in url: url = P + "/" + url
    return url


def url_relatively(url):
    """
    绝对路径转相对路径
    替换路径中的项目路径，返回相对于根目录下的相对路径
    """
    url = url_escape(url)
    from os import path
    P = url_escape(path.dirname(path.dirname(__file__))) + "/"
    return str_replace(url, P, "")


def file_extension(file):
    """
    获取文件后缀名
    :param file: [str] 完整文件名,可以含路径
    :return: [str] '.jpg'
    """
    from os.path import splitext
    return splitext(file)[-1]


def file_mime_type(file):
    """
    获取文件MIME类型,根据文件后缀名返回相应的 MIME 类型
    :param file: [str] 完整的文件名,可以含路径
    :return: [str] 'image/jpeg'
    """
    from mimetypes import guess_type
    r = guess_type(file)[0]
    if not r:  # mimetypes 库中没有, 追加部分
        r = {
            '.svg': 'image/svg+xml',
            '.woff': 'application/x-font-woff',
            '.woff2': 'application/x-font-woff',
            '.ttf': 'application/octet-stream',
            '.eot': 'application/vnd.ms-fontobject',
            '.otf': 'application/octet-stream',
            '.rar': 'application/x-rar-compressed',
        }.get(file_extension(file), None)
    return r


def file_list(path, type=1, form=1, subdirectory=False, suffix='*',
              filter=[".DS_Store", ".idea", "__pycache__", "Thumbs.db"]):
    """
    获取path下的文件、目录
    :param path: [str] 要搜索的路径，相对于项目根目录路径：file_list('upload/article')
    :param type: [int] 需要返回的数据，0表示所有，1表示文件，2表示目录
    :param form: [int] 返回的文件是否含路径：0只返回文件名称、1返回相对路径+文件名、2返回物理路径+文件名， 01.jpg|../image/01.jpg|E:/image/01.jpg
    :param subdirectory: [bool] 是否遍历当前路径下的所有子目录和文件
    :param suffix: [*|list] 获取的文件类型，文件后缀名，*时为所有，多个后缀名使用LIST：['.jpg','.png','.gif']
    :param filter: [list] 要过滤掉的文件，为空时不过滤
    :return: [list] 返回一个列表类型的数据
    :Example: file_list('upload/article')
    """
    import os
    r = []
    for root, dirs, files in os.walk(url_absolute(path)):  # 转绝对路径
        # 路径
        if form == 2:
            url = url_escape(root) + "/"
        elif form == 1:
            url = url_relatively(url_escape(root) + "/")
        else:
            url = ""

        # 文件
        if type in (0, 1):
            for name in files:
                if not (filter and name in filter):  # 过滤文件
                    if suffix == '*':
                        r.append(url + name)
                    else:
                        if not isinstance(suffix, list): suffix = [suffix]
                        if file_extension(name) in suffix: r.append(url + name)  # 指定文件类型

        # 目录
        if type in (0, 2):
            for name in dirs:
                if not (filter and name in filter):  # 过滤文件
                    r.append(url + name)
        if not subdirectory: break
    return r


def get_contents(url, mode='rb', header={}, data={}, charset="utf-8", method='GET'):
    """
    将一个文件或网址读入到字符串中
    类似PHP的 file_get_contents 方法
    :param url: [str] 文件路径或网址URL
    :param mode: [str] 打开方式: w以写方式打开, wb以二进制写模式打开
    :param header: [dict] 请求头：{"Accept-Encoding": "", "": ""} Accept-Encoding 为空不压缩，压缩时部分站点会乱码
    :param data: [dict] 请求数据： {"name": "zh-CN"}, POST请求时此为必须参数
    :param charset: [str] 字符编码，为空时自动不转换
    :param charset: [str] 请求方式, 默认为GET请求
    :return: [str]
    :get_contents("https://www.qq.com", header={"Accept-Encoding": ""}, charset="gbk")
    """
    from urllib.request import urlopen, Request
    import json
    from ssl import _create_unverified_context  # 不验证SSL证书
    try:
        if url.find('://') > 0:  # http
            if method == 'POST':
                data = url_query2dict(data).encode('utf-8')
                req = Request(url, data, header, method="POST")
            else:
                if data:
                    data = url_query2dict(data)
                    url = url + '&' + data if '?' in url else url + '?' + data
                req = Request(url, method="GET")
            r = urlopen(url=req, context=_create_unverified_context()).read()
        else:  # 本地
            url = url_absolute(url)  # 转物理路径
            fp = open(url, mode)
            r = fp.read()
            fp.close()
        if charset:
            r = r.decode(encoding=charset, errors="strict")
    except (FileNotFoundError, PermissionError, Exception) as e:
        r = str(e)
    return r


import json, time
# from utils.common import json2dict,numerics

# appid = 'wxc3ff38b8a112295c'
# secret = '9967ba2eed102ed773a11d3e357c44ee'
# datas = {
#     'appid': appid,
#     'secret': secret,
# }
# access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
# access_token = json2dict(get_contents(access_token_url, data=datas))['access_token']
# print(access_token)
# 菜单路由
# mue_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
json_data = {
    "button": [
        {
            "name": "qq",
            "sub_button": [
                {
                    "type": "scancode_waitmsg",
                    "name": "qq",
                    "key": "rselfmenu_0_0",
                    "sub_button": []
                }

            ]
        },
        {
            "name": "qq",
            "sub_button": [
                {
                    "type": "pic_sysphoto",
                    "name": "q",
                    "key": "rselfmenu_1_0",
                    "sub_button": []
                }
            ]
        },
        {
            "name": "q",
            "sub_button": [
                {
                    "type": "pic_sysphoto",
                    "name": "qq",
                    "key": "rselfmenu_2_0",
                    "sub_button": []
                }
            ]
        },

    ]
}
# mue_data = json2dict(json_data)

# mue_data = json.dumps(json_data, ensure_ascii=False).encode('utf-8')
# print(mue_data)
# data = url_query2dict(json_data).encode('gbk')
# print(data)
# mue = get_contents(mue_url, data=mue_data, method='POST')


# print(mue)


# post请求
# post_response = get_contents(' http://127.0.0.1:5000/bookstore/api/v1/books/', data={'price': 1, 'title': '哈哈', 'auther': '朱莹莹'}, method='POST')
# print(post_response)
# print(json2dict(post_response))
# get请求
# get_response = get_contents(' http://127.0.0.1:5000/bookstore/api/v1/books')
# print(get_response)
# print(json2dict(get_response))

# print(get_contents("https://www.qq.com", header={"Accept-Encoding": ""}, charset="gbk"))


def put_contents(filename, data='', mode='w', charset="utf-8"):
    """
    将一个字符串写入文件
    文件不存在则自动创建，类似PHP的 file_put_contents 方法
    :param filename: [str] 保存的文件名路径：dir/000.txt
    :param data: [str] 要写入的字符串
    :param mode: [str] 打开方式: w以写方式打开, wb以二进制写模式打开
    :param charset: [str] 字符编码
    :return: None
    put_contents("000.zip", a, "wb")
    """
    filename = url_absolute(filename)
    if mode in ("wb", "rb+", "wb+", "ab+"):
        f = open(filename, mode)  # 二进制不可设置编码
    else:
        f = open(filename, mode, encoding=charset)
        data = str(data)  # 出错时返回错误信息
    f.write(data)
    f.close()


def write_error(errmsg='', bottom='', title='itzyy Error', debug_mode=1):
    """
    错误消息模板
    :param errmsg: [str] 消息内容,支持Html,可以换行
    :param bottom: [str] 底部信息,服务器信息/文件完整路径等
    :param title: [str] 消息头、标题
    :param debug_mode [bool] 是否为调试模式，调试模式时显示错误信息，正常模式时显示空白
    :return HTML
    """
    if debug_mode:
        tpl = '<html><head><title>%s</title></head><body><h1>%s</h1><div style="line-height:25px;">%s%s</div></body></html>'
        s1 = ('<p>%s</p>' % errmsg) if errmsg else ''
        s2 = """<hr align="left" style="height:1px; border:none; border-top:1px dashed #333; width:800px;">
        <address>%s . <a href="http://www.itzyy.top" target="_blank">itzyy</a></address><br /><br /><br />"""
        s2 = s2 % bottom if bottom else ''
        return tpl % (title, title, s1, s2)
    else:
        return ''


def exists(path, type='dir'):
    """
    判断文件或路径是否存在
    :param path: [str] 文件或路径
    :param type: [str:dir|file] dir:检测目录是否存在, file:检测文件是否存在
    :return: bool
    """
    import os
    return os.path.exists(path) if type == 'dir' else os.path.isfile(path)


def notfound_404():
    """404消息页面模板"""
    x404 = url_absolute('static/404/index.html')
    if exists(x404, "file"):
        return get_contents(x404)
    else:
        return '404 Not Found'


def is_format(str, act='email'):
    """
    判断是否为一个合法格式的 email|phone|username|card
    :param str: 需要判断的字符
    :param act:
            [email]: 判断是否为一个正确的 E-Mail
            [phone]: 判断是否为一个手机号
            [username]: 判断是否为一个用户名: 字母开头，允许4-16字节，允许字母数字下划线
            [card]: 判断是否为一个合法的身份证号码: 15位或18位
    :return: [bool]
    """
    import re
    if act == 'email':
        return True if re.match(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', str) else False
    elif act == 'phone':
        return True if re.match(r"^1[35678]\d{9}$", str) else False
    elif act == 'username':
        return True if re.match(r"^[a-zA-Z][a-zA-Z0-9_]{3,15}$", str) else False
    elif act == 'card':
        return True if re.match(r'\d{15}|\d{18}', str) else False
    else:
        return False


def md5(data):
    """
    md5 加密
    :param data: 需要加密的字符串
    :return: str
    """
    import hashlib
    return hashlib.md5(str(data).encode(encoding='UTF-8')).hexdigest()


def cipher(string, operation=0, expiry=0, key=None):
    """
    字符串加密解密
    :param string: 原文或者密文
    :param operation: 动作，1加密、0解密
    :param expiry: 密文有效期, 加密时候有效， 单位 秒，0 为永久有效
    :param key: 密钥，用于加密解密的密钥，默认使用 "config/key.ini" 配置参数
    :return: str
    """
    from time import time
    from base64 import encodebytes, b64decode
    if key is None: key = get_contents("config/key.ini")
    key = md5(key)
    key_before = md5(key[:16])
    key_rear = md5(key[16:])

    # 32位随机密码，加密时追加随机密码，解密获取随机密码
    keyc = md5(time()) if operation else string[:32]

    cryptkey = key_before + md5(key_before + keyc)  # 64位密码，32位固定密码加32位随机密码
    key_length = len(cryptkey)  # 密码长度，64

    # 加密追加过期时间
    if operation:  # 加密
        string = '%010d' % (int(time() + expiry) if expiry else 0) + md5(string + key_rear)[:16] + string
    else:  # 解密，获取32位随机密码以后的字符串
        string = url_code(string)
        string = b64decode(string[32:]).decode("utf-8")

    box = range(256)
    box = dict(zip(box, box))  # 生成0-256列表并转成字典

    rndkey = {}
    for i in range(0, 256): rndkey[i] = ord(cryptkey[i % key_length])

    j = 0
    for i in range(0, 256):
        j = (j + box[i] + rndkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp

    a = j = 0
    result = ""
    for i in range(0, len(string)):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result = "%s%s" % (result, chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256])))

    if operation:  # 加密
        result = keyc + encodebytes(result.encode("utf-8")).strip().decode(encoding="utf-8")  # 加密
        result = url_code(str_replace(result, ["\r", "\n", " "], ""), 1)
    else:  # 解密
        expired = numeric(result[0:10])
        if (expired == 0 or expired - time() > 0) and result[10:26] == (md5(result[26:] + key_rear))[:16]:
            result = result[26:]  # 从解密字符串中截取内容
        else:
            result = ""  # 密文过期或密码错误
    return result


def time_check(start=0, end=0):
    """
    通过时间戳判断时间是多久前发生的
    :param start: 开始时间
    :param end: 结束时间, 为0时自动获取当前时间戳
    :return: [str] 3小时前
    """
    if not end: import time; end = time.time()
    SS = int(end - start)  # 获取秒时间差
    MM = int(SS / 60)  # 获取分钟时间差
    HH = int(MM / 60)  # 获取小时时间差
    DD = int(HH / 24)  # 获取天时间差

    if DD <= 1:
        if SS <= 60:
            r = "刚刚"
        elif 60 < SS <= 60 * 60:
            r = '%s分钟前' % MM
        elif 60 * 60 < SS <= 60 * 60 * 24:
            r = '%s小时前' % HH
        else:
            r = '%s天前' % DD
    elif 30 > DD > 1:
        r = '%s天前' % DD
    elif 30 <= DD < 365:
        r = '%s月前' % int(DD / 30)
    elif DD >= 365:
        r = '%s年前' % int(DD / 365)
    return r


def date(unix_time=0, format='%Y-%m-%d %H:%M:%S'):
    """
    日期时间格式化
    :param unix_time: 时间戳, 默认当前时间
    :param format: 格式:
                %y 两位数的年份表示（00-99）
                %Y 四位数的年份表示（000-9999）
                %m 月份（01-12）
                %d 日，月内中的一天（0-31）
                %H 24小时制小时数（0-23）
                %I 12小时制小时数（01-12）
                %M 分钟数（00=59）
                %S 秒（00-59）
                %a 本地简化星期名称
                %A 本地完整星期名称
                %b 本地简化的月份名称, 英文
                %B 本地完整的月份名称, 英文
                %c 本地相应的日期表示和时间表示
                %j 年内的一天（001-366）
                %p 本地A.M.或P.M.的等价符
                %U 一年中的星期数（00-53）星期天为星期的开始（第n周）
                %w 星期（0-6），星期天为星期的开始
                %W 一年中的星期数（00-53）星期一为星期的开始（第n周）
                %x 本地相应的日期表示
                %X 本地相应的时间表示
                %Z 当前时区的名称
                %% %号本身
    :return: [str]
    """
    import time
    unix_time = int(unix_time) if unix_time else int(time.time())
    format = format.encode('unicode_escape').decode('utf8')  # 转码, 否则中文(%Y年%m月%d日)会报错
    return time.strftime(format, time.localtime(numeric(unix_time))).encode('utf-8').decode('unicode_escape')


def mk_time(date, format='%Y-%m-%d %H:%M:%S'):
    """
    将日期转成时间戳
    :param date: 日期
    :param format: 日期格式
    :return: [int] 时间戳
    """
    from time import mktime, strptime
    try:
        r = int(mktime(strptime(date, format)))
    except Exception:
        r = 0
    return r


def json2dict(data=None, file=None, trans=True, force=False):
    """
    JSON <-> DICT 互转: 将 JSON 格式字符串转成 DICT 或 将 DICT 数据转成 JSON 格式字符串
    :param data: json|dict
                json: 将转成 dict
                dict: 将会转成 json
    :param trans: 是否转义特殊字符, 写数据库JSON格式时必须转义
    :param file: 文件URL，将文件转 Dict|List|Tuple 等，List|Tuple 格式可能需要开启 force=True
    :param force: 是否强制将 str 转成 list 或 tuple 等，将直接使用 eval() 执行，适用于不规范的 json 文件
    :return: [str|dict]
    """
    import json, re
    if file:
        data = get_contents(file)
        data = re.sub(r"\/\*([\S\s]*?)\*\/", "", data)  # 删除注释
    # 判断是否为一个路径
    if isinstance(data, str):  # JSON 字串转字典
        try:
            r = json.loads(data)
        except:
            r = data
    elif isinstance(data, (dict, list, tuple)):  # 字典|列表|元组转JSON字符串
        r = json.dumps(data, ensure_ascii=False)
        if trans:
            r = str_replace(r, ['\\', '\0', '\n', '\r', '\032', "'", '"'],
                            ['\\\\', '\\0', '\\n', '\\r', '\\Z', "\\'", '\\"'])
    else:
        r = data
    if force:
        try:
            r = eval(r)
        except:
            r = data
    return r


def dict2json_file(dict, file='temp/temp.json'):
    """
    将 dict 数据存储为 json 文件
    :param dict: 要存储的数据
    :param file: 可在的文件路径
    :return: [bool]
    """
    data = json2dict(dict, trans=False)
    put_contents(file, data)


def ip2address(db, ip):
    """
    查询IP地址信息
    查询数据库 ipaddress 表
    :param db: 数据库对象
    :param ip: IP地址
    :return: ipaddress 表所有字段
    """
    return db.list(table="ipaddress", field="*", where="ip = \"%s\"" % ip, order="`id` DESC", limit=1, shift=1,
                   log=False)


def log(db, kg, type=1, info={}):
    """
    日志记录: info = {"state": "SUCCESS", "table": "admin", "where": 69, "edit_count": 1}
    :param db: 数据库对象
    :param kg: 全局变量
    :param type: [int] 日志类型(1查询敏感数据/2添加数据 ...)
    :param info: [dict] MySQL json
    :return: None

    特殊情况下KG全局变量改变时应用：
                kg = {
                    "web": {"id": self.kg["web"]["id"]},
                    "server": {"WEB_URL": self.kg['server']['WEB_URL'], "HTTP_ADDR": self.kg['server']['HTTP_ADDR']},
                    "admin": {"id": login.get("id", 0)},
                    "session": {
                        "KGCMS_ADMIN_LOGIN_ID": login["loginid"],
                        "KGCMS_USER_LOGIN_ID": self.kg["session"].get("KGCMS_USER_LOGIN_ID", ""),
                    },
                    "user": {"id": self.kg['user']['id']},
                    "run_start_time": self.kg['run_start_time'],
                }
    """
    ips = ip2address(db, kg['server']['HTTP_ADDR'])
    data = {
        'webid': kg["web"]["id"],
        'type': type,
        'info': json2dict(info),
        'pageurl': kg['server']['WEB_URL'],
        'userid': kg['user']['id'],
        'adminid': kg['admin']['id'],
        'loginid': '{"admin":"%s","user":"%s"}' % (
        kg['session'].get("KGCMS_ADMIN_LOGIN_ID", ""), kg['session'].get("KGCMS_USER_LOGIN_ID", "")),
        'ip': kg['server']['HTTP_ADDR'],
        'address': ips["country"] + ips["province"] + ips["city"] + ips["ips"] if ips else "-",
        'addtime': kg['run_start_time'][1]
    }
    db.add('log', data, False)