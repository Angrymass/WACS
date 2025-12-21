from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QPushButton, QDialog, QDialogButtonBox, QLineEdit, QMessageBox
from PyQt6.QtGui import QIcon

default_crono = "Nessun Voto"
default_media_tot = "Nessun Voto"
default_media_materie = "Nessuna Materia"

def resource_path(relative_path):
    import sys, os
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__() 

        self.list_voti = []
        self.crono_materie = {}
        self.label_crono_voti_text = default_crono
        self.label_media_tot_text = default_media_tot
        self.label_media_materie_text = default_media_materie

        self.setWindowTitle("Calcolatore Media Ponderata Materie")
        self.setWindowIcon(QIcon(resource_path("Tachimetro.ico")))
        self.setMinimumSize(300, 300)
        self.label_crono_voti = QLabel(self.label_crono_voti_text)
        self.label_crono_voti.setWordWrap(True)

        self.label_media_tot = QLabel(self.label_media_tot_text)
        self.label_media_tot.setWordWrap(True)

        self.button_aggvoto = QPushButton("Aggiungi Voto...")
        self.button_aggvoto.clicked.connect(self.nvoto)

        self.label_media_materie = QLabel(self.label_media_materie_text)
        self.label_media_materie.setWordWrap(True)

        self.cancella_voto = QPushButton("Cancella Ultimo Voto")
        self.cancella_voto.clicked.connect(self.on_cancella_voto)

        layout = QGridLayout()
        layout.addWidget(self.label_crono_voti, 0, 0)
        layout.addWidget(self.label_media_tot, 0, 1)
        layout.addWidget(self.button_aggvoto, 1, 0)
        layout.addWidget(self.label_media_materie, 1, 1)
        layout.addWidget(self.cancella_voto, 2, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.aggiorna()

    def nvoto(self):
        DialogAggiungiVoto(self).exec()
        self.aggiorna()	
    
    def on_cancella_voto(self):
        if len(self.list_voti) > 0:
            self.list_voti.pop()
        self.aggiorna()

    def make_label_crono_voti(self):
        if len(self.list_voti) != 0:
            text = ""
            for i in range(len(self.list_voti), 0, -1):
                v = self.list_voti[i-1]
                if v[2] == 100:
                    text += "%s - %s\n" % (v[0], v[1])
                else:
                    text += "%s (peso %s) - %s\n" % (v[0], str(v[2]) + "%", v[1])
        else:
            text = default_crono
        self.label_crono_voti.setText(text)
    
    def aggiorna(self):
        self.make_crono_materie()
        self.make_label_crono_voti()
        self.make_label_media_tot()
        self.make_label_media_materie()

    def make_label_media_tot(self):
        if len(self.list_voti) != 0:
            total = 0
            peso = 0
            for voto in self.list_voti:
                total += voto[0] * (voto[2] / 100)
                peso += (voto[2] / 100)
            media = (total / peso) if peso != 0 else 0
            media = str(round(media, 2))
            text = "Media: %s" % media
        else:
            text = default_media_tot
        self.label_media_tot.setText(text)

    def make_crono_materie(self):
        self.crono_materie = {}
        for voto in self.list_voti:
            materia = voto[1]
            if materia not in self.crono_materie:
                self.crono_materie[materia] = []
            self.crono_materie[materia].append([voto[0], voto[2]])

    def make_label_media_materie(self):	
        if len(self.crono_materie) != 0:
            text = ""
            for materia, voti in self.crono_materie.items():
                media_materia = 0
                peso = 0
                for voto in voti:
                    media_materia += voto[0] * (voto[1] / 100)
                    peso += (voto[1] / 100)
                media_materia = (media_materia / peso) if peso != 0 else 0
                media_materia = str(round(media_materia, 2))
                text += "%s: %s\n" % (materia, media_materia)
        else:
            text = default_media_materie
        self.label_media_materie.setText(text)

class DialogAggiungiVoto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Voto")
        self.votolabel = QLabel("Inserisci il voto:")
        self.matlabel = QLabel("Inserisci la materia:")
        self.pesolabel = QLabel("Inserisci il peso:")
        self.votoinput = QLineEdit()
        self.votoinput.setPlaceholderText("Voto (0.0-100.0)")
        self.matinput = QLineEdit()
        self.matinput.setPlaceholderText("Materia")
        self.pesoinput = QLineEdit()
        self.pesoinput.setPlaceholderText("Peso (1-100)")
        self.pesoinput.setText("100")
        buttonbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.okvoto)
        buttonbox.rejected.connect(self.reject)
        layout = QGridLayout()
        layout.addWidget(self.votolabel, 0, 0)
        layout.addWidget(self.votoinput, 0, 1)
        layout.addWidget(self.matlabel, 1, 0)
        layout.addWidget(self.matinput, 1, 1)
        layout.addWidget(self.pesolabel, 2, 0)
        layout.addWidget(self.pesoinput, 2, 1)
        layout.addWidget(buttonbox, 3, 0, 1, 2)
        self.setLayout(layout)

    def okvoto(self):
        try:
            voto = float(self.votoinput.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Errore", "Inserisci un voto valido.")
            return
        materia = self.matinput.text().strip()
        try:
            peso = int(self.pesoinput.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Errore", "Inserisci un peso valido.")
            return
        if peso < 1 or peso > 100:
            QMessageBox.warning(self, "Errore", "Inserisci un peso valido (1-100).")
            return
        if voto < 0 or voto > 100:
            QMessageBox.warning(self, "Errore", "Inserisci un voto valido (0.0-100.0).")
            return
        if materia == "":
            QMessageBox.warning(self, "Errore", "Inserisci una materia valida.")
            return
        parent = self.parent()
        parent.list_voti.append([voto, materia, peso])
        parent.make_crono_materie()
        parent.aggiorna()
        super().accept()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()