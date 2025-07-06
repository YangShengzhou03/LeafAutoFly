import ctypes
import json
import os
import re
import threading
import time
from datetime import datetime
from typing import Optional, Dict, List, Any

import requests
from PyQt6 import QtCore, QtMultimedia
from PyQt6.QtCore import QDateTime, pyqtSignal

from System_info import read_key_value
from common import log, get_current_time, log_print, get_resource_path


class WorkerThreadBase(QtCore.QThread):
    pause_changed = QtCore.pyqtSignal(bool)
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_paused = False
        self._is_running = False
        self._stop_event = threading.Event()
        self._stop_lock = threading.Lock()
        log_print("[WORKER_BASE] Thread initialized")

    def run(self):
        log_print("[WORKER_BASE] Error: Subclass must implement run() method")
        raise NotImplementedError("Subclasses must implement the run method")

    def request_interruption(self) -> None:
        with self._stop_lock:
            self._stop_event.set()
            self._is_running = False

    def pause(self):
        self._is_paused = True
        self.pause_changed.emit(True)
        log_print("[WORKER_BASE] Thread paused")

    def resume(self):
        self._is_paused = False
        self.pause_changed.emit(False)
        log_print("[WORKER_BASE] Thread resumed")

    def requestInterruption(self):
        self._stop_event.set()
        self._is_running = False
        log_print("[WORKER_BASE] Thread interruption requested")

    def isPaused(self) -> bool:
        return self._is_paused

    def isRunning(self) -> bool:
        return self._is_running

    def check_interruption(self) -> bool:
        """检查是否请求中断"""
        with self._stop_lock:
            if self._stop_event.is_set():
                return True
        return False


class AiWorkerThread(WorkerThreadBase):
    status_updated = QtCore.pyqtSignal(str)

    def __init__(self, app_instance, receiver, model="月之暗面", role="你很温馨,回复简单明了。", only_at=False):
        super().__init__()
        log_print("[AI_WORKER] Initializing thread")
        self.app_instance = app_instance
        self.receiver = receiver
        self.model = model
        self.system_content = role
        log_print(f"[AI_WORKER] Loading reply rules")
        self.rules = self._load_rules()
        self.only_at = only_at
        self.at_me = "@" + self.app_instance.wx.nickname
        self.receiver_list = [r.strip() for r in receiver.replace(';', '；').split('；') if r.strip()]
        log_print(f"[AI_WORKER] Receiver list: {self.receiver_list}")
        self.listen_list = []
        self.init_listeners()
        self.status = "Ready"
        log_print("[AI_WORKER] Initialization completed")

    def init_listeners(self):
        log_print(f"[AI_WORKER] Starting listener initialization, targets: {len(self.receiver_list)}")
        for target in self.receiver_list:
            log_print(f"[AI_WORKER] Attempting to listen: {target}")
            if self.check_interruption():
                log_print("[AI_WORKER] Listener initialization interrupted")
                return
            try:
                self.app_instance.wx.AddListenChat(who=target)
                self.listen_list.append(target)
                log_print(f"[AI_WORKER] Successfully listening: {target}")
            except Exception as e:
                log("ERROR", f"添加监听失败: {target}, 错误: {str(e)}")

    def _load_rules(self):
        log_print("[AI_WORKER] Loading reply rules")
        try:
            with open(get_resource_path('_internal/AutoReply_Rules.json'), 'r', encoding='utf-8') as f:
                rules = json.load(f)
                log_print(f"[AI_WORKER] Successfully loaded {len(rules)} reply rules")
                return rules
        except FileNotFoundError:
            log_print("[AI_WORKER] Reply rules file not found")
            return None
        except json.JSONDecodeError:
            log_print("[AI_WORKER] Error decoding reply rules file")
            return []

    def _get_chat_name(self, who):
        if not hasattr(self.app_instance.wx, 'GetChatName'):
            log_print(f"[AI_WORKER] No GetChatName method, using raw ID: {who}")
            return who
        chat_name = self.app_instance.wx.GetChatName(who)
        log_print(f"[AI_WORKER] Retrieved chat name: {who} -> {chat_name}")
        return chat_name

    def _match_rule(self, msg, who):
        log_print(f"[AI_WORKER] Matching message rule: '{msg[:30]}...' from {who}")
        if not self.rules or self.check_interruption():
            log_print("[AI_WORKER] No rules or interrupted, skipping match")
            return []
        matched_replies = []
        msg = msg.strip()
        chat_name = self._get_chat_name(who)
        log_print(f"[AI_WORKER] Chat name: {chat_name}")

        for rule in self.rules:
            if self.check_interruption():
                log_print("[AI_WORKER] Match process interrupted")
                break
            keyword = rule['keyword'].strip()
            if not keyword:
                continue

            apply_to = rule.get('apply_to', '全部').strip()
            log_print(f"[AI_WORKER] Checking rule: '{keyword}', Apply to: {apply_to}")

            if apply_to != '全部':
                groups = [g.strip() for g in apply_to.replace(';', '；').split('；') if g.strip()]
                if chat_name not in groups:
                    log_print(f"[AI_WORKER] Rule does not apply to current chat: {chat_name}")
                    continue

            match_type = rule['match_type']
            log_print(f"[AI_WORKER] Match type: {match_type}")

            if match_type == '等于':
                if msg == keyword:
                    log_print(f"[AI_WORKER] Match success (equals): {keyword}")
                    matched_replies.append(rule['reply_content'])
            elif match_type == '包含':
                if keyword in msg:
                    log_print(f"[AI_WORKER] Match success (contains): {keyword}")
                    matched_replies.append(rule['reply_content'])
            elif match_type == '正则':
                try:
                    if re.search(keyword, msg):
                        log_print(f"[AI_WORKER] Match success (regex): {keyword}")
                        matched_replies.append(rule['reply_content'])
                except re.error:
                    log("ERROR", f"无效的正则表达式: {keyword}")
                    continue
        log_print(f"[AI_WORKER] Match completed, found {len(matched_replies)} replies")
        return matched_replies

    def run(self):
        log_print("[AI_WORKER] Thread started")
        with self._stop_lock:
            self._is_running = True
            self.status = "Initializing"
            self.status_updated.emit(self.status)
            log_print("[AI_WORKER] Status set to: Initializing")

        try:
            log_print(f"[AI_WORKER] Starting initialization send, receivers: {len(self.receiver_list)}")
            for receiver in self.receiver_list:
                if self.check_interruption():
                    log_print("[AI_WORKER] Initialization send interrupted")
                    return
                log_print(f"[AI_WORKER] Sending initialization message to: {receiver}")
                self.app_instance.wx.SendMsg(msg=" ", who=receiver)
        except Exception as e:
            log("ERROR", f"初始化发送失败: {str(e)}")
            self.app_instance.on_thread_finished()
            return

        self.status = "Running"
        self.status_updated.emit(self.status)
        log_print("[AI_WORKER] Status set to: Running")

        while self.isRunning() and not self.check_interruption():
            try:
                if self._is_paused:
                    log_print("[AI_WORKER] Thread paused, sleeping 100ms")
                    self.msleep(100)
                    continue

                log_print("[AI_WORKER] Starting message processing")
                self._handle_messages()
            except Exception as e:
                log("ERROR", f"处理消息时发生异常: {str(e)}")
                break
            finally:
                self.msleep(100)

        self.status = "Stopped"
        self.status_updated.emit(self.status)
        log_print("[AI_WORKER] Status set to: Stopped")
        self.app_instance.on_thread_finished()
        with self._stop_lock:
            self._is_running = False
            log_print("[AI_WORKER] Thread stopped")

    def _handle_messages(self):
        log_print("[AI_WORKER] Retrieving listened messages")
        if self.check_interruption():
            log_print("[AI_WORKER] Message processing interrupted")
            return

        messages_dict = self.app_instance.wx.GetListenMessage()
        log_print(f"[AI_WORKER] Retrieved messages from {len(messages_dict)} chats")

        for chat, messages in messages_dict.items():
            log_print(f"[AI_WORKER] Processing chat: {chat.who}, messages: {len(messages)}")
            if self.check_interruption():
                log_print("[AI_WORKER] Message processing interrupted")
                break

            for message in messages:
                if self.check_interruption():
                    log_print("[AI_WORKER] Message processing interrupted")
                    break

                if self._is_ignored_message(message):
                    log_print(
                        f"[AI_WORKER] Ignoring message: type={getattr(message, 'type', 'unknown')}, sender={getattr(message, 'sender', 'unknown')}")
                    continue

                log_print(f"[AI_WORKER] Processing message: '{message.content[:30]}...' from {chat.who}")
                self._process_message(message.content, chat.who, message)

    def _is_ignored_message(self, message):
        if hasattr(message, 'type') and message.type.lower() == 'sys':
            return True
        if hasattr(message, 'sender') and message.sender == 'Self':
            return True
        if hasattr(message, 'type') and message.type.lower() != 'friend':
            return True
        return False

    def _process_message(self, msg, who, message):
        log_print(f"[AI_WORKER] Processing message content: '{msg[:30]}...' from {who}")
        if self.check_interruption():
            log_print("[AI_WORKER] Message content processing interrupted")
            return

        if self.only_at and self.at_me not in msg:
            log_print(f"[AI_WORKER] Message does not contain @, ignoring: '{msg[:30]}...'")
            return

        if self.at_me in msg:
            original_msg = msg
            msg = msg.replace(self.at_me, "").strip()
            log_print(f"[AI_WORKER] Removed @ marker: '{original_msg[:30]}...' -> '{msg[:30]}...'")

        is_group = who in self.receiver_list
        log_print(f"[AI_WORKER] Is group chat: {is_group}")

        if self.rules:
            log_print("[AI_WORKER] Checking rule matches")
            matched_replies = self._match_rule(msg, who)
            if matched_replies:
                log_print(f"[AI_WORKER] Found {len(matched_replies)} matching rules")
                for reply in matched_replies:
                    log_print(f"[AI_WORKER] Sending rule-based reply: '{reply[:30]}...' to {who}")
                    self._send_reply(reply, who, is_group, message.sender if is_group else None)
                return

        if self.model != "禁用模型":
            log_print(f"[AI_WORKER] Using {self.model} model to generate response")
            self._send_ai_response(msg, who, is_group, message.sender if is_group else None)

    def _send_reply(self, reply, who, is_group=False, at_user=None):
        log_print(f"[AI_WORKER] Preparing to send reply: '{reply[:30]}...' to {who}")
        try:
            if os.path.isdir(os.path.dirname(reply)):
                if os.path.isfile(reply):
                    log_print(f"[AI_WORKER] Sending file: {os.path.basename(reply)} to {who}")
                    self.app_instance.wx.SendFiles(filepath=reply, who=who)
                else:
                    raise FileNotFoundError(f"回复规则有误,没有 {os.path.basename(reply)} 文件")
            else:
                delay = int(read_key_value('reply_delay'))
                log_print(f"[AI_WORKER] Sending text message with {delay}s delay: '{reply[:30]}...' to {who}")
                time.sleep(delay)
                if is_group and at_user and self.only_at:
                    log_print(f"[AI_WORKER] Group message, @user: {at_user}")
                    self.app_instance.wx.SendMsg(msg=reply, who=who, at=at_user)
                else:
                    self.app_instance.wx.SendMsg(msg=reply, who=who)
        except Exception as e:
            log("ERROR", f"发送回复失败: {str(e)}")

    def _send_ai_response(self, msg, who, is_group=False, at_user=None):
        log_print(f"[AI_WORKER] Calling AI model for message: '{msg[:30]}...'")
        result = self._query_ai_model(msg)
        if result:
            log_print(f"[AI_WORKER] AI model returned: '{result[:30]}...'")
            if is_group and at_user and self.only_at:
                log_print(f"[AI_WORKER] Sending AI response (group @): '{result[:30]}...' to {who}")
                self.app_instance.wx.SendMsg(msg=result, who=who, at=at_user)
            else:
                log_print(f"[AI_WORKER] Sending AI response: '{result[:30]}...' to {who}")
                self.app_instance.wx.SendMsg(msg=result, who=who)

    def _query_api(self, url, payload=None, headers=None, params=None, method='POST'):
        log_print(f"[AI_WORKER] Calling API: {url}")
        try:
            response = requests.request(method=method, url=url, json=payload, headers=headers, params=params)
            response.raise_for_status()
            log_print(f"[AI_WORKER] API call successful")
            return response.json()
        except requests.RequestException as e:
            log("ERROR", f"API请求失败: {e}")
            return None

    def _get_access_token(self):
        log_print("[AI_WORKER] Retrieving Baidu API access token")
        response = self._query_api(
            "https://aip.baidubce.com/oauth/2.0/token",
            params={'grant_type': 'client_credentials',
                    'client_id': 'eCB39lMiTbHXV0mTt1d6bBw7',
                    'client_secret': 'WUbEO3XdMNJLTJKNQfFbMSQvtBVzRhvu'}
        )
        token = response.get("access_token") if response else None
        log_print(f"[AI_WORKER] Access token retrieval result: {bool(token)}")
        return token

    def _query_ai_model(self, msg):
        log_print(f"[AI_WORKER] Querying {self.model} model: '{msg[:30]}...'")
        if self.model == "禁用模型":
            log_print("[AI_WORKER] Model disabled")
            return None
        try:
            if self.model == "文心一言":
                return self._query_wenxin_model(msg)
            elif self.model == "月之暗面":
                return self._query_moonshot_model(msg)
            elif self.model == "星火讯飞":
                return self._query_other_model(msg)
            else:
                log_print(f"[AI_WORKER] Unknown AI model: {self.model}")
                return "未知的AI模型"
        except Exception as e:
            log_print(f"[AI_WORKER] Error querying AI model: {str(e)}")
            return "抱歉，AI模型查询失败，请稍后再试。"

    def _query_wenxin_model(self, msg):
        log_print("[AI_WORKER] Querying Wenxin Yiyan model")
        access_token = self._get_access_token()
        if not access_token:
            log_print("[AI_WORKER] Failed to retrieve Baidu API access token")
            return "无法获取百度API访问令牌"

        payload = {"messages": [{"role": "user", "content": msg}]}
        log_print(f"[AI_WORKER] Sending request to Wenxin Yiyan: {payload}")
        response = self._query_api(
            f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}",
            payload=payload,
            headers={'Content-Type': 'application/json'}
        )
        result = response.get('result', "无法解析响应") if response else "请求失败"
        log_print(f"[AI_WORKER] Wenxin Yiyan returned: {result[:30]}...")
        return result

    def _query_moonshot_model(self, msg):
        log_print("[AI_WORKER] Querying Moonshot model")
        from openai import OpenAI
        client = OpenAI(api_key="sk-dx1RuweBS0LU0bCR5HizbWjXLuBL6HrS8BT21NEEGwbeyuo6",
                        base_url="https://api.moonshot.cn/v1")
        log_print(f"[AI_WORKER] Sending request to Moonshot")
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "system", "content": self.system_content},
                      {"role": "user", "content": msg}],
            temperature=0.9,
        )
        log_print(f"[AI_WORKER] Moonshot returned: {completion.choices[0].message.content[:30]}...")
        return completion.choices[0].message.content

    def _query_other_model(self, msg):
        log_print("[AI_WORKER] Querying Xinghuo Xunfei model")
        data = {
            "max_tokens": 64,
            "top_k": 4,
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": msg}
            ],
            "model": "4.0Ultra"
        }
        header = {
            "Authorization": "Bearer xCPWitJxfzhLaZNOAdtl:PgJXiEyvKjUaoGzKwgIi",
            "Content-Type": "application/json"
        }
        log_print(f"[AI_WORKER] Sending request to Xinghuo Xunfei")
        response = self._query_api("https://spark-api-open.xf-yun.com/v1/chat/completions", data, header)
        result = response['choices'][0]['message']['content'] if response else "无法解析响应"
        log_print(f"[AI_WORKER] Xinghuo Xunfei returned: {result[:30]}...")
        return result


class SplitWorkerThread(WorkerThreadBase):
    """消息拆分发送工作线程"""
    sent_signal = QtCore.pyqtSignal(str, bool)

    def __init__(self, app_instance, receiver: str, sentences: List[str], wx: Any):
        super().__init__()
        self.app_instance = app_instance
        self.receiver = receiver
        self.sentences = sentences
        self.wx = wx
        self._is_running = True

    def run(self) -> None:
        """线程主循环"""
        self._is_running = True
        log("INFO", f"SplitWorkerThread 已启动，准备将 {len(self.sentences)} 条信息发给 {self.receiver}")

        for i, sentence in enumerate(self.sentences):
            if self._stop_event.is_set() or not self._is_running:
                log("INFO", f"收到停止信号，终止发送任务，当前进度: {i + 1}/{len(self.sentences)}")
                break

            try:
                log("INFO", f"发送 ({i + 1}/{len(self.sentences)}) '{sentence[:30]}...' 给 {self.receiver}")
                if self.wx:
                    self.wx.SendMsg(msg=sentence, who=self.receiver)
                    self.sent_signal.emit(sentence, True)  # 发送成功信号
                else:
                    log("ERROR", f"找不到微信实例，无法发送消息给 {self.receiver}")
                    self.sent_signal.emit(sentence, False)  # 发送失败信号
                    self._stop_event.set()
                    break

                # 添加发送间隔，避免过快
                for _ in range(5):
                    if self._stop_event.is_set():
                        break
                    self.msleep(100)

            except Exception as e:
                log("ERROR", f"发送消息时出错: {str(e)}")
                self.sent_signal.emit(sentence, False)  # 发送失败信号
                self.app_instance.is_sending = False
                self._stop_event.set()
                break

        log("INFO", f"拆句发送已完成，共发送 {len(self.sentences)} 条消息")
        self._is_running = False
        self.finished.emit()


class WorkerThread(WorkerThreadBase):
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002

    finished = pyqtSignal()

    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.prevent_sleep = False
        self.current_time = 'sys'
        self._system_state = None

    def run(self) -> None:
        """线程主循环"""
        self._is_running = True

        # 设置系统不进入睡眠和锁屏状态
        if self.prevent_sleep:
            self._set_system_state(self.ES_CONTINUOUS | self.ES_SYSTEM_REQUIRED | self.ES_DISPLAY_REQUIRED)
            log("WARNING", "已阻止系统休眠和锁屏")

        try:
            while self._is_running and not self._stop_event.is_set():
                if self.check_interruption():
                    break

                next_task = self._find_next_ready_task()
                if next_task is None:
                    log("INFO", "没有找到待执行的任务，线程退出")
                    break

                try:
                    task_time = datetime.strptime(next_task['time'], '%Y-%m-%dT%H:%M:%S')
                    remaining_time = (task_time - get_current_time(self.current_time)).total_seconds()

                    if remaining_time > 0:
                        hours, remainder = divmod(int(remaining_time), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_parts = []
                        if hours > 0:
                            time_parts.append(f"{hours}时")
                        if minutes > 0:
                            time_parts.append(f"{minutes}分")
                        if seconds > 0 or not time_parts:
                            time_parts.append(f"{seconds}秒")
                        friendly_time = ''.join(time_parts)

                        log("INFO", f"下一个任务将在 {friendly_time} 后执行")

                        while remaining_time > 0 and not self.check_interruption():
                            sleep_time = min(remaining_time, 0.5)  # 每次最多休眠0.5秒
                            self.msleep(int(sleep_time * 1000))
                            remaining_time -= sleep_time

                            if self.check_interruption():
                                break

                        if self.check_interruption():
                            break

                    if self.check_interruption():
                        break

                    success = self._execute_task(next_task)

                    if self.check_interruption():
                        log("WARNING", "任务执行过程中被用户终止")
                        break

                    if success:
                        self.app_instance.update_task_status(next_task, '成功')
                    else:
                        self.app_instance.update_task_status(next_task, '出错')

                except Exception as e:
                    log("ERROR", f"处理任务时出错: {str(e)}")
                    self.app_instance.update_task_status(next_task, '出错')
                    time.sleep(1)

        finally:
            if self.prevent_sleep:
                self._set_system_state(self.ES_CONTINUOUS)
                log("WARNING", "已恢复系统休眠和锁屏设置")
            self._is_running = False
            self.finished.emit()

    def _set_system_state(self, state_flags: int) -> None:
        try:
            self._system_state = ctypes.windll.kernel32.SetThreadExecutionState(state_flags)
            if not self._system_state:
                log("ERROR", f"设置系统状态失败，错误码: {ctypes.GetLastError()}")
        except Exception as e:
            log("ERROR", f"调用系统API设置状态时出错: {str(e)}")

    def _find_next_ready_task(self) -> Optional[Dict]:
        next_task = None
        min_time = None

        for task in self.app_instance.ready_tasks:
            try:
                task_time = QDateTime.fromString(task['time'], "yyyy-MM-ddTHH:mm:ss").toSecsSinceEpoch()
                if min_time is None or task_time < min_time:
                    min_time = task_time
                    next_task = task
            except Exception as e:
                log("ERROR", f"解析任务时间时出错: {str(e)}")

        return next_task

    def _execute_task(self, task: Dict) -> bool:
        max_retries = 3
        retries = 0
        success = False

        log("INFO", f"开始执行任务: {task.get('name', '未知')}")

        while retries < max_retries and not success and not self.check_interruption():
            try:
                name = task['name']
                info = task['info']
                wx_nickname = task['wx_nickname']

                if self.check_interruption():
                    return False

                wx_instance = self._get_wx_instance(wx_nickname)
                if not wx_instance:
                    log("ERROR", f"找不到微信实例 '{wx_nickname}'，无法执行任务")
                    raise ValueError(f"找不到微信实例 '{wx_nickname}'")

                if self.check_interruption():
                    return False

                if os.path.isdir(os.path.dirname(info)):
                    if os.path.isfile(info):
                        file_name = os.path.basename(info)
                        log("INFO", f"开始把文件 {file_name} 发给 {name} (发送方: {wx_nickname})")
                        success = self._send_with_interruption(lambda: wx_instance.SendFiles(filepath=info, who=name))
                    else:
                        raise FileNotFoundError(f"该路径下没有 {os.path.basename(info)} 文件")
                else:
                    log("INFO", f"开始把消息 '{info[:30]}...' 发给 {name} (发送方: {wx_nickname})")
                    if "@所有人" in info:
                        info = info.replace("@所有人", "").strip()
                        success = self._send_with_interruption(lambda: wx_instance.AtAll(msg=info, who=name))
                    else:
                        success = self._send_with_interruption(lambda: wx_instance.SendMsg(msg=info, who=name))

                if success:
                    log("DEBUG", f"成功执行任务: 发送给 {name} (发送方: {wx_nickname})")

            except Exception as e:
                log("ERROR", f"执行任务失败 (尝试 {retries + 1}/{max_retries}): {str(e)}")
                retries += 1

                if retries < max_retries and not self.check_interruption():
                    log("WARNING", "尝试重新连接微信客户端...")
                    try:
                        self.app_instance.parent.update_wx()
                        for _ in range(10):
                            if self.check_interruption():
                                break
                            self.msleep(100)
                    except Exception as we:
                        log("ERROR", f"更新微信客户端失败: {str(we)}")

        return success

    def _get_wx_instance(self, wx_nickname: str) -> Any:
        try:
            wx_dict = self.app_instance.wx_dict

            if wx_nickname in wx_dict:
                return wx_dict[wx_nickname]

            log("WARNING", f"找不到微信实例 '{wx_nickname}'，将使用默认实例")
            if wx_dict:
                return next(iter(wx_dict.values()))

            log("ERROR", "没有可用的微信实例")
            return None
        except Exception as e:
            log("ERROR", f"获取微信实例失败: {str(e)}")
            return None

    def _send_with_interruption(self, send_func):
        if self.check_interruption():
            return False

        try:
            send_thread = threading.Thread(target=send_func)
            send_thread.daemon = True
            send_thread.start()

            while send_thread.is_alive():
                if self.check_interruption():
                    send_thread.join(timeout=0.5)
                    return False
                self.msleep(100)

            return True

        except Exception as e:
            log("ERROR", f"发送过程中出错: {str(e)}")
            return False


class ErrorSoundThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    _is_running = False

    def __init__(self):
        super().__init__()
        self.sound_file = None
        self.player = None
        self.audio_output = None
        log_print("[ERROR_SOUND] Thread initialized")

    def update_sound_file(self, sound_file_path):
        log_print(f"[ERROR_SOUND] Sound file updated: {sound_file_path}")
        self.sound_file = sound_file_path

    def run(self):
        log_print("[ERROR_SOUND] Thread started")
        if not self.sound_file or not os.path.exists(self.sound_file) or self._is_running:
            log_print("[ERROR_SOUND] Sound file not found or thread already running")
            return
        self._is_running = True

        if self.player:
            self.player.mediaStatusChanged.disconnect()
            self.player.stop()
            self.player = None

        if self.audio_output:
            self.audio_output = None

        self.audio_output = QtMultimedia.QAudioOutput()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QtCore.QUrl.fromLocalFile(self.sound_file))
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)
        self.player.play()
        log_print(f"[ERROR_SOUND] Playing sound: {self.sound_file}")

        loop = QtCore.QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec()

    def _on_media_status_changed(self, status):
        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            log_print("[ERROR_SOUND] Sound playback completed")
            self.cleanup_resources()

    def cleanup_resources(self):
        log_print("[ERROR_SOUND] Cleaning up resources")
        if self.player:
            self.player.stop()
            self.player.mediaStatusChanged.disconnect()
            self.player = None

        if self.audio_output:
            self.audio_output = None

        self._is_running = False
        self.finished.emit()

    def stop_playback(self):
        if self._is_running:
            log_print("[ERROR_SOUND] Playback stopped by user")
            self.cleanup_resources()

    def play_test(self):
        if not self.isRunning() and not self._is_running:
            log_print("[ERROR_SOUND] Testing sound playback")
            self.start()