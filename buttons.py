import math
from PySide6.QtWidgets import QGridLayout, QPushButton
from PySide6.QtCore import Slot
from utils import isNumOrDot, isEmpty, isValidNumber
from variables import MEDIUM_FONT_SIZE

from typing import TYPE_CHECKING #checka tipagem
if TYPE_CHECKING:
    from display import Display
    from info import Info

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
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs)->None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()


    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, colNumber)
                slot = self._makeSlot(self._insertButtonTextoToDisplay, button)
                self._connectButtonClicked(button, slot) #type: ignore

            
    def _connectButtonClicked(self, button, slot):
           button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-/*^':
            self._connectButtonClicked(
                button,
                  self._makeSlot(self._operatorClicked, button)
            )

        if text in '=':
            self._connectButtonClicked(button, self._eq)

        if text in 'D':
            self._connectButtonClicked(button, self.display.backspace)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot


    def _insertButtonTextoToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
    
    def _operatorClicked(self, button):
        buttonText = button.text() # +-/* (etc...)
        displayText = self.display.text() #Número esquerdo _left
        self.display.clear()
        #Se a pessoa clicou no operador 
        # sem configurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            print('Não tem nada para colocar no valor da esquerda')
            return
        # Se ja houver algo na esquerda não faz nada
        # Apenas aguarda o número da direita
        if self._left is None:
            self._left = float(displayText)
        
        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
        
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            print('Sem nada para a direita')
            return
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation) #avalia uma string como código python
        except ZeroDivisionError:
            print('Zero Divsion Error')
        except OverflowError:
            print('Número muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result != 'error':
            self._left = None

       

        