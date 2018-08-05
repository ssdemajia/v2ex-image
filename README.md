# v2ex-image
一个简单图床，主要用于[v2ex](www.v2ex.com)发表情和发照片:tada:

![](http://image.dowob.cn/image/screen2.png)
# 使用

每次上传需要输入秘钥才能上传，输入重命名可以上传后的图片改名，**秘钥需要在config.json中修改**

# 安装
首先git clone项目
```bash
git clone https://github.com/ssdemajia/v2ex-image.git
cd v2ex-image
```
需要在服务器中安装supervisor、virtualenv
```bash
pip install virtualenv
```
生成虚拟环境
```bash
virtualenv env
```
此时在v2ex-image目录下就会有一个env文件夹，里面包括pip、python等，我们需要激活这个环境
```bash
source env/bin/activite
```
在bash命令符就变成这样
![](http://image.dowob.cn/image/screen1.png)
<br/>在生成环境中有用uwsgi和gunicorn，这里我选择使用uwsgi，安装uwsgi
```python
(env) ➜  v2ex-image git:(master) ✗ pip install uwsgi
```
这时候需要安装项目需要的依赖, **一定要激活virtualenv的时候安装**
```bash
pip install -r requirement.txt
```
然后是编写uwsgi的配置文件`config.ini`
```bash
[uwsgi]
socket = 127.0.0.1:8989
wsgi-file = server.py
callable = app
processes = 1
threads = 2
stats = 127.0.0.1:9191
```
接下来配置supervisor
```bash
[program:v2image]   # 控制的名称是v2image
command=/home/ubuntu/v2ex-image/env/bin/uwsgi /home/ubuntu/v2ex-image/config.ini  #uwsgi会被安装在虚拟环境中，所以是在这个路径
directory=/home/ubuntu/v2ex-image  # 项目目录所在路径
user=root
autostart=true
autorestart=true
stdout_logfile=/home/ubuntu/supervisor/log/v2ex-image/v2.log  # 日志位置，这个v2.log必须是一个文件，需要自己新建
```
启动v2image，这在上面配置中定义的，启动停止的命令如下
```bash
supervisorctl start v2image
supervisorctl stop v2image
```

接下来配置Nginx，image.dowob.cn是我自己的域名，需要按需更改
```bash
server {
   listen 80;
   server_name  image.dowob.cn;
   location / {
      include uwsgi_params;
      uwsgi_pass 127.0.0.1:8989;
      uwsgi_param UWSGI_PYHOME /home/ubuntu/v2ex-image/env;
      uwsgi_param UWSGI_CHDIR /home/ubuntu/v2ex-image;
      uwsgi_param UWSGI_SCRIPT server:app;
   }
}
```
然后重新读取配置文件
```bash
nginx -s reload
```
# Todo
-[] 增加拖拽上传
-[] 移动端适配
-[] 图片限制大小
