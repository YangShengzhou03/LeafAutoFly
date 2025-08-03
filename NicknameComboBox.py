from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QFont, QStandardItemModel, QStandardItem

from common import log, log_print


class CenterAlignedDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class NicknameComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        log_print("[NicknameComboBox] 初始化账号昵称选择下拉列表...")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.setSizePolicy(sizePolicy)

        font = QFont()
        font.setFamily("微软雅黑, sans-serif")
        font.setPointSize(12)
        self.setFont(font)

        self.setMinimumSize(QtCore.QSize(120, 30))
        self.setMaximumSize(QtCore.QSize(200, 30))

        self.view = QtWidgets.QListView()
        self.view.setSpacing(1)
        self.view.setAlternatingRowColors(False)
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.view.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.view.setItemDelegate(CenterAlignedDelegate())

        self.view.setStyleSheet("""
            QListView {
                border-radius: 8px;
                padding: 4px 0;
                outline: none;
            }
        """)

        self.setModel(QStandardItemModel(self))
        self.setView(self.view)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().setStyleSheet("""
            border: none; 
            background: transparent;
            text-align: center;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
            color: white;
            padding: 0 4px;
        """)

        self.lineEdit().installEventFilter(self)
        self.view.viewport().installEventFilter(self)

        self._current_nickname = None
        self._is_open = False
        self._init_styles()

        log_print("[NicknameComboBox] 初始化完成")

    def _init_styles(self):
        self.setStyleSheet("""
            QComboBox {
                background: transparent;
                border: 1px solid transparent;
                color: white;
                padding: 6px 12px;
                padding-right: 30px;
                border-radius: 8px;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            }

            QComboBox:hover {
                background: transparent;
                border-color: rgba(255, 255, 255, 40);
            }

            QComboBox:focus {
                background: transparent;
                border-color: #7B61FF;
                outline: none;
                box-shadow: 0 0 0 2px rgba(123, 97, 255, 30);
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                height: 28px;
                border: none;
                background: transparent;
                border-radius: 0px;
                margin-right: 2px;
            }

            QComboBox::drop-down:hover {
                background: transparent;
            }

            QComboBox::down-arrow {
                image: url("resources/img/List/下拉.svg");
                width: 24px;
                height: 24px;
                opacity: 0.9;
                transition: transform 0.2s ease;
            }

            QComboBox::down-arrow:hover {
                opacity: 1;
            }

            QComboBox::down-arrow:pressed {
                transform: translateY(1px);
            }

            QComboBox QAbstractItemView {
                border-radius: 0;
                background: white;
                border: 0;
                padding: 0px;          /* 视图内边距归零 */
                margin: 0px;           /* 视图外边距归零 */
                color: #333;
                outline: none;
                show-decoration-selected: 0;
            }

            QComboBox QAbstractItemView::item {
                height: 26px;
                padding: 0px;
                margin: 0px;
                border-radius: 0;
                transition: all 0.2s ease;
                border: none;
            }

            QComboBox QAbstractItemView::item:hover {
                background: #F0F5FF;
                color: #7B61FF;
            }

            QComboBox QAbstractItemView::item:selected {
                background: #7B61FF;
                color: white;
                border-radius: 0;
            }

            QComboBox QAbstractItemView::item:selected:hover {
                background: #6A50E0;
            }

            QComboBox:disabled {
                background: rgba(255, 255, 255, 5);
                color: #AAAAAA;
                border-color: transparent;
            }

            QComboBox:disabled QComboBox::down-arrow {
                opacity: 0.4;
            }
        """)

    def eventFilter(self, obj, event):
        try:
            if obj == self.lineEdit() and event.type() == QEvent.Type.MouseButtonRelease:
                self.showPopup()
                return True

            if obj == self.view.viewport() and event.type() == QEvent.Type.MouseButtonRelease:
                index = self.view.indexAt(event.pos())
                if index.isValid():
                    nickname = index.data()
                    self._current_nickname = nickname
                    self.setEditText(nickname)
                    log_print(f"[NicknameComboBox] 选择昵称: {nickname}")
                    self.hidePopup()
                    return True

            return super().eventFilter(obj, event)

        except Exception as e:
            log_print(f"[NicknameComboBox] 事件过滤器错误: {str(e)}")
            return False

    def showPopup(self):
        if self._is_open:
            return

        self._is_open = True
        self.view.setMinimumWidth(self.width())
        super().showPopup()

    def hidePopup(self):
        if not self._is_open:
            return

        self._is_open = False
        super().hidePopup()

    def add_nickname(self, nickname, icon=None):
        try:
            log_print(f"[NicknameComboBox] 添加昵称: {nickname}")
            model = self.model()

            if icon:
                item = QStandardItem(icon, nickname)
            else:
                item = QStandardItem(nickname)

            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            model.appendRow(item)

            if self.count() == 1:
                self.setCurrentIndex(0)
                self._current_nickname = nickname
                self.setEditText(nickname)

        except Exception as e:
            log_print(f"[NicknameComboBox] 添加昵称错误: {str(e)}")

    def get_current_nickname(self):
        return self._current_nickname

    def set_current_nickname(self, nickname):
        index = self.findText(nickname)
        if index >= 0:
            self.setCurrentIndex(index)
            self._current_nickname = nickname
            self.setEditText(nickname)
            log_print(f"[NicknameComboBox] 设置当前昵称: {nickname}")
        else:
            log_print(f"[NicknameComboBox] 昵称 '{nickname}' 不存在")

    def clear_nicknames(self):
        self.clear()
        self._current_nickname = None
        self.setEditText("")
