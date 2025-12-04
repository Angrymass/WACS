from PyQt6 import QtGui, QtCore
import sys
class MainWindow(QtGui.QWindow):
      def __init__(self):
              QtGui.QWindow.__init__(self)
              self.resize(350, 250)
              self.setTitle('MainWindow')
app = QtGui.QGuiApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())