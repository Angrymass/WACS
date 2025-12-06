import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__() 

        self.setWindowTitle("Calcolatore Media Ponderata Materie")
        self.setMinimumSize(300, 300)

        voti = QLabel("10-Matematica\n6-Disegno")
        voti.setWordWrap(True)

        totmedia = QLabel("Media: 8")
        totmedia.setWordWrap(True)

        aggvoto = QPushButton("Aggiungi Voto...")

        matmedia = QLabel("Medie Materie\nMatematica:10\nDisegno:6")

        layout = QGridLayout()
        layout.addWidget(voti, 0, 0)
        layout.addWidget(totmedia, 0, 1)
        layout.addWidget(aggvoto, 1, 0)
        layout.addWidget(matmedia, 1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()