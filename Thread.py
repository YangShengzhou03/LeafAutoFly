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

from common import log, get_current_time


class WorkerThreadBase(QtCore.QThread):
    """线程基类，提供终止功能"""
    finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._stop_event = threading.Event()
        self._stop_lock = threading.Lock()  # 添加锁确保线程安全

    def run(self) -> None:
        raise NotImplementedError("子类必须实现run方法")

    def request_interruption(self) -> None:
        """请求线程中断并设置运行状态"""
        with self._stop_lock:
            self._stop_event.set()
            self._is_running = False
        log("WARNING", f"{self.__class__.__name__} 收到用户的终止请求")

    def is_running(self) -> bool:
        with self._stop_lock:
            return self._is_running

    def check_interruption(self) -> bool:
        """检查是否请求中断"""
        with self._stop_lock:
            if self._stop_event.is_set():
                return True
        return False


class AiWorkerThread(WorkerThreadBase):
    """AI自动回复工作线程"""

    def __init__(self, app_instance, receiver: str, wx: Any, model: str = "月之暗面",
                 role: str = "你很温馨,回复简单明了。"):
        super().__init__()
        self.app_instance = app_instance
        self.receiver = receiver
        self.wx = wx
        self.model = model
        self.system_content = role
        self.rules = self._load_rules()
        self._is_running = True

    def _load_rules(self) -> Optional[List[Dict]]:
        """加载自动回复规则"""
        try:
            if os.path.exists('_internal/AutoReply_Rules.json'):
                with open('_internal/AutoReply_Rules.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                log("WARNING", "回复规则文件不存在,您可新建规则")
                return None
        except json.JSONDecodeError as e:
            log("ERROR", f"JSON解析错误: {str(e)}")
            return []
        except Exception as e:
            log("ERROR", f"加载回复规则时出错: {str(e)}")
            return []

    def _match_rule(self, msg: str) -> List[str]:
        """匹配自动回复规则"""
        if not self.rules:
            return []

        matched_replies = []
        for rule in self.rules:
            try:
                if rule['match_type'] == '全匹配':
                    if msg.strip() == rule['keyword'].strip():
                        matched_replies.append(rule['reply_content'])
                elif rule['match_type'] == '半匹配':
                    if rule['keyword'].strip() in msg.strip():
                        matched_replies.append(rule['reply_content'])
            except KeyError as e:
                log("ERROR", f"规则格式错误，缺少键: {str(e)}")

        return matched_replies

    def run(self) -> None:
        """线程主循环"""
        self._is_running = True
        log("INFO", f"AiWorkerThread 已启动，接收者: {self.receiver}")

        # 初始化连接检查
        if self.receiver != "全局Ai接管" and self._is_running:
            try:
                if self.wx:
                    self.wx.SendMsg(msg=" ", who=self.receiver)
                    log("INFO", f"与 {self.receiver} 的连接初始化成功")
                else:
                    log("ERROR", f"找不到微信实例，无法初始化与 {self.receiver} 的连接")
                    self._is_running = False
            except Exception as e:
                log("ERROR", f"初始化与 {self.receiver} 的连接失败: {str(e)}")
                self._is_running = False

        # 主消息循环
        while self._is_running and not self._stop_event.is_set():
            try:
                if self.receiver == "全局Ai接管":
                    self._handle_global_messages()
                else:
                    self._handle_specific_messages()

            except Exception as e:
                log("ERROR", f"处理消息时出错: {str(e)}")
                time.sleep(1)  # 出错后休眠，避免CPU占用过高
            finally:
                # 短暂休眠，避免CPU占用过高，同时检查中断请求
                for _ in range(5):
                    if self._stop_event.is_set():
                        break
                    self.msleep(20)

        log("INFO", f"AiWorkerThread 已停止，接收者: {self.receiver}")
        self.finished.emit()

    def _get_wx_instance(self) -> Any:
        """获取微信实例"""
        return self.wx

    def _handle_global_messages(self) -> None:
        """处理全局消息"""
        if self._stop_event.is_set():
            return

        wx_instance = self._get_wx_instance()
        if not wx_instance:
            return

        new_msg = wx_instance.GetAllNewMessage()
        if not new_msg:
            return

        # 获取最新消息的发送者和内容
        who = next(iter(new_msg))
        who = re.sub(r'\s*[（(]\d+[）)]\s*$', '', who)

        msgs = wx_instance.GetAllMessage()
        if msgs and msgs[-1].type == "friend":
            msg = msgs[-1].content
            self._process_message(msg, who)

    def _handle_specific_messages(self) -> None:
        """处理特定接收者的消息"""
        if self._stop_event.is_set():
            return

        wx_instance = self._get_wx_instance()
        if not wx_instance:
            return

        msgs = wx_instance.GetAllMessage()
        if msgs and msgs[-1].type == "friend":
            msg = msgs[-1].content
            self._process_message(msg, self.receiver)

    def _process_message(self, msg: str, who: str) -> None:
        """处理消息并决定是否回复"""
        if self._stop_event.is_set():
            return

        if self.rules:
            matched_replies = self._match_rule(msg)
            if matched_replies:
                wx_instance = self._get_wx_instance()
                if not wx_instance:
                    return

                for reply in matched_replies:
                    if self._stop_event.is_set():
                        return

                    try:
                        if os.path.isdir(os.path.dirname(reply)):
                            if os.path.isfile(reply):
                                log("INFO", f"根据规则发送文件 {os.path.basename(reply)} 给 {who}")
                                wx_instance.SendFiles(filepath=reply, who=who)
                            else:
                                log("ERROR", f"回复规则有误,文件不存在: {os.path.basename(reply)}")
                        else:
                            log("INFO", f"根据规则自动回复 '{reply}' 给 {who}")
                            wx_instance.SendMsg(msg=reply, who=who)
                    except Exception as e:
                        log("ERROR", f"发送自动回复时出错: {str(e)}")
                return

        # 如果没有匹配的规则，调用AI回复
        self._generate_ai_reply(msg, who)

    def _generate_ai_reply(self, msg: str, who: str) -> None:
        """调用AI模型生成回复"""
        if self._stop_event.is_set():
            return

        try:
            if self.model == "文心一言":
                result = self._query_wenxin_api(msg)
            elif self.model == "月之暗面":
                result = self._query_moonshot_api(msg)
            else:
                result = self._query_default_api(msg)

            if result and not self._stop_event.is_set():
                wx_instance = self._get_wx_instance()
                if wx_instance:
                    wx_instance.SendMsg(msg=result, who=who)
                    log("INFO", f"Ai发送给 {who}: {result[:30]}...")

        except Exception as e:
            log("ERROR", f"调用AI API时出错: {str(e)}")

    def _query_wenxin_api(self, msg: str) -> str:
        """调用文心一言API"""
        access_token = self._get_access_token()
        if not access_token:
            return "无法获取访问令牌"

        payload = {"messages": [{"role": "user", "content": msg}]}
        result = self._query_api(
            f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}",
            payload=payload,
            headers={'Content-Type': 'application/json'}
        )

        return result.get('result', "无法解析响应")

    def _get_access_token(self) -> Optional[str]:
        """获取百度API访问令牌"""
        result = self._query_api(
            "https://aip.baidubce.com/oauth/2.0/token",
            params={'grant_type': 'client_credentials',
                    'client_id': 'eCB39lMiTbHXV0mTt1d6bBw7',
                    'client_secret': 'WUbEO3XdMNJLTJKNQfFbMSQvtBVzRhvu'}
        )

        return result.get("access_token") if result else None

    def _query_moonshot_api(self, msg: str) -> str:
        """调用月之暗面API"""
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
        """调用默认API"""
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

    def _query_api(self, url: str, payload: Optional[Dict] = None,
                   headers: Optional[Dict] = None, params: Optional[Dict] = None,
                   method: str = 'POST') -> Optional[Dict]:
        """通用API查询方法"""
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                params=params,
                timeout=30  # 添加超时设置
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log("ERROR", f"API请求失败: {str(e)}")
            return None
        except Exception as e:
            log("ERROR", f"处理API响应时出错: {str(e)}")
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
    """定时任务工作线程"""

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
                        # 格式化为友好的时间表示
                        hours, remainder = divmod(int(remaining_time), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_parts = []
                        if hours > 0:
                            time_parts.append(f"{hours}时")
                        if minutes > 0:
                            time_parts.append(f"{minutes}分")
                        if seconds > 0 or not time_parts:  # 确保至少显示0秒
                            time_parts.append(f"{seconds}秒")
                        friendly_time = ''.join(time_parts)

                        log("INFO", f"下一个任务将在 {friendly_time} 后执行")

                        # 分段休眠，以便能够及时响应停止请求
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
                    # 出错后适当休眠，避免CPU占用过高
                    time.sleep(1)

        finally:
            # 恢复系统睡眠设置
            if self.prevent_sleep:
                self._set_system_state(self.ES_CONTINUOUS)
                log("WARNING", "已恢复系统休眠和锁屏设置")
            self._is_running = False
            self.finished.emit()

    def _set_system_state(self, state_flags: int) -> None:
        """设置系统执行状态并记录当前状态"""
        try:
            self._system_state = ctypes.windll.kernel32.SetThreadExecutionState(state_flags)
            if not self._system_state:
                log("ERROR", f"设置系统状态失败，错误码: {ctypes.GetLastError()}")
        except Exception as e:
            log("ERROR", f"调用系统API设置状态时出错: {str(e)}")

    def _find_next_ready_task(self) -> Optional[Dict]:
        """查找下一个要执行的任务"""
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
        """执行任务并返回成功/失败状态"""
        max_retries = 3
        retries = 0
        success = False

        log("INFO", f"开始执行任务: {task.get('name', '未知')}")

        while retries < max_retries and not success and not self.check_interruption():
            try:
                name = task['name']
                info = task['info']
                wx_nickname = task['wx_nickname']

                # 执行任务前检查是否终止
                if self.check_interruption():
                    return False

                # 获取对应的微信实例
                wx_instance = self._get_wx_instance(wx_nickname)
                if not wx_instance:
                    log("ERROR", f"找不到微信实例 '{wx_nickname}'，无法执行任务")
                    raise ValueError(f"找不到微信实例 '{wx_nickname}'")

                # 执行任务前检查是否终止
                if self.check_interruption():
                    return False

                if os.path.isdir(os.path.dirname(info)):
                    if os.path.isfile(info):
                        file_name = os.path.basename(info)
                        log("INFO", f"开始把文件 {file_name} 发给 {name} (发送方: {wx_nickname})")
                        # 使用可中断的发送方法
                        success = self._send_with_interruption(lambda: wx_instance.SendFiles(filepath=info, who=name))
                    else:
                        raise FileNotFoundError(f"该路径下没有 {os.path.basename(info)} 文件")
                else:
                    log("INFO", f"开始把消息 '{info[:30]}...' 发给 {name} (发送方: {wx_nickname})")
                    if "@所有人" in info:
                        info = info.replace("@所有人", "").strip()
                        # 使用可中断的发送方法
                        success = self._send_with_interruption(lambda: wx_instance.AtAll(msg=info, who=name))
                    else:
                        # 使用可中断的发送方法
                        success = self._send_with_interruption(lambda: wx_instance.SendMsg(msg=info, who=name))

                if success:
                    log("DEBUG", f"成功执行任务: 发送给 {name} (发送方: {wx_nickname})")

            except Exception as e:
                log("ERROR", f"执行任务失败 (尝试 {retries + 1}/{max_retries}): {str(e)}")
                retries += 1

                # 如果不是最后一次尝试，尝试重新加载微信客户端
                if retries < max_retries and not self.check_interruption():
                    log("WARNING", "尝试重新连接微信客户端...")
                    try:
                        self.app_instance.parent.update_wx()
                        # 等待一段时间，让微信客户端稳定
                        for _ in range(10):
                            if self.check_interruption():
                                break
                            self.msleep(100)
                    except Exception as we:
                        log("ERROR", f"更新微信客户端失败: {str(we)}")

        return success

    def _get_wx_instance(self, wx_nickname: str) -> Any:
        """根据微信昵称获取对应的微信实例"""
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
        """包装发送方法，使其可以被中断"""
        # 检查是否有停止请求
        if self.check_interruption():
            return False

        try:
            # 创建一个线程执行发送操作
            send_thread = threading.Thread(target=send_func)
            send_thread.daemon = True
            send_thread.start()

            # 等待发送线程完成或被中断
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
    """错误提示音播放线程"""
    finished = QtCore.pyqtSignal()
    _is_running = False

    def __init__(self):
        super().__init__()
        self.sound_file = None
        self.player = None
        self.audio_output = None

    def update_sound_file(self, sound_file_path: str) -> None:
        self.sound_file = sound_file_path

    def run(self) -> None:
        if not self.sound_file or not os.path.exists(self.sound_file) or self._is_running:
            return
        self._is_running = True

        # 确保每次都创建新的播放器和音频输出
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

        # 使用更安全的方式等待播放完成
        loop = QtCore.QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec()

    def _on_media_status_changed(self, status: QtMultimedia.QMediaPlayer.MediaStatus) -> None:
        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            self.cleanup_resources()

    def cleanup_resources(self) -> None:
        if self.player:
            self.player.stop()
            self.player.mediaStatusChanged.disconnect()
            self.player = None

        if self.audio_output:
            self.audio_output = None

        self._is_running = False
        self.finished.emit()

    def stop_playback(self) -> None:
        if self._is_running:
            self.cleanup_resources()

    def play_test(self) -> None:
        if not self.isRunning() and not self._is_running:
            self.start()
