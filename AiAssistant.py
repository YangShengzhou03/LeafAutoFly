from PyQt6 import QtWidgets, QtCore, QtGui

from Thread import AiWorkerThread
from common import log, get_resource_path


class AiAssistant(QtWidgets.QWidget):
    def __init__(self, wx_instances, membership, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.wx_instances = wx_instances  # 存储所有微信实例的字典
        self.current_wx = None  # 当前选中的微信实例
        self.Membership = membership
        self.ai_thread = None
        self.is_taking_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0

        # 初始化时设置当前微信实例
        self.update_current_wx()
        print(f"[AiAssistant] 初始化完成，会员类型: {self.Membership}")

    def update_current_wx(self):
        """更新当前选中的微信实例"""
        selected_nickname = self.parent.comboBox_nickName.currentText()
        if selected_nickname in self.wx_instances:
            self.current_wx = self.wx_instances[selected_nickname]
            return True
        else:
            log("WARNING", f"[AiAssistant] 所选微信账号 {selected_nickname} 未初始化")
            return False

    def updateAiEditStatus(self):
        try:
            is_checked = self.parent.Global_takeover.isChecked()
            if is_checked:
                self.parent.takeOverReceiver_lineEdit.setText("全局Ai接管")
                self.parent.takeOverReceiver_lineEdit.setEnabled(False)
                print("[AiAssistant] 已启用全局AI接管")
            else:
                self.parent.takeOverReceiver_lineEdit.setText("")
                self.parent.takeOverReceiver_lineEdit.setEnabled(True)
                print("[AiAssistant] 已禁用全局AI接管")
        except Exception as e:
            print(f"[AiAssistant] 更新AI编辑状态失败: {str(e)}")

    def start_takeover(self):
        print("[AiAssistant] 尝试启动接管...")
        # 每次启动接管前先更新当前微信实例
        if not self.update_current_wx() or self.current_wx is None:
            QtWidgets.QMessageBox.warning(self, "微信实例错误", "未选择有效的微信账号，请先选择微信账号")
            return

        if self.is_taking_over:
            print("[AiAssistant] 已在接管中，停止当前接管")
            try:
                if self.ai_thread is not None:
                    assert isinstance(self.ai_thread, AiWorkerThread)
                    self.ai_thread.requestInterruption()
                    self.ai_thread = None
                self.is_taking_over = False
                self.timer.stop()
                print("[AiAssistant] 接管已停止")
            except Exception as e:
                print(f"[AiAssistant] 停止接管失败: {str(e)}")
        else:
            try:
                if not self.parent.takeOverReceiver_lineEdit.text():
                    print("[AiAssistant] 接管联系人为空，取消接管")
                    QtWidgets.QMessageBox.warning(self, "接管联系人为空", "接管联系人为空，请先输入联系人")
                    return

                self.is_taking_over = True
                self.elapsed_time = 0
                model = self.parent.comboBox_AiLmodel.currentText()
                role = self.parent.Characters_lineEdit.text()
                print(
                    f"[AiAssistant] 开始接管，接收者: {self.parent.takeOverReceiver_lineEdit.text()}, 模型: {model}, 角色: {role}")

                # 将当前选中的微信实例传递给工作线程
                self.ai_thread = AiWorkerThread(
                    self,
                    self.parent.takeOverReceiver_lineEdit.text(),
                    wx=self.current_wx,  # 传递当前选中的微信实例
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

    def on_thread_finished(self):
        try:
            log("INFO", "Leaf Ai 接管线程结束")
            self.is_taking_over = False
            self.timer.stop()
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
                minutes, seconds = divmod(self.elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                html = f"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt;\">{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)

                if self.Membership == 'Free':
                    max_time = 60  # 1分钟
                elif self.Membership == 'Base':
                    max_time = 60  # 1分钟
                elif self.Membership == 'AiVIP':
                    max_time = 1800  # 30分钟
                else:
                    max_time = float('inf')  # 不限时

                print(f"[AiAssistant] 接管已运行: {time_str}, 会员类型: {self.Membership}, 最大时长: {max_time}秒")

                if self.elapsed_time >= max_time:
                    print(f"[AiAssistant] 达到会员时长限制({max_time}秒)，停止接管")
                    self.is_taking_over = False
                    self.timer.stop()
                    if self.ai_thread is not None:
                        self.ai_thread.requestInterruption()
                        self.ai_thread = None
                    self.update_button_icon('resources/img/page3/page3_开始接管.svg')
                    self.parent.label_7.setText(
                        self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))
                    QtWidgets.QMessageBox.warning(self, "版本限制", "版本限制,接管终止,超级会员尊享无限接管")
            else:
                minutes, seconds = divmod(self.elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                html = f"<html><head/><body><p align=\"center\"><span style=\" font-size:88pt;\">{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)
        except Exception as e:
            print(f"[AiAssistant] 更新计时器失败: {str(e)}")

    def update_button_icon(self, icon_path):
        try:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(get_resource_path(icon_path)), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.parent.pushButton_takeover.setIcon(icon)
            self.parent.pushButton_takeover.setIconSize(QtCore.QSize(38, 38))
            print(f"[AiAssistant] 按钮图标已更新为: {icon_path}")
        except Exception as e:
            print(f"[AiAssistant] 更新按钮图标失败: {str(e)}")