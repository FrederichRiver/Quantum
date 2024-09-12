import imp
import time
import psutil
import platform
import matplotlib.pyplot as plt

class SystemMonitor(object):
    def __init__(self) -> None:
        self.system_info = {}
        self.system_info['os'] = f"{platform.system()} {platform.release()}"
        self.system_info['processor'] = platform.processor()
        self.cpu_physical_cores = psutil.cpu_count(logical=False)
        self.cpu_logical_cores = psutil.cpu_count(logical=True)
        self.cpu_freq_mhz = psutil.cpu_freq().current
        mem = psutil.virtual_memory()
        self.total_memory_GByte = mem.total / 1024 / 1024 / 1024
        self.free_memory_GByte = mem.available / 1024 / 1024 / 1024
        self.used_memory_GByte = mem.used / 1024 / 1024 / 1024
        self.memory_percent = mem.percent
        self.total_disk_GByte = 0.0
        self.free_disk_GByte = 0.0
        self.used_disk_GByte = 0.0
        self.disk_percent = 0.0
    
    def __str__(self) -> str:
        return (
            f"System: {self.system_info['os']}\n"
            f"CPU architure: {self.system_info['processor']}\n"
            f"Physical cores: {self.cpu_physical_cores}\n"
            f"Logical cores: {self.cpu_logical_cores}\n"
            f"CPU frequency: {self.cpu_freq_mhz:.1f}Mhz\n"
            f"Total memory: {self.total_memory_GByte:.1f}GB\n"
            )

    def get_memory_info(self):
        mem = psutil.virtual_memory()
        self.free_memory_GByte = mem.available * (9.31E-10)
        self.used_memory_GByte = mem.used * (9.31E-10)
        self.memory_percent = mem.percent

    def get_disk_info(self):
        total, used, free, percentage = psutil.disk_usage('/')
        self.total_disk_GByte = total * (9.31E-10)
        self.free_disk_GByte = free * (9.31E-10)
        self.used_disk_GByte = used * (9.31E-10)
        self.disk_percent = percentage

    # report_disk_info方法将get_disk_info方法获得的数据转换为报告输出
    def report_disk_info(self):
        self.get_disk_info()
        # 将total转换为GB
        timestamp = time.strftime('%Y-%m-%d', time.localtime())
        sizes = [self.used_disk_GByte, self.free_disk_GByte]
        explode = (0, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=None, autopct='%1.1f%%', shadow=False, startangle=90)
        ax1.axis('equal')
        plt.title(f"Disk usage on {timestamp}")
        # 以当前时间戳为文件名保存图片
        plt.savefig(f"disk_usage_{timestamp}.png")
        plt.close()


def memoryMonitor():
    # 使用SystemMonitor类每隔1分钟获取一次内存信息
    # 将内存信息保存到sqlite数据库里
    # 从数据库中调出内存使用率数据，绘制内存使用率曲线图
    create_db()
    cnt = 1000
    while cnt:
        save_memory_info()
        cnt -= 1
        time.sleep(1)
    plot_memory_usage()

import sqlite3
import psutil
import time
import matplotlib.pyplot as plt
from datetime import datetime
import platform

def create_db():
    conn = sqlite3.connect('memory_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_usage (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            memory_percent REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_memory_info():
    monitor = SystemMonitor()
    memory_percent = monitor.memory_percent
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('memory_usage.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO memory_usage (timestamp, memory_percent)
        VALUES (?, ?)
    ''', (timestamp, memory_percent))
    conn.commit()
    conn.close()

def retrieve_memory_data():
    conn = sqlite3.connect('memory_usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, memory_percent FROM memory_usage')
    data = cursor.fetchall()
    conn.close()
    return data

def plot_memory_usage():
    data = retrieve_memory_data()
    timestamps = [row[0] for row in data]
    memory_percent = [row[1] for row in data]
    plt.plot(timestamps, memory_percent)
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory Usage Over Time')
    plt.xticks([10, len(timestamps)-1])
    plt.tight_layout()
    plt.savefig('memory_usage.png')
    plt.close()


# 生成unittest测试代码

import unittest
# from utils.system_rs import SystemMonitor

class TestSystemMonitor(unittest.TestCase):
    def test_get_disk_info(self):
        monitor = SystemMonitor()
        monitor.get_disk_info()
        self.assertGreater(monitor.total_disk_GByte, 0)
        self.assertGreater(monitor.free_disk_GByte, 0)
        self.assertGreater(monitor.used_disk_GByte, 0)
        self.assertGreater(monitor.disk_percent, 0)
    
    def test_report_disk_info(self):
        monitor = SystemMonitor()
        monitor.report_disk_info()
    
    def test_get_system_info(self):
        monitor = SystemMonitor()
        monitor.get_memory_info()
        self.assertGreater(monitor.total_memory_GByte, 0)
        self.assertGreater(monitor.free_memory_GByte, 0)
        self.assertGreater(monitor.used_memory_GByte, 0)
        self.assertGreater(monitor.memory_percent, 0)

if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(TestSystemMonitor('test_get_disk_info'))
    # suite.addTest(TestSystemMonitor('test_report_disk_info'))
    # suite.addTest(TestSystemMonitor('test_get_system_info'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    memoryMonitor()
