import json
import os
import sys
import winreg
from datetime import datetime

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtWidgets import QCompleter, QListView
from wxautox import WeChat

import common
from ActivitiesWindow import ActivitiesWindow
from AiAssistant import AiAssistant
from AutoInfo import AutoInfo
from NicknameComboBox import NicknameComboBox
from Reply import ReplyDialog
from SettingWindow import SettingWindow
from Split import Split
from System_info import read_key_value, ensure_config_file_exists, write_key_value
from Ui_MainWindow import Ui_MainWindow
from UpdateDialog import check_update
from clickableComboBox import clickableComboBox
from common import get_resource_path, log, get_current_time, log_print, get_url

wx_instances = {}
current_version = 4.39


def reload_wx():
    global wx_instances
    try:
        log_print("Starting to reload WeChat instances")
        temp_wx = WeChat(language=read_key_value('language'))
        nicknames = temp_wx.get_wx_nicknames()
        if not nicknames:
            log_print("No WeChat windows found during reload")
            return '未找到微信窗口'

        wx_instances.clear()
        for nickname in nicknames:
            wx = WeChat(nickname=nickname, language=read_key_value('language'))
            wx_instances[nickname] = wx
            log("DEBUG", f"微信初始化完成, {nickname} 欢迎您！")
            log_print(f"Successfully initialized WeChat instance for {nickname}")

        if wx_instances:
            default_nickname = next(iter(wx_instances))
            MainWindow.wx = wx_instances[default_nickname]
            log_print(f"Default WeChat instance set to {default_nickname}")
            return f"已初始化 {len(wx_instances)} 个微信"
        else:
            log_print("Failed to create any WeChat instances during reload")
            return '初始化失败，未创建任何实例'

    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'NativeWindowHandle'":
            log_print("WeChat not logged in during reload")
            log("ERROR", "微信未登录, 请登录微信后重启枫叶")
            return '微信未登录'
        else:
            log_print(f"Exception occurred during reload: {str(e)}")
            log("ERROR", f"程序初始化出错, 错误原因:{e}")
            return '初始化出错'


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        global wx_instances
        log_print("Initializing MainWindow")
        self.setupUi(self)
        old_combobox = self.comboBox_Frequency
        geometry = old_combobox.geometry()
        parent_layout = old_combobox.parentWidget().layout()

        if parent_layout:
            for i in range(parent_layout.count()):
                if parent_layout.itemAt(i).widget() == old_combobox:
                    parent_layout.removeItem(parent_layout.itemAt(i))
        old_combobox.deleteLater()

        self.comboBox_Frequency = clickableComboBox(self)
        self.comboBox_Frequency.setGeometry(geometry)
        self.comboBox_Frequency.setObjectName("comboBox_Frequency")

        self.comboBox_Frequency.add_item("仅一次")
        self.comboBox_Frequency.add_item("星期一")
        self.comboBox_Frequency.add_item("星期二")
        self.comboBox_Frequency.add_item("星期三")
        self.comboBox_Frequency.add_item("星期四")
        self.comboBox_Frequency.add_item("星期五")
        self.comboBox_Frequency.add_item("星期六")
        self.comboBox_Frequency.add_item("星期日")

        if parent_layout:
            parent_layout.addWidget(self.comboBox_Frequency)

        old_combobox = self.comboBox_nickName
        parent_widget = old_combobox.parentWidget()
        parent_layout = parent_widget.layout()
        geometry = old_combobox.geometry()
        object_name = old_combobox.objectName()

        if parent_layout:
            for i in range(parent_layout.count()):
                item = parent_layout.itemAt(i)
                if item.widget() == old_combobox:
                    parent_layout.removeWidget(old_combobox)
                    break
        old_combobox.deleteLater()

        self.comboBox_nickName = NicknameComboBox(parent=parent_widget)
        self.comboBox_nickName.setGeometry(geometry)
        self.comboBox_nickName.setObjectName(object_name)

        if parent_layout:
            insert_index = -1
            for i in range(parent_layout.count()):
                if isinstance(parent_layout.itemAt(i), QtWidgets.QSpacerItem):
                    insert_index = i + 1
                    break
            if insert_index != -1:
                parent_layout.insertWidget(insert_index, self.comboBox_nickName)
            else:
                parent_layout.addWidget(self.comboBox_nickName)

        self.ui = Ui_MainWindow()
        self.setWindowTitle("LeafAuto Pro")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/icon.ico')))
        common.main_window = self

        try:
            log_print("Ensuring configuration file exists")
            ensure_config_file_exists()
            self.language = read_key_value('language')
            self.Membership = read_key_value('membership')
            self.expiration_time = read_key_value('expiration_time')
            self.version = read_key_value('version')
            if float(self.version) < current_version:
                log_print(f"Updating version from {self.version} to {current_version}")
                self.Version = write_key_value('version', str(current_version))
        except Exception as e:
            log_print(f"Exception during configuration initialization: {str(e)}")
            print(e)
            QtWidgets.QMessageBox.critical(self, "初始化失败", "首次启动,需连接网络并[以管理员身份运行]")
            sys.exit()

        try:
            result = reload_wx()
            self.comboBox_nickName.clear()

            if '已初始化' in result:
                for nickname in wx_instances.keys():
                    self.comboBox_nickName.addItem(nickname)
                if wx_instances:
                    default_nickname = next(iter(wx_instances))
                    self.comboBox_nickName.setCurrentText(default_nickname)
                    self.comboBox_nickName.currentTextChanged.connect(self.change_current_wx)
            else:
                self.comboBox_nickName.addItem(result)
                self.comboBox_nickName.setCurrentText(result)

        except Exception as e:
            log("ERROR", f"初始化微信实例时出错: {e}")
            self.comboBox_nickName.clear()
            self.comboBox_nickName.addItem('初始化出错')
            self.comboBox_nickName.setCurrentText('初始化出错')

        self.auto_info = AutoInfo(wx_instances, self.Membership, self)
        self.split = Split(wx_instances, self.Membership, self)
        self.ai_assistant = AiAssistant(wx_instances, self.Membership, self)

        self.create_tray()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.mousePosition = None
        self.mousePressEvent = self._mouse_press_event
        self.mouseMoveEvent = self._mouse_move_event
        self.setAcceptDrops(True)

        self.connect_signals()
        self._update_ui_elements()
        self.apply_Membership_limits(self.Membership)

        if common.str_to_bool(read_key_value('auto_update')):
            check_update()
        if common.str_to_bool(read_key_value('serve_lock')):
            self.disable_rdp_lock()

        self.load_tasks_from_json()

        try:
            if wx_instances:
                default_wx = next(iter(wx_instances.values()))
                default_wx.GetSessionList()
                completer = QCompleter(default_wx.predict, self)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)
                completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
                popup = completer.popup()
                if isinstance(popup, QListView):
                    popup.setStyleSheet(common.load_stylesheet("completer_QListView.css"))
                self.receiver_lineEdit.setCompleter(completer)
        except Exception as e:
            print(e)

    def update_wx(self):
        global wx_instances
        log_print("Updating WeChat instances")
        result = reload_wx()

        self.comboBox_nickName.clear()

        if '已初始化' in result:
            log_print(f"Successfully updated WeChat instances: {result}")
            for nickname in wx_instances.keys():
                self.comboBox_nickName.addItem(nickname)
            if wx_instances:
                default_nickname = next(iter(wx_instances))
                self.comboBox_nickName.setCurrentText(default_nickname)
                log_print(f"Set current WeChat nickname to {default_nickname}")
        else:
            self.comboBox_nickName.addItem(result)
            self.comboBox_nickName.setCurrentText(result)

        self.auto_info.wx_instances = wx_instances
        self.split.wx_instances = wx_instances
        self.ai_assistant.wx_instances = wx_instances
        log_print("WeChat instances update completed")

    def change_current_wx(self):
        selected_nickname = self.comboBox_nickName.currentText()
        log_print(f"Changing current WeChat instance to {selected_nickname}")
        if selected_nickname in wx_instances:
            MainWindow.wx = wx_instances[selected_nickname]
            log("WARNING", f"当前微信账号已切换成: {selected_nickname}")
            log_print(f"Successfully changed current WeChat instance to {selected_nickname}")
        else:
            log("WARNING", f"所选微信账号 {selected_nickname} 未初始化")

    def load_tasks_from_json(self):
        json_file_path = '_internal/tasks.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                try:
                    loaded_tasks = json.load(f)
                    self.auto_info.ready_tasks.clear()
                    current_time = datetime.now()
                    membership_limits = {'Free': 5, 'VIP': 9999, 'Base': 30}
                    membership_limit = membership_limits.get(self.Membership, 5)
                    remaining_slots = membership_limit - len(self.auto_info.ready_tasks)
                    for task in loaded_tasks:
                        required_keys = ['time', 'name', 'info', 'sender']
                        valid = True
                        for key in required_keys:
                            if key not in task or not task[key]:
                                valid = False
                                break
                        if 'frequency' not in task:
                            valid = False
                        if not valid:
                            log("WARNING", "跳过不完整的任务数据")
                            continue
                        if remaining_slots <= 0:
                            log("WARNING", f"已达到最大任务限制 {membership_limit}，剩余任务将被忽略")
                            break
                        try:
                            task_time = datetime.fromisoformat(task['time'])
                        except ValueError:
                            log("WARNING", f"跳过时间格式错误的任务: {task['time']}")
                            continue
                        if task_time < current_time and task['frequency']:
                            adjusted_time = self.auto_info.calculate_next_time(task_time, task['frequency'])
                            if adjusted_time:
                                task_time = adjusted_time
                                log_print(f"任务时间已调整为未来时间: {task_time.isoformat()}")
                            else:
                                log("WARNING", f"无法调整过期任务时间，已跳过: {task['name']}")
                                continue
                        self.auto_info.task_id_counter += 1
                        task_id = self.auto_info.task_id_counter
                        task_data = {
                            'id': task_id,
                            'time': task_time.isoformat(),
                            'name': task['name'],
                            'info': task['info'],
                            'sender': task['sender'],
                            'frequency': task['frequency']
                        }
                        self.auto_info.ready_tasks[task_id] = task_data
                        time_str = task_time.isoformat()
                        if time_str not in self.auto_info.tasks_by_time:
                            self.auto_info.tasks_by_time[time_str] = []
                        self.auto_info.tasks_by_time[time_str].append(task_id)
                        widget_item = self.auto_info.create_widget(
                            task_id, time_str, task['name'], task['info'], task['frequency'], task['sender']
                        )
                        if widget_item:
                            self.formLayout_3.addRow(widget_item)
                        else:
                            log("WARNING", f"创建任务UI控件失败: {task['name']}")
                        remaining_slots -= 1
                    if remaining_slots <= 0:
                        log("WARNING", f"当前已达到最大任务限制 {membership_limit}, 请升级会员")
                        log_print(f"Task limit reached for current membership: {membership_limit} tasks")
                    self.auto_info.save_tasks_to_json()
                except json.JSONDecodeError:
                    log("ERROR", "无法解析JSON文件")
                    log_print(f"Failed to parse JSON file: {json_file_path}")
                    self.auto_info.ready_tasks.clear()
                except Exception as e:
                    log("ERROR", f"加载任务时出错: {str(e)}")
                    log_print(f"Unexpected error while loading tasks: {str(e)}")
                    self.auto_info.ready_tasks.clear()

    def on_vip_frame_clicked(self, event):
        log_print("VIP frame clicked")
        expiration_format = "%Y-%m-%d %H:%M:%S"
        try:
            expiration_datetime = datetime.strptime(
                self.expiration_time,
                expiration_format
            )
            log_print(f"Expiration datetime parsed: {expiration_datetime}")
        except ValueError:
            expiration_datetime = datetime.now()
            log_print("Failed to parse expiration datetime, using current time")
        current_datetime = datetime.now()
        remaining_days = (expiration_datetime - current_datetime).days
        log_print(f"Membership: {self.Membership}, remaining days: {remaining_days}")
        if self.Membership != 'VIP' or remaining_days <= 7:
            log_print("Opening activities window")
            self.open_activities_window()
        else:
            self.feedback()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        try:
            urls = event.mimeData().urls()
            if not urls:
                return

            for url in urls:
                file_name = url.toLocalFile()
                if not file_name:
                    continue

                if os.path.isdir(file_name):
                    log('ERROR', '暂不支持发送文件夹，您可压缩后发送')
                    log_print(f"Directory dropped: {file_name}, not supported")
                    return

                if file_name.endswith('.xlsx'):
                    log_print(f"Excel file dropped: {file_name}, loading configuration")
                    self.auto_info.load_configuration(filepath=file_name)
                else:
                    log_print(f"File dropped: {file_name}, opening as normal file")
                    self.auto_info.open_file_dialog(filepath=file_name)

            log_print("Drop event processed successfully")
            event.accept()
        except Exception as e:
            log_print(f"Exception during drop event: {str(e)}")
            pass

    def _update_ui_elements(self):
        self.get_notice()
        self.dateTimeEdit.setDateTime(get_current_time('mix'))
        self.label_5.setText(self.expiration_time[:10])
        self.label_76.setText('LV.' + read_key_value('membership_class'))
        self.label_78.setText('ON' if common.str_to_bool(read_key_value('error_sound')) else 'OFF')
        self.label_80.setText(self.language.upper())
        self.label_82.setText('V' + self.version)
        self.log_textEdit.setReadOnly(True)

    def create_tray(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(get_resource_path('resources/img/tray.ico')))

        menu = QtWidgets.QMenu(self)
        menu.setTitle("LeafAuto Pro")
        menu.setStyleSheet(common.load_stylesheet("menu.setStyleSheet.css"))

        show_main_action = QAction("显示面板", self)
        show_main_action.triggered.connect(self.show_main_interface)
        menu.addAction(show_main_action)

        set_up_action = QAction("设置", self)
        set_up_action.triggered.connect(self.open_setting_window)
        menu.addAction(set_up_action)

        contact_feedback_action = QAction("帮助反馈", self)
        contact_feedback_action.triggered.connect(common.author)
        menu.addAction(contact_feedback_action)

        exit_action = QAction("退出枫叶", self)
        exit_action.triggered.connect(self.close_application)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        log_print("System tray icon created")

    def on_tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            if self.isMinimized():
                self.showNormal()
                self.raise_()
                self.activateWindow()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

    def apply_Membership_limits(self, membership):
        allow_icon = QtGui.QIcon()
        allow_icon.addPixmap(QtGui.QPixmap(get_resource_path('resources/img/page0/page0_允许白钩.svg')),
                             QtGui.QIcon.Mode.Normal,
                             QtGui.QIcon.State.Off)
        if membership == 'Free':
            log_print("Applying Free membership limits")
            small_member_image = get_resource_path('resources/img/小标/小标-免费试用版本.svg')
            retain_day = max(0, (
                        datetime.strptime(self.expiration_time, '%Y-%m-%d %H:%M:%S') - get_current_time('mix')).days)
            if retain_day == 0:
                log_print("Free trial expired")
                member_image = get_resource_path('resources/img/头标/头标-银色体验会员.svg')
                self.Free_pushButton.setText("免费试用已结束")
                self.open_activities_window()
            else:
                log_print(f"Free trial remaining days: {retain_day}")
                member_image = get_resource_path('resources/img/头标/头标-铂金体验会员.svg')
                self.Free_pushButton.setText("您正在免费试用中")
            self.welcome_label.setText(
                f"<html><head/><body><p><span style=\"font-size:16pt; font-weight:700; color:#ffffff;\">试用还剩{retain_day}天 快充分利用吧(≧◡≦)</span></p></body></html>"
            )
            self.label_64.setText("12%")
            self.label_66.setText("6%")
            self.checkBox_Ai.setEnabled(False)
            self.checkBox_stopSleep.setEnabled(False)
            self.checkBox_period.setChecked(True)
            self.checkBox_comma.setChecked(True)
            self.checkBox_Space.setChecked(True)
        elif membership == 'Base':
            log_print("Applying Base membership limits")
            small_member_image = get_resource_path('resources/img/小标/小标-标准会员版本.svg')
            member_image = get_resource_path('resources/img/头标/头标-银色标准会员.svg')
            self.label_64.setText("74%")
            self.label_66.setText("24%")
            self.Free_pushButton.setText("正在使用标准版")
            self.label_68.setText("使用中")
            self.welcome_label.setText(
                f"<html><head/><body><p><span style=\"font-size:16pt; font-weight:700; color:#ffffff;\">愿你充满动力 继续加油(⁎˃ᆺ˂)</span></p></body></html>"
            )
            self.checkBox_Ai.setChecked(True)
            self.checkBox_stopSleep.setChecked(True)
            self.base_pushButton.setEnabled(False)
            self.label_8.setText("已解锁 正在享用")
        elif membership == 'AiVIP':
            log_print("Applying AiVIP membership limits")
            small_member_image = get_resource_path('resources/img/小标/小标-高级会员版本.svg')
            member_image = get_resource_path('resources/img/头标/头标-紫银高级会员.svg')
            self.label_64.setText("99%")
            self.label_66.setText("78%")
            self.Free_pushButton.setText("正在使用Ai+版")
            self.pushButton_29.setIcon(allow_icon)
            self.label_68.setText("使用中")
            self.label_69.setText("使用中")
            self.welcome_label.setText(
                f"<html><head/><body><p><span style=\"font-size:16pt; font-weight:700; color:#ffffff;\">尊敬的会员 愿您再创佳绩(*´∀`*)</span></p></body></html>"
            )
            self.checkBox_Ai.setChecked(True)
            self.checkBox_stopSleep.setChecked(True)
            self.base_pushButton.setEnabled(False)
            self.Ai_pushButton.setEnabled(False)
            self.label_8.setText("已解锁 正在享用")
            self.label_85.setText("已解锁 正在享用")
        else:
            log_print("Applying VIP membership limits")
            small_member_image = get_resource_path('resources/img/小标/小标-超级会员版本.svg')
            member_image = get_resource_path('resources/img/头标/头标-荣耀超级会员.svg')
            self.label_64.setText("99%")
            self.label_66.setText("99%")
            self.Free_pushButton.setText("正在使用超级至尊版")
            self.pushButton_29.setIcon(allow_icon)
            self.pushButton_30.setIcon(allow_icon)
            self.label_68.setText("使用中")
            self.label_69.setText("使用中")
            self.label_70.setText("使用中")
            self.welcome_label.setText(
                f"<html><head/><body><p><span style=\"font-size:16pt; font-weight:700; color:#ffffff;\">尊贵的超级会员 欢迎您(◍•ᴗ•◍)</span></p></body></html>"
            )
            self.checkBox_Ai.setChecked(True)
            self.checkBox_stopSleep.setChecked(True)
            self.base_pushButton.setEnabled(False)
            self.Ai_pushButton.setEnabled(False)
            self.vip_pushButton.setEnabled(False)
            self.label_8.setText("已解锁 正在享用")
            self.label_85.setText("已解锁 正在享用")
            self.label_87.setText("已解锁 正在享用")

        self.vip_frame.setStyleSheet(
            f"image: url({member_image});\n"
            "background: transparent;\n"
            "border-radius:26px")
        self.version_frame.setStyleSheet("QFrame {\n"
                                         "padding: 8px;\n"
                                         f"image: url({small_member_image});\n"
                                         "background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
                                         "stop:0 rgba(155, 81, 45, 255),\n"
                                         "stop:1 rgba(175, 91, 55, 255));\n"
                                         "border: 0px solid red;\n"
                                         "border-radius: 10px;\n"
                                         "}")
        log_print("Membership limits applied")

    def connect_signals(self):
        self.setting_window = SettingWindow()
        self.activities_window = ActivitiesWindow()
        self.key_reply = ReplyDialog()
        self.emotion_pushButton.clicked.connect(self.auto_info.add_emotion_to_message)
        self.file_pushButton.clicked.connect(self.auto_info.open_file_dialog)
        self.pushButton_save.clicked.connect(self.auto_info.save_configuration)
        self.pushButton_import.clicked.connect(self.auto_info.load_configuration)
        self.add_pushButton.clicked.connect(self.auto_info.add_list_item)
        self.message_lineEdit.returnPressed.connect(self.auto_info.add_list_item)
        self.receiver_lineEdit.returnPressed.connect(self.auto_info.add_list_item)

        self.close_pushButton.clicked.connect(self.head_close)
        self.maximize_pushButton.clicked.connect(self.toggle_maximize_restore)
        self.minimize_pushButton.clicked.connect(self.minimize_window)
        self.setup_pushButton.clicked.connect(self.open_setting_window)
        self.feedback_pushButton.clicked.connect(self.feedback)

        self.Free_pushButton.clicked.connect(common.author)
        self.base_pushButton.clicked.connect(self.open_activities_window)
        self.Ai_pushButton.clicked.connect(self.open_activities_window)
        self.vip_pushButton.clicked.connect(self.open_activities_window)

        self.start_pushButton.clicked.connect(self.auto_info.on_start_clicked)
        self.pushButton_split.clicked.connect(self.split.on_start_split_clicked)
        self.pushButton_startSplit.clicked.connect(self.split.on_start_send_clicked)
        self.pushButton_takeover.clicked.connect(self.ai_assistant.start_takeover)
        self.takeOverReceiver_lineEdit.returnPressed.connect(self.ai_assistant.start_takeover)
        self.pushButton_addRule.clicked.connect(self.key_reply.show)

        checkboxes = [self.checkBox_Ai, self.checkBox_period, self.checkBox_comma, self.checkBox_Space]
        for checkbox in checkboxes:
            checkbox.clicked.connect(lambda checked, c=checkbox: self.handle_checkbox_click(c))

        self.vip_frame.mouseReleaseEvent = self.on_vip_frame_clicked

    def feedback(self):
        QDesktopServices.openUrl(QUrl('https://qun.qq.com/universal-share/share?ac=1&authKey=wjyQkU9iG7wc'
                                      '%2BsIEOWFE6cA0ayLLBdYwpMsKYveyufXSOE5FBe7bb9xxvuNYVsEn&busi_data'
                                      '=eyJncm91cENvZGUiOiIxMDIxNDcxODEzIiwidG9rZW4iOiJDaFYxYVpySU9FUVJr'
                                      'RzkwdUZ2QlFVUTQzZzV2VS83TE9mY0NNREluaUZCR05YcnNjWmpKU2V5Q2FYTllFVlJ'
                                      'MIiwidWluIjoiMzU1NTg0NDY3OSJ9&data=M7fVC3YlI68T2S2VpmsR20t9s_xJj6HNpF'
                                      '0GGk2ImSQ9iCE8fZomQgrn_ADRZF0Ee4OSY0x6k2tI5P47NlkWug&svctype=4&tempid'
                                      '=h5_group_info'))

    def open_setting_window(self):
        try:
            write_key_value('admin_log', 'Test')
            log_print("Successfully wrote to admin_log, sufficient permissions")
        except Exception:
            QtWidgets.QMessageBox.critical(self, "非管理员身份", "当前非管理员身份运行，设置可能无法保存")
        self.setting_window.show()
        self.setting_window.activateWindow()

    def open_activities_window(self):
        try:
            write_key_value('admin_log', 'Test')
        except Exception:
            QtWidgets.QMessageBox.critical(self, "非管理员身份", "当前非管理员身份运行，会员无法激活")
        else:
            self.activities_window.show()
            self.activities_window.activateWindow()

    def open_keyReply(self):
        self.key_reply.show()

    def handle_checkbox_click(self, checkbox):
        if checkbox.isChecked():
            log_print(f"Checkbox {checkbox.objectName()} checked")
            if checkbox == self.checkBox_Ai:
                self.checkBox_period.setChecked(False)
                self.checkBox_comma.setChecked(False)
                self.checkBox_Space.setChecked(False)
            else:
                self.checkBox_Ai.setChecked(False)

    def minimize_window(self):
        self.showMinimized()

    def close_application(self):
        QtWidgets.QApplication.quit()

    def head_close(self):
        if common.str_to_bool(read_key_value('close_option')):
            self.hide_to_tray()
        else:
            QtWidgets.QApplication.quit()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            "定时任务在后台继续执行",
            "枫叶已最小化到系统托盘",
            QtWidgets.QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.resize(1289, 734)
            self.maximize_pushButton.setIcon(QtGui.QIcon(get_resource_path(
                'resources/img/窗口控制/窗口控制-最大化.svg')))
        else:
            self.showMaximized()
            self.maximize_pushButton.setIcon(QtGui.QIcon(get_resource_path('resources/img/窗口控制/窗口控制-还原.svg')))

    def _mouse_press_event(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mousePosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _mouse_move_event(self, event):
        if self.mousePosition is not None and event.buttons() & QtCore.Qt.MouseButton.LeftButton:
            new_position = event.globalPosition().toPoint() - self.mousePosition
            self.move(new_position)
            event.accept()

    def show_main_interface(self):
        if self.isMinimized():
            self.showNormal()
        else:
            self.show()
        self.raise_()
        self.activateWindow()

    def get_notice(self):
        try:
            Key, notice_content = get_url()
            if notice_content:
                self.textBrowser.setHtml(notice_content)
        except Exception:
            self.textBrowser.setHtml("""<div style="text-align:center; padding:20px; border:2px solid #ff9800; 
            border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.2); "> <h2 style="color:#ffffff; 
            font-family:'Microsoft YaHei', sans-serif;">欢迎使用LeafAuto PRO</h2> <p style="font-size:16px; text-align:left; 
            margin-top:15px; color:#ffffff; font-family:'Microsoft YaHei', sans-serif; text-indent:2em;"> LeafAuto 
            是我在2024年大二时写的练习程序，没想到居然这么多人爱用。希望大家多提宝贵意见，同时也希望大家会喜欢她。 </p> <p style="font-size:16px; text-align:left; 
            margin-top:15px; color:#ffffff; font-family:'Microsoft YaHei', sans-serif; text-indent:2em;"> 当前 LeafAuto 
            仅支持微信 v3.9 版本（微信 4.0 暂不兼容），您可前往微信官网下载 v3.9 版本使用。 </p> <p style="font-size:16px; text-align:left; 
            margin-top:15px; color:#ffffff; font-family:'Microsoft YaHei', sans-serif; text-indent:2em;"> 
            如果您觉得好用，可以推荐给更多人，这样能让她变得更好！ </p> </div> """)

    def disable_rdp_lock(self):
        try:
            if sys.getwindowsversion().major >= 6:
                log_print("Windows version is 6 or higher, checking admin privileges")
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                    log_print("Not running as admin, requesting elevation")
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    return False

            log_print("Creating/opening registry key")
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services")
            log_print("Setting NoLockScreen registry value")
            winreg.SetValueEx(key, "NoLockScreen", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            log_print("Successfully disabled RDP lock screen")
            log("INFO", "已成功禁用远程桌面断开连接后锁屏")
        except Exception as e:
            log_print(f"Failed to disable RDP lock screen: {str(e)}")
            log("ERROR", f"禁用锁屏失败: {str(e)}")
