import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import glob
import sys

# ---------- SETTINGS ----------
base_path = sys.argv[1]                 # <-- from GUI
base_dirs = ["period1", "period2"]
axes = ["X", "Y", "Z"]

max_freq = 500

# Helper to fix timestamps with too many microseconds
def fix_timestamp(ts):
    if "." in ts:
        base, frac = ts.split(".")
        frac = frac[:6]  # keep only microseconds
        ts = base + "." + frac
    return ts

# =========================================================
# LOOP OVER PERIODS + AXES
# =========================================================
for period in base_dirs:
    print(f"\n===== Processing {period} =====")

    for axis in axes:
        print(f"\n--- Axis: {axis} ---")

        input_dir = os.path.join(base_path, period, axis)
        output_dir = os.path.join(base_path, period, f"FFT_{axis}")
        os.makedirs(output_dir, exist_ok=True)

        files = sorted(glob.glob(os.path.join(input_dir, "*.csv")))

        if not files:
            print(f"No files found in {input_dir}")
            continue

        # =========================================================
        # PASS 1: GLOBAL MAX
        # =========================================================
        global_max = 0

        for input_file in files:
            timestamps = []
            values = []

            with open(input_file, "r") as f:
                lines = f.readlines()[3:]  # skip header lines
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        try:
                            timestamps.append(parts[1])
                            values.append(float(parts[2]))
                        except:
                            print(f"Skipping invalid line in {input_file}: {line.strip()}")

            if len(values) < 2:
                print(f"Skipping {input_file} (not enough data)")
                continue  # <-- skip empty files

            values = np.array(values)
            time_seconds = np.array([datetime.fromisoformat(fix_timestamp(ts)).timestamp() for ts in timestamps])

            if len(time_seconds) < 2:
                print(f"Skipping {input_file} (not enough timestamps)")
                continue

            dt = np.mean(np.diff(time_seconds))

            values = values - np.mean(values)
            window = np.hanning(len(values))
            values_windowed = values * window

            fft_vals = np.fft.rfft(values_windowed)
            magnitude = np.abs(fft_vals)

            global_max = max(global_max, np.max(magnitude))

        print(f"Global max amplitude: {global_max:.3f}")

        # =========================================================
        # PASS 2: FFT + PLOT
        # =========================================================
        for input_file in files:
            print(f"Processing: {input_file}")

            timestamps = []
            values = []

            with open(input_file, "r") as f:
                lines = f.readlines()[3:]
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        try:
                            timestamps.append(parts[1])
                            values.append(float(parts[2]))
                        except:
                            print(f"Skipping invalid line in {input_file}: {line.strip()}")

            if len(values) < 2:
                print(f"Skipping {input_file} (not enough data)")
                continue  # <-- skip empty files

            values = np.array(values)
            time_seconds = np.array([datetime.fromisoformat(fix_timestamp(ts)).timestamp() for ts in timestamps])

            if len(time_seconds) < 2:
                print(f"Skipping {input_file} (not enough timestamps)")
                continue

            dt = np.mean(np.diff(time_seconds))
            fs = 1.0 / dt

            values = values - np.mean(values)
            window = np.hanning(len(values))
            values_windowed = values * window

            N = len(values_windowed)
            fft_vals = np.fft.rfft(values_windowed)
            freqs = np.fft.rfftfreq(N, d=dt)
            magnitude = np.abs(fft_vals)

            # ---------- PLOT ----------
            plt.figure()
            plt.plot(freqs, magnitude)
            plt.xlim(0, max_freq)
            plt.ylim(0, global_max)
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Amplitude")
            plt.title(f"{period} - Axis {axis}\n{os.path.basename(input_file)}")
            plt.grid()

            # ---------- SAVE ----------
            base = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"fft_{base}.png")
            plt.savefig(output_file)
            plt.close()

        print(f"Finished {period} - {axis}")

print("\nAll FFT plots created.")
