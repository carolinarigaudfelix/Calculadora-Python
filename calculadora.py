import sys
from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit
from variables import WINDOW_ICON_PATH
from styles import setupTheme
from buttons import Button, ButtonsGrid

#line edit e text edit é pra qnd n for algo mais simples como o qlabel

if __name__ == '__main__':
    #Cria Aplicação
    
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

   # label1 = QLabel('O meu texto')
    # label1.setStyleSheet('font-size: 150px;')
    # window.VLayout.addWidget(label1)
    #Defina ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    
    #Info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)
    
    #Display
    display = Display()
    window.addWidgetToVLayout(display)

    #Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.VLayout.addLayout(buttonsGrid) #adiciona buttonsgrid no VLayout

    

    # Button
    # buttonsGrid.addWidget(Button('0'), 0, 0)
    # buttonsGrid.addWidget(Button('1'), 0, 1)
    # buttonsGrid.addWidget(Button('2'), 0, 2)
    # buttonsGrid.addWidget(Button('3'), 1, 1, 1 ,2)


    
    #Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()