import ctypes
import json
import os
import threading
import time
from datetime import datetime
from typing import Optional, Dict, List, Any

import requests
from PyQt6 import QtCore, QtMultimedia
from PyQt6.QtCore import QDateTime, pyqtSignal

from common import log, get_current_time, log_print


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
    def __init__(self, wx, receiver, model="月之暗面", role="你很温馨,回复简单明了。", only_at_mode=False,
                 at_nickname=""):
        super().__init__()
        self.wx = wx
        self.receiver = receiver
        self.model = model
        self.system_content = role
        self.rules = self._load_rules()
        self._is_running = True
        self.only_at_mode = only_at_mode
        self.at_nickname = at_nickname
        log_print(f"[AI_WORKER] Thread initialized - OnlyAt: {only_at_mode}, Nickname: {at_nickname}")

    def _load_rules(self) -> Optional[List[Dict]]:
        log_print("[AI_WORKER] Loading auto-reply rules...")
        try:
            if os.path.exists('_internal/AutoReply_Rules.json'):
                with open('_internal/AutoReply_Rules.json', 'r', encoding='utf-8') as f:
                    log_print("[AI_WORKER] Rules loaded successfully")
                    return json.load(f)
            else:
                log("WARNING", "自动回复规则文件不存在，你可以创建一个")
                log_print("[AI_WORKER] Rules file not found")
                return None
        except json.JSONDecodeError as e:
            log("ERROR", "规则文件中的JSON格式无效")
            log_print(f"[AI_WORKER] JSON decoding error: {str(e)}")
            return []
        except Exception as e:
            log("ERROR", f"加载回复规则时出错: {str(e)}")
            log_print(f"[AI_WORKER] Unexpected error loading rules: {str(e)}")
            return []

    def _match_rule(self, msg: str) -> List[str]:
        log_print(f"[AI_WORKER] Matching message: '{msg[:30]}...' against rules")
        if not self.rules:
            log_print("[AI_WORKER] No rules to match")
            return []

        matched_replies = []
        for rule in self.rules:
            try:
                processed_msg = msg
                # 在仅被@模式下，移除@前缀后再进行匹配
                if self.only_at_mode and self.at_nickname:
                    at_prefix = f"@{self.at_nickname}"
                    if at_prefix in processed_msg:
                        processed_msg = processed_msg.replace(at_prefix, "").strip()
                        log_print(f"[AI_WORKER] Processed message in OnlyAt mode: '{processed_msg[:30]}...'")

                if rule['match_type'] == '等于':
                    if processed_msg.strip() == rule['keyword'].strip():
                        log_print(f"[AI_WORKER] Full match found for keyword: {rule['keyword']}")
                        matched_replies.append(rule['reply_content'])
                elif rule['match_type'] == '包含':
                    if rule['keyword'].strip() in processed_msg.strip():
                        log_print(f"[AI_WORKER] Partial match found for keyword: {rule['keyword']}")
                        matched_replies.append(rule['reply_content'])
            except KeyError as e:
                log("ERROR", f"无效的规则格式: {rule}")
                log_print(f"[AI_WORKER] Rule format error: Missing key {str(e)}")

        return matched_replies

    def run(self):
        self._is_running = True
        log_print("[AI_WORKER] Thread started")

        if self._is_running:
            try:
                log_print(f"[AI_WORKER] Initializing connection with {self.receiver}")
                self.wx.SendMsg(msg=" ", who=self.receiver)
                log_print(f"[AI_WORKER] Connection initialized successfully")
            except Exception as e:
                log("ERROR", f"无法与 {self.receiver} 初始化连接: {str(e)}")
                log_print(f"[AI_WORKER] Connection initialization failed: {str(e)}")
                self._is_running = False

        while self._is_running and not self._stop_event.is_set():
            try:
                if self._is_paused:
                    log_print("[AI_WORKER] Thread paused, sleeping...")
                    time.sleep(0.1)
                    continue

                self._handle_specific_messages()

            except Exception as e:
                log("ERROR", f"处理消息时出错: {str(e)}")
                log_print(f"[AI_WORKER] Critical error in main loop: {str(e)}")
                time.sleep(1)
            finally:
                self.msleep(10)

        log_print("[AI_WORKER] Thread finished")
        self.finished.emit()

    def _handle_specific_messages(self):
        msgs = self.wx.GetAllMessage()
        if msgs and msgs[-1].type == "friend":
            msg = msgs[-1].content
            whoName = msgs[-1][0]
            if self._should_reply(msg):
                self._process_message(msg, self.receiver, whoName)

    def _should_reply(self, msg: str) -> bool:
        if self.only_at_mode and self.at_nickname:
            log_print(f"[AI_WORKER] Checking message for @{self.at_nickname}: {msg[:30]}...")
            return f"@{self.at_nickname}" in msg
        log_print("[AI_WORKER] Replying to all messages")
        return True

    def _process_message(self, msg: str, who: str, who_name: str) -> None:
        log_print(f"[AI_WORKER] Processing message: '{msg[:30]}...' from {who}")

        # 提取@信息（如果有）
        at_info = None
        if self.only_at_mode and self.at_nickname:
            at_prefix = f"@{self.at_nickname}"
            if at_prefix in msg:
                # 保存原始消息用于匹配规则
                original_msg = msg
                # 处理后的消息用于匹配规则（移除@前缀）
                processed_msg = original_msg.replace(at_prefix, "").strip()
                at_info = at_prefix  # 保存@信息用于回复
        else:
            processed_msg = msg

        if self.rules:
            # 使用处理后的消息进行规则匹配
            matched_replies = self._match_rule(processed_msg if self.only_at_mode else msg)
            if matched_replies:
                for reply in matched_replies:
                    try:
                        if os.path.isdir(os.path.dirname(reply)):
                            if os.path.isfile(reply):
                                log("INFO", f"发送文件 {os.path.basename(reply)} 给 {who} 根据规则")
                                log_print(f"[AI_WORKER] Sending file: {os.path.basename(reply)} to {who}")
                                self.wx.SendFiles(filepath=reply, who=who)
                            else:
                                log("ERROR", f"无效的规则: 文件不存在: {os.path.basename(reply)}")
                                log_print(f"[AI_WORKER] File not found: {os.path.basename(reply)}")
                        else:
                            log("INFO", f"根据规则自动回复 '{reply}' 给 {who}")
                            log_print(f"[AI_WORKER] Sending auto-reply: '{reply[:30]}...' to {who}")

                            if self.only_at_mode:
                                self.wx.SendMsg(msg=reply, who=who, at=who_name)
                            else:
                                self.wx.SendMsg(msg=reply, who=who)
                    except Exception as e:
                        log("ERROR", f"发送自动回复时出错: {str(e)}")
                        log_print(f"[AI_WORKER] Error sending auto-reply: {str(e)}")
                return

        if self.model == "禁用模型":
            return

        log_print(f"[AI_WORKER] No rule matches, generating AI reply for: '{processed_msg[:30]}...'")
        self._generate_ai_reply(processed_msg if self.only_at_mode else msg, who, who_name)

    def _generate_ai_reply(self, msg: str, who: str, who_name: str):
        log_print(f"[AI_WORKER] Generating AI reply using {self.model} model")
        try:
            if self.model == "文心一言":
                result = self._query_wenxin_api(msg)
            elif self.model == "月之暗面":
                result = self._query_moonshot_api(msg)
            else:
                result = self._query_default_api(msg)

            if result:
                log("INFO", f"AI回复发送给 {who}: {result[:30]}...")
                log_print(f"[AI_WORKER] AI reply sent to {who}: {result[:30]}...")

                if self.only_at_mode:
                    self.wx.SendMsg(msg=result, who=who, at=who_name)
                else:
                    self.wx.SendMsg(msg=result, who=who)

        except Exception as e:
            log("ERROR", f"调用AI API时出错: {str(e)}")
            log_print(f"[AI_WORKER] Critical error calling AI API: {str(e)}")

    def _query_wenxin_api(self, msg: str) -> str:
        log_print("[AI_WORKER] Querying Wenxin Yiyan API")
        access_token = self._get_access_token()
        if not access_token:
            log_print("[AI_WORKER] Failed to get access token")
            return "Unable to obtain access token"

        payload = {"messages": [{"role": "user", "content": msg}]}
        result = self._query_api(
            f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}",
            payload=payload,
            headers={'Content-Type': 'application/json'}
        )

        return result.get('result', "Unable to parse response")

    def _get_access_token(self) -> Optional[str]:
        log_print("[AI_WORKER] Fetching Baidu API access token")
        result = self._query_api(
            "https://aip.baidubce.com/oauth/2.0/token",
            params={'grant_type': 'client_credentials',
                    'client_id': 'eCB39lMiTbHXV0mTt1d6bBw7',
                    'client_secret': 'WUbEO3XdMNJLTJKNQfFbMSQvtBVzRhvu'}
        )

        return result.get("access_token") if result else None

    def _query_moonshot_api(self, msg: str) -> str:
        log_print("[AI_WORKER] Querying Moonshot API")
        from openai import OpenAI

        client = OpenAI(
            api_key="sk-dx1RuweBS0LU0bCR5HizbWjXLuBL6HrS8BT21NEEGwbeyuo6",
            base_url="https://api.moonshot.cn/v1"
        )

        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "system", "content": self.system_content},
                      {"role": "user", "content": msg}],
            temperature=0.9,
        )

        return completion.choices[0].message.content

    def _query_default_api(self, msg: str) -> str:
        log_print("[AI_WORKER] Querying default API")
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
        return response['choices'][0]['message']['content'] if response else "Unable to parse response"

    def _query_api(self, url: str, payload: Optional[Dict] = None,
                   headers: Optional[Dict] = None, params: Optional[Dict] = None,
                   method: str = 'POST') -> Optional[Dict]:
        log_print(f"[AI_WORKER] Making API request to: {url[:50]}...")
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            log_print(f"[AI_WORKER] API request successful: {url[:30]}...")
            return response.json()
        except requests.RequestException as e:
            log("ERROR", f"API请求失败: {str(e)}")
            log_print(f"[AI_WORKER] API request error: {str(e)}")
            return None
        except Exception as e:
            log("ERROR", f"处理API响应时出错: {str(e)}")
            log_print(f"[AI_WORKER] Unexpected error processing API response: {str(e)}")
            return None


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