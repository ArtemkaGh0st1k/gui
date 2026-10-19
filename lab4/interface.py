import os 
from PyQt5.QtCore import QObject, QTimer, QMetaObject, Q_ARG, pyqtSlot, QVariant
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

class Interface(QObject):
    def __init__(self, engine = None):

        super().__init__()
        self.engine = engine if engine else QQmlApplicationEngine()

        # создаем таймер для автосохранения
        self.timer = QTimer(self)
        self.timer.setInterval(5000) # сохранения каждые 5 секунд
        self.timer.timeout.connect(self.autosave)
        self.timer.start()


    @pyqtSlot()
    def autosave(self):
        """Слот, вызываемый по таймеру для автосохранения canvas"""

        root_objects = self.engine.rootObjects()
        if not root_objects:
            print("Ошибка: Не удалось получить корневой объект QML!")
            return

        root_object = root_objects[0]
        # находим объект canvas
        canvas = root_object.findChild(QObject, "canvas")

        if canvas:
            save_path = "lab4/saved_canvas.png"

            QMetaObject.invokeMethod(
                canvas,
                "saveCanvas",
                Q_ARG(QVariant, save_path)
            )

            print(f"[Backend] автосохраение выполнено: {save_path}")

        else:
            print("Ошибка: Не удалось найти объект canvas в QML!")


    def cleanup_environment(self):
        """Слот, вызываемый прямо перед завершением работы PyQt"""
        os.environ.pop("QML2_IMPORT_PATH", None)
        os.environ.pop("QT_PLUGIN_PATH", None)
        print("[System] Переменные окружения успешно очищены!")