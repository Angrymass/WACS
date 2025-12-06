import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QPushButton

crono_voti = "Nessun Voto"
listvoti = []

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__() 

		self.setWindowTitle("Calcolatore Media Ponderata Materie")
		self.setMinimumSize(300, 300)

		self.voti = QLabel(crono_voti)
		self.voti.setWordWrap(True)

		self.totmedia = QLabel("Media: 8")
		self.totmedia.setWordWrap(True)

		self.aggvoto = QPushButton("Aggiungi Voto...")
		self.aggvoto.clicked.connect(self.nvoto)

		self.matmedia = QLabel("Medie Materie\nMatematica:10\nDisegno:6")

		layout = QGridLayout()
		layout.addWidget(self.voti, 0, 0)
		layout.addWidget(self.totmedia, 0, 1)
		layout.addWidget(self.aggvoto, 1, 0)
		layout.addWidget(self.matmedia, 1, 1)

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		self.aggiorna()

	def aggiorna(self):
		self.voti.setText(crono_voti)

	def nvoto(self):
		val = int(input("Voto: "))
		mat = input("Materia: ")
		listvoti.append([val, mat])
		print(listvoti)
		self.make_crono_voti()
		self.aggiorna()

	def make_crono_voti(self):
		global crono_voti
		if len(listvoti) != 0:
			crono_voti = ""
			for i in range(0, len(listvoti)):
				crono_voti += "%s - %s\n" %(listvoti[i][0], listvoti[i][1])
			print(crono_voti)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()