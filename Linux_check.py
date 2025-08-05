import re
import platform
import subprocess

def get_device_os():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME'):
                    os_result = line.split('=')[1].strip().strip('"')
                    return f"主机名: {platform.node()}, OS类型和版本: {os_result}, 系统内核版本: {platform.release()}。"
        return "未知的Linux发型版本, 请手动检查!"
    except FileNotFoundError:
        return "没有找到系统OS文件, 请手动查看!"

def convert_to_mb(value, unit):
    if unit == 'G':
        return value * 1024
    elif unit == 'M':
        return value
    else:
        raise ValueError(f"不支持的单位: {unit}")

def parse_memory_value(value_str):
    match = re.match(r'(\d+\.?\d*)([MG])', value_str)
    if not match:
        num_match = re.match(r'(\d+\.?\d*)', value_str)
        if num_match:
            return float(num_match.group(1)), 'M'
        else:
            raise ValueError(f"无法解析内存值: {value_str}")
    return float(match.group(1)), match.group(2)

def get_mem_swap():
    try:
        result = subprocess.check_output(['free', '-h'], text=True)
        lines = result.strip().split('\n')
        if len(lines) < 3:
            raise ValueError("free命令输出格式不符合预期, 行数不足")
        mem_message = lines[1].strip().split()
        swap_message = lines[2].strip().split()
        
        if len(mem_message) < 3:
            raise ValueError("内存信息字段不足")
        if len(swap_message) < 4:
            raise ValueError("交换空间信息字段不足")

        mem_total, mem_total_unit = parse_memory_value(mem_message[1])
        mem_total_mb = convert_to_mb(mem_total, mem_total_unit)

        mem_used, mem_used_unit = parse_memory_value(mem_message[2])
        mem_used_mb = convert_to_mb(mem_used, mem_used_unit)

        mem_can_use_mb = mem_total_mb - mem_used_mb

        mem_can_use = mem_can_use_mb / 1024 if mem_total_unit == 'G' else mem_can_use_mb
        mem_can_use_rate = round((mem_can_use_mb / mem_total_mb) * 100, 2)

        swap_total, swap_total_unit = parse_memory_value(swap_message[1])
        swap_total_mb = convert_to_mb(swap_total, swap_total_unit)

        swap_free, swap_free_unit = parse_memory_value(swap_message[3])
        swap_free_mb = convert_to_mb(swap_free, swap_free_unit)

        if swap_total_mb == 0:
            swap_info = "\n交换空间已关闭"
        else:
            swap_can_use = round((swap_free_mb / swap_total_mb) * 100, 2)
            swap_info = f"\n交换空间总量为 {swap_total}{swap_total_unit}, 剩余可使用交换空间比例 {swap_can_use}%"

        mem_info = (f"内存总量 {mem_total}{mem_total_unit}, "
                   f"剩余可使用量 {mem_can_use:.2f}{mem_total_unit}, "
                   f"剩余可使用内存比例 {mem_can_use_rate}%;")
        return mem_info + swap_info
    except Exception as e:
        return f"获取内存和交换空间使用情况失败: {str(e)}"

def get_system_runmessage():
    try:
        logined_user = subprocess.check_output(['who'],text=True)
        user_list = logined_user.strip()
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            days = int(uptime_seconds // (3600 * 24))
            hours = int((uptime_seconds % (3600 * 24)) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            uptime_str = f"{days}天 {hours}小时 {minutes}分钟"

        result = subprocess.check_output(['uptime'],text=True)
        load_avg = re.search(r'load average: (.*)',result).group(1)

        return f"登录的用户列表如下:\n{logined_user} \n系统已经运行了{uptime_str}, 系统平均负载为(1m/5m/15m): {load_avg}"
    except Exception as e:
        return f"获取系统当前运行信息失败: {str(e)}"


    try:
        result = subprocess.check_output(['free','-h'],text=True)
        lines = result.strip().split('\n')
        mem_message = lines[1].strip().split()
        swap_message = lines[2].strip().split()

        mem_total = float(re.findall(r'\d+\.?\d*', mem_message[1])[0])
        mem_used = float(re.findall(r'\d+\.?\d*', mem_message[2])[0])
        mem_can_use = mem_total - mem_used
        mem_can_use_rate = round(float((mem_can_use) / mem_total) * 100,2)

        swap_total = float(re.findall(r'\d+\.?\d*', swap_message[1])[0])
        swap_free = float(re.findall(r'\d+\.?\d*', swap_message[3])[0])
        if swap_total == 0:
            swap_info = "\n交换空间已关闭"
        else:
            swap_can_use = round((swap_free / swap_total) * 100, 2)
            swap_info = f"\n交换空间总量为 {swap_total}Gi, 剩余可使用交换空间比例 {swap_can_use}%"

        return f"内存总量 {mem_total}Gi,剩余可使用量 {mem_can_use}Gi,剩余可使用内存比例 {mem_can_use_rate}%;\n{swap_info}"
    except Exception as e:
        return f"获取内存和交换空间使用情况失败: {str(e)}"

def get_mem_usagesort(limit=5):
    try:
        result = subprocess.check_output(['ps','aux','--sort=-%mem','--no-headers'],text=True)
        process = result.strip().split('\n')[:limit]
        output = []
        output.append(f"{'USER':<10} {'PID':<6} {'%MEM':<6} COMMAND")
        for proc in process:
            parts = proc.split()
            if len(parts) >= 10:
                output.append(f"{parts[0]:<10} {parts[1]:<6} {parts[3]:<6} {' '.join(parts[10:])}")
        return '\n'.join(output)
    except Exception as e:
        return f"获取内存使用率前五名的进程信息失败: {str(e)}"

def get_cpu_message():
    try:
        module_result = subprocess.check_output(['cat','/proc/cpuinfo'],text=True)
        module_name = re.search(r'model name\s*:\s*(.+)', module_result).group(1)

        cores_result = subprocess.check_output(['nproc'],text=True)
        cores = cores_result.strip()

        cpu_result = subprocess.check_output(['vmstat','1','2'],text=True)
        lines = cpu_result.strip().split('\n')
        stats = lines[-1].split()
        id = int(stats[14])
        usage = 100 - id

        return f"系统CPU的型号为:{module_name}, 系统CPU核数为:{cores}, CPU使用率为:{usage}%"
    except Exception as e:
        return f"获取CPU相关信息失败: {str(e)}"

def get_cpu_usagesort(limit=5):
    try:
        result = subprocess.check_output(['ps','aux','--sort=-%cpu','--no-headers'],text=True)
        process = result.strip().split('\n')[:limit]
        output = []
        output.append(f"{'USER':<10} {'PID':<6} {'%CPU':<6} COMMAND")
        for proc in process:
            parts = proc.split()
            if len(parts) >= 10:
                output.append(f"{parts[0]:<10} {parts[1]:<6} {parts[2]:<6} {' '.join(parts[10:])}")
        return '\n'.join(output)
    except Exception as e:
        return f"获取CPU使用率前五名的进程信息失败: {str(e)}"

def get_disk_usage():
    try:
        result = subprocess.check_output(['df', '-h'], text=True)
        lines = result.strip().split('\n')[1:]
        disks = []
        for line in lines:
            parts = re.split(r'\s+', line)
            if len(parts) >= 6:
                disks.append({
                    'filesystem': parts[0],
                    'size': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'use_percent': parts[4],
                    'mounted_on': parts[5]
                })
        return disks
    except Exception as e:
        return [f"获取磁盘使用情况失败: {str(e)}"]

def get_inode_usage():
    try:
        result = subprocess.check_output(['df', '-i', '-h'], text=True)
        lines = result.strip().split('\n')[1:]
        inodes = []
        for line in lines:
            parts = re.split(r'\s+', line)
            if len(parts) >= 6:
                inodes.append({
                    'filesystem': parts[0],
                    'inodes': parts[1],
                    'used': parts[2],
                    'free': parts[3],
                    'use_percent': parts[4],
                    'mounted_on': parts[5]
                })
        return inodes
    except Exception as e:
        return [f"获取inode使用情况失败: {str(e)}"]

total_width = 100
def add_title(info, title):
    equal_count = (total_width - len(title)) // 2
    line = "=" * equal_count + title + "=" * (total_width - len(title) - equal_count)
    info.append(line)

def main():
    info = []
    add_title(info,"获取操作系统的参数信息")

    add_title(info,"获取操作系统的OS")
    info.append(f"{get_device_os()}")

    add_title(info,"获取操作系统的运行相关信息")
    info.append(f"{get_system_runmessage()}")

    add_title(info,"内存和交换空间的使用情况")
    info.append(f"{get_mem_swap()}")
    info.append(f"系统中内存使用量前五名(从高至低):\n{get_mem_usagesort()}")

    add_title(info,"CPU信息和使用情况")
    info.append(f"{get_cpu_message()}")
    info.append(f"系统中CPU使用量前五名(从高至低):\n{get_cpu_usagesort()}")

    add_title(info,"磁盘使用情况")
    info.append(f"{'Filesystem':<20} {'Size':<8} {'Used':<8} {'Avail':<8} {'Use%':<6} Mounted on")
    info.append("-" * 100)
    for disk in get_disk_usage():
        if isinstance(disk, dict):
            info.append(f"{disk['filesystem']:<20} {disk['size']:<8} {disk['used']:<8} {disk['available']:<8} {disk['use_percent']:<6} {disk['mounted_on']}")
        else:
            info.append(disk)

    add_title(info,"inode使用情况")
    info.append(f"{'Filesystem':<20} {'Inodes':<8} {'Used':<8} {'Free':<8} {'Use%':<6} Mounted on")
    info.append("-" * 100)
    for inode in get_inode_usage():
        if isinstance(inode, dict):
            info.append(f"{inode['filesystem']:<20} {inode['inodes']:<8} {inode['used']:<8} {inode['free']:<8} {inode['use_percent']:<6} {inode['mounted_on']}")
        else:
            info.append(inode)
    add_title(info,"")

    all_info = '\n\n'.join(info)

    try:
        with open('./system_info.txt', 'w', encoding='utf-8') as f:
            f.write(all_info)
        print("\n检查信息成功保存至 ./system_info.txt 文件")
    except Exception as e:
        print(f"\n保存检查信息时出错: {str(e)}")

if __name__ == '__main__':
    main()
