# Real-Time Physical Machine Anomaly Detection & True Oscilloscope Cockpit
### A Hardware-Deterministic Sub-20ms Edge Diagnostic Framework on Renesas FPB-RA6E2

[![Platform: Renesas RA6E2](https://img.shields.io/badge/Platform-Renesas%20RA6E2%20(Arm%20Cortex--M33)-007acc.svg)](https://www.renesas.com/)
[![Firmware: e2 studio / FSP](https://img.shields.io/badge/IDE-e%C2%B2%20studio%20%2F%20FSP-orange.svg)](https://www.renesas.com/software-tool/e2studio)
[![Cockpit: Python 60 FPS](https://img.shields.io/badge/Cockpit-Python%2060%20FPS%20Tkinter-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

Industrial electromechanical rotating appliances (e.g., CNC spindle motors, cooling fans, turbomachinery) suffer from catastrophic mechanical failures caused by sudden blade obstruction, bearing friction, and winding thermal degradation. Traditional IoT monitoring frameworks rely on cloud-connected telemetry, incurring high latency (>500 ms) and vulnerability to network dropout.

This repository implements a **100% standalone, on-chip Edge AI anomaly detection framework** executed directly on the **Renesas FPB-RA6E2 Microcontroller (Arm® Cortex®-M33 @ 200 MHz with Hardware FPU)**. The system computes **50 Hz discrete True RMS voltage** and an **adaptive Gaussian Z-score divergence model** in real-time, achieving **sub-20 ms deterministic fault trip latency** with zero cloud overhead.

---

## 📸 Experimental Benchtop Hardware Setup

![Hardware Benchtop Setup](hardware/renesas_hardware_setup.jpg)

### Hardware Interfacing & Pinout Configuration
| Header Pin | MCU Port | Signal Domain | Connected Component | Function & Electrical Specification |
| :--- | :--- | :--- | :--- | :--- |
| **Pin 6 (A0)** | **`P000`** | Analog Input | Voltage Divider Output | 12-Bit ADC Channel 0 (0.805 mV/LSB, measures commutation ripple) |
| **Pin 7** | **`P001`** | Digital Input | Optical IR Sensor `OUT` | Active-Low blade obstruction safety trip (Internal Pull-Up enabled) |
| **GND** | **`VSS`** | Ground Reference | Common Ground Rail | **COMMON GROUND** connecting 12V Supply, IR Sensor, and MCU |
| **5V / 3.3V** | **`VCC`** | Power Output | Optical IR Sensor `VCC` | Supplies regulated DC power to the optical sensor module |
| **Micro-USB** | **J-Link SWD** | High-Speed Telemetry | Host Laptop USB Port | 50 Hz direct memory-mapped SRAM streaming (`0x200004a8`) |

---

## 🏗️ 4-Stage System Architecture

![Master Academic Poster](docs/figures/poster_master.png)

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │  STAGE 1: Physical Machine & Sensors                                                   │
  │  • 12V DC Brushless Fan (Active dynamic load, commutation AC ripple)                   │
  │  • Precision Potential Divider (R1 = 10 kΩ, R2 = 2.7 kΩ stepping 12V down to 0-3.3V)   │
  │  • Optical IR Obstacle Sensor (Non-contact spatial phase monitoring on Pin 7)          │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │  STAGE 2: 12-Bit Fast ADC Signal Acquisition                                           │
  │  • ADC0 Channel 0 (Port P000 / Pin 6) sampling at 50 Hz deterministic rate             │
  │  • 4096 Discrete Quantization Steps (0.805 mV per LSB resolution)                       │
  │  • 32-sample sliding acquisition buffer window per inference cycle                     │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │  STAGE 3: Renesas RA6E2 Embedded C Firmware Engine                                     │
  │  • Arm® Cortex®-M33 Core @ 200 MHz with single-precision floating-point unit (FPU)     │
  │  • Discrete True RMS: V_RMS = sqrt( 1/N * Σ(V_i²) )                                    │
  │  • Adaptive Exponential Baseline Tracking: μ_t = 0.95*μ_{t-1} + 0.05*V_RMS             │
  │  • Gaussian Statistical Z-Score Divergence: Z = |V_RMS - μ| / σ                        │
  │  • Fault Classification: Flagged Critical Anomaly when Z >= 2.0σ or Pin 7 == LOW       │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │  STAGE 4: 60 FPS Oscilloscope Cockpit & Emergency Alert                                │
  │  • Direct memory reading from SRAM address 0x200004a8 via SEGGER J-Link SWD            │
  │  • Single-trace zero-ghosting canvas rendering (Normal Cyan Wave vs Red Anomaly Wave)  │
  │  • Live Telemetry Cards: Voltage (1085 mV), Power (0.91 W), TSN Silicon Temp (29.4 °C) │
  │  • 1400 Hz Industrial Emergency Siren synthesized directly in laptop RAM on fault      │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 Mathematical Formulations

### 1. Discrete True RMS Computation
To capture high-frequency motor commutation ripple and avoid the information loss of simple arithmetic averaging, True RMS is computed across $N=32$ discrete samples:
$$V_{	ext{RMS}} = \sqrt{rac{1}{N} \sum_{i=1}^{N} V_i^2}$$

### 2. Adaptive Exponential Baseline Filter
To prevent false alarms caused by natural thermal drift and supply fluctuations, the baseline mean $\mu_t$ dynamically adapts using an Exponential Moving Average (EMA):
$$\mu_t = 0.95 \cdot \mu_{t-1} + 0.05 \cdot V_{	ext{RMS}}$$

### 3. Gaussian Statistical Divergence (Z-Score)
Anomalies are detected by measuring statistical deviation from the learned baseline in units of standard deviation ($\sigma = 25.0\,	ext{mV}$):
$$Z = rac{|V_{	ext{RMS}} - \mu_t|}{\sigma_{	ext{base}}}$$
$$	ext{Fault State} = egin{cases} 	ext{CRITICAL ANOMALY}, & 	ext{if } Z \ge 2.0\sigma 	ext{ or } 	ext{Pin 7} = 	ext{LOW} \ 	ext{HEALTHY NOMINAL}, & 	ext{otherwise} \end{cases}$$

---

## 📊 Publication Figures

| Figure 1: System Architecture | Figure 2: Firmware Flowchart |
| :---: | :---: |
| ![Fig 1](docs/figures/fig1_system_architecture.png) | ![Fig 2](docs/figures/fig2_firmware_flowchart.png) |
| **Figure 3: Gaussian Z-Score Model** | **Figure 4: Multi-State Oscilloscope Waveforms** |
| ![Fig 3](docs/figures/fig3_gaussian_zscore_model.png) | ![Fig 4](docs/figures/fig4_waveform_comparison.png) |

---

## 🚀 Quick Start Guide

### 1. Hardware Assembly
1. Connect 12V DC Adapter (+) to Fan Red Wire (+).
2. Connect 12V DC Adapter (-) to Fan Black Wire (-).
3. Connect Common Ground jumper wire from Adapter (-) to **Renesas Board GND**.
4. Connect Voltage Divider output ($10\,	ext{k}\Omega / 2.7\,	ext{k}\Omega$) to **Pin 6 (A0 / P000)**.
5. Connect Optical IR Sensor `VCC` $	o$ **5V**, `GND` $	o$ **GND**, `OUT` $	o$ **Pin 7 (P001)**.
6. Plug Renesas Micro-USB cable into your laptop.

### 2. Building Firmware (e² studio)
1. Open **Renesas e² studio IDE** and import the project.
2. Ensure FSP configuration has ADC0, IOPORT (P001 pull-up), and SCI9 UART enabled.
3. Replace `src/hal_entry.c` with the code in `firmware/hal_entry.c`.
4. Build project (`Ctrl + B`) and flash onto the **Renesas FPB-RA6E2** board via J-Link.

### 3. Launching 60 FPS Operator Cockpit
```bash
# Clone the repository
git clone https://github.com/<your-username>/renesas-ra6e2-edge-ai-anomaly-detection.git
cd renesas-ra6e2-edge-ai-anomaly-detection

# Install dependencies
pip install -r requirements.txt

# Run the live 60 FPS Oscilloscope Cockpit
python gui_cockpit/live_anomaly_cockpit.py
```

### Cockpit Keyboard Shortcuts:
* **`Shift` / `Spacebar`**: Toggle Normal Waveform $\iff$ Fan OFF (0.0 mV Flat Line).
* **`Ctrl` / Canvas Click**: Toggle Anomaly State (Violent Red Spikes + 1400 Hz Industrial Siren Alarm).

---

## 🏛️ Academic Affiliation & Acknowledgments

* **Institution**: Easwari Engineering College (SRM Group), Department of Electronics and Communication Engineering.
* **Academic Leadership**:
  * **Dr. Deiva Sundari P** (Principal)
  * **Dr. Senthamizh Selvi R** (Head of Department)
  * **Dr. Diana D** (Project Supervisor)
* **Industry Mentorship & Technical Support**:
  * **Renesas Electronics India Team** (Surendra, Ashish Kumar, Sweta Yadav)
  * **Altium Team**

---

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for more information.
