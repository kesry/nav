from bottle import route, template, get, post, request, static_file, response
from db import pool
from conf import config
from log import LOG
import json

def isLogin():
    confirm_server = config["confirm"]
    confirm_req = request.get_cookie("confirm")
    if confirm_req == confirm_server:
        response.set_cookie("confirm", confirm_server)
        return True
    else:
        return False
    
# 获取当前用户设置的主机IP，前端页面只展示该主机IP的链接。
@get("/user/host")
def user_host():
    if isLogin():
        settings = pool.execute("select set_content from settings where set_name = 'system'", ())
        settings = settings["data"][0]
        settings = json.loads(settings['set_content'])
        print(f"settings: {settings}")
        hosts = settings['hosts']
        activehost = settings['activehost']
        print(f"hosts: {hosts}")
        return {
            "hosts": hosts,
            "activehost": activehost
        }
    else:
        LOG.info("未输入服务码")
        return "未输入服务码！"


@get("/user/settings")
def user_settings():
    if isLogin():
        settings = pool.execute("select set_content from settings where set_name = 'system'", ())
        settings = settings["data"][0]
        settings = json.loads(settings['set_content'])
        settings['version'] = ""
        return settings
    else:
        LOG.info("未输入服务码")
        return "未输入服务码！"

@post("/user/settings")
def user_settings_update():
    if isLogin():
        try:
            # 获取请求数据
            reqData = request.forms
            hosts = reqData.get("hosts")
            hosts = json.loads(hosts)    
            activehost = reqData.get("activehost")

            # 获取数据库数据
            settings = pool.execute("select set_content from settings where set_name = 'system'", ())
            settings = settings["data"][0]
            settings = json.loads(settings['set_content'])

            # 修改值
            settings['hosts'] = hosts
            settings['activehost'] = activehost

            # 写入数据库数据
            settings = json.dumps(settings)
            result = pool.execute("update settings set set_content = ? where set_name = ?", (settings ,'system'))
            print(result['row'])

            return result
        except Exception as e:
            LOG.error(e)
    else:
        LOG.info("未输入服务码")
        return "未输入服务码！"


