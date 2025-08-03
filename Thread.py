import ctypes
import json
import os
import random
import re
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import requests
from PyQt6 import QtCore, QtMultimedia
from PyQt6.QtCore import QDateTime

from System_info import read_key_value
from common import log, get_current_time, log_print


class WorkerThreadBase(QtCore.QThread):
    pause_changed = QtCore.pyqtSignal(bool)
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_paused = False
        self._is_running = False
        self._stop_event = threading.Event()
        log_print("[WORKER_BASE] Thread initialized")

    def run(self):
        log_print("[WORKER_BASE] Error: Subclass must implement run() method")
        raise NotImplementedError("Subclasses must implement the run method")

    def pause(self):
        if not self._is_paused:
            self._is_paused = True
            self.pause_changed.emit(True)
            log_print("[WORKER_BASE] Thread paused")

    def resume(self):
        if self._is_paused:
            self._is_paused = False
            self.pause_changed.emit(False)
            log_print("[WORKER_BASE] Thread resumed")

    def requestInterruption(self):
        if self._is_running:
            self._stop_event.set()
            self._is_running = False
            log_print("[WORKER_BASE] Thread interruption requested")

    def isPaused(self) -> bool:
        return self._is_paused

    def isRunning(self) -> bool:
        return self._is_running

    def wait_for_resume(self):
        while self._is_paused and not self._stop_event.is_set():
            self.msleep(100)


class WorkerThread(WorkerThreadBase):
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002

    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.prevent_sleep = False
        self.current_time = 'sys'
        self._system_state = None

    def run(self):
        self._is_running = True
        log_print("[WORKER_THREAD] Thread started")

        if self.prevent_sleep:
            self._set_system_state(self.ES_CONTINUOUS | self.ES_SYSTEM_REQUIRED | self.ES_DISPLAY_REQUIRED)
            log("WARNING", "已阻止系统休眠和锁屏")
            log_print("[WORKER_THREAD] System sleep prevention enabled")

        try:
            while self._is_running and not self._stop_event.is_set():
                if self._is_paused:
                    self.wait_for_resume()
                    continue

                next_task = self._find_next_ready_task()
                if next_task is None:
                    log("INFO", "没有找到待执行的任务，线程退出")
                    log_print("[WORKER_THREAD] No ready tasks found, exiting")
                    break

                try:
                    task_time = datetime.strptime(next_task['time'], '%Y-%m-%dT%H:%M:%S')
                    current_time = get_current_time(self.current_time)
                    remaining_time = (task_time - current_time).total_seconds()

                    if remaining_time > 0:
                        days, remainder = divmod(int(remaining_time), 86400)
                        hours, remainder = divmod(remainder, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_parts = []
                        if days > 0:
                            time_parts.append(f"{days}天")
                        if hours > 0:
                            time_parts.append(f"{hours}时")
                        if minutes > 0:
                            time_parts.append(f"{minutes}分")
                        time_parts.append(f"{seconds}秒")
                        friendly_time = ''.join(time_parts)

                        log("INFO", f"下一个任务将在 {friendly_time} 后执行")
                        log_print(f"[WORKER_THREAD] Next task in {friendly_time}: {next_task['id']}")

                        self._wait_for_task_optimized(task_time)

                    if self._stop_event.is_set():
                        break

                    success = self._execute_task(next_task)

                    if success:
                        self.app_instance.update_task_status(next_task['id'], '成功')
                        log_print(f"[WORKER_THREAD] Task executed successfully: {next_task['id']}")
                    else:
                        self.app_instance.update_task_status(next_task['id'], '出错')
                        log_print(f"[WORKER_THREAD] Task execution failed: {next_task['id']}")

                except Exception as e:
                    log("ERROR", f"处理任务时出错: {str(e)}")
                    self.app_instance.update_task_status(next_task['id'], '出错')
                    log_print(f"[WORKER_THREAD] Task execution failed: {next_task['id']}")
                    time.sleep(1)

        finally:
            if self.prevent_sleep:
                self._set_system_state(self.ES_CONTINUOUS)
                log("WARNING", "已恢复系统休眠和锁屏设置")
                log_print("[WORKER_THREAD] System sleep prevention disabled")

            self._is_running = False
            log_print("[WORKER_THREAD] Thread finished")
            self.finished.emit()

    def _wait_for_task_optimized(self, task_time: datetime):
        start_sys_time = get_current_time(self.current_time)
        start_mono_time = time.monotonic()
        last_check_mono = start_mono_time
        time_discrepancy_threshold = 2.0

        while not self._stop_event.is_set():
            if self._is_paused:
                pause_start_mono = time.monotonic()
                self.wait_for_resume()
                if self._stop_event.is_set():
                    return
                pause_duration = time.monotonic() - pause_start_mono
                start_mono_time += pause_duration
                last_check_mono += pause_duration

            current_sys_time = get_current_time(self.current_time)
            current_mono_time = time.monotonic()
            elapsed_mono = current_mono_time - start_mono_time

            expected_sys_time = start_sys_time + timedelta(seconds=current_mono_time - start_mono_time)

            if current_mono_time - last_check_mono > 1.0:
                sys_mono_diff = (current_sys_time - expected_sys_time).total_seconds()
                if abs(sys_mono_diff) > time_discrepancy_threshold:
                    log("WARNING", f"检测到时间突变！系统时间与实际时间偏差 {sys_mono_diff:.2f}秒，已自动修正")
                    start_sys_time = current_sys_time
                    start_mono_time = current_mono_time
                    expected_sys_time = start_sys_time
                last_check_mono = current_mono_time

            remaining_time = (task_time - current_sys_time).total_seconds()

            if remaining_time <= 0:
                return

            if remaining_time > 86400:
                sleep_interval = 30.0
            elif remaining_time > 3600:
                sleep_interval = 10.0
            elif remaining_time > 60:
                sleep_interval = 5.0
            elif remaining_time > 10:
                sleep_interval = 1.0
            else:
                sleep_interval = 0.1

            sleep_interval = min(sleep_interval, remaining_time)
            self.msleep(int(sleep_interval * 1000))

    def _set_system_state(self, state_flags):
        try:
            self._system_state = ctypes.windll.kernel32.SetThreadExecutionState(state_flags)
            if not self._system_state:
                log("ERROR", f"设置系统状态失败，错误码: {ctypes.GetLastError()}")
                log_print(f"[WORKER_THREAD] Failed to set system state, error code: {ctypes.GetLastError()}")
        except Exception as e:
            log("ERROR", f"调用系统API设置状态时出错: {str(e)}")
            log_print(f"[WORKER_THREAD] Error calling system API: {str(e)}")

    def _find_next_ready_task(self) -> Optional[Dict]:
        next_task = None
        min_time = None

        for task in self.app_instance.ready_tasks.values():
            try:
                task_time = QDateTime.fromString(task['time'], "yyyy-MM-ddTHH:mm:ss").toSecsSinceEpoch()
                if min_time is None or task_time < min_time:
                    min_time = task_time
                    next_task = task
            except Exception as e:
                log("ERROR", f"解析任务时间时出错: {str(e)}")
                log_print(f"[WORKER_THREAD] Error parsing task time: {str(e)}")

        return next_task

    def _execute_task(self, task: Dict) -> bool:
        max_retries = 3
        retries = 0
        success = False

        while retries < max_retries and not success:
            try:
                name = task['name']
                info = task['info']
                sender = task['sender']

                wx_instance = self._get_wx_instance(sender)
                if not wx_instance:
                    log("ERROR", f"找不到微信实例 '{sender}'，无法执行任务 (ID: {task.get('id')})")
                    raise ValueError(f"找不到微信实例 '{sender}'")

                if re.match(r'^Emotion:\d+$', info):
                    emotion_index = int(info.split(':')[1])
                    success = self._send_emotion(wx_instance=wx_instance, emotion_index=emotion_index, who=name)
                elif os.path.isdir(os.path.dirname(info)):
                    if os.path.isfile(info):
                        file_name = os.path.basename(info)
                        log("WARNING", f"开始把文件 {file_name} 发给 {name} (发送方: {sender})")
                        success = self._send_files(wx_instance=wx_instance, filepath=info, who=name)
                    else:
                        raise FileNotFoundError(f"该路径下没有 {os.path.basename(info)} 文件")
                else:
                    log("WARNING",
                        f"开始把消息 '{info[:30]}...' 发给 {name} (发送方: {sender})")
                    if "@所有人" in info:
                        info = info.replace("@所有人", "").strip()
                        success = self._At_all(wx_instance=wx_instance, msg=info, who=name)
                    else:
                        success = self._send_message(wx_instance=wx_instance, msg=info, who=name)

                if success:
                    log("DEBUG", f"成功执行任务: 发送给 {name} (发送方: {sender})")

            except Exception as e:
                log("ERROR", f"执行任务失败 (尝试 {retries + 1}/{max_retries}): {str(e)}")
                retries += 1

                if retries < max_retries:
                    log("WARNING", "尝试重新连接微信客户端...")
                    try:
                        self.app_instance.parent.update_wx()
                        for _ in range(10):
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
                return wx_dict

            log("ERROR", "没有可用的微信实例")
            return None
        except Exception as e:
            log("ERROR", f"获取微信实例失败: {str(e)}")
            return None

    def _send_message(self, wx_instance: any, msg: str, who: str) -> bool:
        return self._retry_operation(lambda: wx_instance.SendMsg(msg=msg, who=who))

    def _At_all(self, wx_instance: any, msg: str, who: str) -> bool:
        return self._retry_operation(lambda: wx_instance.AtAll(msg=msg, who=who, exact=True))

    def _send_files(self, wx_instance: any, filepath: str, who: str) -> bool:
        return self._retry_operation(lambda: wx_instance.SendFiles(filepath=filepath, who=who))

    def _send_emotion(self, wx_instance: any, emotion_index: int, who: str) -> bool:
        return self._retry_operation(lambda: wx_instance.SendEmotion(emotion_index=emotion_index, who=who, exact=True))

    def _retry_operation(self, operation, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = operation()
                if result["status"] == "成功":
                    return True
                else:
                    raise LookupError(f"操作失败: {result.get('message', '未知错误')}")
            except Exception as e:
                log("ERROR", f"操作失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    log("WARNING", "尝试重新连接微信客户端...")
                    try:
                        self.app_instance.parent.update_wx()
                        time.sleep(1)
                    except Exception as we:
                        log("ERROR", f"更新微信客户端失败: {str(we)}")
        return False


class AiWorkerThread(WorkerThreadBase):
    status_updated = QtCore.pyqtSignal(str)

    def __init__(self, app_instance, receiver, model="月之暗面", role="你很温馨,回复简单明了。", only_at=False):
        super().__init__()
        self.app_instance = app_instance
        self.receiver = receiver
        self.model = model
        self.system_content = role
        self.rules = self._load_rules()
        self.only_at = only_at
        self.at_me = "@" + self.app_instance.wx.nickname
        self.receiver_list = [r.strip() for r in receiver.replace(';', '；').split('；') if r.strip()]
        self.listen_list = []
        self.last_sent_messages = {}
        self._message_lock = threading.Lock()
        log_print(f"[AI_WORKER] Thread initialized for receiver(s): {self.receiver}")

    def init_listeners(self):
        if self._stop_event.is_set() or not self._is_running:
            log_print("[AI_WORKER] Listener initialization interrupted")
            return False

        for target in self.receiver_list:
            if self._stop_event.is_set() or not self._is_running:
                log_print("[AI_WORKER] Listener initialization interrupted")
                return False

            try:
                self.app_instance.wx.AddListenChat(who=target)
                self.listen_list.append(target)
                log_print(f"[AI_WORKER] Added listener for: {target}")
            except Exception as e:
                log("ERROR", f"添加监听失败: {target}, 错误: {str(e)}")
                log_print(f"[AI_WORKER] Failed to add listener: {target}, error: {str(e)}")
                raise e
        return True

    def _load_rules(self):
        try:
            with open('_internal/AutoReply_Rules.json', 'r', encoding='utf-8') as f:
                log_print(f"[AI_WORKER] Loaded auto-reply rules")
                return json.load(f)
        except FileNotFoundError:
            log_print("[AI_WORKER] Auto-reply rules file not found")
            return None
        except json.JSONDecodeError:
            log_print("[AI_WORKER] Failed to parse auto-reply rules file")
            return []

    def _get_chat_name(self, who):
        if not hasattr(self.app_instance.wx, 'GetChatName'):
            return who
        return self.app_instance.wx.GetChatName(who)

    def _match_rule(self, msg, who):
        if not self.rules:
            return []
        matched_replies = []
        msg = msg.strip()
        chat_name = self._get_chat_name(who)

        for rule in self.rules:
            if self._stop_event.is_set() or not self._is_running:
                return []

            keyword = rule['keyword'].strip()
            if not keyword:
                continue

            apply_to = rule.get('apply_to', '全部').strip()
            if apply_to != '全部':
                groups = [g.strip() for g in apply_to.replace(';', '；').split('；') if g.strip()]
                if chat_name not in groups:
                    continue

            match_type = rule['match_type']
            if match_type == '等于':
                if msg == keyword:
                    matched_replies.append(rule['reply_content'])
            elif match_type == '包含':
                if keyword in msg:
                    matched_replies.append(rule['reply_content'])
            elif match_type == '正则':
                try:
                    if re.search(keyword, msg):
                        matched_replies.append(rule['reply_content'])
                except re.error:
                    log("ERROR", f"无效的正则表达式: {keyword}")
                    log_print(f"[AI_WORKER] Invalid regular expression: {keyword}")
                    continue
        return matched_replies

    def run(self):
        self._is_running = True
        log_print("[AI_WORKER] start thread")

        try:
            if not self.init_listeners():
                log_print("[AI_WORKER] Listener initialization interrupted")
                return

            for receiver in self.receiver_list:
                if self._stop_event.is_set() or not self._is_running:
                    return

                response = self.app_instance.wx.SendMsg(msg=" ", who=receiver)
                if response.get('status') == '失败':
                    raise ValueError(f"初始化发送失败: {response.get('message', '未找到该备注的好友')}")
        except Exception as e:
            log("ERROR", f"初始化发送失败: {str(e)}")
            self.app_instance.on_thread_finished()
            return

        while not self._stop_event.is_set() and self._is_running:
            try:
                if self.isPaused():
                    self.wait_for_resume()
                    continue

                if self._stop_event.is_set() or not self._is_running:
                    break

                self._handle_messages()
            except Exception as e:
                log("ERROR", f"处理消息时发生异常: {str(e)}")
                if self._stop_event.is_set() or not self._is_running:
                    break
            finally:
                self.msleep(100)

        self._cleanup()
        self._is_running = False
        self.app_instance.on_thread_finished()

    def _handle_messages(self):
        if self._stop_event.is_set() or not self._is_running:
            return

        messages_dict = self.app_instance.wx.GetListenMessage()
        for chat, messages in messages_dict.items():
            if self._stop_event.is_set() or not self._is_running:
                return

            for message in messages:
                if self._stop_event.is_set() or not self._is_running:
                    return

                if self._is_ignored_message(message):
                    continue
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
        if self._stop_event.is_set() or not self._is_running:
            return

        if self.only_at and self.at_me not in msg:
            return

        if self.at_me in msg:
            msg = msg.replace(self.at_me, "").strip()

        is_group = who in self.receiver_list

        if self.rules:
            matched_replies = self._match_rule(msg, who)
            if matched_replies:
                for reply in matched_replies:
                    if self._stop_event.is_set() or not self._is_running:
                        return
                    self._send_reply(reply, who, is_group, message.sender if is_group else None)
                return

        if self.model != "禁用模型":
            if self._stop_event.is_set() or not self._is_running:
                return
            self._send_ai_response(msg, who, is_group, message.sender if is_group else None)

    def _cleanup(self):
        log_print("[AI_WORKER] cleanup")
        try:
            for target in self.listen_list:
                if hasattr(self.app_instance.wx, 'RemoveListenChat'):
                    self.app_instance.wx.RemoveListenChat(who=target)
            self.listen_list.clear()
        except Exception as e:
            log("ERROR", f"清理监听时出错: {str(e)}")

    def _should_prevent_duplicate(self, reply, who):
        chat_name = self._get_chat_name(who)
        current_time = time.time()
        same_reply_threshold = int(read_key_value('same_reply')) * 60

        with self._message_lock:
            if chat_name in self.last_sent_messages:
                last_message, last_time = self.last_sent_messages[chat_name]
                if reply == last_message:
                    time_diff = current_time - last_time
                    if time_diff < same_reply_threshold:
                        log("WARNING", f"阻止向 {chat_name} 发送重复消息: {reply}")
                        return True
        return False

    def _update_last_sent(self, reply, who):
        chat_name = self._get_chat_name(who)
        current_time = time.time()
        cutoff = current_time - 3600

        with self._message_lock:
            before_count = len(self.last_sent_messages)
            self.last_sent_messages = {
                k: v for k, v in self.last_sent_messages.items()
                if v[1] > cutoff
            }
            after_count = len(self.last_sent_messages)
            self.last_sent_messages[chat_name] = (reply, current_time)
            cleaned_count = before_count - (after_count - 1)
            if cleaned_count > 0:
                log("WARNING", "已清理监听缓存，释放内存空间")
                log_print(f"[AI_WORKER] Cleaned {cleaned_count} expired message caches, "
                          f"current cache remaining: {after_count} entries")

    def _send_reply(self, reply, who, is_group=False, at_user=None):
        try:
            if self._should_prevent_duplicate(reply, who):
                return

            if os.path.isdir(os.path.dirname(reply)):
                if os.path.isfile(reply):
                    response = self.app_instance.wx.SendFiles(filepath=reply, who=who)
                    log_print(response)
                    if response.get('status') == '失败':
                        raise ValueError(f"发送文件失败: {response.get('message', '未找到该备注的好友')}")
                    self._update_last_sent(f"[文件] {os.path.basename(reply)}", who)
                else:
                    raise FileNotFoundError(f"回复规则有误,没有 {os.path.basename(reply)} 文件")
                return

            time.sleep(int(read_key_value('reply_delay')))

            emotion_match = re.match(r'^SendEmotion:([\d,]+)', reply)
            if emotion_match:
                numbers = [int(n) for n in emotion_match.group(1).split(',') if n.strip().isdigit()]
                valid_indices = [n for n in numbers if n >= 1]

                if not valid_indices:
                    raise ValueError("表情索引必须≥1")
                selected_index = random.choice(valid_indices)
                emotion_id = selected_index - 1
                response = self.app_instance.wx.SendEmotion(emotion_id, who=who)
                log_print(response)
                if response.get('status') == '失败':
                    raise ValueError(f"发送表情失败: {response.get('message', '未找到表情包')}")
            else:
                if is_group and at_user and self.only_at:
                    response = self.app_instance.wx.SendMsg(msg=reply, who=who, at=at_user)
                else:
                    response = self.app_instance.wx.SendMsg(msg=reply, who=who)
                log_print(response)
                if response.get('status') == '失败':
                    raise ValueError(f"发送消息失败: {response.get('message', '未找到该备注的好友')}")

            self._update_last_sent(reply, who)

        except FileNotFoundError as e:
            log("ERROR", str(e))
        except ValueError as e:
            log("ERROR", f"无效的表情索引: {str(e)}")
        except Exception as e:
            log("ERROR", f"发送回复失败: {str(e)}")

    def _send_ai_response(self, msg, who, is_group=False, at_user=None):
        result = self._query_ai_model(msg)
        if result:
            if self._should_prevent_duplicate(result, who):
                return

            if is_group and at_user and self.only_at:
                response = self.app_instance.wx.SendMsg(msg=result, who=who, at=at_user)
            else:
                response = self.app_instance.wx.SendMsg(msg=result, who=who)

            if response.get('status') == '失败':
                raise ValueError(f"发送AI回复失败: {response.get('message', '未找到该备注的好友')}")

            self._update_last_sent(result, who)

    def _query_api(self, url, payload=None, headers=None, params=None, method='POST'):
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log("ERROR", f"API请求失败: {e}")
            return None

    def _get_access_token(self):
        response = self._query_api(
            "https://aip.baidubce.com/oauth/2.0/token",
            params={'grant_type': 'client_credentials',
                    'client_id': 'eCB39lMiTbHXV0mTt1d6bBw7',
                    'client_secret': 'WUbEO3XdMNJLTJKNQfFbMSQvtBVzRhvu'}
        )
        return response.get("access_token") if response else None

    def _query_ai_model(self, msg):
        if self.model == "禁用模型":
            return None
        try:
            if self.model == "文心一言":
                return self._query_wenxin_model(msg)
            elif self.model == "月之暗面":
                return self._query_moonshot_model(msg)
            elif self.model == "星火讯飞":
                return self._query_other_model(msg)
            else:
                return "未知的AI模型"
        except Exception as e:
            log("ERROR", f"AI模型查询失败: {str(e)}")
            return "抱歉，AI模型查询失败，请稍后再试。"

    def _query_wenxin_model(self, msg):
        access_token = self._get_access_token()
        if not access_token:
            return "无法获取百度API访问令牌"

        payload = {"messages": [{"role": "user", "content": msg}]}
        response = self._query_api(
            f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}",
            payload=payload,
            headers={'Content-Type': 'application/json'}
        )
        return response.get('result', "无法解析响应") if response else "请求失败"

    def _query_moonshot_model(self, msg):
        from openai import OpenAI
        client = OpenAI(api_key="sk-dx1RuweBS0LU0bCR5HizbWjXLuBL6HrS8BT21NEEGwbeyuo6",
                        base_url="https://api.moonshot.cn/v1")
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "system", "content": self.system_content},
                      {"role": "user", "content": msg}],
            temperature=0.9,
        )
        return completion.choices[0].message.content

    def _query_other_model(self, msg):
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
        response = self._query_api("https://spark-api-open.xf-yun.com/v1/chat/completions", data, header)
        return response['choices'][0]['message']['content'] if response else "无法解析响应"


class SplitWorkerThread(WorkerThreadBase):
    def __init__(self, app_instance, receiver, sentences):
        super().__init__()
        self.app_instance = app_instance
        self.receiver = receiver
        self.sentences = sentences
        log_print(f"[SPLIT_WORKER] Thread initialized for receiver: {receiver}, {len(sentences)} sentences")

    def run(self):
        self._is_running = True
        log_print(f"[SPLIT_WORKER] Thread started, sending {len(self.sentences)} messages to {self.receiver}")

        for i, sentence in enumerate(self.sentences):
            if self._stop_event.is_set() or not self._is_running:
                break

            if self._is_paused:
                self.wait_for_resume()
                if self._stop_event.is_set() or not self._is_running:
                    break

            try:
                log("INFO", f"发送 ({i + 1}/{len(self.sentences)}) '{sentence[:30]}...' 给 {self.receiver}")
                log_print(
                    f"[SPLIT_WORKER] Sending message {i + 1}/{len(self.sentences)}: '{sentence[:30]}...' to {self.receiver}")
                if not self._send_message(sentence, self.receiver):
                    raise LookupError("发送失败")
                self.msleep(500)
            except Exception as e:
                log("ERROR", f"发送消息时出错: {str(e)}")
                log_print(f"[SPLIT_WORKER] Error sending message: {str(e)}")
                self.app_instance.is_sending = False
                self.app_instance.is_scheduled_task_active = False
                self._stop_event.set()
                break

        self._is_running = False
        log_print(f"[SPLIT_WORKER] Thread finished, all messages sent to {self.receiver}")
        self.finished.emit()

    def _send_message(self, msg: str, who: str) -> bool:
        return self._retry_operation(lambda: self.app_instance.wx.SendMsg(msg=msg, who=who))

    def _retry_operation(self, operation, max_retries=3):
        for attempt in range(max_retries):
            try:
                result = operation()
                if result["status"] == "成功":
                    return True
                else:
                    raise LookupError(f"操作失败: {result.get('message', '未知错误')}")
            except Exception as e:
                log("ERROR", f"操作失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    log("WARNING", "尝试重新连接微信客户端...")
                    try:
                        self.app_instance.parent.update_wx()
                        time.sleep(1)
                    except Exception as we:
                        log("ERROR", f"Failed to update WeChat client: {str(we)}")
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
