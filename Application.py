import sys
from PyQt6 import QtWidgets, QtCore

from MainWindow import MainWindow

"""
pyinstaller Application.spec
"""


def main():
    app = QtWidgets.QApplication(sys.argv)
    shared_memory = QtCore.QSharedMemory("LeafAuto_Server")

    if shared_memory.attach():
        print("应用程序已在运行中...")
        sys.exit()

    if not shared_memory.create(1):
        print("无法创建共享内存，应用程序可能已在运行...")
        sys.exit()

    window = MainWindow()
    window.setWindowTitle("枫叶信息自动化")

    window_center(window)
    window.show()

    sys.exit(app.exec())


def window_center(window):
    frame_geometry = window.frameGeometry()
    center_point = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
    frame_geometry.moveCenter(center_point)
    window.move(frame_geometry.topLeft())


if __name__ == '__main__':
    main()
