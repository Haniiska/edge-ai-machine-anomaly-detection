"""
========================================================================================
Ultra-High-End Professional Academic Research Poster Generator (300 DPI Publication Quality)
Generates a prestigious, crystal-clear, Swiss-modernist engineering poster for the project.
========================================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUT_PATH_PNG = r"C:\Users\WELCOME\Desktop\Renesas_Professional_Project_Poster_Master.png"
OUT_PATH_PDF = r"C:\Users\WELCOME\Desktop\Renesas_Professional_Project_Poster_Master.pdf"

# Set High-End Academic Typography & Styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Create 3:4 High-Resolution Poster Canvas (300 DPI, 3000 x 4000 px equivalent)
fig = plt.figure(figsize=(10, 13.33), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 133.3)
ax.axis('off')

# Background: Deep Midnight Navy
bg = patches.Rectangle((0, 0), 100, 133.3, facecolor="#080c17")
ax.add_patch(bg)

# Subtle Background Grid
for gx in range(5, 100, 5):
    ax.axvline(gx, color="#0f172a", lw=0.4, alpha=0.5)
for gy in range(5, 133, 5):
    ax.axhline(gy, color="#0f172a", lw=0.4, alpha=0.5)

# Helper Function: Glassmorphic Panel
def draw_panel(ax, x, y, w, h, title=None, subtitle=None, border_color="#1e293b", bg_color="#0f172a"):
    panel = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
                                   linewidth=1.4, edgecolor=border_color, facecolor=bg_color)
    ax.add_patch(panel)
    if title:
        ax.text(x + 2.5, y + h - 2.8, title, fontsize=10.5, fontweight='bold', color="#38bdf8", va='top')
    if subtitle:
        ax.text(x + 2.5, y + h - 5.0, subtitle, fontsize=7.8, color="#94a3b8", va='top')

# --------------------------------------------------------------------------------------
# 1. HEADER BANNER
# --------------------------------------------------------------------------------------
draw_panel(ax, 4, 114, 92, 15.5, border_color="#0284c7", bg_color="#0d1527")

# Chip Category Badge
badge = patches.FancyBboxPatch((6.5, 125.2), 38, 2.5, boxstyle="round,pad=0.2,rounding_size=0.4",
                              linewidth=0, facecolor="#0369a1")
ax.add_patch(badge)
ax.text(25.5, 126.45, "RENESAS FPB-RA6E2 • EMBEDDED EDGE AI SYSTEM", fontsize=7.5, fontweight='bold', color="#e0f2fe", ha='center', va='center')

# Title & Subtitle
ax.text(6.5, 121.2, "Real-Time Machine Anomaly Detection & True Oscilloscope Cockpit", fontsize=15.5, fontweight='bold', color="#ffffff", va='center')
ax.text(6.5, 117.2, "A Hardware-Deterministic Sub-20ms Edge Diagnostic Framework for Industrial Rotating Appliances", fontsize=8.8, color="#94a3b8", va='center')

# Header Metric Chips
def draw_chip(ax, x, y, w, h, val, lbl, color="#06b6d4"):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.5",
                                  linewidth=1, edgecolor=color, facecolor="#131e36")
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65, val, fontsize=10, fontweight='bold', color=color, ha='center', va='center')
    ax.text(x + w/2, y + h*0.25, lbl, fontsize=6.5, color="#cbd5e1", ha='center', va='center')

draw_chip(ax, 52, 116.2, 12, 5.8, "200 MHz", "Arm Cortex-M33", "#06b6d4")
draw_chip(ax, 65.5, 116.2, 12, 5.8, "12-Bit ADC", "0.805 mV / LSB", "#10b981")
draw_chip(ax, 79, 116.2, 14, 5.8, "< 20 ms", "On-Chip Latency", "#a855f7")

# --------------------------------------------------------------------------------------
# 2. STAGE 1: PHYSICAL MACHINE & SENSING INTERFACE
# --------------------------------------------------------------------------------------
draw_panel(ax, 4, 91.5, 92, 19.5, 
           title="STAGE 1: PHYSICAL MACHINE & TRANSDUCTION INTERFACE", 
           subtitle="12V DC Brushless motor load interfacing with precision potential divider and optical phase sensor",
           border_color="#1e293b", bg_color="#0b1220")

# Sub-card 1: 12V Fan
draw_panel(ax, 6.5, 93.5, 27, 12.5, border_color="#334155", bg_color="#111c30")
ax.text(8.5, 103.8, "[1] 12V DC Brushless Fan", fontsize=9.2, fontweight='bold', color="#ffffff")
ax.text(8.5, 100.8, "• Rotating motor load dynamics\n• Commutation AC back-EMF ripple\n• Nominal load power: 0.91 W\n• Controlled via physical 12V switch", fontsize=7.6, color="#cbd5e1", linespacing=1.35)

# Sub-card 2: Potential Divider
draw_panel(ax, 36.5, 93.5, 27, 12.5, border_color="#334155", bg_color="#111c30")
ax.text(38.5, 103.8, "[2] Precision Potential Divider", fontsize=9.2, fontweight='bold', color="#38bdf8")
ax.text(38.5, 100.8, "• R1 = 10 kΩ | R2 = 2.7 kΩ network\n• Steps 12V down to safe 0 – 3.3V\n• Parallel tap: Zero power loss on fan\n• Feeds Pin 6 (P000 / A0 Analog)", fontsize=7.6, color="#cbd5e1", linespacing=1.35)

# Sub-card 3: Optical IR Sensor
draw_panel(ax, 66.5, 93.5, 27, 12.5, border_color="#334155", bg_color="#111c30")
ax.text(68.5, 103.8, "[3] Optical IR Obstacle Sensor", fontsize=9.2, fontweight='bold', color="#f43f5e")
ax.text(68.5, 100.8, "• Non-contact blade phase detector\n• Active-Low digital output (Pin 7 / P001)\n• Internal pull-up configured via PFS\n• Triggers instant obstacle safety trip", fontsize=7.6, color="#cbd5e1", linespacing=1.35)

# --------------------------------------------------------------------------------------
# 3. STAGE 2: 12-BIT FAST ADC SIGNAL ACQUISITION
# --------------------------------------------------------------------------------------
draw_panel(ax, 4, 73.5, 92, 15.5, 
           title="STAGE 2: 12-BIT FAST ADC SIGNAL QUANTIZATION", 
           subtitle="Hardware-level conversion of analog commutation waveforms into high-resolution digital telemetry",
           border_color="#1e293b", bg_color="#0b1220")

# ADC Specs Grid
adc_items = [
    ("Analog Channel", "ADC0 Ch 0 (Port P000 / Pin 6)"),
    ("Dynamic Input Range", "0.0 V to 3.3 V Reference (VREF)"),
    ("Quantization Levels", "4096 Discrete Steps (2¹² Resolution)"),
    ("Voltage Resolution", "0.805 mV per LSB (3300 mV / 4095)"),
    ("Sampling Window Size", "N = 32 Continuous Samples per Buffer"),
    ("Execution Rate", "50 Hz Deterministic Loop (20 ms Cycle)")
]

for idx, (label, val) in enumerate(adc_items):
    col = idx % 3
    row = idx // 3
    px = 6.5 + col * 30
    py = 81.0 - row * 5.2
    
    card = patches.FancyBboxPatch((px, py), 27, 4.2, boxstyle="round,pad=0.2,rounding_size=0.4",
                                 linewidth=1, edgecolor="#1e293b", facecolor="#111c30")
    ax.add_patch(card)
    ax.text(px + 1.5, py + 2.7, label, fontsize=7.2, color="#94a3b8", fontweight='bold')
    ax.text(px + 1.5, py + 1.0, val, fontsize=8.0, color="#ffffff", fontweight='bold')

# --------------------------------------------------------------------------------------
# 4. STAGE 3: RENESAS RA6E2 EMBEDDED C FIRMWARE ENGINE
# --------------------------------------------------------------------------------------
draw_panel(ax, 4, 46.5, 92, 24.5, 
           title="STAGE 3: RENESAS RA6E2 EMBEDDED C FIRMWARE ENGINE (e² studio)", 
           subtitle="On-chip mathematical algorithms executing in C with Flexible Software Package (FSP) HAL drivers",
           border_color="#1e293b", bg_color="#0b1220")

# Left Column: C Formulas & Algorithms
draw_panel(ax, 6.5, 48.5, 43, 17.5, border_color="#0284c7", bg_color="#111c30")
ax.text(8.5, 63.5, "Core Mathematical Formulations", fontsize=9.2, fontweight='bold', color="#38bdf8")

# Formula 1: True RMS
ax.text(8.5, 60.5, "1. Discrete True RMS Voltage (Single-Cycle FPU):", fontsize=7.6, color="#cbd5e1", fontweight='bold')
ax.text(12.0, 57.5, r"$V_{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} V_i^2} \quad (N = 32)$", fontsize=9.5, color="#38bdf8")

# Formula 2: Adaptive Baseline
ax.text(8.5, 54.0, "2. Adaptive Baseline (Exponential Moving Average):", fontsize=7.6, color="#cbd5e1", fontweight='bold')
ax.text(12.0, 51.5, r"$\mu_t = 0.95 \cdot \mu_{t-1} + 0.05 \cdot V_{RMS}$", fontsize=9.0, color="#10b981")

# Formula 3: Gaussian Z-Score
ax.text(8.5, 48.0, "3. Gaussian Statistical Divergence Z-Score:", fontsize=7.6, color="#cbd5e1", fontweight='bold')
ax.text(12.0, 45.5, r"$Z = \frac{|V_{RMS} - \mu|}{\sigma} \quad [Z \geq 2.0 \rightarrow \mathrm{ANOMALY}]$", fontsize=9.0, color="#f43f5e")

# Right Column: Silicon Hardware Specs
draw_panel(ax, 52.5, 48.5, 41, 17.5, border_color="#10b981", bg_color="#111c30")
ax.text(54.5, 63.5, "Renesas FPB-RA6E2 Silicon Specifications", fontsize=9.2, fontweight='bold', color="#10b981")

mcu_specs = [
    ("Processor Core", "Arm Cortex-M33 running @ 200 MHz"),
    ("Floating-Point Unit", "Single-Precision Hardware FPU & DSP Core"),
    ("Internal Memory", "512 KB Dual-Bank Flash & 128 KB Zero-Wait SRAM"),
    ("On-Chip Temperature", "12-Bit Silicon TSN Diode tracking junction heat (29.4 °C)"),
    ("Security Architecture", "Arm TrustZone with Hardware Cryptographic Engine"),
    ("Development Suite", "Renesas e² studio IDE & Flexible Software Package (FSP)")
]

for idx, (lbl, desc) in enumerate(mcu_specs):
    sy = 60.5 - idx * 2.3
    ax.text(54.5, sy, f"• {lbl}:", fontsize=7.6, color="#94a3b8", fontweight='bold')
    ax.text(68.5, sy, desc, fontsize=7.6, color="#ffffff")

# --------------------------------------------------------------------------------------
# 5. STAGE 4: 60 FPS OPERATOR COCKPIT & LIVE WAVEFORMS
# --------------------------------------------------------------------------------------
draw_panel(ax, 4, 13.5, 92, 30.5, 
           title="STAGE 4: 60 FPS REAL-TIME OSCILLOSCOPE COCKPIT & ACOUSTIC ALERT", 
           subtitle="Single-trace zero-ghosting canvas rendering with 1400 Hz direct laptop speaker alarm",
           border_color="#1e293b", bg_color="#0b1220")

# Waveform 1: Standby
draw_panel(ax, 6.5, 25.5, 27, 13.5, border_color="#475569", bg_color="#111c30")
ax.text(8.5, 36.8, "State 1: Appliance OFF", fontsize=8.8, fontweight='bold', color="#94a3b8")
ax.text(8.5, 34.2, "0.0 mV | 0.00 W | 0.00 sigma (Silent)", fontsize=7.2, color="#64748b")

# Plot flat line
t_pts = np.linspace(8.5, 31.5, 100)
ax.plot(t_pts, np.full_like(t_pts, 29.5), color="#64748b", lw=2.0)
ax.text(20, 27.2, "Dead-Center 0.0 mV Line", fontsize=7.0, color="#64748b", ha='center')

# Waveform 2: Normal Cyan Wave
draw_panel(ax, 36.5, 25.5, 27, 13.5, border_color="#06b6d4", bg_color="#111c30")
ax.text(38.5, 36.8, "State 2: Normal Free-Spin", fontsize=8.8, fontweight='bold', color="#38bdf8")
ax.text(38.5, 34.2, "1085 mV | 0.91 W | 0.35 sigma (Healthy)", fontsize=7.2, color="#06b6d4")

# Plot smooth cyan sine wave
t_pts2 = np.linspace(0, 4*np.pi, 100)
y_sine = 29.5 + 2.8 * np.sin(t_pts2)
x_sine = np.linspace(38.5, 61.5, 100)
ax.plot(x_sine, y_sine, color="#06b6d4", lw=2.0)
ax.text(50, 27.2, "Single-Trace Cyan Sine Wave", fontsize=7.0, color="#06b6d4", ha='center')

# Waveform 3: Anomaly Red Spikes
draw_panel(ax, 66.5, 25.5, 27, 13.5, border_color="#ef4444", bg_color="#111c30")
ax.text(68.5, 36.8, "State 3: Sensor Anomaly", fontsize=8.8, fontweight='bold', color="#f43f5e")
ax.text(68.5, 34.2, "Obstacle | 5.20 sigma | Siren Active!", fontsize=7.2, color="#ef4444")

# Plot sharp red anomaly spikes
t_pts3 = np.linspace(0, 6*np.pi, 100)
y_anom = 29.5 + 3.8 * np.sin(t_pts3) + 1.2 * np.sin(t_pts3 * 2.5)
x_anom = np.linspace(68.5, 91.5, 100)
ax.plot(x_anom, y_anom, color="#ef4444", lw=2.0)
ax.text(80, 27.2, "Violent Red Harmonic Spikes", fontsize=7.0, color="#ef4444", ha='center')

# Bottom Telemetry Highlights Card
draw_panel(ax, 6.5, 15.2, 87, 8.5, border_color="#22c55e", bg_color="#0f291e")
ax.text(8.5, 21.8, "Core Verified Experimental Achievements", fontsize=8.8, fontweight='bold', color="#4ade80")
ax.text(8.5, 19.0, "• 100% Deterministic Execution: Proven sub-20ms latency with zero cloud dependency.", fontsize=7.6, color="#e2e8f0")
ax.text(8.5, 16.8, "• High-Volume Acoustic Alert: 1400 Hz resonant siren synthesized directly in RAM, playing over laptop speakers on fault.", fontsize=7.6, color="#e2e8f0")

# --------------------------------------------------------------------------------------
# 6. FOOTER
# --------------------------------------------------------------------------------------
ax.text(50, 6.0, "Easwari Engineering College (SRM Group) • Department of Electronics and Communication Engineering", 
        fontsize=8.5, color="#94a3b8", ha='center', fontweight='bold')
ax.text(50, 3.2, "Academic Guidance: Dr. Deiva Sundari P (Principal) | Dr. Senthamizh Selvi R (HOD) | Dr. Diana D (Supervisor)", 
        fontsize=7.5, color="#64748b", ha='center')
ax.text(50, 1.2, "Industry Mentorship: Renesas Electronics & Altium Teams (Surendra, Ashish Kumar, Sweta Yadav)", 
        fontsize=7.2, color="#475569", ha='center')

fig.savefig(OUT_PATH_PNG, dpi=300)
fig.savefig(OUT_PATH_PDF)
plt.close(fig)

print(f"Master Professional Academic Poster Successfully Generated!")
print(f"PNG: {OUT_PATH_PNG}")
print(f"PDF: {OUT_PATH_PDF}")
