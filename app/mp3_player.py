import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QFileDialog
from PySide6.QtWidgets import QGridLayout
from pygame import mixer  # Pygame is used for playing music
from datetime import timedelta


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MP3 Player')
        self.setGeometry(100, 100, 400, 200)

        self.audio_file = None
        self.player = mixer.music.load("audio.mp3")  # Load an audio file

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.time_label = QLabel()
        layout.addWidget(self.time_label, 0, 0)
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(0, 100)  # You can adjust the range as per your need
        layout.addWidget(self.time_slider, 1, 0)

        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_audio)
        layout.addWidget(self.play_button, 0, 1)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_audio)
        layout.addWidget(self.stop_button, 1, 1)

        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.pause_audio)
        layout.addWidget(self.pause_button, 2, 0)

        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.valueChanged.connect(self.seek_audio)
        layout.addWidget(self.seek_slider, 3, 0)

        self.open_file_button = QPushButton('Open File')
        self.open_file_button.clicked.connect(self.open_audio_file)
        layout.addWidget(self.open_file_button, 2, 1)

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_player)
        layout.addWidget(self.close_button, 3, 1)

        self.setLayout(layout)

    def convert_ms_to_time(self, milliseconds: int) -> str:
        """Converts time in milliseconds to a human-readable format."""
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def convert_time_to_ms(self, time_str: str) -> int:
        """Converts a human-readable time format to milliseconds."""
        parts = time_str.split(':')
        hours, minutes, seconds = map(int, parts[0].split('.')) + list(map(int, parts[1].split('.')))
        return (hours * 60 + minutes) * 1000 + int(seconds * 100)

    def play_audio(self):
        """Plays the selected audio file."""
        self.audio_file = QFileDialog.getOpenFileName(self, 'Open Audio File', '.', 'Audio Files (*.mp3 *.wav)')
        if self.audio_file[1]:
            mixer.music.load(self.audio_file[0])
            mixer.music.play()
            self.time_slider.setRange(0, 100)  # Adjust the range as per audio duration
            self.seek_slider.setRange(0, 100)
            self.time_label.setText("00:00")
        else:
            print("No file selected.")

    def stop_audio(self):
        """Stops the currently playing audio."""
        if mixer.music.get_busy():
            mixer.music.stop()
            self.time_label.setText("00:00")

    def pause_audio(self):
        """Pauses or resumes the currently playing audio."""
        if mixer.music.get_busy():
            mixer.music.pause()
            self.seek_slider.setEnabled(False)
        else:
            mixer.music.unpause()
            self.seek_slider.setEnabled(True)

    def seek_audio(self, value: int) -> None:
        """Sets the playback position to the given time."""
        if mixer.music.get_busy():
            milliseconds = int(value / 100 * 3600000)  # Adjusted for audio duration
            mixer.music.play(start=milliseconds)
            self.time_label.setText(f"00:{int(milliseconds / 60000):02d}:{(milliseconds % 60000) // 1000:03d}")

    def open_audio_file(self):
        """Opens a file dialog to select an audio file."""
        self.audio_file = QFileDialog.getOpenFileName(self, 'Open Audio File', '.', 'Audio Files (*.mp3 *.wav)')
        if self.audio_file[1]:
            mixer.music.load(self.audio_file[0])
            print(f"Selected audio file: {self.audio_file[0]}")

    def close_player(self):
        """Closes the player and stops any currently playing audio."""
        if mixer.music.get_busy():
            mixer.music.stop()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MP3Player()
    window.show()
    sys.exit(app.exec_())
