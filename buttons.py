import math
from PySide6.QtWidgets import QGridLayout, QPushButton
from PySide6.QtCore import Slot
from utils import isNumOrDot, isEmpty, isValidNumber, converToNumber
from variables import MEDIUM_FONT_SIZE

from typing import TYPE_CHECKING #checka tipagem
if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
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
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                 *args, **kwargs)->None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
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

    def vouApagarVocê(self):
        print('Signal recebido, por "vouApagarVocê" em', type(self).__name__)

    def _makeGrid(self):
        self.display.eqRequested.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, colNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
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
                  self._makeSlot(self._configLeftOp, text)
            )

        if text in '=':
            self._connectButtonClicked(button, self._eq)

        if text in 'D':
            self._connectButtonClicked(button, self.display.backspace)

        if text in 'N':
            self._connectButtonClicked(button, self._invertNumber)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = converToNumber(displayText) * -1
        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()
       

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
        
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text() #Número esquerdo _left
        self.display.clear()
        self.display.setFocus()
        #Se a pessoa clicou no operador 
        # sem configurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return
        # Se ja houver algo na esquerda não faz nada
        # Apenas aguarda o número da direita
        if self._left is None:
            self._left = float(displayText)
        
        self._op = text
        self.equation = f'{self._left} {self._op} ??'
    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta')
            return
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation) #avalia uma string como código python
        except ZeroDivisionError:
            self._showError('Divisão por zero.')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result != 'error':
            self._left = None


    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self.window.makeMsgBox(text)
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information) #icon de warning
        msgBox.exec()

        """
        Texto informativo caso queira especificar um erro
        msgBox.setInformativeText('''
        Lorem Ipsum is simply dummy text of the printing and typesetting 
        industry. Lorem Ipsum has been the industry's 
        standard dummy text ever since the 1500s, when an unknown printer took 
        a galley of type and scrambled it to make a type specimen book.
        ''')
        """

        

        # msgBox.setStandardButtons(        OUTROS BOTÕES
        #     msgBox.StandardButton.Ok |
        #     msgBox.StandardButton.Cancel |
        #     msgBox.StandardButton.Save
        #)

        #msgBox.button(msgBox.StandardButton.NoToAll).setText('Não para todos')
        #acima é como uma tradução


        # if result == msgBox.StandardButton.Ok:
        #     print('Usuário clicou em OK')
        # elif result == msgBox.StandardButton.Cancel:
        #     print('Usuário clicou em Cancel')
        # elif result == msgBox.StandardButton.Save:
        #     print('Usuário clicou em Save')   

        #result = msgBox.exec()

        