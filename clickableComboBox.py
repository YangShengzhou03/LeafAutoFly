from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from common import log, log_print


class clickableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        log_print("[CheckableComboBox] Initializing CheckableComboBox...")

        # 修正QSizePolicy枚举值的使用方式
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(88, 0))
        self.setMaximumSize(QtCore.QSize(88, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.setFont(font)
        self.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid rgb(87, 78, 209);
                border-radius: 2px;
                color: rgb(0, 0, 0);
                font-size: 15px;
                text-align: center;
                padding: 0px;
            }

            QComboBox:hover {
                background-color: rgba(229, 228, 253, 0.2);
            }

            QComboBox:focus {
                border-color: rgb(35, 26, 132);
            }

            QComboBox::drop-down {
                width: 0px;
                border: none;
            }

            QComboBox::down-arrow {
                image: none;
            }

            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 1px solid rgb(87, 78, 209);
                border-radius: 4px;
                color: rgb(0, 0, 0);
                font-size: 15px;
                padding: 0px;
                selection-background-color: rgb(229, 228, 253);
                selection-color: rgb(0, 0, 0);
            }
        """)
        self.view = QtWidgets.QListWidget()
        self.setModel(self.view.model())
        self.setView(self.view)
        self.view.itemChanged.connect(self._on_item_changed)
        self.view.viewport().installEventFilter(self)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # 修正对齐方式的引用 - 使用完整的枚举路径
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().installEventFilter(self)
        self._weekday_items = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        self._once_item_text = "仅一次"
        self._once_item_index = -1
        self._updating = False
        self._first_show = True

        log_print("[CheckableComboBox] Initialization completed")

    def eventFilter(self, obj, event):
        try:
            if obj == self.view.viewport() and event.type() == QtCore.QEvent.Type.MouseButtonRelease:
                index = self.view.indexAt(event.pos())
                if index.isValid():
                    item = self.view.itemFromIndex(index)
                    prev_state = item.checkState()
                    item.setCheckState(
                        Qt.CheckState.Checked if prev_state == Qt.CheckState.Unchecked else Qt.CheckState.Unchecked)
                    log_print(f"[CheckableComboBox] Item toggled: {item.text()} to {item.checkState()}")
                    return True
            elif obj == self.lineEdit() and event.type() == QtCore.QEvent.Type.MouseButtonPress:
                log_print("[CheckableComboBox] Line edit clicked, showing popup")
                self.showPopup()
                return True
            return super().eventFilter(obj, event)
        except Exception as e:
            log_print(f"[CheckableComboBox] Error in event filter: {str(e)}")
            log("ERROR", "组合框事件处理出错")
            return False

    def showPopup(self):
        try:
            log_print("[CheckableComboBox] Showing popup")
            if self._first_show and self._once_item_index >= 0:
                log_print("[CheckableComboBox] First show, initializing '仅一次' as checked")
                self._first_show = False
                self._updating = True
                once_item = self.view.item(self._once_item_index)
                once_item.setCheckState(Qt.CheckState.Checked)
                self._clear_weekday_checks()
                self._updating = False
                self.update_text()
            super().showPopup()
        except Exception as e:
            log_print(f"[CheckableComboBox] Error showing popup: {str(e)}")
            log("ERROR", "显示组合框下拉列表失败")

    def _on_item_changed(self, item):
        try:
            if not item or self._updating:
                return

            log_print(f"[CheckableComboBox] Item changed: {item.text()}, state: {item.checkState()}")
            self._updating = True

            is_once_item = item.text() == self._once_item_text
            is_weekday_item = item.text() in self._weekday_items

            if is_once_item and item.checkState() == Qt.CheckState.Checked:
                log_print("[CheckableComboBox] '仅一次' checked, clearing weekday checks")
                self._clear_weekday_checks()
            elif is_weekday_item and item.checkState() == Qt.CheckState.Checked:
                log_print("[CheckableComboBox] Weekday checked, clearing '仅一次' check")
                self._clear_once_check()

            self._updating = False
            self.update_text()
        except Exception as e:
            log_print(f"[CheckableComboBox] Error in item change handler: {str(e)}")
            log("ERROR", "处理组合框选项变更失败")
            self._updating = False

    def _clear_weekday_checks(self):
        try:
            log_print("[CheckableComboBox] Clearing weekday checks")
            for i in range(self.view.count()):
                list_item = self.view.item(i)
                if list_item.text() in self._weekday_items:
                    list_item.setCheckState(Qt.CheckState.Unchecked)
        except Exception as e:
            log_print(f"[CheckableComboBox] Error clearing weekday checks: {str(e)}")

    def _clear_once_check(self):
        try:
            if self._once_item_index >= 0 and self._once_item_index < self.view.count():
                once_item = self.view.item(self._once_item_index)
                once_item.setCheckState(Qt.CheckState.Unchecked)
                log_print("[CheckableComboBox] Cleared '仅一次' check")
        except Exception as e:
            log_print(f"[CheckableComboBox] Error clearing '仅一次' check: {str(e)}")

    def add_item(self, text, checked=False):
        try:
            log_print(f"[CheckableComboBox] Adding item: {text}, checked: {checked}")
            item = QtWidgets.QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
            self.view.addItem(item)

            if text == self._once_item_text:
                self._once_item_index = self.view.count() - 1
                log_print(f"[CheckableComboBox] '仅一次' item index set to {self._once_item_index}")
        except Exception as e:
            log_print(f"[CheckableComboBox] Error adding item: {str(e)}")
            log("ERROR", f"添加组合框选项 '{text}' 失败")

    def update_text(self):
        try:
            checked_items = self.get_checked_items()
            log_print(f"[CheckableComboBox] Updating text with checked items: {checked_items}")

            if not checked_items:
                self.setEditText("未选择")
            elif checked_items == [self._once_item_text]:
                self.setEditText("仅一次")
            elif all(item in self._weekday_items for item in checked_items):
                self.setEditText("自定义")
            else:
                self.setEditText(", ".join(checked_items))
        except Exception as e:
            log_print(f"[CheckableComboBox] Error updating text: {str(e)}")
            log("ERROR", "更新组合框显示文本失败")

    def get_checked_items(self):
        try:
            checked_items = []
            for i in range(self.view.count()):
                item = self.view.item(i)
                if item.checkState() == Qt.CheckState.Checked:
                    checked_items.append(item.text())
            log_print(f"[CheckableComboBox] Retrieved checked items: {checked_items}")
            return checked_items
        except Exception as e:
            log_print(f"[CheckableComboBox] Error getting checked items: {str(e)}")
            log("ERROR", "获取选中的组合框选项失败")
            return []

    def clear_items(self):
        try:
            log_print("[CheckableComboBox] Clearing all items")
            self.view.clear()
            self._once_item_index = -1
            self._first_show = True
            self.update_text()
        except Exception as e:
            log_print(f"[CheckableComboBox] Error clearing items: {str(e)}")
            log("ERROR", "清空组合框选项失败")

    def set_checked_items(self, items):
        try:
            log_print(f"[CheckableComboBox] Setting checked items: {items}")
            self._updating = True

            for i in range(self.view.count()):
                item = self.view.item(i)
                item.setCheckState(Qt.CheckState.Unchecked)

            if self._once_item_text in items:
                for i in range(self.view.count()):
                    item = self.view.item(i)
                    if item.text() == self._once_item_text:
                        item.setCheckState(Qt.CheckState.Checked)
                        break
            else:
                for i in range(self.view.count()):
                    item = self.view.item(i)
                    if item.text() in items:
                        item.setCheckState(Qt.CheckState.Checked)

            if items:
                self._first_show = False

            self._updating = False
            self.update_text()
        except Exception as e:
            log_print(f"[CheckableComboBox] Error setting checked items: {str(e)}")
            log("ERROR", "设置组合框选中项失败")
            self._updating = False

    def get_checked_weekdays(self):
        try:
            checked = self.get_checked_items()
            weekdays = [day for day in checked if day != self._once_item_text]
            result = "，".join(weekdays)
            log_print(f"[CheckableComboBox] Retrieved checked weekdays: {result}")
            return result
        except Exception as e:
            log_print(f"[CheckableComboBox] Error getting checked weekdays: {str(e)}")
            log("ERROR", "获取选中的工作日失败")
            return ""
