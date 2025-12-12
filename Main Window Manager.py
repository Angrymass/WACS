from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QPushButton, QDialog, QDialogButtonBox, QLineEdit

crono_voti = "Nessun Voto"
media = "Nessun Voto"
matmedia = "Nessuna Materia"

crono_materie = {}
listvoti = []

class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__() 

		self.setWindowTitle("Calcolatore Media Ponderata Materie")
		self.setMinimumSize(300, 300)

		self.voti = QLabel(crono_voti)
		self.voti.setWordWrap(True)

		self.totmedia = QLabel(media)
		self.totmedia.setWordWrap(True)

		self.aggvoto = QPushButton("Aggiungi Voto...")
		self.aggvoto.clicked.connect(self.nvoto)

		self.matmedia = QLabel(matmedia)

		layout = QGridLayout()
		layout.addWidget(self.voti, 0, 0)
		layout.addWidget(self.totmedia, 0, 1)
		layout.addWidget(self.aggvoto, 1, 0)
		layout.addWidget(self.matmedia, 1, 1)

		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		self.aggiorna()

	def nvoto(self):
		DialogAggiungiVoto(self).exec()
		self.aggiorna()	

	def make_crono_voti(self):
		global crono_voti
		if len(listvoti) != 0:
			crono_voti = ""
			for i in range(0, len(listvoti)):
				crono_voti += "%s - %s\n" %(listvoti[i][0], listvoti[i][1])
		self.voti.setText(crono_voti)
	
	def aggiorna(self):
		self.make_crono_voti()
		self.aggmedia()
		self.aggmatmedia()

	def aggmedia(self):
		if len(listvoti) != 0:
			global media
			sommavoti = 0
			for i in range(0, len(listvoti)):
				sommavoti = sommavoti + listvoti[i][0]
			media = round((sommavoti / len(listvoti)), 2)
			media = "Media: %s" %media
			self.totmedia.setText(media)

	def aggmatmedia(self):
		global matmedia
		if len(crono_materie) != 0:
			matmedia = "Medie Materie:\n"
			for materia, voti in crono_materie.items():
				sommavoti = sum(voti)
				mediamat = round((sommavoti / len(voti)), 2)
				matmedia += "%s: %s\n" %(materia, mediamat)
			self.matmedia.setText(matmedia)

class DialogAggiungiVoto(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Aggiungi Voto")
		self.votolabel = QLabel("Inserisci il voto:")
		self.matlabel = QLabel("Inserisci la materia:")
		self.votoinput = QLineEdit()
		self.matinput = QLineEdit()
		buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonbox.accepted.connect(self.accept)
		buttonbox.rejected.connect(self.reject)
		layout = QGridLayout()
		layout.addWidget(self.votolabel, 0, 0)
		layout.addWidget(self.votoinput, 0, 1)
		layout.addWidget(self.matlabel, 1, 0)
		layout.addWidget(self.matinput, 1, 1)
		layout.addWidget(buttonbox, 2, 0, 1, 2)
		self.setLayout(layout)

	def accept(self):
		voto = float(self.votoinput.text())
		materia = self.matinput.text()
		listvoti.append([voto, materia])
		self.parent().aggiorna()
		super().accept()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()