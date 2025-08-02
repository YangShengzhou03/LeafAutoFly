import random
from datetime import timedelta

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QRegularExpression, QUrl
from PyQt6.QtGui import QRegularExpressionValidator, QDesktopServices

from System_info import get_motherboard_serial_number, write_key_value, read_key_value
from Ui_Activities import Ui_ActivitiesWindow
from common import get_resource_path, get_current_time, get_url, log, log_print


class ActivitiesWindow(QtWidgets.QMainWindow, Ui_ActivitiesWindow):
    def __init__(self):
        super().__init__()
        log("DEBUG", "初始化ActivitiesWindow窗口")
        log_print("[ACTIVITY] Initializing ActivitiesWindow")
        self.ui = Ui_ActivitiesWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("激活专业版")
        self.setWindowIcon(QtGui.QIcon(get_resource_path('resources/img/tray.ico')))
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.identify = random.randint(100000, 999999)
        self.current_selected_button = None
        self.connect_signals()
        self.year_vip()

    def connect_signals(self):
        log("DEBUG", "连接UI信号")
        log_print("[ACTIVITY] Connecting UI signals")
        self.ui.pushButton_close.clicked.connect(self.close)
        self.ui.pushButton_year.clicked.connect(self.year_vip)
        self.ui.pushButton_VIP.clicked.connect(self.super_vip)
        self.ui.pushButton_AiVIP.clicked.connect(self.ai_vip)
        self.ui.pushButton_Base.clicked.connect(self.base_vip)
        reg_exp = QRegularExpression(r'^[A-Za-z0-9]{0,12}$')
        validator = QRegularExpressionValidator(reg_exp, self.ui.lineEdit_code)
        self.ui.lineEdit_code.setValidator(validator)
        self.ui.lineEdit_code.returnPressed.connect(self.validate_activation)
        self.ui.pushButton_OK.clicked.connect(self.validate_activation)
        self.ui.lineEdit_code.textChanged.connect(lambda text: self.ui.lineEdit_code.setText(text.upper()))
        self.ui.label_identify.setText(str(self.identify))
        self.ui.pushButton_exchange.clicked.connect(self.QQ_code)
        self.ui.pushButton_check.clicked.connect(self.QQ_code)
        self.ui.pushButton_feedback.clicked.connect(self.help)
        self.ui.pushButton_privilege.clicked.connect(self.help)
        self.apply_default_styles()
        log("DEBUG", "UI信号连接成功")
        log_print("[ACTIVITY] UI signals signals connected successfully")

    def QQ_code(self):
        log("DEBUG", "显示QQ二维码")
        log_print("[ACTIVITY] Displaying QQ code")
        try:
            icon = QtGui.QIcon()
            qq_code_path = get_resource_path('resources/img/activity/QQ_Act.png')
            icon.addPixmap(QtGui.QPixmap(qq_code_path), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.pushButton_Wechat.setIcon(icon)
            self.apply_default_styles()
            log("DEBUG", f"QQ二维码图片加载路径: {qq_code_path}")
            log_print(f"[ACTIVITY] QQ code image loaded from: {qq_code_path}")
        except Exception as e:
            log("ERROR", f"显示QQ二维码失败: {str(e)}")
            log_print(f"[ACTIVITY] Failed to display QQ code: {str(e)}")

    def apply_default_styles(self):
        log("DEBUG", "应用默认按钮样式")
        log_print("[ACTIVITY] Applying default button styles")
        style = """
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
    background: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 153, 170, 88));
    transition: background 0.2s ease-in-out;
}
QPushButton:pressed {
    border: 2px solid rgba(254, 81, 111, 255);
    background: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 153, 170, 88));
    transition: background 0.1s ease-in-out;
}
"""
        for button in [self.ui.pushButton_VIP, self.ui.pushButton_year, self.ui.pushButton_AiVIP,
                       self.ui.pushButton_Base]:
            button.setStyleSheet(style)

    def update_button_style(self, button):
        log("DEBUG", f"更新按钮样式: {button.objectName()}")
        log_print(f"[ACTIVITY] Updating style for {button.objectName()}")
        self.apply_default_styles()
        button.setStyleSheet(self.active_style())
        self.current_selected_button = button

    def active_style(self):
        log("DEBUG", "生成激活状态按钮样式")
        log_print("[ACTIVITY] Generating active button style")
        return """
QPushButton {
    margin-right: 3px;
    margin-bottom: 0px;
    color: rgb(255, 255, 255);
    border: 2px solid rgba(254, 81, 111, 120);
    border-radius: 8px;
    background: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 153, 170, 88));
    font-weight: bold;
    padding: 8px;
}
QPushButton:hover {
    border: 2px solid rgba(254, 81, 111, 120);
    background: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 153, 170, 88));
    transition: background 0.2s ease-in-out;
}
QPushButton:pressed {
    border: 2px solid rgba(254, 81, 111, 255);
    background: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0,
        stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 153, 170, 88));
    transition: background 0.1s ease-in-out;
}
"""

    def super_vip(self):
        log("DEBUG", "选择超级VIP会员")
        log_print("[ACTIVITY] Super VIP selected")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_resource_path('resources/img/activity/wp36.9.png')), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.pushButton_Wechat.setIcon(icon)
        self.update_button_style(self.ui.pushButton_VIP)
        self.ui.label_prices.setText("36.90")
        self.ui.label_prices_2.setText("36.9")

    def year_vip(self):
        log("DEBUG", "选择年度VIP会员")
        log_print("[ACTIVITY] Year VIP selected")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_resource_path('resources/img/activity/wp199.png')), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.pushButton_Wechat.setIcon(icon)
        self.update_button_style(self.ui.pushButton_year)
        self.ui.label_prices.setText("199.00")
        self.ui.label_prices_2.setText("199")

    def ai_vip(self):
        log("DEBUG", "选择AI VIP会员")
        log_print("[ACTIVITY] AI VIP selected")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_resource_path('resources/img/activity/wp29.9.png')), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.pushButton_Wechat.setIcon(icon)
        self.update_button_style(self.ui.pushButton_AiVIP)
        self.ui.label_prices.setText("29.90")
        self.ui.label_prices_2.setText("29.9")

    def base_vip(self):
        log("DEBUG", "选择基础VIP会员")
        log_print("[ACTIVITY] Base VIP selected")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_resource_path('resources/img/activity/wp19.9.png')), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.ui.pushButton_Wechat.setIcon(icon)
        self.update_button_style(self.ui.pushButton_Base)
        self.ui.label_prices.setText("19.90")
        self.ui.label_prices_2.setText("19.9")

    def validate_activation(self):
        log("DEBUG", "验证激活码")
        log_print("[ACTIVITY] Validating activation code")
        try:
            Key_value, _ = get_url()
            log("DEBUG", "成功获取密钥值")
        except Exception as e:
            log("ERROR", f"获取密钥值失败: {e}")
            log_print(f"[ACTIVITY] Failed to fetch key value: {e}")
            Key_value = None

        input_password = self.ui.lineEdit_code.text()
        random_number = self.identify

        hex_base = hex(random_number + 1)[2:].upper()
        hex_ai_vip = hex(random_number + 2)[2:].upper()
        hex_vip = hex(random_number + 3)[2:].upper()
        hex_year_vip = hex(random_number + 4)[2:].upper()

        try:
            last_time = get_current_time('net')
            log("DEBUG", "使用网络时间验证激活")
        except:
            last_time = get_current_time('local')
            log("WARNING", "网络时间获取失败，使用本地时间验证激活")

        if input_password == hex_base:
            membership = 'Base'
            expiration_time = (last_time + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        elif input_password == hex_ai_vip:
            membership = 'AiVIP'
            expiration_time = (last_time + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        elif input_password == hex_vip:
            membership = 'VIP'
            expiration_time = (last_time + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        elif input_password == hex_year_vip:
            membership = 'VIP'
            expiration_time = (last_time + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        elif Key_value is not None and input_password == Key_value:
            membership = 'VIP'
            expiration_time = (last_time + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            log("WARNING", "激活码无效")
            log_print("[ACTIVITY] Invalid activation code")
            QtWidgets.QMessageBox.warning(self, "无效秘钥", "请输入正确的秘钥，如已购买请QQ扫码获取")
            return

        try:
            motherboard_sn = get_motherboard_serial_number()
            log("DEBUG", f"获取主板序列号: {motherboard_sn}")
        except:
            motherboard_sn = "UNKNOWN"
            log("WARNING", "无法获取主板序列号，使用默认值")

        try:
            write_key_value('membership', membership)
            write_key_value('expiration_time', expiration_time)
            write_key_value('motherboardsn', motherboard_sn)
            log("DEBUG", "会员信息写入成功")
        except Exception as e:
            log("ERROR", f"写入激活信息失败: {e}")
            log_print(f"[ACTIVITY] Failed to write activation info: {e}")

        try:
            if read_key_value('membership') != membership or read_key_value(
                    'expiration_time') != expiration_time or read_key_value('motherboardsn') != motherboard_sn:
                log("ERROR", "激活信息验证失败")
                QtWidgets.QMessageBox.critical(self, "激活失败", "激活出错,请以管理员身份运行软件")
            else:
                log("INFO", f"激活成功，有效期至 {expiration_time}")
                log_print(f"[ACTIVITY] Activation successful, expires on {expiration_time}")
                QtWidgets.QMessageBox.information(self, "激活成功", f"会员激活成功,有效期至{expiration_time}")
                QtWidgets.QApplication.quit()
        except Exception as e:
            log("ERROR", f"激活验证失败: {e}")
            log_print(f"[ACTIVITY] Activation verification failed: {e}")
            QtWidgets.QMessageBox.critical(self, "激活失败", "激活出错,请以管理员身份运行软件")

    def help(self):
        log("DEBUG", "打开帮助页面")
        log_print("[ACTIVITY] Opening help URL")
        QDesktopServices.openUrl(QUrl('https://blog.csdn.net/Yang_shengzhou/article/details/143782041'))
