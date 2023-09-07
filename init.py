import sqlite3
import os
from conf import config
import json

version="3.1.6"
# version=os.getenv("VERSION")

INIT_SQL = ""
with open(os.path.join(os.getcwd(), "db/sql/init.sql"), mode="r", encoding="utf-8") as f:
    INIT_SQL = f.read() 


def row_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init():
    print(f"当前版本: v{version}")
    filepath = os.path.join(os.getcwd(), "db/nav.db")
    print(f"数据库文件保存在:{filepath}")
    conn = sqlite3.connect(filepath)
    conn.row_factory = row_factory
    cursor = conn.cursor()
    cursor.executescript(INIT_SQL)
    cursor.close()
    print("*" * 10,end="")
    print("初始化数据库：",end="")
    print("*" * 10)
    print("*" * 10,end="")
    print("数据库初始化成功！：",end="")
    print("*" * 10)

    print(f"服务码: {config['confirm']}")

    # 初始化服务日志
    log_file = os.path.join(os.getcwd(), "logs/nav.log")
    if not os.path.isfile(log_file):

        print("*" * 10,end="")
        print("初始化服务日志！", end="")
        print("*" * 10)

        with open(log_file, mode="a") as f:
            f.write("")

        print("*" * 10,end="")
        print("日志文件创建完毕！", end="")
        print("*" * 10)

    # 判断是否已经更新
    cursor = conn.cursor()
    cursor.execute("select set_content from settings where set_name = 'system'")
    settings = cursor.fetchone()
    print(f"type: {type(settings)}")
    settings = json.loads(settings['set_content'])
    print(settings)
    print(settings['version'])
    cursor.close()
    if settings['version'] != version:
        update_sql_path = os.path.join(os.getcwd(), f"db/sql/v{version}.sql")
        if os.path.isfile(update_sql_path):
            with open(update_sql_path, mode="r", encoding="utf-8") as f:
                update_sql = f.read()
                cursor = conn.cursor()
                cursor.executescript(update_sql)
                cursor.close()
        else:
            print(f"版本{version}的更新sql不存在！")
    print(f"版本{version}已经更新") 
    conn.commit()
    conn.close()

