from PyQt6 import QtWidgets, QtCore, QtGui
from Thread import AiWorkerThread
from common import log, get_resource_path, log_print


class AiAssistant(QtWidgets.QWidget):
    def __init__(self, wx_instances, membership, parent=None):
        super().__init__(parent)
        log("DEBUG", "开始初始化AI助手")
        log_print("[AiAssistant] Starting initialization process")

        self.parent = parent
        self.wx_instances = wx_instances
        self.Membership = membership
        self.ai_thread = None
        self.current_wx = None
        self.is_taking_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0

        log("DEBUG", f"检测到会员等级: {self.Membership}")
        log("DEBUG", f"微信实例数量: {len(wx_instances)}")
        log_print(f"[AiAssistant] Membership level detected: {self.Membership}")
        log_print(f"[AiAssistant] WeChat instances count: {len(wx_instances)}")
        self.update_current_wx()
        log("DEBUG", "AI助手初始化完成")
        log_print("[AiAssistant] Initialization process completed")

    def update_current_wx(self):
        log("DEBUG", "更新当前微信微信实例")
        log_print("[AiAssistant] Updating current WeChat instance")
        selected_nickname = self.parent.comboBox_nickName.currentText()
        log("DEBUG", f"从下拉框选择的昵称: {selected_nickname}")
        log_print(f"[AiAssistant] Selected nickname from combo box: {selected_nickname}")

        self.current_wx = self.wx_instances.get(selected_nickname)

        if self.current_wx:
            log("DEBUG", f"成功设置当前微信实例: {selected_nickname}")
            log_print(f"[AiAssistant] Successfully set current WeChat instance: {selected_nickname}")
        else:
            log("WARNING", f"未找到找到微信实例: {selected_nickname}")
            log_print(f"[AiAssistant] Failed to find WeChat instance for: {selected_nickname}")

        return bool(self.current_wx)

    def updateAiEditStatus(self):
        try:
            log("DEBUG", "更新AI编辑状态")
            log_print("[AiAssistant] Updating AI edit status")

            is_checked = self.parent.Global_takeover.isChecked()
            log("DEBUG", f"全局接管复选框状态: {is_checked}")
            log_print(f"[AiAssistant] Global takeover checkbox state: {is_checked}")

            if is_checked:
                self.parent.takeOverReceiver_lineEdit.setText("全局Ai接管")
                self.parent.takeOverReceiver_lineEdit.setEnabled(False)
                log("DEBUG", "启用全局全局AI接管 - 接收者字段已禁用")
                log_print("[AiAssistant] Global AI takeover enabled - receiver field disabled")
            else:
                self.parent.takeOverReceiver_lineEdit.setText("")
                self.parent.takeOverReceiver_lineEdit.setEnabled(True)
                log("DEBUG", "禁用全局AI接管 - 接收者字段已启用")
                log_print("[AiAssistant] Global AI takeover disabled - receiver field enabled")

        except Exception as e:
            log("ERROR", f"更新AI编辑状态时出错: {str(e)}")
            log_print(f"[AiAssistant] Error updating AI AI edit status: {str(e)}")

    def start_takeover(self):
        log("DEBUG", "触发接管切换")
        log_print("[AiAssistant] Takeover toggle triggered")

        if self.is_taking_over:
            log("DEBUG", "当前状态: 正在接管 - 尝试停止")
            log_print("[AiAssistant] Current state: taking over - attempting to stop")
            try:
                if self.ai_thread:
                    log("DEBUG", f"AI线程存在: {self.ai_thread}")
                    log_print(f"[AiAssistant] AI thread exists: {self.ai_thread}")
                    assert isinstance(self.ai_thread, AiWorkerThread)
                    self.ai_thread.requestInterruption()
                    self.ai_thread = None
                    log("DEBUG", "AI线程已中断并清除")
                    log_print("[AiAssistant] AI thread interrupted and cleared")

                self.is_taking_over = False
                self.timer.stop()
                log("DEBUG", "接管已停止，计时器已暂停")
                log_print("[AiAssistant] Takeover stopped and timer halted")

            except Exception as e:
                log("ERROR", f"停止接管时出错: {str(e)}")
                log_print(f"[AiAssistant] Error stopping takeover: {str(e)}")
        else:
            try:
                log("DEBUG", "当前状态: 未接管 - 尝试启动")
                log_print("[AiAssistant] Current state: not taking over - attempting to start")

                # 验证当前微信实例
                if not self.update_current_wx():
                    log("WARNING", "无法启动接管 - 没有有效的微信实例")
                    log_print("[AiAssistant] Cannot start takeover - no valid WeChat instance")
                    QtWidgets.QMessageBox.warning(self, "微信实例错误", "未找到有效的微信实例，请先选择微信")
                    return

                receiver = self.parent.takeOverReceiver_lineEdit.text()
                log("DEBUG", f"接管接收者输入: {receiver}")
                log_print(f"[AiAssistant] Takeover receiver input: {receiver}")

                if not receiver:
                    log("WARNING", "接管已中止 - 接收者为空")
                    log_print("[AiAssistant] Takeover aborted - receiver is empty")
                    QtWidgets.QMessageBox.warning(self, "接管联系人为空", "接管联系人为空，请先输入联系人")
                    return

                # 设置接管状态并初始化
                self.is_taking_over = True
                self.elapsed_time = 0

                # 从UI获取配置
                model = self.parent.comboBox_AiLmodel.currentText()
                role = self.parent.Characters_lineEdit.text()
                only_at = self.parent.checkBox_onlyAt.isChecked()

                log("DEBUG", f"接管配置 - 模型: {model}, 角色: {role}, 仅@: {only_at}")
                log_print(f"[AiAssistant] Takeover configuration - Model: {model}, Role: {role}, Only @: {only_at}")

                # 创建并启动AI工作线程
                log("DEBUG", "创建新的AI工作线程")
                log_print("[AiAssistant] Creating new AI worker thread")
                self.ai_thread = AiWorkerThread(self.current_wx, receiver, model=model, role=role, only_at=only_at)
                self.ai_thread.finished.connect(self.on_thread_finished)
                self.ai_thread.start()
                self.timer.start(1000)
                log("DEBUG", "AI工作线程已启动，计时器已激活")
                log_print("[AiAssistant] AI worker thread started and timer activated")

                # 更新UI
                log("DEBUG", "Leaf Ai 接管启动")
                self.update_button_icon('resources/img/page3/page3_停止接管.svg')
                self.parent.label_7.setText(
                    self.parent.label_7.text().replace('Leaf Ai接管 准备就绪', 'Leaf Ai 已为您接管'))

                log("INFO", "接管已成功启动")
                log_print("[AiAssistant] Takeover started successfully")

            except Exception as e:
                log("ERROR", f"启动接管失败: {str(e)}")
                log_print(f"[AiAssistant] Failed to start takeover: {str(e)}")
                QtWidgets.QMessageBox.critical(self, "接管错误", f"接管开始时发生了一个错误: {e}")

    def on_thread_finished(self):
        try:
            log("INFO", "Leaf Ai 接管线程结束")
            log_print("[AiAssistant] AI worker thread finished")

            self.is_taking_over = False
            self.timer.stop()
            log("DEBUG", "接管状态已重置，计时器已停止")
            log_print("[AiAssistant] Takeover state reset and timer stopped")

            # 更新UI
            self.update_button_icon('resources/img/page3/page3_开始接管.svg')
            self.parent.label_7.setText(
                self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))

            log("DEBUG", "线程结束处理完成，UI已更新")
            log_print("[AiAssistant] UI thread thread cleanup UI updated successfully")

        except Exception as e:
            log("ERROR", f"处理线程结束时出错: {str(e)}")
            log_print(f"[AiAssistant] Error handling handling thread finish: {str(e)}")

    def update_timer(self):
        try:
            if self.is_taking_over:
                self.elapsed_time += 1
                h, rem = divmod(self.elapsed_time, 3600)
                m, s = divmod(rem, 60)
                time_str = f"{h:02}:{m:02}:{s:02}"
                html = f"<html><body><p align='center'><span style='font-size:72pt;'>{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)
                log("DEBUG", f"接管活跃中 - 已用时间: {time_str}")
                log_print(f"[AiAssistant] Takeover active - elapsed time: {time_str}")

                # 检查会员时间限制
                max_time = {
                    'Free': 60,
                    'Base': 60,
                    'AiVIP': 1800
                }.get(self.Membership, float('inf'))

                log("DEBUG", f"会员时间限制: {max_time}秒")
                log_print(f"[AiAssistant] Membership time limit: {max_time} seconds")

                if self.elapsed_time >= max_time:
                    log("WARNING", f"已达到最大时间({max_time}秒)，停止接管")
                    log_print(f"[AiAssistant] Max time reached ({max_time}s), stopping takeover")

                    self.is_taking_over = False
                    self.timer.stop()

                    if self.ai_thread:
                        self.ai_thread.requestInterruption()
                        self.ai_thread = None

                    self.update_button_icon('resources/img/page3/page3_开始接管.svg')
                    self.parent.label_7.setText(
                        self.parent.label_7.text().replace('Leaf Ai 已为您接管', 'Leaf Ai接管 准备就绪'))

                    QtWidgets.QMessageBox.warning(self, "版本限制", "版本限制 接管终止，超级会员尊享无限接管")
            else:
                # 即使不活跃也更新显示
                h, rem = divmod(self.elapsed_time, 3600)
                m, s = divmod(rem, 60)
                time_str = f"{h:02}:{m:02}:{s:02}"
                html = f"<html><body><p align='center'><span style='font-size:88pt;'>{time_str}</span></p></body></html>"
                self.parent.takeOverTime_label.setText(html)
                log("DEBUG", f"接管未活跃 - 时间显示已更新: {time_str}")
                log_print(f"[AiAssistant] Takeover inactive - time display updated: {time_str}")

        except Exception as e:
            log("ERROR", f"更新计时器时出错: {str(e)}")
            log_print(f"[AiAssistant] Error in update_timer: {str(e)}")

    def update_button_icon(self, icon_path):
        try:
            log("DEBUG", f"更新按钮图标为: {icon_path}")
            log_print(f"[AiAssistant] Updating button icon to: {icon_path}")

            icon = QtGui.QIcon()
            full_path = get_resource_path(icon_path)
            log("DEBUG", f"解析的图标路径: {full_path}")
            log_print(f"[AiAssistant] Resolved icon path: {full_path}")

            icon.addPixmap(QtGui.QPixmap(full_path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.parent.pushButton_takeover.setIcon(icon)
            self.parent.pushButton_takeover.setIconSize(QtCore.QSize(38, 38))

            log("DEBUG", "按钮图标已成功更新")
            log_print("[AiAssistant] Button icon updated successfully")

        except Exception as e:
            log("ERROR", f"更新按钮图标时出错: {str(e)}")
            log_print(f"[AiAssistant] Error updating button icon: {str(e)}")
