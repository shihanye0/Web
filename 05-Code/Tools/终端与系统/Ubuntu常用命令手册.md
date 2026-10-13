# Ubuntu 常用命令手册

> 适用于 Ubuntu Server 22.04+，覆盖日常运维、文件管理、服务管理、网络调试等场景。

---

## 1. 文件与目录操作

### 1.1 列出文件 — `ls`

```bash
ls                  # 列出当前目录文件
ls -l               # 详细信息（权限、所有者、大小、时间）
ls -a               # 显示隐藏文件（以 . 开头）
ls -lh              # 人类可读大小（KB/MB/GB）
ls -la              # 组合：详细 + 隐藏
ls -lt              # 按修改时间排序（最新在前）
ls -ltr             # 按修改时间倒序（最旧在前）
ls -R               # 递归列出子目录内容
```

**输出解读**：
```
drwxr-xr-x  2 ubuntu ubuntu  4096 Jun 24 10:00 mydir
│└──┤└──┤└──┤  │    │    │    │    │         │
│ 权限  │     链接数 所有者 组   大小  时间       文件名
│
d=目录, -=文件, l=软链接
r=读(4) w=写(2) x=执行(1)
三组：所有者 | 同组 | 其他人
```

### 1.2 切换目录 — `cd`

```bash
cd /path/to/dir     # 进入绝对路径
cd relative/path    # 进入相对路径
cd ..               # 上一级目录
cd ../..            # 上两级
cd ~                # 家目录（/home/ubuntu）
cd -                # 回到上一次所在的目录
cd                  # 等同于 cd ~
```

### 1.3 显示当前路径 — `pwd`

```bash
pwd                 # 输出如 /home/ubuntu
```

### 1.4 创建目录 — `mkdir`

```bash
mkdir mydir              # 创建单个目录
mkdir -p a/b/c           # 递归创建多级目录（父目录不存在自动创建）
mkdir -m 755 mydir       # 创建时指定权限
```

### 1.5 复制 — `cp`

```bash
cp file1 file2           # 复制文件
cp file1 /dest/dir/      # 复制到目标目录
cp -r dir1 dir2          # 递归复制目录
cp -i file1 file2        # 覆盖前确认
cp -v file1 file2        # 显示复制过程
cp -a dir1 dir2          # 归档复制（保留权限、时间戳等所有属性）
```

### 1.6 移动/重命名 — `mv`

```bash
mv file1 file2           # 重命名
mv file1 /dest/dir/      # 移动到目标目录
mv -i file1 file2        # 覆盖前确认
mv -v file1 file2        # 显示过程
```

### 1.7 删除 — `rm`

```bash
rm file                  # 删除文件
rm -r dir                # 递归删除目录
rm -f file               # 强制删除（不确认）
rm -rf dir               # 强制递归删除（⚠️ 极其危险，无回收站）
rm -i file               # 删除前确认
```

> ⚠️ **`rm -rf /`** 会删除整个系统，绝对不要执行。

### 1.8 创建空文件/更新时间戳 — `touch`

```bash
touch newfile            # 创建空文件（已存在则更新时间戳）
```

### 1.9 查找文件 — `find`

```bash
find /path -name "*.log"            # 按名称查找
find /path -name "*.log" -delete    # 找到并删除
find /path -type f -size +100M      # 找大于 100MB 的文件
find /path -mtime -7                # 7 天内修改过的文件
find /path -user ubuntu             # 某用户的文件
```

### 1.10 创建软链接 — `ln`

```bash
ln -s /target/path /link/name       # 创建软链接（快捷方式）
```

---

## 2. 查看文件内容

### 2.1 全部输出 — `cat`

```bash
cat file                 # 输出整个文件
cat -n file              # 带行号
cat file1 file2          # 合并输出
```

### 2.2 前/后 N 行 — `head` / `tail`

```bash
head -20 file            # 前 20 行
tail -20 file            # 后 20 行
tail -f file             # 实时跟踪文件更新（看日志必备）
tail -f /var/log/syslog  # 实时看系统日志
```

### 2.3 分页查看 — `less`

```bash
less file                # 分页查看
# 快捷键：空格=下一页, b=上一页, q=退出, /keyword=搜索
```

### 2.4 搜索内容 — `grep`

```bash
grep "error" file                # 搜索关键词
grep -i "error" file             # 忽略大小写
grep -n "error" file             # 显示行号
grep -r "error" /var/log/        # 递归搜索目录
grep -rn "error" /var/log/       # 递归 + 行号
grep -c "error" file             # 统计匹配行数
grep -v "debug" file             # 反向匹配（排除 debug 行）
grep -A 3 "error" file           # 匹配行 + 后 3 行
grep -B 3 "error" file           # 匹配行 + 前 3 行
grep -C 3 "error" file           # 匹配行 + 前后各 3 行
```

### 2.5 统计 — `wc`

```bash
wc -l file               # 统计行数
wc -w file               # 统计单词数
wc -c file               # 统计字节数
```

### 2.6 文本替换 — `sed`

```bash
sed 's/old/new/' file              # 替换每行第一个匹配
sed 's/old/new/g' file             # 替换所有匹配（全局）
sed -i 's/old/new/g' file          # 直接修改文件（不加 -i 只输出不改）
sed -i.bak 's/old/new/g' file     # 修改前备份为 file.bak
sed '10,20d' file                  # 删除第 10-20 行
sed -n '10,20p' file               # 只显示第 10-20 行
```

---

## 3. 权限管理

### 3.1 修改权限 — `chmod`

```bash
chmod 755 file           # rwxr-xr-x
chmod 644 file           # rw-r--r--
chmod +x file            # 给所有人加执行权限
chmod u+x file           # 只给所有者加执行权限
chmod -R 755 dir         # 递归修改目录权限
```

**权限数字对照**：

| 数字 | 权限 | 含义 |
|------|------|------|
| 7 | rwx | 读+写+执行 |
| 6 | rw- | 读+写 |
| 5 | r-x | 读+执行 |
| 4 | r-- | 只读 |
| 0 | --- | 无权限 |

**常用组合**：

| 三位数 | 含义 | 使用场景 |
|--------|------|---------|
| 755 | 所有者全权限，其他人读+执行 | 目录、可执行文件 |
| 644 | 所有者读写，其他人只读 | 普通文件 |
| 600 | 只有所有者读写 | 密钥文件（.env、.pem） |
| 700 | 只有所有者全部权限 | 私有目录 |

### 3.2 修改所有者 — `chown`

```bash
chown ubuntu file                # 修改所有者
chown ubuntu:ubuntu file         # 修改所有者和组
chown -R ubuntu:ubuntu dir       # 递归修改目录
```

### 3.3 以管理员执行 — `sudo`

```bash
sudo command                     # 以 root 身份执行
sudo -u username command         # 以指定用户身份执行
sudo su                          # 切换到 root 用户
sudo !!                          # 以 sudo 重试上一条命令
```

---

## 4. 软件包管理 — `apt`

```bash
apt update                       # 更新软件源列表（不升级）
apt upgrade                      # 升级所有已安装的软件
apt install nginx                # 安装软件
apt install -y nginx             # 安装（自动确认）
apt remove nginx                 # 卸载（保留配置）
apt purge nginx                  # 完全卸载（含配置）
apt autoremove                   # 清理不再需要的依赖
apt search nginx                 # 搜索软件包
apt show nginx                   # 查看软件包信息
dpkg -l | grep nginx             # 查看已安装的包
```

---

## 5. 服务管理 — `systemctl`

```bash
systemctl start nginx            # 启动服务
systemctl stop nginx             # 停止服务
systemctl restart nginx          # 重启服务
systemctl reload nginx           # 重新加载配置（不中断服务）
systemctl status nginx           # 查看状态（是否运行、最近日志）
systemctl enable nginx           # 设置开机自启
systemctl disable nginx          # 取消开机自启
systemctl is-active nginx        # 检查是否正在运行
systemctl list-units --type=service  # 列出所有服务
```

**查看服务日志**：
```bash
journalctl -u nginx              # 查看 nginx 全部日志
journalctl -u nginx -f           # 实时跟踪日志
journalctl -u nginx --since today    # 今天的日志
journalctl -u nginx -n 50        # 最近 50 行
journalctl -u nginx --no-pager   # 不分页输出
```

---

## 6. 进程管理

### 6.1 查看进程 — `ps`

```bash
ps aux                           # 查看所有进程
ps aux | grep python             # 过滤某个进程
ps -ef --forest                  # 树状显示进程关系
```

### 6.2 终止进程 — `kill`

```bash
kill PID                         # 发送 SIGTERM（优雅终止）
kill -9 PID                      # 发送 SIGKILL（强制终止）
killall nginx                    # 按进程名终止
pkill -f "uvicorn"               # 按命令行模式终止
```

### 6.3 实时监控 — `top` / `htop`

```bash
top                              # 实时资源监控
htop                             # 更好看的监控（需安装）
# 快捷键：q=退出, k=杀进程, M=按内存排序, P=按CPU排序
```

### 6.4 后台运行 — `nohup` / `&`

```bash
nohup python app.py &            # 后台运行，退出 SSH 不中断
nohup python app.py > app.log 2>&1 &   # 后台运行 + 日志写入文件
```

---

## 7. 网络操作

### 7.1 HTTP 请求 — `curl`

```bash
curl http://localhost:8080            # GET 请求
curl -I http://localhost:8080         # 只看响应头
curl -X POST http://localhost:8080    # POST 请求
curl -d '{"key":"val"}' -H "Content-Type: application/json" URL  # JSON POST
curl -o file.zip URL                  # 下载文件
curl -s URL                           # 静默模式（不显示进度）
curl -sS URL                          # 静默但显示错误
curl -L URL                           # 跟随重定向
curl -v URL                           # 详细模式（调试用）
curl --connect-timeout 5 URL          # 连接超时 5 秒
```

### 7.2 下载文件 — `wget`

```bash
wget URL                          # 下载文件
wget -O newname.zip URL           # 指定保存文件名
wget -c URL                       # 断点续传
wget -q URL                       # 静默模式
```

### 7.3 网络诊断

```bash
ping google.com                   # 测试连通性
ping -c 4 google.com              # 只 ping 4 次
ss -tlnp                          # 查看监听的 TCP 端口
ss -tlnp | grep :80               # 查看 80 端口
netstat -tlnp                     # 同上（旧命令）
nslookup domain.com               # DNS 查询
traceroute google.com             # 路由追踪
```

### 7.4 文件传输 — `scp`

```bash
# 本地 → 服务器
scp file.txt ubuntu@82.157.186.52:/home/ubuntu/
scp -r ./dir ubuntu@82.157.186.52:/home/ubuntu/

# 服务器 → 本地
scp ubuntu@82.157.186.52:/opt/fortune/.env ./
```

---

## 8. 磁盘与存储

```bash
df -h                            # 查看磁盘使用情况（人类可读）
du -sh /path                     # 查看目录大小
du -sh *                         # 当前目录下各项大小
du -sh * | sort -rh | head -10   # 按大小排序，看前 10
lsblk                            # 查看磁盘分区
mount /dev/sdb1 /mnt             # 挂载磁盘
```

---

## 9. 用户管理

```bash
whoami                           # 当前用户名
id                               # 当前用户的 UID、GID、组
passwd                           # 修改当前用户密码
sudo passwd ubuntu               # 修改指定用户密码
useradd -m newuser               # 创建用户（-m 创建家目录）
userdel -r newuser               # 删除用户（-r 删除家目录）
usermod -aG sudo newuser         # 给用户添加 sudo 权限
groups                           # 查看当前用户所属组
```

---

## 10. 压缩与解压

```bash
# tar.gz
tar -czf archive.tar.gz dir/     # 压缩目录
tar -xzf archive.tar.gz          # 解压
tar -xzf archive.tar.gz -C /dest # 解压到指定目录
tar -tzf archive.tar.gz          # 查看压缩包内容

# zip
apt install unzip
zip -r archive.zip dir/           # 压缩
unzip archive.zip                 # 解压
unzip archive.zip -d /dest        # 解压到指定目录
```

**参数说明**：
| 参数 | 含义 |
|------|------|
| `-c` | 创建压缩包 |
| `-x` | 解压 |
| `-z` | gzip 格式 |
| `-f` | 指定文件名 |
| `-v` | 显示过程 |
| `-C` | 指定解压目录 |
| `-t` | 列出内容 |

---

## 11. 常用工具安装

```bash
apt install -y git               # Git 版本控制
apt install -y curl              # HTTP 客户端
apt install -y wget              # 下载工具
apt install -y htop              # 进程监控
apt install -y tree              # 目录树显示
apt install -y vim               # 文本编辑器
apt install -y nano              # 简单编辑器
apt install -y net-tools         # 网络工具（ifconfig 等）
apt install -y software-properties-common  # add-apt-repository
```

---

## 12. 常见运维场景

### 12.1 查看系统信息

```bash
uname -a                         # 内核版本
lsb_release -a                   # Ubuntu 版本
hostnamectl                      # 主机名和系统信息
uptime                           # 运行时间和负载
free -h                          # 内存使用情况
nproc                            # CPU 核心数
```

### 12.2 定时任务 — `cron`

```bash
crontab -e                       # 编辑定时任务
crontab -l                       # 列出定时任务
```

**格式**：`分 时 日 月 周 命令`
```bash
0 2 * * * /backup.sh             # 每天凌晨 2 点
*/5 * * * * /check.sh            # 每 5 分钟
0 0 * * 0 /cleanup.sh            # 每周日 0 点
```

### 12.3 环境变量

```bash
export VAR=value                 # 设置临时环境变量
echo $VAR                        # 读取环境变量
env                              # 查看所有环境变量
```

永久设置：写入 `~/.bashrc` 或 `/etc/environment`。

### 12.4 常见组合技

```bash
# 查找并杀掉进程
ps aux | grep uvicorn | grep -v grep | awk '{print $2}' | xargs kill

# 查看最近修改的日志
ls -lt /var/log/*.log | head -5

# 实时监控多个日志
tail -f /var/log/syslog /var/log/nginx/error.log

# 统计目录下文件数量
find /path -type f | wc -l

# 批量替换文件内容
grep -rl "old_text" /path | xargs sed -i 's/old_text/new_text/g'
```

---

## 13. 参数通用规则

| 参数 | 含义 | 常见于 |
|------|------|--------|
| `-r` / `-R` | 递归（目录操作） | cp, rm, grep, chmod, chown |
| `-f` | 强制（不确认） | rm, kill, mount |
| `-i` | 交互确认 | rm, mv, cp |
| `-v` | 详细输出 | cp, mv, rm, tar |
| `-a` | 所有/归档 | ls, cp, ps, tar |
| `-n` | 行号/数字 | grep, head, tail |
| `-l` | 长格式列表 | ls, ps |
| `-h` | 人类可读 | ls, df, du |
| `-q` / `-s` | 静默模式 | curl, wget |
| `-o` | 输出到文件 | curl, gcc |
| `-y` | 自动确认 | apt |
| `-p` | 保留权限/显示端口 | mkdir, ss, netstat |
| `-w` | 精确匹配/写入 | grep |

---

## 14. 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 终止当前命令 |
| `Ctrl+Z` | 挂起当前命令（`fg` 恢复） |
| `Ctrl+D` | 退出当前 shell / 输入 EOF |
| `Ctrl+R` | 搜索历史命令 |
| `Ctrl+L` | 清屏（等同 `clear`） |
| `Ctrl+A` | 光标移到行首 |
| `Ctrl+E` | 光标移到行尾 |
| `Ctrl+K` | 删除光标到行尾 |
| `Ctrl+U` | 删除光标到行首 |
| `Tab` | 自动补全路径/命令 |
| `!!` | 重复上一条命令 |
| `!$` | 上一条命令的最后一个参数 |

---

## 15. 排错思路

| 症状 | 排查命令 |
|------|---------|
| 服务访问不了 | `systemctl status xxx` → `journalctl -u xxx -n 50` |
| 端口被占用 | `ss -tlnp \| grep :端口` → `kill PID` |
| 磁盘满了 | `df -h` → `du -sh /* \| sort -rh \| head` |
| 内存不足 | `free -h` → `ps aux --sort=-%mem \| head` |
| CPU 100% | `top` → 看哪个进程占 CPU → `kill` |
| 权限拒绝 | `ls -l` 看权限 → `chmod` / `chown` |
| 找不到命令 | `which xxx` 或 `apt install xxx` |

---

*创建时间：2026-06-24*
*适用环境：Ubuntu Server 22.04+*
