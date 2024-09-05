# 参考qlib的loger生成该系统的loger

import logging
import os
import sys
from logging import handlers

# 使用该loger做装饰器修饰其它函数，用于向log文件写入日志

def loger(func):
    def wrapper(*args, **kwargs):
        # 创建logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        # 创建控制台handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        # 创建文件handler
        file_handler = handlers.TimedRotatingFileHandler(
            filename=os.path.join(os.getcwd(), "log.log"),
            when="D",
            interval=1,
            backupCount=7
        )
        file_handler.setLevel(logging.INFO)
        # 创建formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        # 添加handler
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        # 执行函数
        func(*args, **kwargs)
        # 移除handler
        logger.removeHandler(console_handler)
        logger.removeHandler(file_handler)
    return wrapper