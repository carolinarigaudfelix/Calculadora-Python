import sys
from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QTextEdit
from variables import WINDOW_ICON_PATH
from styles import setupTheme

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
    info = Info('2.0 ^ 10.0 = 1024')
    window.addToVLayout(info)
    
     # Display
    display = Display()
    window.addToVLayout(display)
    #display.setPlaceholderText('Digite algo')

    
    #Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()