import sys
import traceback
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

from MainWindow import MainWindow
from common import log_print

"""
pyinstaller Application.spec
"""


def main():
    server = QLocalServer()
    socket_name = "LeafAuto_Server_Socket"

    client_socket = QLocalSocket()
    client_socket.connectToServer(socket_name)

    if client_socket.waitForConnected(500):
        client_socket.write(b"bring_to_front")
        client_socket.waitForBytesWritten()
        client_socket.disconnectFromServer()
        log_print("The application is already running. Bringing existing window to front.")
        return 1

    QLocalServer.removeServer(socket_name)
    if not server.listen(socket_name):
        log_print(f"Failed to start local server: {server.errorString()}")
        return 1

    server.newConnection.connect(lambda: handle_incoming_connection(server, socket_name))

    shared_memory = QtCore.QSharedMemory("LeafAuto_Server")
    if shared_memory.attach():
        log_print("The application is already running.")
        return 1

    if not shared_memory.create(1):
        log_print("Failed to create shared memory. The application may already be running.")
        return 1

    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName("LeafAuto")
    app.setOrganizationName("LeafAuto")

    window = MainWindow()
    window.setWindowTitle("LeafAuto")

    if hasattr(window, 'centerOnScreen'):
        window.centerOnScreen()

    window.show()

    exit_code = app.exec()

    server.close()
    QLocalServer.removeServer(socket_name)
    shared_memory.detach()

    return exit_code


def handle_incoming_connection(server, socket_name):
    socket = server.nextPendingConnection()

    if socket.waitForReadyRead(1000):
        message = socket.readAll().data().decode('utf-8')
        if message == "bring_to_front":
            for widget in QtWidgets.QApplication.topLevelWidgets():
                if isinstance(widget, QtWidgets.QMainWindow) and widget.windowTitle() == "LeafAuto":
                    if widget.windowState() & QtCore.Qt.WindowState.WindowMinimized:
                        widget.setWindowState(
                            widget.windowState() & ~QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowActive)

                    widget.activateWindow()
                    widget.raise_()
                    break

    socket.disconnectFromServer()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        original_stderr = sys.__stderr__
        original_stderr.write(f"Fatal error: {str(e)}\n")
        original_stderr.write(traceback.format_exc())
        sys.exit(1)
