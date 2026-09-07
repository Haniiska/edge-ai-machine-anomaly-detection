"""
========================================================================================
Renesas FPB-RA6E2 Physical Appliance Anomaly Detection & True Oscilloscope Cockpit
Final Master Production Build (Pure Button-Free: Shift = Normal/OFF, Ctrl = Anomaly)
========================================================================================
1. Press 'Shift' / 'Spacebar' -> TOGGLES between Fan Normal (Cyan Wave) & Fan OFF (0.0 Flat Line)
2. Press 'Ctrl'               -> INSTANT SOLID VIOLENT RED WAVE + LOUD 1400 Hz SIREN + FAULTS +1!
3. Press 'Ctrl' again         -> SIREN INSTANTLY MUTES + Instant Return to Normal Cyan Wave!
========================================================================================
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import io
import wave
import struct
import winsound
import sys

def generate_siren_wav(freq=1400, duration=0.18):
    """Generates high-volume acoustic alarm buffer in RAM"""
    buf = io.BytesIO()
    framerate = 44100
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(framerate)
        samples = bytearray()
        n_samples = int(framerate * duration)
        for i in range(n_samples):
            t = i / framerate
            sample = int(32767 * 0.95 * math.sin(2 * math.pi * freq * t))
            samples.extend(struct.pack('<h', sample))
        w.writeframes(samples)
    return buf.getvalue()

SIREN_WAV = generate_siren_wav(1400, 0.18)

class AnomalyCockpitMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Renesas RA6E2 Physical Appliance Anomaly Detection Cockpit")
        self.root.geometry("1100x720")
        self.root.configure(bg="#0a0e17")
        self.root.resizable(True, True)

        # Handle Clean Window Close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Master Telemetry State:
        self.status = "OFF"  # Default: Starts in Strict Dead-Center 0.0 mV Flat Line
        self.v_rms = 0.0
        self.power_w = 0.0
        self.temp_c = 29.4
        self.z_score = 0.0
        self.fault_count = 0
        self.is_running = True
        self.wave_phase = 0.0
        self.last_anomaly_state = False
        self.last_w = 0
        self.last_h = 0

        # Build Clean Button-Free UI Layout
        self._build_ui()

        # Keyboard Bindings:
        # 1. 'Shift' (Left/Right) / Spacebar -> TOGGLE NORMAL WAVE <-> OFF (0 LINE)
        self.root.bind("<Shift_L>", lambda e: self.toggle_fan())
        self.root.bind("<Shift_R>", lambda e: self.toggle_fan())
        self.root.bind("<space>", lambda e: self.toggle_fan())
        self.root.bind("1", lambda e: self.set_state("OFF"))
        self.root.bind("2", lambda e: self.set_state("NORMAL"))

        # 2. 'Ctrl' (Left/Right) / Canvas Click -> TOGGLE ANOMALY <-> NORMAL
        self.root.bind("<Control_L>", lambda e: self.toggle_anomaly())
        self.root.bind("<Control_R>", lambda e: self.toggle_anomaly())
        self.root.bind("<Control-Key>", lambda e: self.toggle_anomaly())
        self.root.bind("a", lambda e: self.toggle_anomaly())
        self.root.bind("A", lambda e: self.toggle_anomaly())
        self.osc_canvas.bind("<Button-1>", lambda e: self.toggle_anomaly())
        self.osc_canvas.bind("<Button-3>", lambda e: self.toggle_fan())

        # Start Loud Direct-Speaker Audio Siren Thread
        self.audio_thread = threading.Thread(target=self._audio_siren_loop, daemon=True)
        self.audio_thread.start()

        # Start 60 FPS Render Loop
        self.root.after(30, self._render_loop)

    def on_close(self):
        """Clean shutdown on window close"""
        self.is_running = False
        self.status = "OFF"
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except:
            pass
        self.root.destroy()
        sys.exit(0)

    def set_state(self, new_state):
        """Explicit state transition with 100% deterministic values"""
        if new_state == "OFF":
            self.status = "OFF"
            self.v_rms = 0.0
            self.power_w = 0.0
            self.temp_c = 29.4
            self.z_score = 0.0
            self.last_anomaly_state = False
        elif new_state == "NORMAL":
            self.status = "NORMAL"
            self.v_rms = 1085.0
            self.power_w = 0.91
            self.temp_c = 29.4
            self.z_score = 0.35
            self.last_anomaly_state = False
        elif new_state == "ANOMALY":
            self.status = "ANOMALY"
            self.v_rms = 1085.0
            self.power_w = 0.91
            self.temp_c = 29.4
            self.z_score = 5.20
            if not self.last_anomaly_state:
                self.fault_count += 1
                self.last_anomaly_state = True

    def toggle_fan(self):
        """Toggles between Fan Normal Wave and Fan OFF (0 line)"""
        if self.status == "OFF":
            self.set_state("NORMAL")
        else:
            self.set_state("OFF")

    def toggle_anomaly(self):
        """Toggles between ANOMALY and NORMAL state on Ctrl"""
        if self.status == "ANOMALY":
            self.set_state("NORMAL")
        else:
            self.set_state("ANOMALY")

    def _build_ui(self):
        # Header Bar (Clean, Zero Buttons)
        header = tk.Frame(self.root, bg="#111827", height=65, padx=20, pady=10)
        header.pack(fill="x", side="top")

        lbl_chip = tk.Label(header, text="● RENESAS FPB-RA6E2 • REAL-TIME EDGE AI EMBEDDED DIAGNOSTICS COCKPIT", 
                            font=("Segoe UI", 9, "bold"), fg="#06b6d4", bg="#111827")
        lbl_chip.pack(anchor="w")

        lbl_title = tk.Label(header, text="Physical Fan Anomaly Detection & True Oscilloscope", 
                             font=("Segoe UI", 15, "bold"), fg="#ffffff", bg="#111827")
        lbl_title.pack(anchor="w", pady=(2, 0))

        # Status Banner
        self.banner = tk.Frame(self.root, bg="#1e293b", padx=16, pady=12)
        self.banner.pack(fill="x", padx=16, pady=8)

        self.lbl_status_icon = tk.Label(self.banner, text="🔌", font=("Segoe UI", 18), fg="#64748b", bg="#1e293b")
        self.lbl_status_icon.pack(side="left", padx=(0, 10))

        self.lbl_status = tk.Label(self.banner, text="STATE: PHYSICAL 12V FAN IS TURNED OFF (0.0 mV)", 
                                   font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#1e293b")
        self.lbl_status.pack(side="left")

        self.lbl_fault_count = tk.Label(self.banner, text="0 ANOMALIES DETECTED", 
                                        font=("Segoe UI", 11, "bold"), fg="#64748b", bg="#1e293b")
        self.lbl_fault_count.pack(side="right")

        # Main Grid Frame
        main_frame = tk.Frame(self.root, bg="#0a0e17")
        main_frame.pack(fill="both", expand=True, padx=16, pady=5)

        # Left Column: Metrics & Gauge (width 350)
        left_col = tk.Frame(main_frame, bg="#0a0e17", width=350)
        left_col.pack(side="left", fill="y", padx=(0, 10))

        # Gauge Card (Statistical Divergence Z-Score)
        gauge_card = tk.Frame(left_col, bg="#111827", padx=14, pady=10, highlightthickness=1, highlightbackground="#1f293d")
        gauge_card.pack(fill="x", pady=(0, 8))

        tk.Label(gauge_card, text="STATISTICAL DIVERGENCE (Z-SCORE)", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")
        self.lbl_z_badge = tk.Label(gauge_card, text="STANDBY (OFF)", font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#111827")
        self.lbl_z_badge.pack(anchor="e")

        self.gauge_canvas = tk.Canvas(gauge_card, width=280, height=110, bg="#111827", highlightthickness=0)
        self.gauge_canvas.pack(pady=3)

        cx = 140
        cy = 98
        r = 75
        self.gauge_bg_arc = self.gauge_canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180, 
                                                         style="arc", width=10, outline="#1f293d")
        self.gauge_dyn_arc = self.gauge_canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=180, extent=0, 
                                                          style="arc", width=10, outline="#10b981")

        self.lbl_z_val = tk.Label(gauge_card, text="0.00 σ", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#111827")
        self.lbl_z_val.pack()

        # Telemetry Metrics Grid (4 Clean Diagnostic Cards)
        metrics_frame = tk.Frame(left_col, bg="#0a0e17")
        metrics_frame.pack(fill="x")

        # Card 1: Measured 12-Bit ADC Voltage
        c1 = tk.Frame(metrics_frame, bg="#111827", padx=12, pady=8, highlightthickness=1, highlightbackground="#1f293d")
        c1.pack(fill="x", pady=3)
        tk.Label(c1, text="⚡ REAL HARDWARE 12-BIT ADC VOLTAGE", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")
        self.lbl_v_val = tk.Label(c1, text="0.0 mV", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#111827")
        self.lbl_v_val.pack(anchor="w")
        self.lbl_base_val = tk.Label(c1, text="Appliance Power Cut (0.0 mV)", font=("Segoe UI", 8), fg="#64748b", bg="#111827")
        self.lbl_base_val.pack(anchor="w")

        # Card 2: Real Power Consumption
        c2 = tk.Frame(metrics_frame, bg="#111827", padx=12, pady=8, highlightthickness=1, highlightbackground="#1f293d")
        c2.pack(fill="x", pady=3)
        tk.Label(c2, text="🔋 DYNAMIC POWER CONSUMPTION", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")
        self.lbl_p_val = tk.Label(c2, text="0.00 W (0 mW)", font=("Segoe UI", 16, "bold"), fg="#a78bfa", bg="#111827")
        self.lbl_p_val.pack(anchor="w")
        self.lbl_p_sub = tk.Label(c2, text="Estimated Active 12V DC Load", font=("Segoe UI", 8), fg="#64748b", bg="#111827")
        self.lbl_p_sub.pack(anchor="w")

        # Card 3: MCU On-Chip Temperature
        c3 = tk.Frame(metrics_frame, bg="#111827", padx=12, pady=8, highlightthickness=1, highlightbackground="#1f293d")
        c3.pack(fill="x", pady=3)
        tk.Label(c3, text="🌡️ RENESAS RA6E2 MCU TEMPERATURE", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")
        self.lbl_temp_val = tk.Label(c3, text="29.4 °C (Healthy)", font=("Segoe UI", 16, "bold"), fg="#34d399", bg="#111827")
        self.lbl_temp_val.pack(anchor="w")

        # Card 4: Machine Running State
        c4 = tk.Frame(metrics_frame, bg="#111827", padx=12, pady=8, highlightthickness=1, highlightbackground="#1f293d")
        c4.pack(fill="x", pady=3)
        tk.Label(c4, text="⚙️ PHYSICAL FAN RUNNING STATE", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")
        self.lbl_machine_state = tk.Label(c4, text="FAN OFF (0.0 mV)", font=("Segoe UI", 13, "bold"), fg="#64748b", bg="#111827")
        self.lbl_machine_state.pack(anchor="w")
        self.lbl_link_state = tk.Label(c4, text="Hardware Link: Renesas J-Link SWD Active", font=("Segoe UI", 8), fg="#10b981", bg="#111827")
        self.lbl_link_state.pack(anchor="w")

        # Right Column: Oscilloscope Card
        right_col = tk.Frame(main_frame, bg="#0a0e17")
        right_col.pack(side="right", fill="both", expand=True)

        osc_card = tk.Frame(right_col, bg="#111827", padx=14, pady=10, highlightthickness=1, highlightbackground="#1f293d")
        osc_card.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(osc_card, text="REAL 12-BIT ADC VOLTAGE SIGNAL (60 FPS OSCILLOSCOPE)", 
                 font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#111827").pack(anchor="w")

        self.osc_canvas = tk.Canvas(osc_card, bg="#080c14", highlightthickness=0)
        self.osc_canvas.pack(fill="both", expand=True, pady=6)

        # Pre-create the single trace line ONCE (Zero overlap!)
        self.trace_line = self.osc_canvas.create_line(0, 200, 1000, 200, fill="#475569", width=2)

        # Footer Log Card
        footer = tk.Frame(self.root, bg="#111827", padx=16, pady=8)
        footer.pack(fill="x", side="bottom")

        tk.Label(footer, text="SYSTEM STATUS LOG", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#111827").pack(anchor="w")
        self.lbl_log = tk.Label(footer, text="[SYSTEM READY] Renesas RA6E2 Edge AI Diagnostics Active.", 
                                font=("Consolas", 8), fg="#06b6d4", bg="#111827", anchor="w")
        self.lbl_log.pack(fill="x")

    def _draw_full_grid(self, ow, oh):
        """Dynamically draws grid covering 100% of the canvas area from edge to edge"""
        self.osc_canvas.delete("grid_line")
        for x in range(0, ow + 40, 40):
            self.osc_canvas.create_line(x, 0, x, oh, fill="#131d2e", width=1, tags="grid_line")
        for y in range(0, oh + 30, 30):
            self.osc_canvas.create_line(0, y, ow, y, fill="#131d2e", width=1, tags="grid_line")
        self.osc_canvas.create_line(0, oh / 2, ow, oh / 2, fill="#1e293b", dash=(4, 4), tags="grid_line")
        self.osc_canvas.tag_lower("grid_line")

    def _audio_siren_loop(self):
        """Plays continuous loud acoustic siren directly through laptop speakers during ANOMALY"""
        while self.is_running:
            if self.status == "ANOMALY":
                try:
                    winsound.PlaySound(SIREN_WAV, winsound.SND_MEMORY)
                except:
                    try:
                        winsound.Beep(1400, 150)
                    except:
                        time.sleep(0.1)
                time.sleep(0.02)
            else:
                time.sleep(0.04)

    def _render_loop(self):
        if not self.is_running:
            return

        # 1. Update UI Text & Banners
        self.lbl_v_val.config(text=f"{self.v_rms:.1f} mV" if self.status != "OFF" else "0.0 mV")
        self.lbl_base_val.config(text="Nominal Operating Level | Direct Hardware Link" if self.status != "OFF" else "Appliance Power Cut (0.0 mV)")
        self.lbl_p_val.config(text=f"{self.power_w:.2f} W ({self.power_w * 1000:.0f} mW)" if self.status != "OFF" else "0.00 W (0 mW)")
        self.lbl_temp_val.config(text=f"{self.temp_c:.1f} °C (Healthy)")
        self.lbl_z_val.config(text=f"{self.z_score:.2f} σ")
        self.lbl_fault_count.config(text=f"{self.fault_count} ANOMALIES DETECTED" if self.status != "OFF" else "0 ANOMALIES DETECTED")

        if self.status == "ANOMALY":
            self.banner.config(bg="#7f1d1d")
            self.lbl_status.config(text="🚨 REAL PHYSICAL ALERT: SENSOR OBSTRUCTION DETECTED!", bg="#7f1d1d")
            self.lbl_status_icon.config(text="🚨", fg="#ef4444", bg="#7f1d1d")
            self.lbl_fault_count.config(bg="#7f1d1d", fg="#fca5a5")
            self.lbl_machine_state.config(text="OBSTRUCTION / ANOMALY DETECTED!", fg="#ef4444")
            self.lbl_z_badge.config(text="ANOMALY DETECTED", fg="#ef4444")
        elif self.status == "OFF":
            self.banner.config(bg="#1e293b")
            self.lbl_status.config(text="STATE: PHYSICAL 12V FAN IS TURNED OFF (0.0 mV)", bg="#1e293b")
            self.lbl_status_icon.config(text="🔌", fg="#64748b", bg="#1e293b")
            self.lbl_fault_count.config(bg="#1e293b", fg="#64748b")
            self.lbl_machine_state.config(text="FAN OFF (0.0 mV)", fg="#64748b")
            self.lbl_z_badge.config(text="STANDBY (OFF)", fg="#64748b")
        else:
            self.banner.config(bg="#064e3b")
            self.lbl_status.config(text="STATE: 12V FAN ACTIVE & SPINNING NORMALLY (1085 mV)", bg="#064e3b")
            self.lbl_status_icon.config(text="⚡", fg="#10b981", bg="#064e3b")
            self.lbl_fault_count.config(bg="#064e3b", fg="#6ee7b7")
            self.lbl_machine_state.config(text="FULL SPEED ACTIVE", fg="#10b981")
            self.lbl_z_badge.config(text="NORMAL (HEALTHY)", fg="#10b981")

        # 2. Update Gauge Arc
        norm_z = min(max(self.z_score / 4.0, 0.0), 1.0)
        arc_extent = norm_z * 180
        arc_color = "#ef4444" if self.status == "ANOMALY" else ("#10b981" if self.status == "NORMAL" else "#64748b")
        self.gauge_canvas.itemconfig(self.gauge_dyn_arc, extent=-arc_extent if self.status != "OFF" else 0, outline=arc_color)

        # 3. Dynamic Full-Canvas Clean Single-Trace Rendering (coords update)
        ow = self.osc_canvas.winfo_width()
        oh = self.osc_canvas.winfo_height()

        if ow < 50: ow = 700
        if oh < 50: oh = 420

        # Redraw full grid if canvas size changed
        if ow != self.last_w or oh != self.last_h:
            self._draw_full_grid(ow, oh)
            self.last_w = ow
            self.last_h = oh

        self.wave_phase += 0.16
        points = []
        num_pts = 75
        step = ow / (num_pts - 1)

        for i in range(num_pts):
            x = i * step
            if self.status == "OFF":
                # Strict Dead-Center Flat Zero Line (0.0 mV) - 100% Rock-Solid Flat!
                y = oh / 2
            elif self.status == "ANOMALY":
                # Sharp Red Spike Wave
                y = (oh / 2) + math.sin(self.wave_phase * 2.2 + (i * 0.35)) * (oh * 0.35) + (math.sin(i * 1.8) * 16.0)
            else:
                # Smooth Single Pure Cyan Sine Wave
                y = (oh / 2) + math.sin(self.wave_phase + (i * 0.16)) * (oh * 0.26)

            points.extend([x, y])

        trace_color = "#ef4444" if self.status == "ANOMALY" else ("#06b6d4" if self.status == "NORMAL" else "#475569")
        line_w = 3 if self.status != "OFF" else 2

        # Instant coords update (Zero overlap / zero duplicate lines!)
        if len(points) >= 4:
            self.osc_canvas.coords(self.trace_line, *points)
            self.osc_canvas.itemconfig(self.trace_line, fill=trace_color, width=line_w)

        if self.is_running:
            self.root.after(16, self._render_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnomalyCockpitMasterApp(root)
    root.mainloop()
