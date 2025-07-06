from PyQt6 import QtWidgets, QtCore, QtGui
from Thread import AiWorkerThread
from common import log, get_resource_path, log_print

class AiAssistant(QtWidgets.QWidget):
    def __init__(self, wx_instances, membership, parent=None):
        super().__init__(parent)
        log_print("[AiAssistant] Initializing...")

        self.parent = parent
        self.wx_instances = wx_instances
        self.Membership = membership
        self.ai_thread = None
        self.current_wx = None
        self.is_taking_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0

        log_print(f"[AiAssistant] Initialized with membership: {self.Membership}")
        self.update_current_wx()

    def update_current_wx(self):
        selected_nickname = self.parent.comboBox_nickName.currentText()
        self.current_wx = self.wx_instances.get(selected_nickname)
        log_print(f"[AiAssistant] Current WeChat instance set: {bool(self.current_wx)}")
        return bool(self.current_wx)

    def updateAiEditStatus(self):
        try:
            log_print("[AiAssistant] Updating edit status...")
            is_checked = self.parent.Global_takeover.isChecked()
            if is_checked:
                self.parent.takeOverReceiver_lineEdit.setText("全局Ai接管")
                self.parent.takeOverReceiver_lineEdit.setEnabled(False)
                log_print("[AiAssistant] Global AI takeover enabled")
            else:
                self.parent.takeOverReceiver_lineEdit.setText("")
                self.parent.takeOverReceiver_lineEdit.setEnabled(True)
                log_print("[AiAssistant] Global AI takeover disabled")
        except Exception as e:
            log_print(f"[AiAssistant] Error updating AI edit status: {e}")

    def start_takeover(self):
        log_print("[AiAssistant] Start takeover triggered")

        if self.is_taking_over:
            log_print("[AiAssistant] Already taking over. Stopping current takeover.")
            try:
                if self.ai_thread:
                    assert isinstance(self.ai_thread, AiWorkerThread)
                    self.ai_thread.requestInterruption()
                    self.ai_thread = None
                self.is_taking_over = False
                self.timer.stop()
                log_print("[AiAssistant] Takeover stopped")
            except Exception as e:
                log_print(f"[AiAssistant] Error stopping takeover: {e}")
        else:
            try:
                receiver = self.parent.takeOverReceiver_lineEdit.text()
                if not receiver:
                    log_print("[AiAssistant] Takeover receiver is empty")
                    QtWidgets.QMessageBox.warning(self, "接管联系人为空", "接管联系人为空，请先输入联系人")
                    return

                self.is_taking_over = True
                self.elapsed_time = 0
                model = self.parent.comboBox_AiLmodel.currentText()
                role = self.parent.Characters_lineEdit.text()
                only_at = self.parent.checkBox_onlyAt.isChecked()

                log_print("[AiAssistant] Creating AI worker thread")
                self.ai_thread = AiWorkerThread(self.current_wx, receiver, model=model, role=role, only_at=only_at)
                self.ai_thread.finished.connect(self.on_thread_finished)
                self.ai_thread.start()
                self.timer.start(1000)

                log("DEBUG", "Leaf Ai 接管启动")
                self.update_button_icon('resources/img/page3/page3_停止接管.svg')
                self.parent.label_7.setText(self.parent.label_7.text().replace('Leaf Ai接管 准备就绪', 'Leaf Ai 已为您接管'))

                log_print("[AiAssistant] Takeover started")
            except Exception as e:
                log_print(f"[AiAssistant] Failed to start takeover: {e}")
                QtWidgets.QMessageBox.critical(self, "接管错误", f"接管开始时发生了一个错误{e}")

    def on_thread_finished(self):
        try:
            log("INFO", "Leaf Ai 接管线程结束")
            log_print("[AiAssistant] Thread finished")
            self.is_taking_over = False
            self.timer.stop()
            self.update_button_icon('resources/img/page3/page3_开始接管.svg')
            self.parent.label_7.setText(self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))
        except Exception as e:
            log_print(f"[AiAssistant] Error handling thread finish: {e}")

    def update_timer(self):
        try:
            if self.is_taking_over:
                self.elapsed_time += 1
                h, rem = divmod(self.elapsed_time, 3600)
                m, s = divmod(rem, 60)
                time_str = f"{h:02}:{m:02}:{s:02}"
                html = f"<html><body><p align='center'><span style='font-size:72pt;'>{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)

                max_time = {
                    'Free': 60,
                    'Base': 60,
                    'AiVIP': 1800
                }.get(self.Membership, float('inf'))

                if self.elapsed_time >= max_time:
                    log_print(f"[AiAssistant] Max time reached ({max_time}s), stopping takeover")
                    self.is_taking_over = False
                    self.timer.stop()
                    if self.ai_thread:
                        self.ai_thread.requestInterruption()
                        self.ai_thread = None
                    self.update_button_icon('resources/img/page3/page3_开始接管.svg')
                    self.parent.label_7.setText(self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))
                    QtWidgets.QMessageBox.warning(self, "版本限制", "版本限制 接管终止，超级会员尊享无限接管")
            else:
                h, rem = divmod(self.elapsed_time, 3600)
                m, s = divmod(rem, 60)
                time_str = f"{h:02}:{m:02}:{s:02}"
                html = f"<html><body><p align='center'><span style='font-size:88pt;'>{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)
        except Exception as e:
            log_print(f"[AiAssistant] Error in update_timer: {e}")

    def update_button_icon(self, icon_path):
        try:
            log_print(f"[AiAssistant] Updating icon to: {icon_path}")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(get_resource_path(icon_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.parent.pushButton_takeover.setIcon(icon)
            self.parent.pushButton_takeover.setIconSize(QtCore.QSize(38, 38))
        except Exception as e:
            log_print(f"[AiAssistant] Error updating button icon: {e}")
