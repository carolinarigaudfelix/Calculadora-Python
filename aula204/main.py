import sys
import time

from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QWidget
from ui_workerui import Ui_MyWidget

#Faz separado da Thread principal, unidade de processamento separada


class Worker1(QObject):
    started = Signal(str)
    progressed = Signal(str)
    finished = Signal(str)

    def doWork(self):
        value = '0'
        self.started.emit(value)
        for i in range(5):
            value = str(i)
            self.progressed.emit(value)
            time.sleep(1)
        self.finished.emit(value)


class MyWidget(QWidget, Ui_MyWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.button1.clicked.connect(self.hardWork1)
        self.button2.clicked.connect(self.hardWork2)

    def hardWork1(self):
        self._worker = Worker1()
        self._thread = QThread()

        worker = self._worker
        thread = self._thread

        #Mover o worker para a thread
        worker.moveToThread(thread)

        # Run
        thread.started.connect(worker.doWork)
        worker.finished.connect(thread.quit)

        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)

        worker.started.connect(lambda: print('worker iniciado'))
        worker.progressed.connect(lambda: print('progresso'))
        worker.finished.connect(lambda: print('worker finalizado'))

        worker.started.connect(self.worker1Started)
        worker.progressed.connect(self.worker1Progressed)
        worker.finished.connect(self.worker1Finished)

        thread.start()

    def worker1Started(self, value):
        self.button1.setDisabled(True)
        self.label1.setText(value)
        print('worker iniciado')
        print('worker 1 iniciado', value)

    def worker1Progressed(self, value):
        self.label1.setText(value)
        print('em progresso')
        print('1 em progresso', value)

    def worker1Finished(self, value):
        self.label1.setText(value)
        self.button1.setDisabled(False)
        print('worker finalizado')
        print('worker 1 finalizado', value)

    def hardWork2(self):
        # Isso garante que o widget vai ter uma referência para worker e thread
        self._worker2 = Worker1()
        self._thread2 = QThread()

        worker = self._worker2
        thread = self._thread2

        # Mover o worker para a thread
        # Worker é movido para a thread. Todas as funções e métodos do
        # objeto de worker serão executados na thread criado pela QThread.
        worker.moveToThread(thread)

        # Run
        thread.started.connect(worker.doWork)

        # O sinal finished é emitido pelo objeto worker quando o trabalho que
        # ele está executando é concluído. Isso aciona o método quit da qthread
        # que interrompe o loop de eventos dela.
        worker.finished.connect(thread.quit)

        # deleteLater solicita a exclusão do objeto worker do sistema de
        # gerenciamento de memória do Python. Quando o worker finaliza, ele
        # emite um sinal finished que vai executar o método deleteLater.
        # Isso garante que objetos sejam removidos da memória corretamente.
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)
        # Aqui estão seus métodos e início, meio e fim
        # execute o que quiser

        worker.started.connect(lambda: print('worker 2 iniciado'))
        worker.progressed.connect(lambda: print('progresso 2'))
        worker.finished.connect(lambda: print('worker 2 finalizado'))
        # Aqui estão seus métodos e início, meio e fim
        # execute o que quiser
        worker.started.connect(self.worker2Started)
        worker.progressed.connect(self.worker2Progressed)
        worker.finished.connect(self.worker2Finished)
        # Inicie a thread
        thread.start()

    def worker2Started(self, value):
        self.button2.setDisabled(True)
        self.label2.setText(value)
        print('worker 2 iniciado')
        print('worker 2 iniciado', value)

    def worker2Progressed(self, value):
        self.label2.setText(value)
        print('worker 2 iniciado')

    def worker2Finished(self, value):
        self.label2.setText(value)
        self.button2.setDisabled(False)
        print('worker 2 iniciado')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = MyWidget()
    myWidget.show()
    app.exec()

