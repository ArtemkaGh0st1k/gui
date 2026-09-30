from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit
)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        # курсы валют относительно USD
        self.rate_usd_to_rub = 90.
        self.rate_usd_to_eur = 0.92

        self.initUI()


    def initUI(self):

        self.setWindowTitle("Лаб 2 | Конвертер валют")
        self.setGeometry(100, 100, 350, 200)

        main_layout = QVBoxLayout()

        validator = QDoubleValidator(0.0, 10000000.0, 2)    # проверка - числа только с плав точкой
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        # поле USD
        usd_layout = QHBoxLayout()
        usd_label = QLabel("USD:")
        self.usd_input = QLineEdit()
        self.usd_input.setValidator(validator)
        self.usd_input.setPlaceholderText('0.00')
        usd_layout.addWidget(usd_label)
        usd_layout.addWidget(self.usd_input)

        # поле RUB
        rub_layout = QHBoxLayout()
        rub_label = QLabel("RUB:")
        self.rub_input = QLineEdit()
        self.rub_input.setValidator(validator)
        self.rub_input.setPlaceholderText('0.00')
        rub_layout.addWidget(rub_label)
        rub_layout.addWidget(self.rub_input)

        # поле EUR
        eur_layout = QHBoxLayout()
        eur_label = QLabel('EUR (€):')
        self.eur_input = QLineEdit()
        self.eur_input.setValidator(validator)
        self.eur_input.setPlaceholderText('0.00')
        eur_layout.addWidget(eur_label)
        eur_layout.addWidget(self.eur_input)

        # добавляем все строки в основной слой
        main_layout.addLayout(usd_layout)
        main_layout.addLayout(rub_layout)
        main_layout.addLayout(eur_layout)

        self.setLayout(main_layout)

        # подключаем сигнал textChanged к обработчикам
        self.usd_input.textChanged.connect(self.on_usd_changed)
        self.rub_input.textChanged.connect(self.on_rub_changed)
        self.eur_input.textChanged.connect(self.on_eur_changed)


    def parse_value(self, text : str):
        """Вспомогательный метод для безопасной конвертации текста в float"""

        text = text.replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return 0.0


    def on_usd_changed(self, text : str):
        """Обработчик изменения usd"""

        if not text:
            self.clear_other_fields(except_field=self.usd_input)
            return

        usd_val = self.parse_value(text)
        rub_val = usd_val * self.rate_usd_to_rub
        eur_val = usd_val * self.rate_usd_to_eur

        self.rub_input.blockSignals(True)
        self.eur_input.blockSignals(True)

        self.rub_input.setText(f"{rub_val:.2f}")
        self.eur_input.setText(f"{eur_val:.2f}")

        self.rub_input.blockSignals(False)
        self.eur_input.blockSignals(False)


    def on_rub_changed(self, text : str):
        """Обработчик изменения rub"""

        if not text:
            self.clear_other_fields(except_field=self.rub_input)
            return

        rub_val = self.parse_value(text)
        usd_val = rub_val / self.rate_usd_to_rub
        eur_val = usd_val * self.rate_usd_to_eur

        self.usd_input.blockSignals(True)
        self.eur_input.blockSignals(True)

        self.usd_input.setText(f"{usd_val:.2f}")
        self.eur_input.setText(f"{eur_val:.2f}")

        self.usd_input.blockSignals(False)
        self.eur_input.blockSignals(False)


    def on_eur_changed(self, text):
        """Обработчик изменения EUR"""
        
        if not text:
            self.clear_other_fields(except_field=self.eur_input)
            return

        eur_val = self.parse_value(text)
        usd_val = eur_val / self.rate_usd_to_eur
        rub_val = usd_val * self.rate_usd_to_rub

        self.usd_input.blockSignals(True)
        self.rub_input.blockSignals(True)

        self.usd_input.setText(f"{usd_val:.2f}")
        self.rub_input.setText(f"{rub_val:.2f}")

        self.usd_input.blockSignals(False)
        self.rub_input.blockSignals(False)


    def clear_other_fields(self, except_field):
        """Очистка остальных полей, если текущее поле пустое"""
        fileds = [self.usd_input, self.rub_input, self.eur_input]
        for fileld in fileds:
            if fileld != except_field:
                fileld.blockSignals(True)
                fileld.clear()
                fileld.blockSignals(False)
