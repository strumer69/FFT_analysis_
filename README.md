
# FFT Analysis Pipeline — A Small Story of Data from DCDB to a video

It all starts with a simple idea:

> “Take time-series data from the LRZ system, analyze it using FFT, and visualize the results.”

What follows is a pipeline that connects multiple worlds:

* Remote data collection (via SSH)
* Signal processing (FFT)
* Visualization (matplotlib)
* Video generation (ffmpeg)
* A user-friendly GUI (PySide6)

- After cloning this Repo you have to simply run teh auto_GUI.py and wait for few min (depends on the time you choose from DCDB for monitoring.)
- make sure that you have the script  "/home/di97qid/sl/FFT/dcdb_logger.sh" at the apropriate address.

 
---
I am trying to keep it simple. (but its not always easy)

## Step 1: Access to the LRZ System

Before anything else, there is a  prerequisite:

- You **must have passwordless SSH access** to the LRZ host.

Without this, the script `ssh_runner.sh` will fail silently or block waiting for a password.

### Set it up like this:

```bash
ssh-keygen -t rsa
ssh-copy-id your_user@lrz_host
```

Test it:

```bash
ssh your_user@lrz_host
```

If it logs in without asking for a password → you're ready.

---

## Step 2: Clone the Project

Once access is ready:

```bash
git clone https://github.com/strumer69/FFT_analysis_.git
cd FFT_analysis_
```

---

## Step 3: Install Required Tools

This project depends on several key tools. Missing any of them will break the pipeline — and yes, we learned this the hard way

### Python dependencies

Make sure you install:

```bash
pip install numpy matplotlib PySide6
```


---

### Video processing

Install **FFmpeg**:

```bash
brew install ffmpeg
```


---

## Step 4: Run the GUI

After everything is installed, the workflow becomes beautifully simple:

```bash
python3 auto_GUI.py
```

A GUI window will appear.

---

## Step 5: Using the GUI

Inside the GUI, you will:

### 1. Select two time periods

* Period 1: Start → End
* Period 2: Start → End

-  **Tip:**
Start with **very small time ranges (1–2 minute)**
This helps you debug quickly and avoid long processing times.

---

### 2. Choose output directory

Best practice:

Create a **new, dedicated folder** for each run, for example:

```
FFT_run_01/
FFT_test_small/
experiment_2026_03_03/
```

This avoids:

* Mixing outputs
* Overwriting results
* Debugging confusion

---

## What Happens Behind the Scenes

Once you click **Run**, the pipeline executes:

```
1. ssh_runner.sh
   ↓
2. Data fetched from LRZ 
   ↓
3. fft_script.py
   ↓
4. PNG plots generated
   ↓
5. FFmpeg creates videos
```

---

## Lessons Learned (Important!)

This project teaches a few valuable lessons:

---

### 1. Timestamp Precision Problem

We encountered:

```
ValueError: Invalid isoformat string
```

Cause:

* Timestamps had **nanoseconds (9 digits)**
* Python only supports **microseconds (6 digits)**

Fix:
Truncate timestamps before parsing.

---

### 2. Missing Data → Everything Breaks

If FFT images are not generated:

* FFmpeg fails
* Videos are empty
* Final comparison crashes

Always check:

```
period1/FFT_X/
period1/FFT_Y/
period1/FFT_Z/
```

---
## Final Output

If everything works, you will get:

* `period1.mp4`
* `period2.mp4`
* `comparison.mp4` (stacked visualization)

A very clean and powerful result 

---
