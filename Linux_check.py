import psutil
import distro
import platform
import logging
from datetime import datetime
import subprocess

# 配置日志：仅模块标题和状态日志带时间戳
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # 带时间戳格式
    handlers=[
        logging.FileHandler('system_monitor.log'),
    ]
)

def get_os_info():
    try:
        os_info = {
            'system': platform.system(),
            'node_name': platform.node(),
            'release': platform.release(),
            'distro_name': distro.name(),
            'distro_version': distro.version(), 
            'machine': platform.machine()
        }
        logging.info("成功获取到OS信息")  # 状态日志（带时间）
        return os_info
    except Exception as e:
        logging.error(f"获取OS信息失败: {str(e)}")
        return None

def get_login_users():
    try:
        users = psutil.users()
        user_info = []
        for user in users:
            user_info.append({
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
            })
        logging.info("成功获取登录用户信息")
        return user_info
    except Exception as e:
        logging.error(f"获取登录用户信息失败: {e}")
        return None

def get_system_uptime():
    try:
        boot_time = psutil.boot_time()
        boot_time_dt = datetime.fromtimestamp(boot_time)
        now = datetime.now()
        uptime = now - boot_time_dt
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
        logging.info("成功获取系统运行时间")
        return {
            'boot_time': boot_time_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'uptime': uptime_str
        }
    except Exception as e:
        logging.error(f"获取系统运行时间失败: {e}")
        return None

def get_load_average():
    try:
        load_avg = psutil.getloadavg()
        cpu_count = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True)
        load_info = {
            '1min': load_avg[0],
            '5min': load_avg[1],
            '15min': load_avg[2],
            '1min_percent': (load_avg[0] / cpu_count) * 100 if cpu_count > 0 else 0,
            '5min_percent': (load_avg[1] / cpu_count) * 100 if cpu_count > 0 else 0,
            '15min_percent': (load_avg[2] / cpu_count) * 100 if cpu_count > 0 else 0
        }
        logging.info("成功获取系统平均负载")
        return load_info
    except Exception as e:
        logging.error(f"获取系统平均负载失败: {e}")
        return None

def get_memory_info():
    try:
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        
        memory_info = {
            'virtual': {
                'total': virtual_mem.total,
                'available': virtual_mem.available,
                'used': virtual_mem.used,
                'used_percent': virtual_mem.percent,
                'free': virtual_mem.free
            },
            'swap': {
                'total': swap_mem.total,
                'used': swap_mem.used,
                'used_percent': swap_mem.percent,
                'free': swap_mem.free,
                'sin': swap_mem.sin,
                'sout': swap_mem.sout
            }
        }
        logging.info("成功获取内存和交换空间信息")
        return memory_info
    except Exception as e:
        logging.error(f"获取内存和交换空间信息失败: {e}")
        return None

def get_top_memory_processes(count=5):
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'memory_info']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'memory_percent': proc.info['memory_percent'],
                    'memory_used': proc.info['memory_info'].rss
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        logging.info(f"成功获取内存使用率最高的{count}个进程")
        return processes[:count]
    except Exception as e:
        logging.error(f"获取内存使用率最高的进程失败: {e}")
        return None

def get_cpu_info():
    try:
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_per_core = psutil.cpu_percent(percpu=True, interval=0)
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            'physical_cores': physical_cores,
            'logical_cores': logical_cores,
            'total_percent': cpu_percent,
            'per_core_percent': cpu_per_core,
            'frequency': {
                'current': cpu_freq.current,
                'min': cpu_freq.min,
                'max': cpu_freq.max
            }
        }
        logging.info("成功获取CPU信息")
        return cpu_info
    except Exception as e:
        logging.error(f"获取CPU信息失败: {e}")
        return None

def get_top_cpu_processes(count=5):
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                proc.cpu_percent(interval=0.1)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        psutil.cpu_percent(interval=1)
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'cpu_percent': proc.info['cpu_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        logging.info(f"成功获取CPU使用率最高的{count}个进程")
        return processes[:count]
    except Exception as e:
        logging.error(f"获取CPU使用率最高的进程失败: {e}")
        return None

def get_disk_info():
    try:
        disk_info = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'mountpoint': partition.mountpoint,
                    'total': usage.total,
                    'used': usage.used,
                    'used_percent': usage.percent,
                    'free': usage.free
                })
            except (PermissionError, OSError):
                continue
        logging.info("成功获取磁盘使用情况")
        return disk_info
    except Exception as e:
        logging.error(f"获取磁盘使用情况失败: {e}")
        return None

def get_inode_info():
    try:
        # 用 universal_newlines=True 替代 text=True，兼容Python 3.6及以下版本
        result = subprocess.run(
            ['df', '-i'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # 替代 text=True，将输出转为字符串
            check=True
        )
        output = result.stdout
        inode_info = []
        lines = output.strip().split('\n')[1:]
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 6:
                inode_info.append({
                    'filesystem': parts[0],
                    'inodes_total': parts[1],
                    'inodes_used': parts[2],
                    'inodes_free': parts[3],
                    'inodes_used_percent': parts[4],
                    'mountpoint': parts[5]
                })
        
        logging.info("成功获取Inode使用情况")
        return inode_info
    except Exception as e:
        logging.error(f"获取Inode使用情况失败: {e}")
        return None


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def print_system_info():
    # 打开日志文件，用于写入模块内无时间戳的内容
    with open('system_monitor.log', 'a', encoding='utf-8') as f:
        # 报告头部（带时间戳）
        logging.info("=" * 50)
        logging.info(f"系统信息报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("=" * 50)
        f.write("\n" + "=" * 50 + "\n")  # 无时间戳分隔线

        # 1. 操作系统信息（模块标题带时间，内容无时间）
        logging.info("1. 操作系统信息")  # 模块标题（带时间）
        f.write("=" * 125 + "\n")  # 模块内分隔线（无时间）
        os_info = get_os_info()
        if os_info:
            f.write(
                f"系统OS信息如下:\n\n"
                f"操作系统: {os_info['system']}\n"
                f"主机名: {os_info['node_name']}\n"
                f"内核版本: {os_info['release']}\n"
                f"发行版名称: {os_info['distro_name']}\n"
                f"发行版版本: {os_info['distro_version']}\n"
                f"机器类型: {os_info['machine']}\n"
            )

        # 2. 登录用户信息
        logging.info("2. 登录用户信息")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        users = get_login_users()
        if users:
            f.write(f"当前系统登录用户如下:\n\n")
            for i, user in enumerate(users, 1):
                f.write(
                    f"用户 {i}:\n"
                    f"  用户名: {user['name']}\n"
                    f"  终端: {user['terminal'] or 'N/A'}\n"
                    f"  主机: {user['host'] or 'N/A'}\n"
                    f"  登录时间: {user['started']}\n"
                )
        else:
            f.write("没有获取到登录用户信息\n")

        # 3. 系统运行时间与平均负载
        logging.info("3. 系统运行时间与平均负载")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        uptime = get_system_uptime()
        if uptime:
            f.write(
                f"系统运行相关信息如下:\n\n"
                f"启动时间: {uptime['boot_time']}\n"
                f"运行时间: {uptime['uptime']}\n"
            )
        load_avg = get_load_average()
        if load_avg:
            f.write(
                f"\n系统平均负载:\n"
                f"  1分钟负载: {load_avg['1min']:.2f} ({load_avg['1min_percent']:.1f}%)\n"
                f"  5分钟负载: {load_avg['5min']:.2f} ({load_avg['5min_percent']:.1f}%)\n"
                f"  15分钟负载: {load_avg['15min']:.2f} ({load_avg['15min_percent']:.1f}%)\n"
            )

        # 4. 内存和交换空间信息
        logging.info("4. 内存和交换空间信息")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        memory_info = get_memory_info()

        if memory_info:
            f.write(f"内存和交换空间使用情况如下:\n\n")
            f.write(
                f"物理内存:\n"
                f"  总计: {format_size(memory_info['virtual']['total'])}\n"
                f"  可用: {format_size(memory_info['virtual']['available'])}\n"
                f"  已使用: {format_size(memory_info['virtual']['used'])} ({memory_info['virtual']['used_percent']}%)\n"
                f"  空闲: {format_size(memory_info['virtual']['free'])}\n"
            )
            f.write(
                f"\n交换空间:\n"
                f"  总计: {format_size(memory_info['swap']['total'])}\n"
                f"  已使用: {format_size(memory_info['swap']['used'])} ({memory_info['swap']['used_percent']}%)\n"
                f"  空闲: {format_size(memory_info['swap']['free'])}\n"
                f"  从磁盘换入: {format_size(memory_info['swap']['sin'])}\n"
                f"  换出到磁盘: {format_size(memory_info['swap']['sout'])}\n"
            )

        # 5. 内存使用率最高的5个进程
        logging.info("5. 内存使用率最高的5个进程")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        top_mem_procs = get_top_memory_processes()
        if top_mem_procs:
            f.write(f"内存使用率最高的5个进程信息如下:\n\n{'PID':<8} {'username':<12} {'mem_used_percent':<18} {'mem_used':<15} {'process_name':<15}\n")
            f.write("-" * 125 + "\n")
            for proc in top_mem_procs:
                f.write(f"{proc['pid']:<8} {str(proc['username'])[:10]:<12} {proc['memory_percent']:<18.2f} {format_size(proc['memory_used']):<15} {proc['name'][:18]:<15}\n")
        else:
            f.write("没有获取到进程内存使用信息\n")

        # 6. CPU使用情况
        logging.info("6. CPU使用情况")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        cpu_info = get_cpu_info()
        if cpu_info:
            f.write(
                f"CPU使用情况如下:\n\n"
                f"物理核心数: {cpu_info['physical_cores']}\n"
                f"逻辑核心数: {cpu_info['logical_cores']}\n"
                f"总CPU使用率: {cpu_info['total_percent']}%\n"
            )
            f.write("\n各核心CPU使用率:\n")
            for i, percent in enumerate(cpu_info['per_core_percent'], 1):
                f.write(f"  核心 {i}: {percent}%\n")
            
            f.write(
                f"\nCPU频率:\n"
                f"  当前: {cpu_info['frequency']['current']:.2f} MHz\n"
                f"  最小: {cpu_info['frequency']['min']:.2f} MHz\n"
                f"  最大: {cpu_info['frequency']['max']:.2f} MHz\n"
            )

        # 7. CPU使用率最高的5个进程
        logging.info("7. CPU使用率最高的5个进程")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        top_cpu_procs = get_top_cpu_processes()
        if top_cpu_procs:
            f.write(f"CPU使用率最高的5个进程信息如下:\n\n{'PID':<8} {'username':<15} {'cpu_used(%)':<15} {'process_name':<20}\n")
            f.write("-" * 125 + "\n")
            for proc in top_cpu_procs:
                f.write(f"{proc['pid']:<8} {str(proc['username'])[:13]:<15} {proc['cpu_percent']:<15.2f} {proc['name'][:18]:<20}\n")
        else:
            f.write("没有获取到进程CPU使用信息\n")

        # 8. 磁盘使用情况
        logging.info("8. 磁盘使用情况")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        disk_info = get_disk_info()
        if disk_info:
            f.write(f"磁盘使用情况如下:\n\n{'Device':<20} {'Filesystem':<15} {'Mounted on':<25} {'Size':<15} {'Used':<15} {'Used_percent(%)':<20} {'Free':<15}\n")
            f.write("-" * 125 + "\n")
            for disk in disk_info:
                f.write(f"{disk['device'][:18]:<20} {disk['fstype'][:8]:<15} {disk['mountpoint'][:18]:<25} {format_size(disk['total']):<15} {format_size(disk['used']):<15} {(disk['used_percent']):<20} {format_size(disk['free']):<15}\n")

        # 9. Inode使用情况
        logging.info("9. Inode使用情况")  # 模块标题（带时间）
        f.write("\n" + "=" * 125 + "\n")
        inode_info = get_inode_info()
        if inode_info:
            f.write(f"Inode使用情况如下:\n\n{'Filesystem':<15} {'Total_inodes':<15} {'Used_inodes':<15} {'Free_inodes':<15} {'used_percent(%)':<20} {'Mounted on':<20}\n")
            f.write("-" * 125 + "\n")
            for inode in inode_info:
                f.write(f"{inode['filesystem'][:18]:<15} {inode['inodes_total']:<15} {inode['inodes_used']:<15} {inode['inodes_free']:<15} {inode['inodes_used_percent']:<20} {inode['mountpoint'][:18]:<20}\n")

        # 报告结尾
        f.write("\n" + "=" * 125 + "\n")
        f.write("系统信息报告结束\n")
        f.write("=" * 125 + "\n")

if __name__ == "__main__":
    print_system_info()