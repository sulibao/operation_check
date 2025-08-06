# -*- coding: utf-8 -*-
import psutil
import platform
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_info.txt"),
        logging.StreamHandler()
    ]
)

def get_system_info():
    info = {}
    info['CPU使用率'] = psutil.cpu_percent(interval=1)
    info['CPU物理核数'] = psutil.cpu_count(logical=False)
    info['CPU逻辑核数'] = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()
    info['内存总量(GB)'] = round(mem.total / (1024**3), 2)
    info['内存剩余可使用量(GB)'] = round(mem.available / (1024**3), 2)
    info['内存使用率(%)'] = mem.percent

    if platform.system() == 'Windows':
        disk_usage = psutil.disk_usage('C:')
    else:
        disk_usage = psutil.disk_usage('/')
    info['根分区磁盘总量(GB)'] = round(disk_usage.total / (1024**3), 2)
    info['根分区磁盘使用量(GB)'] = round(disk_usage.used / (1024**3), 2)
    info['根分区磁盘剩余可使用量(GB)'] = round(disk_usage.free / (1024**3), 2)
    info['根分区磁盘使用率(%)'] = disk_usage.percent

    net_io = psutil.net_io_counters()
    info['网络流量流出(GB)'] = round(net_io.bytes_sent / (1024**3), 2)
    info['网络流量流入(GB)'] = round(net_io.bytes_recv / (1024**3), 2)

    boot_time_timestamp = psutil.boot_time()
    info['系统上次开机时间(年-月-日 时-分-秒)'] = datetime.fromtimestamp(boot_time_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return info

def main():
    logging.info("开始收集系统信息...")
    system_info = get_system_info()
    logging.info("系统信息收集完成：")
    for key, value in system_info.items():
        logging.info(f"  {key}: {value}")
    logging.info("系统信息已记录到 system_info.txt 文件中。")

if __name__ == "__main__":
    main()