from PyQt6 import QtWidgets, QtCore, QtGui

from Thread import AiWorkerThread
from common import log, get_resource_path, log_print


class AiAssistant(QtWidgets.QWidget):
    def __init__(self, wx_instances, membership, parent=None):
        super().__init__(parent)
        log_print("[AiAssistant] Initializing AI assistant...")

        self.parent = parent
        self.wx_instances = wx_instances
        self.Membership = membership
        self.ai_thread = None
        self.current_wx = None
        self.is_taking_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0

        log_print(f"[AiAssistant] Initialization completed, membership type: {self.Membership}")

        self.update_current_wx()

    def update_current_wx(self):
        selected_nickname = self.parent.comboBox_nickName.currentText()
        self.current_wx = self.wx_instances.get(selected_nickname)
        return bool(self.current_wx)

    def updateAiEditStatus(self):
        try:
            log_print("[AiAssistant] Updating AI edit status...")

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
            log_print(f"[AiAssistant] Failed to update AI edit status: {str(e)}")

    def start_takeover(self):
        log_print("[AiAssistant] Attempting to start takeover...")

        if self.is_taking_over:
            log_print("[AiAssistant] Already in takeover mode, stopping current takeover")
            try:
                if self.ai_thread is not None:
                    assert isinstance(self.ai_thread, AiWorkerThread)
                    self.ai_thread.requestInterruption()
                    self.ai_thread = None
                self.is_taking_over = False
                self.timer.stop()
                log_print("[AiAssistant] Takeover stopped successfully")
            except Exception as e:
                log_print(f"[AiAssistant] Failed to stop takeover: {str(e)}")
        else:
            try:
                log_print("[AiAssistant] Validating takeover parameters...")

                if not self.parent.takeOverReceiver_lineEdit.text():
                    log_print("[AiAssistant] Takeover receiver is empty, takeover canceled")
                    QtWidgets.QMessageBox.warning(self, "接管联系人为空", "接管联系人为空，请先输入联系人")
                    return

                self.is_taking_over = True
                self.elapsed_time = 0
                model = self.parent.comboBox_AiLmodel.currentText()
                role = self.parent.Characters_lineEdit.text()

                log_print(
                    f"[AiAssistant] Starting takeover - Receiver: {self.parent.takeOverReceiver_lineEdit.text()}, Model: {model}, Role: {role}")

                log_print("[AiAssistant] Creating and starting AI worker thread...")
                self.ai_thread = AiWorkerThread(self.current_wx, self.parent.takeOverReceiver_lineEdit.text(),
                                                model=model, role=role)
                self.ai_thread.finished.connect(self.on_thread_finished)
                self.ai_thread.start()
                self.timer.start(1000)

                log("DEBUG", "Leaf Ai 接管启动")
                self.update_button_icon('resources/img/page3/page3_停止接管.svg')
                self.parent.label_7.setText(
                    self.parent.label_7.text().replace('Leaf Ai接管 准备就绪', 'Leaf Ai 已为您接管'))

                log_print("[AiAssistant] AI worker thread started successfully")
            except Exception as e:
                log_print(f"[AiAssistant] Failed to start takeover: {str(e)}")
                QtWidgets.QMessageBox.critical(self, "接管错误", f"接管开始时发生了一个错误{str(e)}")

    def on_thread_finished(self):
        try:
            log("INFO", "Leaf Ai 接管线程结束")
            log_print("[AiAssistant] Handling thread finished event...")

            self.is_taking_over = False
            self.timer.stop()
            self.update_button_icon('resources/img/page3/page3_开始接管.svg')
            self.parent.label_7.setText(
                self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))

            log_print("[AiAssistant] AI worker thread completed successfully")
        except Exception as e:
            log_print(f"[AiAssistant] Failed to handle thread finished event: {str(e)}")

    def update_timer(self):
        try:
            if self.is_taking_over:
                self.elapsed_time += 1
                minutes, seconds = divmod(self.elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                html = f"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt;\">{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)

                # Determine time limits based on membership
                if self.Membership == 'Free':
                    max_time = 60  # 1 minute
                elif self.Membership == 'Base':
                    max_time = 60  # 1 minute
                elif self.Membership == 'AiVIP':
                    max_time = 1800  # 30 minutes
                else:
                    max_time = float('inf')  # Unlimited

                if self.elapsed_time >= max_time:
                    log_print(f"[AiAssistant] Membership time limit reached ({max_time} seconds), stopping takeover")
                    self.is_taking_over = False
                    self.timer.stop()
                    if self.ai_thread is not None:
                        self.ai_thread.requestInterruption()
                        self.ai_thread = None
                    self.update_button_icon('resources/img/page3/page3_开始接管.svg')
                    self.parent.label_7.setText(
                        self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))
                    QtWidgets.QMessageBox.warning(self, "版本限制", "版本限制 接管终止，超级会员尊享无限接管")
            else:
                # Update timer display even when not taking over
                minutes, seconds = divmod(self.elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                html = f"<html><head/><body><p align=\"center\"><span style=\" font-size:88pt;\">{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)

        except Exception as e:
            log_print(f"[AiAssistant] Failed to update timer: {str(e)}")

    def update_button_icon(self, icon_path):
        try:
            log_print(f"[AiAssistant] Updating button icon to: {icon_path}")

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(get_resource_path(icon_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.parent.pushButton_takeover.setIcon(icon)
            self.parent.pushButton_takeover.setIconSize(QtCore.QSize(38, 38))

            log_print("[AiAssistant] Button icon updated successfully")
        except Exception as e:
            log_print(f"[AiAssistant] Failed to update button icon: {str(e)}")
