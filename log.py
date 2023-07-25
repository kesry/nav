"""
日志模块，用于写入日志
"""

from conf import config
import logging
from logging.handlers import TimedRotatingFileHandler

# 前置数据初始化
LOG_CONFIG = config['server']['log'];

"""
%(asctime)s 字符串形式的当前时间。默认格式是“2021-09-08 16:49:45,896”。逗号后面的是毫秒
%(created)f 时间戳, 等同于time.time()
%(relativeCreated)d 日志发生的时间相对于logging模块加载时间的相对毫秒数
%(msecs)d 日志时间发生的毫秒部分
%(levelname)s 日志级别str格式
%(levelno)s 日志级别数字形式(10, 20, 30, 40, 50)
%(name)s 日志器名称, 默认root
%(message)s 日志内容
%(pathname)s 日志全路径
%(filename)s 文件名含后缀
%(module)s 文件名不含后缀
%(lineno)d 调用日志记录函数源代码的行号
%(funcName)s 调用日志记录函数的函数名
%(process)d 进程id
%(processName)s 进程名称
%(thread)d 线程ID
%(threadName)s 线程名称
"""

formatter = '[%(levelname)s]%(asctime)s:%(msecs)s.%(process)d,%(thread)d#>[%(funcName)s]:%(lineno)s  %(message)s'
fmt = logging.Formatter(formatter)

handler = TimedRotatingFileHandler(LOG_CONFIG['path'], when='D')
handler.setFormatter(fmt)
# handler.setLevel(LOG_CONFIG['level'])

# 输出到控制台
console = logging.StreamHandler()
console.setFormatter(fmt)
console.setLevel(LOG_CONFIG['level'])

LOG = logging.getLogger('server')
print(LOG_CONFIG)
LOG.setLevel(LOG_CONFIG['level'])
LOG.addHandler(handler)
LOG.addHandler(console)


