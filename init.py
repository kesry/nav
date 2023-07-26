import sqlite3
import os
from conf import config

INIT_SQL = '''
    create table if not exists nav(
        navid integer primary key autoincrement,
        navname varchar(255) not null,
        navpath varchar(255) not null,
        picpath varchar(255),
        picbase64 varchar(2000),
        openstatus tinyint default 1, -- 1 - 打开；0 - 关闭
        navtype tinyint default 0 -- 0 - 内网；1 - 外网 
    );
'''

def row_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init():
    print(f"当前版本: {os.getenv('VERSION')}")
    filepath = os.path.join(os.getcwd(), "db/nav.db")
    print(f"数据库文件保存在:{filepath}")
    conn = sqlite3.connect(filepath)
    conn.row_factory = row_factory
    cursor = conn.cursor()
    cursor.executescript(INIT_SQL)
    print("*" * 10,end="")
    print("初始化数据库：",end="")
    print("*" * 10)

    print(f"服务码: {config['confirm']}")

    print("*" * 10,end="")
    print("数据库初始化成功！：",end="")
    print("*" * 10)

    print("*" * 10,end="")
    print("初始化日志！", end="")
    print("*" * 10)

    with open("./logs/nav.log", mode="a") as f:
        f.write("")

    print("*" * 10,end="")
    print("日志文件创建完毕！", end="")
    print("*" * 10)
    cursor.close()
    conn.commit()
    conn.close()

