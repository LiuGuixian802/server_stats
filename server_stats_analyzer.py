import psutil
import time
from tabulate import tabulate
import os

def bytes_to_mb(bytes_val):
    return round(bytes_val / (1024 * 1024), 2)

def get_cpu_info():
    return {
        "CPU 使用率 (%)": psutil.cpu_percent(interval=1),
        "CPU 核心数": psutil.cpu_count(logical=True),
        "CPU 物理核心数": psutil.cpu_count(logical=False)
    }

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "总内存 (MB)": bytes_to_mb(mem.total),
        "已使用内存 (MB)": bytes_to_mb(mem.used),
        "空闲内存 (MB)": bytes_to_mb(mem.available),
        "内存使用率 (%)": mem.percent
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "总磁盘 (GB)": round(disk.total / (1024**3), 2),
        "已使用磁盘 (GB)": round(disk.used / (1024**3), 2),
        "可用磁盘 (GB)": round(disk.free / (1024**3), 2),
        "磁盘使用率 (%)": disk.percent
    }

def get_network_info():
    net = psutil.net_io_counters()
    return {
        "发送数据 (MB)": bytes_to_mb(net.bytes_sent),
        "接收数据 (MB)": bytes_to_mb(net.bytes_recv),
        "发送包数": net.packets_sent,
        "接收包数": net.packets_recv
    }

def get_load_avg():
    if hasattr(os, 'getloadavg'):
        load1, load5, load15 = os.getloadavg()
        return {
            "1分钟负载": load1,
            "5分钟负载": load5,
            "15分钟负载": load15
        }
    else:
        return {"负载": "不可用"}

def print_stats():
    print("\n📊 服务器性能统计信息\n")

    data_sections = {
        "CPU 信息": get_cpu_info(),
        "内存信息": get_memory_info(),
        "磁盘信息": get_disk_info(),
        "网络信息": get_network_info(),
        "系统负载": get_load_avg()
    }

    for section, data in data_sections.items():
        print(f"\n=== {section} ===")
        print(tabulate(data.items(), headers=["指标", "值"], tablefmt="grid"))

if __name__ == "__main__":
    print_stats()
