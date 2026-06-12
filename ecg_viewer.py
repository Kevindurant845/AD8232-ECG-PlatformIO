import sys
import serial
import numpy as np
from collections import deque
from scipy.signal import find_peaks
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

# =========================
# CONFIGURATION
# =========================
PORT = "COM9"          # CHANGE THIS
BAUD = 115200
FS = 360              # sampling frequency

# =========================
# SERIAL CONNECTION
# =========================
ser = serial.Serial(PORT, BAUD)

# =========================
# DATA BUFFER (real-time window)
# =========================
buffer_size = 1000
ecg_data = deque([0]*buffer_size, maxlen=buffer_size)

# =========================
# APP SETUP
# =========================
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="ECG Real-Time Monitor")
win.resize(1000, 500)

plot = win.addPlot(title="ECG Signal")
curve = plot.plot(pen='g')
plot.setYRange(0, 4095)
plot.setLabel('left', 'Amplitude')
plot.setLabel('bottom', 'Samples')

# BPM display text
bpm_text = pg.TextItem(text="BPM: --", color='r', anchor=(0, 0))
plot.addItem(bpm_text)

# =========================
# BPM CALCULATION
# =========================


def calculate_bpm(signal):
    signal = np.array(signal)

    # detect peaks (R-waves)
    peaks, _ = find_peaks(signal, distance=FS*0.4)

    if len(peaks) < 2:
        return 0

    # compute time between peaks
    rr_intervals = np.diff(peaks) / FS
    avg_rr = np.mean(rr_intervals)

    bpm = 60 / avg_rr
    return int(bpm)

# =========================
# UPDATE FUNCTION
# =========================


def update():
    global ecg_data

    try:
        line = ser.readline().decode().strip()
        if line.isdigit():
            value = int(line)
            ecg_data.append(value)

            curve.setData(list(ecg_data))

            bpm = calculate_bpm(ecg_data)
            bpm_text.setText(f"BPM: {bpm}")

    except:
        pass


# =========================
# TIMER (real-time loop)
# =========================
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)

# =========================
# START APP
# =========================
win.show()
sys.exit(app.exec_())
