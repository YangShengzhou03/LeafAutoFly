import os
import sys
import subprocess
import time
from server_manager import start_vue_server, open_browser


print('正在启动Flask后端服务器和前端...')
flask_process = subprocess.Popen(
    ['python', 'app.py'],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True
)

print('等待Flask服务器启动...')
for i in range(5):
    print(f'倒计时: {5 - i}秒')
    time.sleep(1)

print('正在启动Vue前端服务器...')
start_vue_server()

print('正在打开浏览器...')
open_browser()

print('应用已成功启动！请在浏览器中访问 http://localhost:8080')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('正在关闭应用...')
    flask_process.kill()
    print('应用已关闭')
    sys.exit(0)