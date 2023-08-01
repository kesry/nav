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
    print(f"confirm = {confirm_post}")
    print(f"server = {config['confirm']}")
    if confirm_post == config["confirm"]:
        response.set_cookie("confirm", confirm_post)
        return "yes"
    else:
        return "no"

@get("/nav/section/<opr>")
def write_section(opr):
    print(f"当前操作为：{opr}")
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
            print(f"filepath = {filepath};filename = {filename}")
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
        print(f"total = {total}")
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
    print(navid)
    if navid and isLogin():
        conn = pool.getConn()
        print(type(navid))
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
    sql = "update nav set navname = ?, navpath = ?, picpath = ?, picbase64 = ?, navtype = ? where navid = ?";
    conn = pool.getConn()
    result = conn.execute(sql, (
        nav.get("navname"), nav.get("navpath"), nav.get("picpath"), nav.get("picbase64"), nav.get("navtype"), nav.get("navid")))
    pool.release(conn)
    return result