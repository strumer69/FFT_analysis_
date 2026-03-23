import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)


class DCDBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCDB Query Tool")

        # -------------------------------------Widgets
        # --- FIRST PERIOD ---
        self.start_label1 = QLabel("Start Time 1: (YYY-MM-DD HH:MM:SS)")
        self.start_input1 = QLineEdit()

        self.end_label1 = QLabel("End Time 1: (YYY-MM-DD HH:MM:SS)")
        self.end_input1 = QLineEdit()

        # --- SECOND PERIOD ---
        self.start_label2 = QLabel("Start Time 2")
        self.start_input2 = QLineEdit()

        self.end_label2 = QLabel("End Time 2")
        self.end_input2 = QLineEdit()

        self.output_label = QLabel("Output Directory")
        self.output_input = QLineEdit()

        self.browse_btn = QPushButton("Browse")
        self.run_btn = QPushButton("Run")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(QLabel("=== Period 1 ==="))
        layout.addWidget(self.start_label1)
        layout.addWidget(self.start_input1)
        layout.addWidget(self.end_label1)
        layout.addWidget(self.end_input1)

        layout.addWidget(QLabel("=== Period 2 ==="))
        layout.addWidget(self.start_label2)
        layout.addWidget(self.start_input2)
        layout.addWidget(self.end_label2)
        layout.addWidget(self.end_input2)

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
        start1 = self.start_input1.text()
        end1 = self.end_input1.text()

        start2 = self.start_input2.text()
        end2 = self.end_input2.text()

        output = self.output_input.text()
        

        # ---- Period 1 ----
        self.log_box.append(f"[PERIOD 1] {start1} → {end1}")

        cmd1 = ["bash", "ssh_runner.sh", start1, end1, output, "period1"]

        result1 = subprocess.run(cmd1, capture_output=True, text=True)
        self.log_box.append(result1.stdout)
        self.log_box.append(result1.stderr)

        # ---- Period 2 ----
        self.log_box.append(f"[PERIOD 2] {start2} → {end2}")

        cmd2 = ["bash", "ssh_runner.sh", start2, end2, output, "period2"]

        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        self.log_box.append(result2.stdout)
        self.log_box.append(result2.stderr)

    def run_script(self):
        start1 = self.start_input1.text()
        end1 = self.end_input1.text()

        start2 = self.start_input2.text()
        end2 = self.end_input2.text()

        output = self.output_input.text()

        # ---- Period 1 ----
        self.log_box.append(f"[PERIOD 1] {start1} → {end1}")

        cmd1 = ["bash", "ssh_runner.sh", start1, end1, output, "period1"]

        result1 = subprocess.run(cmd1, capture_output=True, text=True)
        self.log_box.append(result1.stdout)
        self.log_box.append(result1.stderr)

        # ---- Period 2 ----
        self.log_box.append(f"[PERIOD 2] {start2} → {end2}")

        cmd2 = ["bash", "ssh_runner.sh", start2, end2, output, "period2"]

        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        self.log_box.append(result2.stdout)
        self.log_box.append(result2.stderr)

        # ---- NOW run FFT (after data exists) ----
        self.log_box.append("Running FFT processing...")

        fft_result = subprocess.run(
            ["python3", "fft_script.py", output],
            capture_output=True,
            text=True
        )

        self.log_box.append(fft_result.stdout)
        self.log_box.append(fft_result.stderr)

        # ---- CREATE VIDEOS ----
        self.log_box.append("Creating videos...")

        # Period 1 video
        subprocess.run([
            "ffmpeg",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period1/FFT_X/*.png",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period1/FFT_Y/*.png",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period1/FFT_Z/*.png",
            "-filter_complex", "[0:v][1:v][2:v]hstack=inputs=3",
            "-c:v", "mpeg4",
            "-pix_fmt", "yuv420p",
            f"{output}/period1.mp4"
        ])

        # Period 2 video
        subprocess.run([
            "ffmpeg",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period2/FFT_X/*.png",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period2/FFT_Y/*.png",
            "-framerate", "1",
            "-pattern_type", "glob", "-i", f"{output}/period2/FFT_Z/*.png",
            "-filter_complex", "[0:v][1:v][2:v]hstack=inputs=3",
            "-c:v", "mpeg4",
            "-pix_fmt", "yuv420p",
            f"{output}/period2.mp4"
        ])

        # ---- COMBINE VIDEOS ----
        self.log_box.append("Creating comparison video...")

        subprocess.run([
            "ffmpeg",
            "-i", f"{output}/period1.mp4",
            "-i", f"{output}/period2.mp4",
            "-filter_complex", "[0:v][1:v]vstack=inputs=2",
            "-c:v", "mpeg4",
            "-pix_fmt", "yuv420p",
            f"{output}/comparison.mp4"
        ])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DCDBApp()
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec())

#------------------------------------------------ end of logging ---------------------
