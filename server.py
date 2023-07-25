# 导入service中的route

import nav
from bottle import run


class Server(object):
    def __init__(self, config={'port': 8080, 'host': 'localhost'}):
        self.port = config['port']
        self.host = config['host']
        self.config = config;

    def start(self):
        run(host=self.host, port=self.port)
