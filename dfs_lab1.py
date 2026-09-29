import sys
from PyQt5.QtWidgets import QApplication

from main_window import DFSVisualization


def main():
    app = QApplication(sys.argv)
    window = DFSVisualization()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()