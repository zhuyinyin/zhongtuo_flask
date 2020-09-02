import os, sys
from flask import Flask, request
# # 前台蓝图
from app.web.views import web_bpt
# 管理员蓝图
from app.admin.views import admin_bpt
import settings

def create_app():
    # 路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, r'app\web\static')
    templates_dir = os.path.join(BASE_DIR, r'app\web\templates')
    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    # # 注册前台蓝图
    app.register_blueprint(blueprint=web_bpt, url_prefix='/')
    # 后台蓝图
    app.register_blueprint(blueprint=admin_bpt, url_prefix='/admin')

    # 导入配置文件
    app.config.from_object(settings.DevelopmentConfig)

    # 模板冲突解决
    # 优先使用当前蓝图的模板
    @app.before_request
    def before_request():
        if request.blueprint is not None:
            bp = app.blueprints[request.blueprint]
            if bp.jinja_loader is not None:
                newsearchpath = bp.jinja_loader.searchpath + app.jinja_loader.searchpath
                app.jinja_loader.searchpath = newsearchpath
            # 如果访问非蓝图模块或蓝图中没有指定template_folder,默认使用app注册时指定的全局template_floder.
            else:
                app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]
        else:
            app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]

    # 模板全局变量
    @app.context_processor
    def context_processor():
        zyy = {
            "web": {
                "title": "中山市中拓劳务派遣有限公司"
            },

            # ----------------------------------------------------------------

            "globals": {
                "debug_mode": 1,
                "cache_control": 0,
                "cookie_expire": 120,
                "server_protocol": "https",
                "admin_dir": "admin2020pyx",
                "admin_language": "chinese",
                "admin_template": "default",
                "static_path": "",
                "static_file": "MP_verify_ujq1FqHu7yyO5Z9n.txt",
                "upload_type": ['png', 'jpg', 'jpeg', 'gif', 'rar', 'zip', 'gz', 'ico', 'csv', 'mp3', 'mp4'],
                "upload_file_size": 51,
                "upload_imag_size": 61,
                "mysql_log": 1,
                "access_count": 1,
                "task_plan": 1,
                "log_max_row": 10000,
                "access_max_row": 10000,
                "editor_size": ['52%', ' 63%'],
                "icp": "鄂ICP备19026508号-1",
                "beian": "鄂公网安备 42011102003681号"
            },

            # ----------------------------------------------------------------

            "server": {
                "WEB_URL": "http://www.itzyy.top/environ",
                "ROOT_PATH": "/data/kgcms/www/",
                "PATH_INFO": "/environ",
                "HTTP_ADDR": "120.231.109.249",
                "HTTP_HOST": "http://www.itzyy.top",
                "HTTP_REFERER": "",
                "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "HTTP_OS": "Windows NT 10.0; Win64; x64",
                "SERVER_PORT": "8000",
                "SERVER_PROTOCOL": "http",
                "SERVER_ADDR": "0",
                "SERVER_OS": ('Linux', '3.10.0', '64bit', 'itzyy'),
                "SERVER_SOFTWARE": "WSGIServer/0.2",
                "KGCMS_VERSION": "1.0.0"
            },

            # ----------------------------------------------------------------

            "get":{},

            # ----------------------------------------------------------------

            "post":{},

            # ----------------------------------------------------------------

            "cookie": {
                "ITZYY_ACCESS_ID": "MpYcoXsQuNTkyOFRssmIaLz7Stnx8EJV",
                "ITZYY_SESSION_ID": "VMYSoYyye1A8yC25JvIyC4aQF3dHtJQL"
            },

              # ----------------------------------------------------------------

            "session": {
                "KGCMS_USER_ID": 29,
                "KGCMS_USER_FREQUECY": 140,
                "KGCMS_USER_LOGIN_ID": "zhuyinyin"
            },

              # ----------------------------------------------------------------

            "user": {
                "id": 29,
                "username": "zhuyinyin",
                "password": "a9f8b7de51268bd00edacdeb9ebb5cb0",
                "encryption": "IohpAfGN",
                "type": 0,
                "openid": "",
                "email": "zyy15377553496@163.com",
                "qq": "1258209501",
                "sex": 2,
                "nickname": "按时开心",
                "image": "",
                "money": "0.00",
                "usemoney": "0.00",
                "scores": 840,
                "level": [5],
                "problem": "",
                "answer": "",
                "companyname": "中山凯格",
                "companyweb": "itzyy.top",
                "companyaddress": "中环广场",
                "phone": "15377553497",
                "fax": "",
                "frequency": 140,
                "jointime": "2020-04-01 14:22:52",
                "joinip": "163.179.46.47",
                "joinaddress": "广东省中山市",
                "audit": 0,
                "effective": 1,
                "rank_name": "代理商",
                "discount": "0.7",
                "logintime": [0, 0],
                "loginip": ['', '']
            },

              # ----------------------------------------------------------------

            "admin": {
                id: 0
            },

              # ----------------------------------------------------------------

            "run_start_time": (1594977985.949554, 1595125583.695405),

              # ----------------------------------------------------------------

            "db_request_count": 9,

              # ----------------------------------------------------------------

            "model": ('web', 'environ'),

              # ----------------------------------------------------------------

            "current_path": ['environ'],

              # ----------------------------------------------------------------

            "tpl": "environ.tpl",

              # ----------------------------------------------------------------

            "tpl_url": "https://www.itzyy.top/template/frontend/test/",

              # ----------------------------------------------------------------

            "lang": {},

              # ----------------------------------------------------------------

            "environ": {
                "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin",
                "_": "/data/app/python3/bin/python3.8",
                "PWD": "/",
                "LANG": "zh_CN.UTF-8",
                "SHLVL": "2",
                "SERVER_NAME": "Kyger",
                "GATEWAY_INTERFACE": "CGI/1.1",
                "SERVER_PORT": "8000",
                "REMOTE_HOST": "",
                "CONTENT_LENGTH": "",
                "SCRIPT_NAME": "",
                "SERVER_PROTOCOL": "HTTP/1.0",
                "SERVER_SOFTWARE": "WSGIServer/0.2",
                "REQUEST_METHOD": "GET",
                "PATH_INFO": "/environ",
                "QUERY_STRING": "",
                "REMOTE_ADDR": "127.0.0.1",
                "CONTENT_TYPE": "text/plain",
                "HTTP_HOST": "www.kgcms.com",
                "HTTP_X_REAL_IP": "120.231.109.249",
                "HTTP_X_FORWARDED_FOR": "120.231.109.249",
                "HTTP_CONNECTION": "close",
                "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
                "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "HTTP_SEC_FETCH_SITE": "cross-site",
                "HTTP_SEC_FETCH_MODE": "navigate",
                "HTTP_SEC_FETCH_USER": "?1",
                "HTTP_SEC_FETCH_DEST": "document",
                "HTTP_ACCEPT_ENCODING": "gzip, deflate, br",
                "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "HTTP_COOKIE": "KGCMS_ACCESS_ID=MpYcoXsQuNTkyOFRssmIaLz7Stnx8EJV; KGCMS_SESSION_ID=VMYSoYyye1A8yC25JvIyC4aQF3dHtJQL",
                "wsgi.input": "<_io.BufferedReader name=4>",
                "wsgi.errors": "<_io.TextIOWrapper name='' mode='w' encoding='utf-8'>",
                "wsgi.version": (1, 0),
                "wsgi.run_once": False,
                "wsgi.url_scheme": "http",
                "wsgi.multithread": False,
                "wsgi.multiprocess": False,
                "wsgi.file_wrapper": ""
            }
        }
        return dict(itzyy=zyy, region="NA")

    return app
