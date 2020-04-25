
from PyQt5.QtWidgets import QApplication
from movement_monitor.viewmodels.MainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    pass
