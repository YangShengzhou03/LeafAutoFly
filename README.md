# LeafAuto Pro

## 简介

**LeafAuto Pro** 是 **LeafAuto** 的专业版，旨在解决原版 LeafAuto 的一些局限性，提供更强大、更稳定的自动化体验。这个项目由 LeafAuto 团队开发，最新更新时间为 2025年3月16日。

### 功能概述

- **DLL 注入**：通过注入动态链接库（DLL），建立一个本地服务器来处理自动化任务。
- **HTTP 通信**：DLL 作为服务端监听指定端口，接收来自 LeafAuto Pro 客户端的 GET 或 POST 请求。
- **独立运行**：即使锁屏或后台运行，也能继续执行任务，不影响用户的正常操作。

### 关键特性

- **即开即用**：快速部署，适用于大部分版本。
- **模拟操作**：通过模拟用户操作实现自动化。
- **改进的用户体验**：避免与用户实际操作冲突，减少对其他应用的影响。

## 工作原理

### 架构设计

- **DLL**：注入的 DLL 源代码，可用 Visual Studio 打开项目。
- **inject_dll.py**：用于注入 DLL 的 Python 脚本。
- **Main.py**：当前的测试代码。

### 通信机制

1. **DLL 注入后运行**：
   - DLL 建立一个服务器并监听 20035 端口，接收来自 Python 客户端的请求。
   
2. **收到请求后**：
   - DLL 执行下一步操作，并将结果发送回客户端。

3. **Python 客户端**：
   - Python 客户端建立一个服务器并监听 20042 端口，获取来自 DLL 的数据。
   - DLL 在 hook 到数据后会自动发送给 Python 服务器。
   - DLL 每十秒向 20042 客户端发送心跳包。

### 示例通信流程

- **DLL 建立服务器**：在 20035 端口上建立服务器并监听。
- **Python 客户端**：在 20042 端口上建立服务器，监听来自 DLL 的数据。
- **Python 向 20035 发送请求**：使用 POST 或 GET 方法发送请求，并监听 20042 端口以接收响应。

## 为什么选择 LeafAuto Pro？

LeafAuto Pro 通过 DLL 注入和 HTTP 通信技术解决了原版 LeafAuto 的不足之处，提供了更高效、更稳定的自动化体验。

### 主要特性

- **DLL 注入**：通过注入动态链接库（DLL），建立一个本地服务器来处理自动化任务。
- **HTTP 通信**：DLL 作为服务端监听 8080 端口，接收来自 LeafAuto Pro 客户端的 GET 或 POST 请求。
- **独立运行**：即使锁屏或后台运行，也能继续执行任务，不影响用户的正常操作。

### 兼容性

当前版本支持的操作系统及软件版本：

- **操作系统**：Windows
- **软件版本**：3.9.12.51（仅限此版本）

### 功能计划

我们正在积极开发和完善以下功能：

- **发送文字**：支持向目标应用程序发送文本消息。
- **发送图片**：支持发送图像文件。
- **发送文件**：支持发送各种类型的文件。

## 使用方法

### 安装步骤

1. **下载并安装 LeafAuto Pro 客户端**：
   - 访问 [LeafAuto 官方网站](https://leafauto.com) 下载最新版本的客户端。

2. **将配套的 DLL 文件注入到目标应用程序中**：
   - 使用 `inject_dll.py` 脚本将提供的 DLL 文件注入到目标应用程序中。

3. **启动 LeafAuto Pro 客户端，配置连接参数（默认端口为 8080）**：
   - 打开客户端，输入正确的 IP 地址和端口号（默认为 `http://localhost:8080`）。

4. **通过客户端发送命令，开始自动化任务**：
   - 使用客户端界面或编写脚本发送 HTTP 请求来控制自动化任务。

### 示例代码

下面是一个简单的示例，展示如何通过 HTTP 请求控制 LeafAuto Pro：

```python
import requests
import json

def request_handler(endpoint, method='POST'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            url = f"http://localhost:8080{endpoint}"
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

# 使用示例
result = send_text_payload(who='filehelper', msg='Hello from LeafAuto Pro!')
print(result)