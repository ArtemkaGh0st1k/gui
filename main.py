from PyQt5.QtWidgets import QApplication
import sys
from lab1.main_molule import ImageApp



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    sys.exit(app.exec_())