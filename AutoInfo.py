import json
import os
import re
import smtplib
import time
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
from queue import Queue
from threading import Thread

import openpyxl
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

from System_info import read_key_value
from Thread import WorkerThread, ErrorSoundThread
from common import get_resource_path, log, str_to_bool

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
        print(f"[AutoInfo] 初始化完成，会员类型: {self.Membership}")

    def openFileNameDialog(self, filepath=None):
        try:
            if filepath:
                self.parent.message_lineEdit.setText(str(filepath))
                print(f"[AutoInfo] 设置文件路径: {filepath}")
                return

            file_filters = (
                "所有文件 (*);;"
                "图像文件 (*.bmp *.gif *.jpg *.jpeg *.png *.svg *.tiff);;"
                "文档文件 (*.doc *.docx *.pdf *.txt *.odt);;"
                "电子表格 (*.xls *.xlsx *.ods);;"
                "演示文稿 (*.ppt *.pptx *.odp);;"
                "音频文件 (*.mp3 *.wav *.flac *.aac);;"
                "视频文件 (*.mp4 *.avi *.mkv *.mov);;"
                "压缩文件 (*.zip *.rar *.tar *.gz *.bz2)"
            )

            options = QtWidgets.QFileDialog.Option.ReadOnly
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "选择要发送的文件",
                "",
                file_filters,
                options=options
            )

            if fileName:
                self.parent.message_lineEdit.setText(fileName)
                print(f"[AutoInfo] 选择文件: {fileName}")
        except Exception as e:
            print(f"[AutoInfo] 打开文件对话框失败: {str(e)}")

    def video_chat(self):
        try:
            self.parent.message_lineEdit.setText('Video_chat')
            print("[AutoInfo] 设置为视频聊天")
        except Exception as e:
            print(f"[AutoInfo] 设置视频聊天失败: {str(e)}")

    def save_tasks_to_json(self):
        try:
            with open('_internal/tasks.json', 'w', encoding='utf-8') as f:
                json.dump(self.ready_tasks, f, ensure_ascii=False, indent=4)
            print(f"[AutoInfo] 任务保存成功，共 {len(self.ready_tasks)} 个任务")
        except Exception as e:
            print(f"[AutoInfo] 任务保存失败: {str(e)}")
            log("ERROR", "非管理员身份运行软件,未能将操作保存")

    def add_list_item(self):
        print("[AutoInfo] 尝试添加任务...")
        try:
            time_text, name_text, info_text, frequency = self.get_input_values()
            wx_nickname = self.parent.comboBox_nickName.currentText()

            if not all([time_text, name_text, info_text]):
                print("[AutoInfo] 添加任务失败：输入不完整")
                log("WARNING", "请先输入有效内容和接收人再添加任务")
                return

            if self.Membership == 'Free' and len(self.ready_tasks) >= 5:
                print("[AutoInfo] 添加任务失败：免费版任务数量限制")
                log("WARNING", "试用版最多添加5个任务，请升级版本")
                QtWidgets.QMessageBox.warning(self, "试用版限制", "试用版最多添加5个任务，请升级版本")
                return
            elif self.Membership == 'Base' and len(self.ready_tasks) >= 30:
                print("[AutoInfo] 添加任务失败：基础版任务数量限制")
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
            print(f"[AutoInfo] 任务添加成功：{name_text} - {info_text[:20]}... (发送方: {wx_nickname})")

            self.parent.dateTimeEdit.setDateTime(
                datetime.fromisoformat(time_text) + timedelta(minutes=int(read_key_value('add_timestep'))))

            self.save_tasks_to_json()
        except Exception as e:
            print(f"[AutoInfo] 添加任务异常: {str(e)}")

    def create_widget(self, time_text, name_text, info_text, frequency, wx_nickname):
        try:
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

            print(f"[AutoInfo] 创建任务控件成功：{name_text} - {info_text[:20]}... (发送方: {wx_nickname})")
            return widget_item

        except Exception as e:
            print(f"[AutoInfo] 创建任务控件失败: {str(e)}")
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
        print(f"[AutoInfo] 尝试删除任务：{name_text} - {info_text[:20]}...")
        try:
            if self.error_sound_thread._is_running:
                self.error_sound_thread.stop_playback()
                print("[AutoInfo] 已停止错误声音")

            for task in self.ready_tasks:
                if (task['time'] == time_text and
                        task['name'] == name_text and
                        task['info'] == info_text and
                        task['wx_nickname'] == wx_nickname):
                    self.ready_tasks.remove(task)
                    log('WARNING', f'已删除任务 {info_text[:35] + "……" if len(info_text) > 30 else info_text}')
                    print(f"[AutoInfo] 任务删除成功")
                    break

            if not self.ready_tasks:
                self.is_executing = False
                self.parent.start_pushButton.setText("开始执行")
                if self.worker_thread is not None:
                    self.worker_thread.requestInterruption()
                    self.worker_thread = None
                    print("[AutoInfo] 已停止工作线程")

            self.update_ui()
            self.save_tasks_to_json()
        except Exception as e:
            print(f"[AutoInfo] 删除任务失败: {str(e)}")

    def update_ui(self):
        print("[AutoInfo] 更新UI显示...")
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
            print(f"[AutoInfo] UI更新完成，显示 {len(self.ready_tasks)} 个任务")
        except Exception as e:
            print(f"[AutoInfo] UI更新失败: {str(e)}")

    def get_input_values(self):
        try:
            name_text = self.parent.receiver_lineEdit.text()
            info_text = self.parent.message_lineEdit.text()
            time_text = self.parent.dateTimeEdit.dateTime().toString(QtCore.Qt.DateFormat.ISODate)
            frequency = self.parent.comboBox_Frequency.currentText()
            return time_text, name_text, info_text, frequency
        except Exception as e:
            print(f"[AutoInfo] 获取输入值失败: {str(e)}")
            return None, None, None, None

    def on_start_clicked(self):
        print("[AutoInfo] 执行按钮点击事件...")
        try:
            if self.is_executing:
                self.is_executing = False
                self.parent.start_pushButton.setText("开始执行")
                if self.worker_thread is not None:
                    self.worker_thread.requestInterruption()
                    self.worker_thread = None
                    print("[AutoInfo] 已停止工作线程")
                if self.error_sound_thread._is_running:
                    self.error_sound_thread.stop_playback()
                    print("[AutoInfo] 已停止错误声音")
                print("[AutoInfo] 已停止执行所有任务")
            else:
                if not self.ready_tasks:
                    log("WARNING", "任务列表为空，请先添加任务至任务列表")
                    print("[AutoInfo] 任务列表为空，无法开始执行")
                else:
                    self.is_executing = True
                    self.parent.start_pushButton.setText("停止执行")
                    self.worker_thread = WorkerThread(self)
                    self.worker_thread.prevent_sleep = self.parent.checkBox_stopSleep.isChecked()
                    self.worker_thread.current_time = 'mix' if str_to_bool(read_key_value('net_time')) else 'sys'
                    self.worker_thread.finished.connect(self.on_thread_finished)
                    self.worker_thread.start()
                    print("[AutoInfo] 已开始执行任务，工作线程已启动")
        except Exception as e:
            print(f"[AutoInfo] 执行按钮点击事件处理失败: {str(e)}")

    def clear_layout(self, layout):
        try:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        except Exception as e:
            print(f"[AutoInfo] 清除布局失败: {str(e)}")

    def update_task_status(self, task, status):
        print(f"[AutoInfo] 更新任务状态: {task['name']} - {status}")
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
                                widget_item.task[key] == task[key] for key in ['time', 'name', 'info', 'frequency']):
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
                                        print(f"[AutoInfo] 任务 {task['name']} 已失败 {task['error_count']} 次")

                                new_icon_path = get_resource_path(f'resources/img/page1/{icon_path_key}')
                                widget_image.setStyleSheet(f"image: url({new_icon_path});")

                                # 强制重绘部件，确保视觉更新
                                widget_image.update()
                                widget_item.update()

                            # 处理重复任务
                            next_time = datetime.fromisoformat(task['time'])

                            if task['frequency'] == '每天':
                                next_time += timedelta(days=1)
                                # 修复：添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])
                            elif task['frequency'] == '每周':
                                next_time += timedelta(days=7)
                                # 修复：添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])
                            elif task['frequency'] == '工作日':
                                while True:
                                    next_time += timedelta(days=1)
                                    if next_time.weekday() < 5:  # 0-4 为周一至周五
                                        break
                                # 修复：添加 wx_nickname 参数
                                self.add_next_task(next_time.isoformat(), task['name'], task['info'], task['frequency'],
                                                   task['wx_nickname'])

                            self.save_tasks_to_json()
                            print(f"[AutoInfo] 任务状态更新完成: {task['name']} - {status}")
                            break
        except Exception as e:
            print(f"[AutoInfo] 更新任务状态失败: {str(e)}")

    def add_next_task(self, time_text, name_text, info_text, frequency, wx_nickname):
        print(f"[AutoInfo] 添加下一次重复任务: {name_text} @ {time_text} (发送方: {wx_nickname})")
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
            print(f"[AutoInfo] 添加重复任务失败: {str(e)}")

    def on_thread_finished(self):
        print("[AutoInfo] 工作线程已完成")
        try:
            log("DEBUG", "所有任务执行完毕")
            self.is_executing = False
            self.parent.start_pushButton.setText("开始执行")
            if self.parent.checkBox_Shutdown.isChecked():
                self.shutdown_computer()
        except Exception as e:
            print(f"[AutoInfo] 处理线程完成事件失败: {str(e)}")

    def shutdown_computer(self):
        print("[AutoInfo] 准备关机...")
        try:
            for i in range(10, 0, -1):
                log("WARNING", f"电脑在 {i} 秒后自动关机")
                print(f"[AutoInfo] 倒计时关机: {i} 秒")
                time.sleep(1)
            log("DEBUG", "正在关机中...")
            os.system('shutdown /s /t 0')
        except Exception as e:
            print(f"[AutoInfo] 关机失败: {str(e)}")

    def save_configuration(self):
        print("[AutoInfo] 保存配置...")
        try:
            if not self.ready_tasks:
                log("WARNING", "当前任务列表为空,没有任务可供保存")
                print("[AutoInfo] 任务列表为空，无法保存")
                return

            documents_dir = os.path.expanduser("~/Documents")
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存任务计划",
                                                                 os.path.join(documents_dir, "LeafAuto专业版计划"),
                                                                 "枫叶任务文件(*.xlsx);;所有文件(*)")

            if file_name:
                if not file_name.lower().endswith('.xlsx'):
                    file_name += '.xlsx'

                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.append(['Time', 'Name', 'Info', 'Frequency', 'WxNickname'])

                for task in self.ready_tasks:
                    sheet.append([task['time'], task['name'], task['info'], task['frequency'], task['wx_nickname']])

                workbook.properties.creator = "LeafAutoPRO"
                workbook.properties.title = "枫叶信息自动化系统任务计划"
                workbook.properties.description = "LeafAutoPRO的定时任务计划，仅供专业版使用。"
                workbook.properties.lastModifiedBy = "LeafAutoPRO"
                workbook.save(file_name)
                log("DEBUG", f"任务文件已保存至{file_name}")
                print(f"[AutoInfo] 配置已保存至: {file_name}")
        except Exception as e:
            print(f"[AutoInfo] 保存配置失败: {str(e)}")

    def load_configuration(self, filepath=None):
        print("[AutoInfo] 加载配置...")
        try:
            documents_dir = os.path.expanduser("~/Documents")
            file_name = filepath or QtWidgets.QFileDialog.getOpenFileName(
                self, "导入任务计划", documents_dir, "枫叶专业版任务文件(*.xlsx);;所有文件(*)"
            )[0]

            if not file_name:
                print("[AutoInfo] 未选择文件，取消导入")
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
                tasks.append(task)

            workbook.close()

        except Exception as e:
            log("ERROR", f"导入失败: {str(e)}")
            print(f"[AutoInfo] 导入配置失败: {str(e)}")
            return

        if not tasks:
            log("ERROR", f"导入失败, 未找到有效任务数据")
            print("[AutoInfo] 未找到有效任务数据")
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
                print(f"[AutoInfo] 会员限制，当前版本最多支持{limit}个任务")
                return
            tasks = tasks[:remaining]
            log("WARNING", f"由于会员限制，只导入前{remaining}个任务")
            print(f"[AutoInfo] 由于会员限制，只导入前{remaining}个任务")

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
                print(f"[AutoInfo] 成功导入任务: {task['Name']} (发送方: {task['wx_nickname']})")
            except Exception as e:
                log("ERROR", f"创建任务失败: {task['Name']}")
                print(f"[AutoInfo] 创建任务失败: {task['Name']}, 错误: {str(e)}")

        log("INFO", f"成功导入 {len(tasks)} 个任务")
        print(f"[AutoInfo] 成功导入 {len(tasks)} 个任务")
        self.save_tasks_to_json()

    def play_error_sound(self):
        print("[AutoInfo] 尝试播放错误声音...")
        try:
            if str_to_bool(read_key_value('error_sound')):
                if self.error_sound_thread._is_running:
                    print("[AutoInfo] 已有错误音频在播放，跳过本次")
                    return

                try:
                    selected_audio_index = int(read_key_value('selected_audio_index'))
                except Exception:
                    selected_audio_index = 0

                if selected_audio_index in self.audio_files:
                    self.selected_audio_file = self.audio_files[selected_audio_index]
                else:
                    log("ERROR", f"音频播放失败: 无效索引 {selected_audio_index}")
                    print(f"[AutoInfo] 音频播放失败: 无效索引 {selected_audio_index}")
                    return

                self.error_sound_thread.update_sound_file(self.selected_audio_file)
                self.error_sound_thread.start()
                print(f"[AutoInfo] 播放错误音频: {self.selected_audio_file}")
        except Exception as e:
            print(f"[AutoInfo] 播放错误音频失败: {str(e)}")

    def send_error_email(self, task):
        print(f"[AutoInfo] 尝试发送错误邮件: {task['name']}")
        if str_to_bool(read_key_value('error_email')):
            self.email_queue.put(task)

    def _process_email_queue(self):
        print("[AutoInfo] 邮件处理线程已启动")
        while True:
            task = self.email_queue.get()
            if task is None:
                break
            self._send_email_safely(task)
            self.email_queue.task_done()

    def _send_email_safely(self, task):
        try:
            current_time = time.time()
            if current_time - self.last_email_time < self.email_cooldown:
                print(
                    f"[AutoInfo] 邮件发送冷却中，剩余 {self.email_cooldown - (current_time - self.last_email_time):.1f} 秒")
                return

            sender_email = '3555844679@qq.com'
            receiver_email = read_key_value('email')
            smtp_server = 'smtp.qq.com'
            smtp_port = 465

            username = '3555844679@qq.com'
            password = 'xtibpzrdwnppchhi'

            subject = f"{task['time']}未把信息发给{task['name']}"
            body = (
                f"尊敬的用户：\n"
                f"我们遗憾地通知您，在【{task['time']}】尝试发送方账号【{task['wx_nickname']}】发送【{task['info']}】给【{task['name']}】时因故障未能成功。\n"
                "\n对此造成的不便，深表歉意。请检查提供的信息是否准确，并确认填写的接收者应与备注完全一致。\n"
                "\n若问题依旧，请联系客户服务团队获取帮助：\n"
                "- 发送电子邮件至支持邮箱 3555844679@qq.com；\n"
                "\n我们将尽快解决此问题，持续改进服务。对于给您带来的不便再次表示歉意，感谢您的理解与耐心。\n"
                f"\n祝好，\n枫叶信息服务保障团队\n"
                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
            )

            receiver_name = '枫叶信息自动'

            message = MIMEText(body, 'plain', 'utf-8')
            message['From'] = 'LeafAuto <3555844679@qq.com>'
            message['To'] = f"{Header(receiver_name, 'utf-8')} <{receiver_email}>"
            message['Subject'] = Header(subject, 'utf-8')

            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(username, password)
                server.sendmail(sender_email, [receiver_email], message.as_string())
                self.last_email_time = current_time
                print(f"[AutoInfo] 邮件发送成功: {task['name']}")

        except Exception as e:
            print(f"[AutoInfo] 邮件发送失败: {str(e)}")
            log("ERROR", f"邮件发送失败: {str(e)}")
