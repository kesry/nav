from bottle import route, template, get, post, request, static_file, response
from db import pool
from conf import config
from log import LOG


@post("/api/nav/edit")
def remote_update():
    new_info = request.forms
    if new_info.get("confirm") == config["confirm"]:
        if len(pool.execute("select navid from nav where navid = ?", (new_info.get("navid"),))["data"]) > 0:
            sql = "update nav set navpath = ? where navid = ?"
            if pool.execute(sql, (new_info.get("navpath"), new_info.get("navid")))["row"] > 0:
                return "success"
        return "update fail"
    else:
        return "Invalid requests"


@get("/api/nav/<navid>")
def remote_get_navpath(navid):
    confirm = request.query.confirm
    if confirm != config["confirm"]:
        return "验证失败！"
    try:
        navid = int(navid)
        if navid < 1:
            return "id不能小于1"
        result = pool.execute("select navpath from nav where navid = ?", (navid,))
        print(result['data'])
        if len(result['data']) > 0:
            return result['data'][0]['navpath']
        return "no data"
    except e:
        LOG.error(f"数据值错误：{navid}，错误原因：{e}")
        return "Invalid Request"
        