import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)


class DCDBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCDB Query Tool")

        # Widgets
        self.start_label = QLabel("Start Time (YYYY-MM-DD HH:MM:SS)")
        self.start_input = QLineEdit()

        self.end_label = QLabel("End Time (YYYY-MM-DD HH:MM:SS)")
        self.end_input = QLineEdit()

        self.output_label = QLabel("Output Directory")
        self.output_input = QLineEdit()

        self.browse_btn = QPushButton("Browse")
        self.run_btn = QPushButton("Run")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_label)
        layout.addWidget(self.start_input)
        layout.addWidget(self.end_label)
        layout.addWidget(self.end_input)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_input)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.log_box)

        self.setLayout(layout)

        # Signals
        self.browse_btn.clicked.connect(self.browse_folder)
        self.run_btn.clicked.connect(self.run_script)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_input.setText(folder)

    def run_script(self):
        start = self.start_input.text()
        end = self.end_input.text()
        output = self.output_input.text()

        self.log_box.append(f"Running from {start} to {end}")

        command = [
            "bash", "ssh_runner.sh",
            start, end, output
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            self.log_box.append(result.stdout)
            self.log_box.append(result.stderr)
        except Exception as e:
            self.log_box.append(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DCDBApp()
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec())