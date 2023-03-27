#informações não são editáveis
import sys

from typing import Optional

from PySide6.QtWidgets import QLabel, QWidget
from variables import SMALL_FONT_SIZE
from PySide6.QtCore import Qt



#obs: clicar com o botão direito em QLabel, ir pra definição e copiar init

class Info(QLabel):
    def __init__(
        self, text: str, parent: QWidget | None = None 
    )-> None:  # | ou n vai ter nada ou vai ser um QWidget
        super().__init__(text, parent) 
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    