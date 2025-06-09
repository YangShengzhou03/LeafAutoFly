import random
from datetime import timedelta
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QRegularExpression, QUrl
from PyQt6.QtGui import QRegularExpressionValidator, QDesktopServices

from System_info import get_motherboard_serial_number, write_key_value, read_key_value
from Ui_Activities import Ui_ActivitiesWindow
from common import get_resource_path, get_current_time, get_url


class ActivitiesWindow(QtWidgets.QMainWindow, Ui_ActivitiesWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ActivitiesWindow()
        self.ui.setupUi(self)
        self._setup_window()
        self._setup_validator()
        self._setup_buttons()
        self._setup_connections()
        self._init_membership_data()

    def _setup_window(self):
        """设置窗口基本属性"""
        self.setWindowTitle("激活枫叶")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/tray.ico')))
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.center_on_screen()

    def center_on_screen(self):
        """将窗口居中显示在屏幕上"""
        frame_geometry = self.frameGeometry()
        center_point = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def _setup_validator(self):
        """设置激活码输入验证"""
        reg_exp = QRegularExpression(r'^[A-Za-z0-9]{0,12}$')
        validator = QRegularExpressionValidator(reg_exp, self.ui.lineEdit_code)
        self.ui.lineEdit_code.setValidator(validator)
        self.ui.lineEdit_code.textChanged.connect(lambda text: self.ui.lineEdit_code.setText(text.upper()))

    def _setup_buttons(self):
        """初始化按钮样式和数据"""
        self.identify = random.randint(100000, 999999)
        self.ui.label_identify.setText(str(self.identify))
        self.current_selected_button = None

        # 会员类型数据
        self.membership_data = {
            'base': {
                'button': self.ui.pushButton_Base,
                'price': '9.90',
                'image': 'resources/img/activity/wp9.9.jpg',
                'days': 30,
                'level': 'Base'
            },
            'ai': {
                'button': self.ui.pushButton_AiVIP,
                'price': '17.90',
                'image': 'resources/img/activity/wp17.9.jpg',
                'days': 30,
                'level': 'AiVIP'
            },
            'vip': {
                'button': self.ui.pushButton_VIP,
                'price': '18.90',
                'image': 'resources/img/activity/wp18.9.jpg',
                'days': 30,
                'level': 'VIP'
            },
            'year': {
                'button': self.ui.pushButton_year,
                'price': '99.00',
                'image': 'resources/img/activity/wp99.jpg',
                'days': 365,
                'level': 'VIP'
            }
        }

        self.apply_default_styles()

    def _setup_connections(self):
        """连接信号与槽"""
        self.ui.pushButton_close.clicked.connect(self.close)
        self.ui.pushButton_OK.clicked.connect(self.validate_activation)
        self.ui.lineEdit_code.returnPressed.connect(self.validate_activation)

        # 会员按钮连接
        self.ui.pushButton_Base.clicked.connect(lambda: self.select_membership('base'))
        self.ui.pushButton_AiVIP.clicked.connect(lambda: self.select_membership('ai'))
        self.ui.pushButton_VIP.clicked.connect(lambda: self.select_membership('vip'))
        self.ui.pushButton_year.clicked.connect(lambda: self.select_membership('year'))

        # 辅助按钮连接
        self.ui.pushButton_exchange.clicked.connect(self.QQ_code)
        self.ui.pushButton_check.clicked.connect(self.QQ_code)
        self.ui.pushButton_feedback.clicked.connect(self.QQ_code)
        self.ui.pushButton_privilege.clicked.connect(self.help)

    def _init_membership_data(self):
        """初始化选择第一个会员类型"""
        self.select_membership('year')

    def apply_default_styles(self):
        """应用默认按钮样式"""
        default_style = """
QPushButton {
    margin-right: 3px;
    margin-bottom: 0px;
    color: rgb(255, 255, 255);
    border: 2px solid rgba(120, 120, 120, 60);
    border-radius: 8px;
    background: none;
    font-weight: bold;
    padding: 8px;
}

QPushButton:hover {
    border: 2px solid rgba(254, 81, 111, 120);
    background: qlineargradient(
        spread:pad,
        x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0),
        stop:1 rgba(255, 153, 170, 88)
    );
    transition: background 0.2s ease-in-out;
}

QPushButton:pressed {
    border: 2px solid rgba(254, 81, 111, 255);
    background: qlineargradient(
        spread:pad,
        x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0),
        stop:1 rgba(255, 153, 170, 88)
    );
    transition: background 0.1s ease-in-out;
}
"""
        for data in self.membership_data.values():
            data['button'].setStyleSheet(default_style)

    def update_button_style(self, button):
        """更新选中按钮样式"""
        active_style = """
QPushButton {
    margin-right: 3px;
    margin-bottom: 0px;
    color: rgb(255, 255, 255);
    border: 2px solid rgba(254, 81, 111, 120);
    border-radius: 8px;
    background: qlineargradient(
        spread:pad,
        x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0),
        stop:1 rgba(255, 153, 170, 88)
    );
    font-weight: bold;
    padding: 8px;
}

QPushButton:hover {
    border: 2px solid rgba(254, 81, 111, 120);
    background: qlineargradient(
        spread:pad,
        x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0),
        stop:1 rgba(255, 153, 170, 88)
    );
    transition: background 0.2s ease-in-out;
}

QPushButton:pressed {
    border: 2px solid rgba(254, 81, 111, 255);
    background: qlineargradient(
        spread:pad,
        x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0),
        stop:1 rgba(255, 153, 170, 88)
    );
    transition: background 0.1s ease-in-out;
}
"""
        self.apply_default_styles()
        button.setStyleSheet(active_style)
        self.current_selected_button = button

    def select_membership(self, membership_type):
        """选择会员类型"""
        data = self.membership_data[membership_type]

        # 更新按钮样式
        self.update_button_style(data['button'])

        # 更新价格标签
        self.ui.label_prices.setText(data['price'])
        self.ui.label_prices_2.setText(data['price'].rstrip('0').rstrip('.'))

        # 更新支付二维码图片
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(get_resource_path(data['image'])),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off
        )
        self.ui.pushButton_Wechat.setIcon(icon)

    def QQ_code(self):
        """显示QQ二维码"""
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(get_resource_path('resources/img/activity/QQ_Act.png')),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off
        )
        self.ui.pushButton_Wechat.setIcon(icon)
        self.apply_default_styles()

    def validate_activation(self):
        """验证激活码"""
        try:
            key_value, _ = get_url()
        except Exception:
            key_value = None

        input_password = self.ui.lineEdit_code.text()
        random_number = self.identify

        # 生成预设激活码
        activation_codes = {
            hex(random_number + 1)[2:].upper(): ('Base', 30),
            hex(random_number + 2)[2:].upper(): ('AiVIP', 30),
            hex(random_number + 3)[2:].upper(): ('VIP', 30),
            hex(random_number + 4)[2:].upper(): ('VIP', 365)
        }

        last_time = get_current_time('net')

        # 检查预设激活码
        if input_password in activation_codes:
            membership, days = activation_codes[input_password]
            expiration_time = (last_time + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        # 检查网络密钥
        elif key_value is not None and input_password == key_value:
            membership = 'VIP'
            expiration_time = (last_time + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            QtWidgets.QMessageBox.warning(self, "无效秘钥", "请输入正确的秘钥，如已购买请QQ扫码获取")
            return

        # 保存激活信息
        motherboard_sn = get_motherboard_serial_number()
        write_key_value('membership', membership)
        write_key_value('expiration_time', expiration_time)
        write_key_value('motherboardsn', motherboard_sn)

        # 验证保存结果
        if (read_key_value('membership') != membership or
                read_key_value('expiration_time') != expiration_time or
                read_key_value('motherboardsn') != motherboard_sn):
            QtWidgets.QMessageBox.critical(self, "激活失败", "激活出错,请以管理员身份运行软件")
        else:
            QtWidgets.QMessageBox.information(self, "激活成功", f"会员激活成功,有效期至{expiration_time}")
            QtWidgets.QApplication.quit()

    def help(self):
        """打开帮助链接"""
        QDesktopServices.openUrl(QUrl('https://blog.csdn.net/Yang_shengzhou/article/details/143782041'))
