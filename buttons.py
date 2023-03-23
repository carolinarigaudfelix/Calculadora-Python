from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isNumOrDot, isEmpty
from variables import MEDIUM_FONT_SIZE

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        #self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px; ')
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        #font.setItalic(True)
        #font.setBold(True)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        


class ButtonsGrid(QGridLayout):
    def __init__(self, *args, **kwargs)->None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self._makeGrid()

    def _makeGrid(self):
        for row_number, rowData in enumerate(self._gridMask):
            for column_number, button_text in enumerate(rowData):
                button = Button(button_text)

                if not isNumOrDot(button_text) and not isEmpty(button_text):
                    button.setProperty('cssClass', 'specialButton')

                self.addWidget(button, row_number, column_number)
