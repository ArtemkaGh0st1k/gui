import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl

from lab1.main_molule import ImageApp
from lab2.currency_converter import CurrencyConverter
from lab3.db_window import DbWindow
from lab4.interface import Interface


class LabRunner():
    def __init__(self):
        pass

    def start_1_lab(self):
        app = QApplication(sys.argv)
        ex = ImageApp()
        ex.show()
        sys.exit(app.exec_())


    def start_2_lab(self):
        app = QApplication(sys.argv)
        window = CurrencyConverter()
        window.show()

    def start_3_lab(self):
        app = QApplication(sys.argv)
        window = DbWindow()
        window.show()
        sys.exit(app.exec_())


    def start_4_lab(self):
        app = QApplication(sys.argv)

        #qml_dir = "lab4/resources/template"
        engine = QQmlApplicationEngine()
        #engine.addImportPath(qml_dir)

        interface = Interface(engine)

        app.aboutToQuit.connect(interface.cleanup_environment)

        engine.rootContext().setContextProperty("_backend", interface)

        engine.load(QUrl.fromLocalFile("lab4/resources/template/mainWindow.qml"))

        if not engine.rootObjects():
            print("Ошибка: Не удалось загрузить QML файл!")
            sys.exit(-1)

        sys.exit(app.exec_())
