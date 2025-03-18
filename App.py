import sys
import winreg
import socket
import json
import requests
import threading
import tkinter as tk
from tkinter import messagebox
"""
Dll监听20035，并向20042发送信息
"""

def get_wx_version():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat", 0, winreg.KEY_READ) as key:
            int_version = winreg.QueryValueEx(key, "Version")[0]
            hex_version = hex(int_version)
            hex_str = hex_version[2:]
            new_hex_str = "0" + hex_str[1:]
            new_hex_num = int(new_hex_str, 16)
            major = (new_hex_num >> 24) & 0xFF
            minor = (new_hex_num >> 16) & 0xFF
            patch = (new_hex_num >> 8) & 0xFF
            build = (new_hex_num >> 0) & 0xFF
            return "{}.{}.{}.{}".format(major, minor, patch, build)
    except Exception as e:
        print("打开注册表失败：{}".format(e))
        return None

def request_handler(endpoint, method='POST'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            url = f"http://localhost:20035{endpoint}"
            headers = {'Content-Type': 'application/json'}
            payload = func(*args, **kwargs)

            try:
                if method.upper() == 'POST':
                    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
                elif method.upper() == 'GET':
                    response = requests.get(url, headers=headers, params=payload, timeout=10)
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")

                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"{method}请求失败，状态码：{response.status_code}，响应：{response.text}")
                    return None
            except requests.exceptions.Timeout as e:
                print(f"请求超时：{str(e)}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"请求错误：{str(e)}")
                return None

        return wrapper

    return decorator

@request_handler("/api/sendtext", method="POST")
def send_text_payload(who='filehelper', msg='Hello LeafAuto'):
    return {
        "who": who,
        "msg": msg
    }

def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 20042))
    server_socket.listen(5)
    print("Server started on port 20042")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data: {data.decode('utf-8')}")
                # 在这里可以对收到的数据进行处理
            except ConnectionResetError:
                print("Connection reset by peer")
                break

        client_socket.close()
        print(f"Connection closed with {addr}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("微信数据接收器")
        self.geometry("400x200")

        self.label = tk.Label(self, text="等待微信数据...")
        self.label.pack(pady=20)

        self.send_button = tk.Button(self, text="发送消息", command=self.send_message)
        self.send_button.pack(pady=20)

        self.wx_version = get_wx_version()
        if self.wx_version != "3.9.12.51":
            messagebox.showwarning("警告", f"当前微信版本为：{self.wx_version}，请确保你的微信版本是 3.9.12.51")
            sys.exit(0)

    def send_message(self):
        result = send_text_payload()
        if result:
            messagebox.showinfo("成功", f"请求成功，响应：{result}")
        else:
            messagebox.showerror("失败", "请求失败")

if __name__ == "__main__":
    # 启动TCP服务器在一个单独的线程中
    tcp_server_thread = threading.Thread(target=start_tcp_server)
    tcp_server_thread.daemon = True
    tcp_server_thread.start()

    app = App()
    app.mainloop()