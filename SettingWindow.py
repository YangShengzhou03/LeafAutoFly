import os
import re
import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QInputDialog, QMessageBox

import UpdateDialog
from System_info import write_key_value, read_key_value
from Thread import ErrorSoundThread
from Ui_SettingWindow import Ui_SettingWindow
from common import str_to_bool, log, get_resource_path, log_print


class SettingWindow(QtWidgets.QMainWindow, Ui_SettingWindow):
    language_map = {'cn': '简体中文', 'cn_t': '繁体中文', 'en': 'English'}
    reverse_language_map = {v: k for k, v in language_map.items()}

    def __init__(self):
        super().__init__()
        log_print("[SETTINGS] Initializing SettingWindow")
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("设置枫叶")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/icon.ico')))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # 添加初始化标记，防止启动时自动播放试音
        self._is_initializing = True

        self.error_sound_thread = ErrorSoundThread()

        self.ui.checkBox_Email.clicked.connect(self.select_email)
        self.ui.pushButton_exit_setting.clicked.connect(self.save_close)
        self.ui.pushButton_test_sound.clicked.connect(self.toggle_audio)
        self.ui.pushButton_check_updata.clicked.connect(self.check_update)
        self.ui.pushButton_clean.clicked.connect(self.clean_date)
        self.ui.pushButton_help.clicked.connect(self.help)

        membership = read_key_value('membership')
        log_print(f"[SETTINGS] Detected membership: {membership}")
        if membership == 'VIP':
            pass
        elif membership == 'AiVIP':
            self.ui.checkBox_Email.setEnabled(False)
            log_print("[SETTINGS] Disabled Email checkbox for AiVIP membership")
        else:
            self.ui.checkBox_net_time.setEnabled(False)
            self.ui.checkBox_Email.setEnabled(False)
            log_print("[SETTINGS] Disabled net_time and Email checkboxes for Free membership")

        self.setting_init()
        self.ui.comboBox_errorAudio.currentIndexChanged.connect(self.update_selected_sound)

        # 初始化完成
        self._is_initializing = False

    def clean_date(self):
        log_print("[SETTINGS] Clean data operation requested")
        files_to_clean = ['_internal/AutoReply_Rules.json', '_internal/tasks.json', '_internal/log.txt']
        cleaned = False
        for file in files_to_clean:
            if os.path.exists(file):
                os.remove(file)
                cleaned = True
                log_print(f"[SETTINGS] Removed file: {file}")
        if not cleaned:
            log_print("[SETTINGS] No files to clean")
            QtWidgets.QMessageBox.warning(self, "无需清理", "已经很干净了，无需清理。")
        else:
            log_print("[SETTINGS] Cleanup complete, restarting application")
            QtWidgets.QMessageBox.information(self, "清理完成", "数据已清理，即将重启以完成。")
            sys.exit(0)

    def select_email(self, state):
        log_print(f"[SETTINGS] Email checkbox state changed: {state}")
        if state:
            email = self.show_input_dialog()
            if email:
                write_key_value('email', email)
                log_print(f"[SETTINGS] Email saved: {email}")
            else:
                self.ui.checkBox_Email.setChecked(False)
                log_print("[SETTINGS] Email input cancelled, unchecking checkbox")
        else:
            self.ui.checkBox_Email.setChecked(False)
            log_print("[SETTINGS] Unchecking Email checkbox")

    def show_input_dialog(self):
        log_print("[SETTINGS] Showing email input dialog")
        email, ok = QInputDialog.getText(self, '输入邮箱', '请输入用于接收出错信息的邮箱:')
        if ok and email:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                log_print(f"[SETTINGS] Valid email entered: {email}")
                return email
            else:
                log_print(f"[SETTINGS] Invalid email format: {email}")
                QMessageBox.warning(self, "错误", "邮箱格式无效,请输入正确的邮箱")
                return None
        log_print("[SETTINGS] Email input dialog cancelled")
        return None

    def help(self):
        log_print("[SETTINGS] Opening help URL")
        QDesktopServices.openUrl(QUrl('https://blog.csdn.net/Yang_shengzhou/article/details/143782041'))

    def check_update(self):
        log_print("[SETTINGS] Checking for updates")
        if UpdateDialog.check_update() == 0:
            log_print("[SETTINGS] Application is up-to-date")
            QtWidgets.QMessageBox.information(self, "已经是最新版本", "当前运行的已经是最新版本")

    def toggle_audio(self):
        log_print("[SETTINGS] Test sound button clicked")
        if hasattr(self, 'selected_audio_file'):
            log_print(f"[SETTINGS] Playing test sound: {self.selected_audio_file}")
            self.error_sound_thread.update_sound_file(self.selected_audio_file)
            self.error_sound_thread.play_test()
        else:
            log_print("[SETTINGS] No selected audio file, skipping test")

    def setting_init(self):
        log_print("[SETTINGS] Initializing settings")
        for key, checkbox in [
            ('error_email', self.ui.checkBox_Email),
            ('error_sound', self.ui.checkBox_sound),
            ('net_time', self.ui.checkBox_net_time),
            ('auto_update', self.ui.checkBox_updata),
            ('serve_lock', self.ui.checkBox_sever),
            ('close_option', self.ui.checkBox_close_option)
        ]:
            value = str_to_bool(read_key_value(key))
            checkbox.setChecked(value)
            log_print(f"[SETTINGS] Set {key} checkbox to: {value}")

        lang_code = read_key_value('language')
        lang_name = self.language_map.get(lang_code, '简体中文')
        index = self.ui.comboBox_language.findText(lang_name)
        if index >= 0:
            self.ui.comboBox_language.setCurrentIndex(index)
            log_print(f"[SETTINGS] Set language to: {lang_name}")
        else:
            log_print(f"[SETTINGS] Language not found: {lang_name}, using default")

        version = read_key_value('version')
        self.ui.label_version.setText('V' + version)
        log_print(f"[SETTINGS] Set version label to: {version}")

        timestep = int(read_key_value('add_timestep'))
        self.ui.spinBox_timestep.setValue(timestep)
        log_print(f"[SETTINGS] Set timestep to: {timestep}")

        self.audio_files = {
            0: get_resource_path('resources/sound/error_sound_1.mp3'),
            1: get_resource_path('resources/sound/error_sound_2.mp3'),
            2: get_resource_path('resources/sound/error_sound_3.mp3'),
            3: get_resource_path('resources/sound/error_sound_4.mp3'),
            4: get_resource_path('resources/sound/error_sound_5.mp3')
        }

        selected_index = int(read_key_value('selected_audio_index') or 0)
        log_print(f"[SETTINGS] Loading audio selection: {selected_index}")

        self.ui.comboBox_errorAudio.blockSignals(True)
        self.ui.comboBox_errorAudio.clear()
        for i in range(5):
            self.ui.comboBox_errorAudio.addItem(f"提示音{i + 1}")
        self.ui.comboBox_errorAudio.blockSignals(False)

        if 0 <= selected_index < 5:
            self.ui.comboBox_errorAudio.setCurrentIndex(selected_index)
            self.update_selected_sound(selected_index)
            log_print(f"[SETTINGS] Set audio index to: {selected_index}")
        else:
            log('ERROR', f'无效的索引: {selected_index}')
            self.ui.comboBox_errorAudio.setCurrentIndex(0)
            self.update_selected_sound(0)
            log_print("[SETTINGS] Reset to default audio index 0")

    def save_close(self):
        log_print("[SETTINGS] Saving settings and closing window")
        try:
            if self.error_sound_thread._is_running:
                self.error_sound_thread.stop_playback()
                log_print("[SETTINGS] Stopped running audio thread")

            for key, checkbox in [
                ('error_email', self.ui.checkBox_Email),
                ('error_sound', self.ui.checkBox_sound),
                ('net_time', self.ui.checkBox_net_time),
                ('auto_update', self.ui.checkBox_updata),
                ('serve_lock', self.ui.checkBox_sever),
                ('close_option', self.ui.checkBox_close_option)
            ]:
                value = str(checkbox.isChecked())
                write_key_value(key, value)
                log_print(f"[SETTINGS] Saved {key} as: {value}")

            timestep = str(self.ui.spinBox_timestep.value())
            write_key_value('add_timestep', timestep)
            log_print(f"[SETTINGS] Saved add_timestep as: {timestep}")

            lang_code = self.reverse_language_map.get(self.ui.comboBox_language.currentText(), 'cn')
            write_key_value('language', lang_code)
            log_print(f"[SETTINGS] Saved language as: {lang_code}")

            audio_index = str(self.ui.comboBox_errorAudio.currentIndex())
            write_key_value('selected_audio_index', audio_index)
            log_print(f"[SETTINGS] Saved selected_audio_index as: {audio_index}")

        except Exception as e:
            log('ERROR', f'设置保存失败，请用管理员身份运行软件。')
            log_print(f"[SETTINGS] Error saving settings: {str(e)}")
        else:
            log('DEBUG', '设置保存成功，部分功能需重启生效')
            log_print("[SETTINGS] Settings saved successfully")
            QtWidgets.QMessageBox.information(self, "设置保存成功", "设置保存成功，部分功能需重启生效")
        self.close()

    def update_selected_sound(self, index):
        log_print(f"[SETTINGS] Updating selected sound to index: {index}")
        if 0 <= index < len(self.audio_files):
            if self.error_sound_thread._is_running:
                self.error_sound_thread.stop_playback()
                log_print("[SETTINGS] Stopped running audio thread")
            self.selected_audio_file = self.audio_files[index]
            log_print(f"[SETTINGS] Selected audio file: {self.selected_audio_file}")

            # 只有当用户主动点击试音按钮时才播放，初始化阶段不播放
            if not self._is_initializing:
                self.toggle_audio()
        else:
            log('ERROR', f'报错音频索引无效: {index}')
            log_print(f"[SETTINGS] Invalid audio index: {index}")
