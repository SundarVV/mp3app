from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
import sys
from app.mp3_player import AudioPlayer

# Set the required Qt attribute
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

app = QApplication(sys.argv)

loader = QUiLoader()
ui = loader.load("D:/Python/MP3App/app/ui/MP3App.ui")
main_window = AudioPlayer()

main_window.show()
sys.exit(app.exec())

