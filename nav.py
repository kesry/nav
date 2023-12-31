from bottle import route, template, get, post, request, static_file, response
from db import pool
from conf import config
from log import LOG


# @route("/user/:username")
# def getUser(username):
#     return template("<h3>用户名:{{username}}</h3>", username=username)


def isLogin():
    confirm_server = config["confirm"]
    confirm_req = request.get_cookie("confirm")
    if confirm_req == confirm_server:
        response.set_cookie("confirm", confirm_server)
        return True
    else:
        return False


@get("/")
def index():
    return staticfile("index.html")


@get("/index")
def index2():
    return staticfile("index.html")


@get("/login")
def islogin():
    confirm_server = config["confirm"]
    confirm_req = request.get_cookie("confirm")
    if confirm_req == confirm_server:
        response.set_cookie("confirm", confirm_server)
        return "yes"
    else:
        return "no"


@get("/admin")
def admin():
    return staticfile("admin.html")


@post("/login")
def dologin():
    confirm_post = request.forms.get("confirm")
    if confirm_post == config["confirm"]:
        response.set_cookie("confirm", confirm_post)
        return "yes"
    else:
        return "no"


@get("/nav/section/<opr>")
def write_section(opr):
    if isLogin():
        return static_file(f"{opr}.html", root=f"./static/section")

    return ""


# 静态资源管理
@route('/<filepath:re:.*[(\.css)|(\.js)|(\.png)|(\.jpg)|(\.gif)|(\.ttf)|(\.txt)|(\.ico)|(\.html)]$>')
def staticfile(filepath):
    i = filepath.rfind("/")
    if i != -1:
        filename = filepath[(i + 1):]
        filepath = filepath[:i]
        if filepath.lower().endswith("section"):
            return "Invalid request!"
    else:
        filename = filepath
        filepath = ""
    return static_file(filename, root=f"./static/{filepath}")


@get("/nav")
def navs():
    page = request.query.page
    size = request.query.size
    if not page or not size:
        return "Invalid Data"

    page = int(page)
    size = int(size)
    if page and size:
        conn = pool.getConn()
        sql = "select * from nav limit ? offset ? "
        result = conn.execute(sql, (size, (page - 1) * size))

        # 如果result中的数据量小于size，则必定没有下一页
        total_res = pool.execute("select 1 from nav")
        total = len(total_res["data"])
        if total > size * page:
            result["hasNext"] = 1
        else:
            result["hasNext"] = 0

        pool.release(conn)
        return result
    else:
        LOG.warn("Invalid Data!")
        return "非法数据！"


@post("/nav/add")
def add_nav():
    nav = request.forms
    sql = "insert into nav(navname, navpath, picpath, picbase64, navtype) values(?, ?, ?, ?, ?)";
    conn = pool.getConn()
    result = conn.execute(sql, (
        nav.get("navname"), nav.get("navpath"), nav.get("picpath"), nav.get("picbase64"), nav.get("navtype")))
    pool.release(conn)
    return result


@post("/nav/del")
def del_nav():
    navid = int(request.forms.get("navid"))
    if navid and isLogin():
        conn = pool.getConn()
        result = conn.execute("delete from nav where navid = ?", (navid,))
        pool.release(conn)
        return result
    else:
        LOG.warn("Invalid Request")
        return "Invalid Request"


@post("/nav/edit")
def edit_nav():
    if not isLogin():
        LOG.warn("Invalid Request!")
        return "Invalid Request!"

    nav = request.forms
    sql = "update nav set navname = ?, navpath = ?, picpath = ?, picbase64 = ?, navtype = ?, openstatus = ? where navid = ?"
    conn = pool.getConn()
    result = conn.execute(sql, (
        nav.get("navname"), nav.get("navpath"), nav.get("picpath"), nav.get("picbase64"), nav.get("navtype"), nav.get("openstatus"),
        nav.get("navid")))
    pool.release(conn)
    return result

@post("/nav/<navid>/<opr>")
def nav_change_status(navid, opr):
    if not isLogin():
        LOG.warn("Invalid Request!Not Login!")
        return "Invalid Request!Not Login!"
    print(f"navid = {navid}, opr = {opr}")
    if opr != 'open' and opr != 'close':
        response.status = 404
        return '404'
    
    try:
        navid = int(navid)
        if navid < 1 :
            return "id不能小于1"
        
        status = 1
        if opr == 'close':
            status = 0
        
        sql = "update nav set openstatus = ? where navid = ?"
        return pool.execute(sql,(status, navid))
                          
    except Exception as e:
        LOG.error(f"数据值错误：{navid}，错误原因：{e}")
        return "Invalid Request"
    
    
