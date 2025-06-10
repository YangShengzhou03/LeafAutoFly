from PyQt6 import QtWidgets, QtCore, QtGui
from Thread import AiWorkerThread
from common import log, get_resource_path


class AiAssistant(QtWidgets.QWidget):
    def __init__(self, wx_instances, membership, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.wx_instances = wx_instances
        self.current_wx = None
        self.Membership = membership
        self.ai_thread = None
        self.is_taking_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        self.membership_time_limits = {
            'Free': 60,
            'Base': 60,
            'AiVIP': 1800,
        }

        self.update_current_wx()
        print(f"[AiAssistant] 初始化完成，会员类型: {self.Membership}")

    def update_current_wx(self):
        """更新当前选中的微信实例"""
        selected_nickname = self.parent.comboBox_nickName.currentText()
        self.current_wx = self.wx_instances.get(selected_nickname)

        if not self.current_wx:
            return False
        return True

    def updateAiEditStatus(self):
        try:
            is_checked = self.parent.Global_takeover.isChecked()
            line_edit = self.parent.takeOverReceiver_lineEdit

            if is_checked:
                line_edit.setText("全局Ai接管")
                line_edit.setEnabled(False)
                print("[AiAssistant] 已启用全局AI接管")
            else:
                line_edit.setText("")
                line_edit.setEnabled(True)
                print("[AiAssistant] 已禁用全局AI接管")

        except Exception as e:
            print(f"[AiAssistant] 更新AI编辑状态失败: {str(e)}")

    def start_takeover(self):
        print("[AiAssistant] 尝试启动接管...")

        if not self.update_current_wx() or self.current_wx is None:
            QtWidgets.QMessageBox.warning(self, "微信实例错误", "未选择有效的微信账号，请先选择微信账号")
            return

        if self.is_taking_over:
            print("[AiAssistant] 已在接管中，停止当前接管")
            self._stop_takeover()
        else:
            receiver = self.parent.takeOverReceiver_lineEdit.text()
            if not receiver:
                print("[AiAssistant] 接管联系人为空，取消接管")
                QtWidgets.QMessageBox.warning(self, "接管联系人为空", "接管联系人为空，请先输入联系人")
                return

            try:
                self.is_taking_over = True
                self.elapsed_time = 0
                model = self.parent.comboBox_AiLmodel.currentText()
                role = self.parent.Characters_lineEdit.text()

                print(f"[AiAssistant] 开始接管，接收者: {receiver}, 模型: {model}, 角色: {role}")

                self.ai_thread = AiWorkerThread(
                    self,
                    receiver,
                    wx=self.current_wx,
                    model=model,
                    role=role
                )
                self.ai_thread.finished.connect(self.on_thread_finished)
                self.ai_thread.start()
                self.timer.start(1000)

                log("DEBUG", "Leaf Ai 接管启动")
                self.update_button_icon('resources/img/page3/page3_停止接管.svg')
                self.parent.label_7.setText(
                    self.parent.label_7.text().replace('Leaf Ai接管 准备就绪', 'Leaf Ai 已为您接管'))

                print("[AiAssistant] AI工作线程已启动")

            except Exception as e:
                print(f"[AiAssistant] 启动接管失败: {str(e)}")
                QtWidgets.QMessageBox.critical(self, "接管错误", f"接管开始时发生了一个错误{str(e)}")

    def _stop_takeover(self):
        try:
            if self.ai_thread:
                self.ai_thread.requestInterruption()
                self.ai_thread = None

            self.is_taking_over = False
            self.timer.stop()
            print("[AiAssistant] 接管已停止")
            log("DEBUG", "Ai 接管已停止")
            self.update_button_icon('resources/img/page3/page3_开始接管.svg')
            self.parent.label_7.setText(
                self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))

        except Exception as e:
            print(f"[AiAssistant] 停止接管失败: {str(e)}")

    def on_thread_finished(self):
        try:
            log("INFO", "Leaf Ai 接管线程结束")
            self._stop_takeover()
            self.update_button_icon('resources/img/page3/page3_开始接管.svg')
            self.parent.label_7.setText(
                self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))

            print("[AiAssistant] AI工作线程已完成")

        except Exception as e:
            print(f"[AiAssistant] 处理线程完成事件失败: {str(e)}")

    def update_timer(self):
        try:
            if self.is_taking_over:
                self.elapsed_time += 1
                time_str = self._format_time(self.elapsed_time)
                self.parent.takeOverTime_label.setText(self._create_time_html(time_str, 72))

                max_time = self.membership_time_limits.get(self.Membership, float('inf'))
                print(f"[AiAssistant] 接管已运行: {time_str}, 会员类型: {self.Membership}, 最大时长: {max_time}秒")

                if self.elapsed_time >= max_time:
                    print(f"[AiAssistant] 达到会员时长限制({max_time}秒)，停止接管")
                    self._stop_takeover()
                    self.update_button_icon('resources/img/page3/page3_开始接管.svg')
                    self.parent.label_7.setText(
                        self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))
                    QtWidgets.QMessageBox.warning(self, "版本限制", "版本限制,接管终止,超级会员尊享无限接管")
            else:
                time_str = self._format_time(self.elapsed_time)
                self.parent.takeOverTime_label.setText(self._create_time_html(time_str, 88))

        except Exception as e:
            print(f"[AiAssistant] 更新计时器失败: {str(e)}")

    def _format_time(self, seconds):
        """将秒数格式化为 HH:MM:SS 字符串"""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def _create_time_html(self, time_str, font_size):
        """创建时间显示的HTML字符串"""
        return f"<html><head/><body><p align=\"center\"><span style=\" font-size:{font_size}pt;\">{time_str}</span></p></body></html>"

    def update_button_icon(self, icon_path):
        try:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(get_resource_path(icon_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)

            button = self.parent.pushButton_takeover
            button.setIcon(icon)
            button.setIconSize(QtCore.QSize(38, 38))

            print(f"[AiAssistant] 按钮图标已更新为: {icon_path}")

        except Exception as e:
            print(f"[AiAssistant] 更新按钮图标失败: {str(e)}")
