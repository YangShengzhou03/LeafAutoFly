import json
import os
import re
import smtplib
import time
from datetime import datetime, timedelta
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from queue import Queue
from threading import Thread

import openpyxl
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

from System_info import read_key_value
from Thread import WorkerThread, ErrorSoundThread
from common import get_resource_path, log, str_to_bool, log_print


class AutoInfo(QtWidgets.QWidget):
    def __init__(self, wx_dict, membership, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.wx_dict = wx_dict
        self.Membership = membership
        self.ready_tasks = []
        self.completed_tasks = []
        self.is_executing = False
        self.worker_thread = None
        self.error_sound_thread = ErrorSoundThread()
        self.audio_files = {
            0: get_resource_path('resources/sound/error_sound_1.mp3'),
            1: get_resource_path('resources/sound/error_sound_2.mp3'),
            2: get_resource_path('resources/sound/error_sound_3.mp3'),
            3: get_resource_path('resources/sound/error_sound_4.mp3'),
            4: get_resource_path('resources/sound/error_sound_5.mp3')
        }

        self.email_queue = Queue()
        self.email_thread = Thread(target=self._process_email_queue, daemon=True)
        self.email_thread.start()
        self.last_email_time = 0
        self.email_cooldown = 60
        log_print(f"[AutoInfo] Initialization completed, membership type: {self.Membership}")

    def openFileNameDialog(self, filepath=None):
        try:
            if filepath:
                self.parent.message_lineEdit.setText(str(filepath))
                log_print(f"[AutoInfo] File path set: {filepath}")
                return

            file_filters = (
                "All Files (*);;"
                "Image Files (*.bmp *.gif *.jpg *.jpeg *.png *.svg *.tiff);;"
                "Document Files (*.doc *.docx *.pdf *.txt *.odt);;"
                "Spreadsheets (*.xls *.xlsx *.ods);;"
                "Presentations (*.ppt *.pptx *.odp);;"
                "Audio Files (*.mp3 *.wav *.flac *.aac);;"
                "Video Files (*.mp4 *.avi *.mkv *.mov);;"
                "Compressed Files (*.zip *.rar *.tar *.gz *.bz2)"
            )

            options = QtWidgets.QFileDialog.Option.ReadOnly
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Select File to Send",
                "",
                file_filters,
                options=options
            )

            if fileName:
                self.parent.message_lineEdit.setText(fileName)
                log_print(f"[AutoInfo] File selected: {fileName}")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to open file dialog: {str(e)}")

    def video_chat(self):
        try:
            self.parent.message_lineEdit.setText('Video_chat')
            log_print("[AutoInfo] Set to video chat")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to set video chat: {str(e)}")

    def save_tasks_to_json(self):
        try:
            with open('_internal/tasks.json', 'w', encoding='utf-8') as f:
                json.dump(self.ready_tasks, f, ensure_ascii=False, indent=4)
            log_print(f"[AutoInfo] Tasks saved successfully, total {len(self.ready_tasks)} tasks")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to save tasks: {str(e)}")
            log("ERROR", "非管理员身份运行软件,未能将操作保存")

    def add_list_item(self):
        log_print("[AutoInfo] Attempting to add task...")
        try:
            time_text, name_text, info_text, frequency = self.get_input_values()
            wx_nickname = self.parent.comboBox_nickName.currentText()

            if not all([time_text, name_text, info_text]):
                log_print("[AutoInfo] Failed to add task: Incomplete input")
                log("WARNING", "请先输入有效内容和接收人再添加任务")
                return

            if self.Membership == 'Free' and len(self.ready_tasks) >= 5:
                log_print("[AutoInfo] Failed to add task: Free version task limit reached")
                log("WARNING", "试用版最多添加5个任务，请升级版本")
                QtWidgets.QMessageBox.warning(self, "试用版限制", "试用版最多添加5个任务，请升级版本")
                return
            elif self.Membership == 'Base' and len(self.ready_tasks) >= 30:
                log_print("[AutoInfo] Failed to add task: Basic version task limit reached")
                log("WARNING", "基础版最多添加30个任务,升级Ai版无限制")
                QtWidgets.QMessageBox.warning(self, "标准版限制", "标准版最多添加30个任务，请升级版本")
                return

            widget_item = self.create_widget(time_text, name_text, info_text, frequency, wx_nickname)
            self.parent.formLayout_3.addRow(widget_item)
            self.ready_tasks.append({
                'time': time_text,
                'name': name_text,
                'info': info_text,
                'frequency': frequency,
                'wx_nickname': wx_nickname
            })
            log('INFO',
                f'已添加 {time_text[-8:]} 把 {info_text[:25] + "……" if len(info_text) > 25 else info_text} 发给 {name_text[:8]} (发送方: {wx_nickname})')
            log_print(f"[AutoInfo] Task added successfully: {name_text} - {info_text[:20]}... (Sender: {wx_nickname})")

            self.parent.dateTimeEdit.setDateTime(
                datetime.fromisoformat(time_text) + timedelta(minutes=int(read_key_value('add_timestep'))))

            self.save_tasks_to_json()
        except Exception as e:
            log_print(f"[AutoInfo] Error adding task: {str(e)}")

    def create_widget(self, time_text, name_text, info_text, frequency, wx_nickname):
        try:
            # 确保所有文本参数都是字符串类型
            name_text = str(name_text)
            info_text = str(info_text)
            wx_nickname = str(wx_nickname)

            widget_item = QtWidgets.QWidget(parent=self.parent.scrollAreaWidgetContents_3)
            widget_item.setMinimumSize(QtCore.QSize(360, 70))
            widget_item.setMaximumSize(QtCore.QSize(360, 70))
            widget_item.setStyleSheet("background-color: rgb(255, 255, 255);\nborder-radius:18px")
            widget_item.setObjectName("widget_item")

            horizontalLayout_76 = QtWidgets.QHBoxLayout(widget_item)
            horizontalLayout_76.setContentsMargins(12, 2, 12, 2)
            horizontalLayout_76.setSpacing(6)

            widget_54 = QtWidgets.QWidget()
            widget_54.setMinimumSize(QtCore.QSize(36, 36))
            widget_54.setMaximumSize(QtCore.QSize(36, 36))
            widget_54.setStyleSheet(f"image: url({get_resource_path('resources/img/page1/page1_发送就绪.svg')});")
            horizontalLayout_76.addWidget(widget_54)

            verticalLayout_64 = QtWidgets.QVBoxLayout()
            verticalLayout_64.setContentsMargins(6, 6, 6, 6)
            verticalLayout_64.setSpacing(0)
            horizontalLayout_76.addLayout(verticalLayout_64)

            top_layout = QtWidgets.QHBoxLayout()
            top_layout.setContentsMargins(0, 0, 0, 0)
            top_layout.setSpacing(4)

            receiver_label = QtWidgets.QLabel(name_text)
            receiver_label.setStyleSheet("color:rgb(0, 0, 0);")
            receiver_label.setFont(QtGui.QFont("微软雅黑 Light", 12))
            receiver_label.setWordWrap(False)
            receiver_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            receiver_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            receiver_label.setMinimumWidth(1)
            receiver_label.installEventFilter(self)
            top_layout.addWidget(receiver_label)

            wx_label = QtWidgets.QLabel(wx_nickname)
            wx_label.setStyleSheet("color: rgb(105, 27, 253); padding-left: 8px;")
            wx_label.setFont(QtGui.QFont("微软雅黑 Light", 10))
            wx_label.setWordWrap(False)
            wx_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            wx_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            wx_label.setMinimumWidth(1)
            wx_label.installEventFilter(self)
            top_layout.addWidget(wx_label)

            time_label = QtWidgets.QLabel(time_text)
            time_label.setStyleSheet("color: rgb(169, 169, 169);")
            time_label.setFont(QtGui.QFont("微软雅黑", 10))
            time_label.setAlignment(
                Qt.AlignmentFlag.AlignRight |
                Qt.AlignmentFlag.AlignTrailing |
                Qt.AlignmentFlag.AlignVCenter
            )
            time_label.setFixedWidth(140)
            time_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            top_layout.addWidget(time_label)

            top_layout.setStretch(0, 1)
            verticalLayout_64.addLayout(top_layout)

            bottom_layout = QtWidgets.QHBoxLayout()
            bottom_layout.setContentsMargins(0, 6, 12, 3)
            bottom_layout.setSpacing(4)

            message_label = QtWidgets.QLabel(info_text)
            message_label.setStyleSheet("color: rgb(169, 169, 169);")
            message_label.setFont(QtGui.QFont("微软雅黑", 10))
            message_label.setWordWrap(False)
            message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            message_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            message_label.setMinimumWidth(1)
            message_label.installEventFilter(self)
            bottom_layout.addWidget(message_label)

            delete_button = QtWidgets.QPushButton("删除")
            delete_button.setFixedSize(50, 25)
            delete_button.setStyleSheet(
                "QPushButton { background-color: transparent; color: red; } "
                "QPushButton:hover { background-color: rgba(255, 0, 0, 0.1); }"
            )
            delete_button.clicked.connect(
                lambda _, t=time_text, n=name_text, i=info_text, wx=wx_nickname: self.remove_task(t, n, i, wx)
            )
            delete_button.setVisible(False)
            bottom_layout.addWidget(delete_button)

            verticalLayout_64.addLayout(bottom_layout)

            widget_item.enterEvent = lambda e, btn=delete_button: btn.setVisible(True)
            widget_item.leaveEvent = lambda e, btn=delete_button: btn.setVisible(False)

            widget_item.task = {
                'time': time_text,
                'name': name_text,
                'info': info_text,
                'frequency': frequency,
                'wx_nickname': wx_nickname
            }

            log_print(
                f"[AutoInfo] Task widget created successfully: {name_text} - {info_text[:20]}... (Sender: {wx_nickname})")
            return widget_item

        except Exception as e:
            log_print(f"[AutoInfo] Failed to create task widget: {str(e)}")
            return None

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.Resize and isinstance(obj, QtWidgets.QLabel):
            width = obj.width() - 2
            original_text = obj.property("originalText")
            if not original_text:
                original_text = obj.text()
                obj.setProperty("originalText", original_text)

            font_metrics = obj.fontMetrics()
            elided_text = font_metrics.elidedText(original_text, Qt.TextElideMode.ElideRight, width)
            obj.setText(elided_text)

        return super().eventFilter(obj, event)

    def remove_task(self, time_text, name_text, info_text, wx_nickname):
        log_print(f"[AutoInfo] Attempting to delete task: {name_text} - {info_text[:20]}... (Sender: {wx_nickname})")
        try:
            if self.error_sound_thread._is_running:
                self.error_sound_thread.stop_playback()
                log_print("[AutoInfo] Error sound stopped")

            for task in self.ready_tasks:
                if (task['time'] == time_text and
                        task['name'] == name_text and
                        task['info'] == info_text and
                        task['wx_nickname'] == wx_nickname):
                    self.ready_tasks.remove(task)
                    log('WARNING', f'已删除任务 {info_text[:35] + "……" if len(info_text) > 30 else info_text}')
                    log_print(f"[AutoInfo] Task deleted successfully")
                    break

            if not self.ready_tasks:
                self.is_executing = False
                self.parent.start_pushButton.setText("开始执行")
                if self.worker_thread is not None:
                    self.worker_thread.request_interruption()
                    self.worker_thread = None
                    log_print("[AutoInfo] Worker thread stopped")

            self.update_ui()
            self.save_tasks_to_json()
        except Exception as e:
            log_print(f"[AutoInfo] Failed to delete task: {str(e)}")

    def update_ui(self):
        log_print("[AutoInfo] Updating UI display...")
        try:
            self.clear_layout(self.parent.formLayout_3)
            for task in self.ready_tasks:
                widget = self.create_widget(
                    task['time'],
                    task['name'],
                    task['info'],
                    task['frequency'],
                    task['wx_nickname']
                )
                self.parent.formLayout_3.addRow(widget)
            log_print(f"[AutoInfo] UI updated, displaying {len(self.ready_tasks)} tasks")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to update UI: {str(e)}")

    def get_input_values(self):
        try:
            name_text = self.parent.receiver_lineEdit.text()
            info_text = self.parent.message_lineEdit.text()
            time_text = self.parent.dateTimeEdit.dateTime().toString(QtCore.Qt.DateFormat.ISODate)
            frequency = self.parent.comboBox_Frequency.currentText()
            return time_text, name_text, info_text, frequency
        except Exception as e:
            log_print(f"[AutoInfo] Failed to get input values: {str(e)}")
            return None, None, None, None

    def on_start_clicked(self):
        log_print("[AutoInfo] Start button clicked...")
        try:
            if self.is_executing:
                self.is_executing = False
                self.parent.start_pushButton.setText("开始执行")
                if self.worker_thread is not None:
                    self.worker_thread.request_interruption()
                    self.worker_thread = None
                    log_print("[AutoInfo] Worker thread stopped")
                if self.error_sound_thread._is_running:
                    self.error_sound_thread.stop_playback()
                    log_print("[AutoInfo] Error sound stopped")
                log_print("[AutoInfo] Stopped executing all tasks")
            else:
                if not self.ready_tasks:
                    log("WARNING", "任务列表为空，请先添加任务至任务列表")
                    log_print("[AutoInfo] Task list is empty, cannot start execution")
                else:
                    self.is_executing = True
                    self.parent.start_pushButton.setText("停止执行")
                    self.worker_thread = WorkerThread(self)
                    self.worker_thread.prevent_sleep = self.parent.checkBox_stopSleep.isChecked()
                    self.worker_thread.current_time = 'mix' if str_to_bool(read_key_value('net_time')) else 'sys'
                    self.worker_thread.finished.connect(self.on_thread_finished)
                    self.worker_thread.start()
                    log_print("[AutoInfo] Started executing tasks, worker thread launched")
        except Exception as e:
            log_print(f"[AutoInfo] Error handling start button click: {str(e)}")

    def clear_layout(self, layout):
        try:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        except Exception as e:
            log_print(f"[AutoInfo] Failed to clear layout: {str(e)}")

    def update_task_status(self, task, status):
        log_print(f"[AutoInfo] Updating task status: {task['name']} - {status} (Sender: {task['wx_nickname']})")
        try:
            if task in self.ready_tasks:
                task_index = self.ready_tasks.index(task)
                self.ready_tasks[task_index]['status'] = status
                self.completed_tasks.append(self.ready_tasks.pop(task_index))

                for i in range(self.parent.formLayout_3.count()):
                    item = self.parent.formLayout_3.itemAt(i)
                    if item and item.widget():
                        widget_item = item.widget()
                        if hasattr(widget_item, 'task') and all(
                                widget_item.task[key] == task[key] for key in
                                ['time', 'name', 'info', 'frequency', 'wx_nickname']):
                            # 修改：使用正确的方式查找图标部件
                            widget_image = widget_item.findChild(QtWidgets.QWidget, None)
                            if widget_image and widget_image.minimumSize() == QtCore.QSize(36, 36):
                                if status == '成功':
                                    icon_path_key = 'page1_发送成功.svg'
                                else:
                                    icon_path_key = 'page1_发送失败.svg'
                                    # 仅在首次失败时播放声音和发送邮件
                                    if 'error_count' not in task:
                                        task['error_count'] = 1
                                        self.play_error_sound()
                                        self.send_error_email(task)
                                    else:
                                        task['error_count'] += 1
                                        log_print(
                                            f"[AutoInfo] Task {task['name']} has failed {task['error_count']} times")

                                new_icon_path = get_resource_path(f'resources/img/page1/{icon_path_key}')
                                widget_image.setStyleSheet(f"image: url({new_icon_path});")

                                # 强制重绘部件，确保视觉更新
                                widget_image.update()
                                widget_item.update()

                            # 处理重复任务
                            next_time = datetime.fromisoformat(task['time'])

                            if task['frequency'] == '每天':
                                next_time += timedelta(days=1)
                                # 添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])
                            elif task['frequency'] == '每周':
                                next_time += timedelta(days=7)
                                # 添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])
                            elif task['frequency'] == '工作日':
                                while True:
                                    next_time += timedelta(days=1)
                                    if next_time.weekday() < 5:  # 0-4 为周一至周五
                                        break
                                # 添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])

                            self.save_tasks_to_json()
                            log_print(f"[AutoInfo] Task status updated: {task['name']} - {status}")
                            break
        except Exception as e:
            log_print(f"[AutoInfo] Failed to update task status: {str(e)}")

    def add_next_task(self, time_text, name_text, info_text, frequency, wx_nickname):
        log_print(f"[AutoInfo] Adding next recurring task: {name_text} @ {time_text} (Sender: {wx_nickname})")
        try:
            widget_item = self.create_widget(time_text, name_text, info_text, frequency, wx_nickname)
            self.parent.formLayout_3.addRow(widget_item)
            self.ready_tasks.append({
                'time': time_text,
                'name': name_text,
                'info': info_text,
                'frequency': frequency,
                'wx_nickname': wx_nickname
            })
            log('INFO',
                f'自动添加 {time_text} 把 {info_text[:25] + "……" if len(info_text) > 25 else info_text} 发给 {name_text[:8]} (发送方: {wx_nickname})')
            self.save_tasks_to_json()
        except Exception as e:
            log_print(f"[AutoInfo] Failed to add recurring task: {str(e)}")

    def on_thread_finished(self):
        log_print("[AutoInfo] Worker thread finished")
        try:
            log("DEBUG", "所有任务执行完毕")
            self.is_executing = False
            self.parent.start_pushButton.setText("开始执行")
            if self.parent.checkBox_Shutdown.isChecked():
                self.shutdown_computer()
        except Exception as e:
            log_print(f"[AutoInfo] Error handling thread finished event: {str(e)}")

    def shutdown_computer(self):
        log_print("[AutoInfo] Preparing to shut down computer...")
        try:
            for i in range(10, 0, -1):
                log("WARNING", f"电脑在 {i} 秒后自动关机")
                log_print(f"[AutoInfo] Shutdown countdown: {i} seconds")
                time.sleep(1)
            log("DEBUG", "正在关机中...")
            os.system('shutdown /s /t 0')
        except Exception as e:
            log_print(f"[AutoInfo] Failed to shut down computer: {str(e)}")

    def save_configuration(self):
        log_print("[AutoInfo] Saving configuration...")
        try:
            if not self.ready_tasks:
                log("WARNING", "当前任务列表为空,没有任务可供保存")
                log_print("[AutoInfo] Task list is empty, nothing to save")
                return

            documents_dir = os.path.expanduser("~/Documents")
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存任务计划",
                                                                 os.path.join(documents_dir, "LeafAuto PRO任务计划"),
                                                                 "枫叶任务文件(*.xlsx);;所有文件(*)")

            if file_name:
                if not file_name.lower().endswith('.xlsx'):
                    file_name += '.xlsx'

                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(['Time', 'Name', 'Info', 'Frequency', 'WxNickname'])

                for task in self.ready_tasks:
                    sheet.append([task['time'], task['name'], task['info'], task['frequency'], task['wx_nickname']])

                workbook.properties.creator = "LeafAuto PRO"
                workbook.properties.title = "枫叶信息自动专业版任务计划"
                workbook.properties.description = "LeafAuto专业版定时任务计划，仅供专业版使用。"
                workbook.properties.lastModifiedBy = "LeafAutoPRO"
                workbook.save(file_name)
                log("DEBUG", f"任务文件已保存至{file_name}")
                log_print(f"[AutoInfo] Configuration saved to: {file_name}")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to save configuration: {str(e)}")

    def load_configuration(self, filepath=None):
        log_print("[AutoInfo] Loading configuration...")
        try:
            documents_dir = os.path.expanduser("~/Documents")
            file_name = filepath or QtWidgets.QFileDialog.getOpenFileName(
                self, "导入任务计划", documents_dir, "LeafAuto PRO 任务文件(*.xlsx);;所有文件(*)"
            )[0]

            if not file_name:
                log_print("[AutoInfo] No file selected, import cancelled")
                return

            workbook = openpyxl.load_workbook(file_name, read_only=True)
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1]]

            required_headers = ['Time', 'Name', 'Info', 'Frequency']
            missing_headers = [h for h in required_headers if h not in headers]
            if missing_headers:
                raise ValueError(f"文件格式不正确，缺少必要的列: {', '.join(missing_headers)}")

            wx_nickname_idx = headers.index('WxNickname') if 'WxNickname' in headers else None

            tasks = []
            for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                task = dict(zip(headers, row))
                if not (task.get('Time') and task.get('Name') and task.get('Info')):
                    continue
                if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", task['Time']):
                    continue
                if not task.get('Frequency'):
                    task['Frequency'] = "仅一次"
                if wx_nickname_idx is not None and row[wx_nickname_idx]:
                    task['wx_nickname'] = row[wx_nickname_idx]
                else:
                    task['wx_nickname'] = self.parent.comboBox_nickName.currentText()

                # 确保name和info作为字符串处理
                task['Name'] = str(task['Name']) if task['Name'] is not None else ""
                task['Info'] = str(task['Info']) if task['Info'] is not None else ""

                tasks.append(task)

            workbook.close()

        except Exception as e:
            log("ERROR", f"导入失败: {str(e)}")
            log_print(f"[AutoInfo] Failed to load configuration: {str(e)}")
            return

        if not tasks:
            log("ERROR", f"导入失败, 未找到有效任务数据")
            log_print("[AutoInfo] No valid task data found")
            return

        MEMBERSHIP_LIMITS = {
            'Free': 5,
            'Base': 30,
            'AiVIP': float('inf'),
            'VIP': float('inf')
        }

        limit = MEMBERSHIP_LIMITS.get(self.Membership, 5)
        if len(self.ready_tasks) + len(tasks) > limit:
            remaining = limit - len(self.ready_tasks)
            if remaining <= 0:
                log("WARNING", f"会员限制, 当前版本最多支持{limit}个任务")
                log_print(f"[AutoInfo] Membership limit reached, current version supports up to {limit} tasks")
                return
            tasks = tasks[:remaining]
            log("WARNING", f"由于会员限制，只导入前{remaining}个任务")
            log_print(f"[AutoInfo] Due to membership limitations, only importing first {remaining} tasks")

        for task in tasks:
            try:
                widget = self.create_widget(
                    task['Time'],
                    task['Name'],
                    task['Info'],
                    task['Frequency'],
                    task['wx_nickname']
                )
                self.parent.formLayout_3.addRow(widget)
                self.ready_tasks.append({
                    'time': task['Time'],
                    'name': task['Name'],
                    'info': task['Info'],
                    'frequency': task['Frequency'],
                    'wx_nickname': task['wx_nickname']
                })
                log_print(f"[AutoInfo] Task imported successfully: {task['Name']} (Sender: {task['wx_nickname']})")
            except Exception as e:
                log("ERROR", f"创建任务失败: {task['Name']}")
                log_print(f"[AutoInfo] Failed to create task: {task['Name']}, Error: {str(e)}")

        log("INFO", f"成功导入 {len(tasks)} 个任务")
        log_print(f"[AutoInfo] Successfully imported {len(tasks)} tasks")
        self.save_tasks_to_json()

    def play_error_sound(self):
        log_print("[AutoInfo] Attempting to play error sound...")
        try:
            if str_to_bool(read_key_value('error_sound')):
                if self.error_sound_thread._is_running:
                    log_print("[AutoInfo] Error sound already playing, skipping this time")
                    return

                try:
                    selected_audio_index = int(read_key_value('selected_audio_index'))
                except Exception:
                    selected_audio_index = 0

                if selected_audio_index in self.audio_files:
                    self.selected_audio_file = self.audio_files[selected_audio_index]
                else:
                    log("ERROR", f"音频播放失败: 无效索引 {selected_audio_index}")
                    log_print(f"[AutoInfo] Failed to play audio: Invalid index {selected_audio_index}")
                    return

                self.error_sound_thread.update_sound_file(self.selected_audio_file)
                self.error_sound_thread.start()
                log_print(f"[AutoInfo] Playing error sound: {self.selected_audio_file}")
        except Exception as e:
            log_print(f"[AutoInfo] Failed to play error sound: {str(e)}")

    def send_error_email(self, task):
        log_print(f"[AutoInfo] Attempting to send error email: {task['name']}")
        if str_to_bool(read_key_value('error_email')):
            self.email_queue.put(task)

    def _process_email_queue(self):
        log_print("[AutoInfo] Email processing thread started")
        while True:
            task = self.email_queue.get()
            if task is None:
                break
            self._send_email_safely(task)
            self.email_queue.task_done()

    def _send_email_safely(self, task):
        try:
            # Check email cooldown
            current_time = time.time()
            if current_time - self.last_email_time < self.email_cooldown:
                log_print(
                    f"[AutoInfo] Email cooldown active, remaining {self.email_cooldown - (current_time - self.last_email_time):.1f} seconds")
                return

            log_print(f"[AutoInfo] Sending error email for task: {task['name']}")

            # Email configuration
            sender_email = '3555844679@qq.com'
            receiver_email = read_key_value('email')
            smtp_server = 'smtp.qq.com'
            smtp_port = 465
            username = '3555844679@qq.com'
            password = 'xtibpzrdwnppchhi'

            subject = f"定时任务执行失败 {task['time']}"

            # Create message container
            message = MIMEMultipart('related')
            message['From'] = 'LeafAuto PRO <3555844679@qq.com>'
            message['To'] = receiver_email
            message['Subject'] = Header(subject, 'utf-8')

            # HTML template with inline CSS for better email client compatibility
            html_content = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4a6fa5; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                    .content {{ background-color: white; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                    .section {{ margin-bottom: 20px; }}
                    .highlight {{ background-color: #f0f4f8; padding: 10px; border-radius: 3px; }}
                    .button {{ display: inline-block; background-color: #4a6fa5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; }}
                    .footer {{ margin-top: 20px; text-align: center; color: #6c757d; font-size: 12px; }}
                    .support {{ margin-top: 10px; }}
                    .separator {{ border-top: 1px solid #e9ecef; margin: 20px 0; }}
                    .footer-image {{ max-width: 100%; margin-top: 20px; border-radius: 3px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>LeafAuto 消息通知</h2>
                    </div>
                    <div class="content">
                        <div class="section">
                            <p>尊敬的用户,</p>
                            <p style="color: #d9534f; font-weight: bold;">😔 非常抱歉地通知您，枫叶未能成功发送您设置的定时信息。</p>
                        </div>

                        <div class="section highlight">
                            <h3>📌 失败任务详情</h3>
                            <p>🕒 时间: {task['time']}</p>
                            <p>👤 接收人: {task['name']}</p>
                            <p>💬 消息内容: {task['info']}</p>
                            <p style="color: #d9534f;">❌ 失败原因: 未知错误。</p>
                        </div>

                        <div class="section">
                            <h3>🔧 建议操作</h3>
                            <ol>
                                <li>检查接收人名称是否与联系人完全一致</li>
                                <li>确认接收人当前状态是否可以接收消息</li>
                                <li>尝试手动发送相同内容进行验证</li>
                            </ol>
                        </div>

                        <div class="section separator"></div>

                        <div class="section">
                            <p>Dear Valued User 👋,</p>
                            <p style="color: #d9534f; font-weight: bold;">😔 We sincerely apologize for the inconvenience caused. Our system failed to deliver a scheduled message.</p>
                        </div>

                        <div class="section highlight">
                            <h3>📌 Delivery Failure Details</h3>
                            <p>🕒 Time: {task['time']}</p>
                            <p>👤 Recipient: {task['name']}</p>
                            <p>💬 Message: {task['info']}</p>
                            <p style="color: #d9534f;">❌ Failure Reason: System error</p>
                        </div>

                        <div class="section">
                            <h3>🔧 Recommended Actions</h3>
                            <ol>
                                <li>Verify the recipient's name matches exactly as in your contacts</li>
                                <li>Confirm the recipient is currently available to receive messages</li>
                                <li>Attempt to send the same content manually for validation</li>
                            </ol>
                        </div>

                        <div class="section separator"></div>

                        <div class="section">
                            <p>🙇‍♀️ 对于此次未能准时送达的情况，我们深表歉意。感谢您的理解与支持。</p>
                        </div>

                        <div class="section support">
                            <h3>需要帮助？ | Need Help?</h3>
                            <p>✉️ 邮箱: 3555844679@qq.com</p>
                            <p>🕙 服务群: 1021471813</p>
                        </div>

                        <div class="section">
                            <img src="cid:footer_image" alt="Service Support" class="footer-image">
                        </div>
                    </div>
                    <div class="footer">
                        <p>LeafAuto Team | {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} (GMT+8)</p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Attach HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)

            # Attach footer image using get_resource_path()
            try:
                footer_image_path = get_resource_path('resources/img/page1/email.png')
                with open(footer_image_path, 'rb') as f:
                    footer_image = MIMEImage(f.read())
                    footer_image.add_header('Content-ID', '<footer_image>')
                    message.attach(footer_image)
            except Exception as e:
                log_print(f"[AutoInfo] Failed to attach footer image: {str(e)}")

            # Use SMTP with SSL
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(username, password)
                server.sendmail(sender_email, [receiver_email], message.as_string())
                self.last_email_time = current_time
                log_print(f"[AutoInfo] Error email sent successfully: {task['name']}")

        except Exception as e:
            log_print(f"[AutoInfo] Failed to send error email: {str(e)}")
