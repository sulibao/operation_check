# operation_check

# 功能背景

1.此代码项目用于对Linux设备的系统相关信息进行查询输出，可以作为自动化巡检的一个参考。

2.涉及到以下几项的查询操作

- 设备的OS信息、主机名、内核版本
- 操作系统登录用户、系统已运行时间、系统平均负载
- 内存和交换空间的使用情况、内存使用率前5的进程信息
- CPU使用情况, CPU使用率前5的进程信息
- 磁盘和Inode的使用情况

3.建议环境

```bash
python >= 3.12.0 版本
pip >= 3 版本
```
# 使用方式

1.运行演示

```python
'''将文件下载/复制/拉取倒服务器上，执行python3 Linux_check.py即可'''
python3 Linux_check.py 
检查信息成功保存至 ./system_info.txt 文件
```

2.运行结果实例

```bash
root@sulibao-None:/home/sulibao/python# python3 Linux_check.py 

检查信息成功保存至 ./system_info.txt 文件
root@sulibao-None:/home/sulibao/python# cat system_info.txt 
============================================获取操作系统的参数信息=============================================

=============================================获取操作系统的OS==============================================

主机名: sulibao-None, OS类型和版本: Ubuntu 24.04.2 LTS, 系统内核版本: 6.8.0-71-generic。

===========================================获取操作系统的运行相关信息============================================

登录的用户列表如下:
sulibao  seat0        2025-08-05 09:02 (login screen)
sulibao  tty2         2025-08-05 09:02 (tty2)
sulibao  pts/2        2025-08-05 11:33
sulibao  pts/3        2025-08-05 11:36 (192.168.2.2)
sulibao  pts/4        2025-08-05 11:48 (192.168.2.2)
 
系统已经运行了0天 2小时 46分钟, 系统平均负载为(1m/5m/15m): 0.00, 0.03, 0.12

============================================内存和交换空间的使用情况============================================

内存总量 7.7G, 剩余可使用量 4.10G, 剩余可使用内存比例 53.25%;
交换空间总量为 4.0G, 剩余可使用交换空间比例 100.0%

系统中内存使用量前五名(从高至低):
USER       PID    %MEM   COMMAND
sulibao    4977   17.5   /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/node /home/sulibao/.vscode-server/extensions/ms-python.vscode-pylance-2025.7.1/dist/server.bundle.js --cancellationReceive=file:561ef9c9fed294e242a32bb1fe3d2efd23b18c9214 --node-ipc --clientProcessId=4699
sulibao    4699   9.3    /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/node --dns-result-order=ipv4first /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/out/bootstrap-fork --type=extensionHost --transformURIs --useHostProxy=false
sulibao    3449   3.5    /usr/bin/gnome-shell
1001       2556   1.7    /opt/bitnami/minio/bin/minio server --certs-dir /certs --console-address :9001 --address :9000 /bitnami/minio/data
sulibao    3669   1.4    /usr/libexec/evolution-data-server/evolution-alarm-notify

=============================================CPU信息和使用情况=============================================

系统CPU的型号为:Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz, 系统CPU核数为:4, CPU使用率为:0%

系统中CPU使用量前五名(从高至低):
USER       PID    %CPU   COMMAND
root       16076  200    ps aux --sort=-%cpu --no-headers
sulibao    4977   17.6   /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/node /home/sulibao/.vscode-server/extensions/ms-python.vscode-pylance-2025.7.1/dist/server.bundle.js --cancellationReceive=file:561ef9c9fed294e242a32bb1fe3d2efd23b18c9214 --node-ipc --clientProcessId=4699
sulibao    4699   2.7    /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/node --dns-result-order=ipv4first /home/sulibao/.vscode-server/cli/servers/Stable-488a1f239235055e34e673291fb8d8c810886f81/server/out/bootstrap-fork --type=extensionHost --transformURIs --useHostProxy=false
root       16068  1.8    python3 Linux_check.py
sulibao    4534   1.0    sshd: sulibao@notty

===============================================磁盘使用情况===============================================

Filesystem           Size     Used     Avail    Use%   Mounted on

----------------------------------------------------------------------------------------------------

tmpfs                790M     2.2M     788M     1%     /run

/dev/sda2            30G      18G      11G      63%    /

tmpfs                3.9G     0        3.9G     0%     /dev/shm

tmpfs                5.0M     8.0K     5.0M     1%     /run/lock

overlay              30G      18G      11G      63%    /data/docker_data/overlay2/1166005196fc6867b5bf4c8006b2f0bed44b03eaf6cfc373f6f6ea4defa10b41/merged

overlay              30G      18G      11G      63%    /data/docker_data/overlay2/d16527bcfad68e85c83dc2580c5fb8c2a1cfb2767f3787e07aabadb7a8ddea27/merged

tmpfs                790M     124K     790M     1%     /run/user/1000

/dev/sr0             4.9G     4.9G     0        100%   /media/sulibao/Ubuntu

=============================================inode使用情况==============================================

Filesystem           Inodes   Used     Free     Use%   Mounted on

----------------------------------------------------------------------------------------------------

tmpfs                987K     1.4K     986K     1%     /run

/dev/sda2            1.9M     289K     1.6M     16%    /

tmpfs                987K     1        987K     1%     /dev/shm

tmpfs                987K     5        987K     1%     /run/lock

overlay              1.9M     289K     1.6M     16%    /data/docker_data/overlay2/1166005196fc6867b5bf4c8006b2f0bed44b03eaf6cfc373f6f6ea4defa10b41/merged

overlay              1.9M     289K     1.6M     16%    /data/docker_data/overlay2/d16527bcfad68e85c83dc2580c5fb8c2a1cfb2767f3787e07aabadb7a8ddea27/merged

tmpfs                198K     165      198K     1%     /run/user/1000

/dev/sr0             0        0        0        -      /media/sulibao/Ubuntu

====================================================================================================root@sulibao-None:/home/sulibao/python# 
```