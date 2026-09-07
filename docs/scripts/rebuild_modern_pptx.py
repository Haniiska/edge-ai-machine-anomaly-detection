"""
Redesign PowerPoint Presentation with Modern High-End Visual Cards & Clean Typography
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_modern_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Modern Palette
    BG_DARK = RGBColor(6, 9, 17)         # #060911
    HEADER_BG = RGBColor(13, 19, 34)     # #0d1322
    CARD_BG = RGBColor(19, 28, 48)       # #131c30
    ACCENT_CYAN = RGBColor(6, 182, 212)  # #06b6d4
    ACCENT_SKY = RGBColor(56, 189, 248)  # #38bdf8
    ACCENT_GREEN = RGBColor(16, 185, 129)# #10b981
    ACCENT_RED = RGBColor(244, 63, 94)   # #f43f5e
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)
    BORDER_COLOR = RGBColor(40, 55, 85)

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

    def add_slide_header(slide, title, category="RENESAS FPB-RA6E2 • EMBEDDED EDGE AI DIAGNOSTICS"):
        h = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.85))
        h.fill.solid()
        h.fill.fore_color.rgb = HEADER_BG
        h.line.color.rgb = BORDER_COLOR
        h.line.width = Pt(1)

        tf = h.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.08)

        p1 = tf.paragraphs[0]
        p1.text = category.upper()
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(17)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.font.name = "Segoe UI"

    def add_glass_card(slide, left, top, width, height, title, items, badge_color=ACCENT_CYAN):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(13)
            p0.font.bold = True
            p0.font.color.rgb = badge_color
            p0.font.name = "Segoe UI"
            p0.space_after = Pt(10)

        for i, item in enumerate(items):
            p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
            p.text = "▸ " + item
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_WHITE
            p.font.name = "Segoe UI"
            p.space_after = Pt(6)

    def add_stat_box(slide, left, top, width, height, val, lbl, sub, color=ACCENT_CYAN):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.12)

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.font.name = "Segoe UI"
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.font.name = "Segoe UI"
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.font.name = "Segoe UI"
        p3.alignment = PP_ALIGN.CENTER

    # 1. TITLE SLIDE
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    hero.fill.solid()
    hero.fill.fore_color.rgb = HEADER_BG
    hero.line.color.rgb = ACCENT_CYAN
    hero.line.width = Pt(2)
    htf = hero.text_frame
    htf.margin_left = Inches(0.6)
    htf.margin_top = Inches(0.5)

    p0 = htf.paragraphs[0]
    p0.text = "RENESAS FPB-RA6E2 EMBEDDED EDGE AI SYSTEM"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN

    p1 = htf.add_paragraph()
    p1.text = "Real-Time Physical Appliance Anomaly Detection\n& True Oscilloscope Cockpit"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = htf.add_paragraph()
    p2.text = "A Hardware-Native Edge Diagnostic Framework for Industrial Rotating Machinery with Sub-20ms Latency"
    p2.font.size = Pt(12)
    p2.font.color.rgb = ACCENT_SKY
    p2.space_after = Pt(22)

    add_stat_box(s1, Inches(1.4), Inches(3.8), Inches(2.4), Inches(1.25), "200 MHz", "Arm Cortex-M33", "Hardware FPU & DSP", ACCENT_CYAN)
    add_stat_box(s1, Inches(4.1), Inches(3.8), Inches(2.4), Inches(1.25), "12-Bit ADC", "Fast True RMS", "50 Hz Sample Window", ACCENT_SKY)
    add_stat_box(s1, Inches(6.8), Inches(3.8), Inches(2.4), Inches(1.25), "< 20 ms", "Edge AI Latency", "Zero Cloud Reliance", ACCENT_GREEN)
    add_stat_box(s1, Inches(9.5), Inches(3.8), Inches(2.4), Inches(1.25), "60 FPS", "Real Oscilloscope", "Single-Trace Cockpit", RGBColor(168, 85, 247))

    # 2. PROBLEM VS SOLUTION
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_slide_header(s2, "Industrial Problem vs. Embedded Edge AI Solution", "CHALLENGE & PARADIGM SHIFT")
    add_glass_card(s2, Inches(0.6), Inches(1.5), Inches(5.8), Inches(5.4), "❌ Traditional Cloud / Static Systems", [
        "High Cloud Latency: > 500 ms round-trip delay fails to prevent physical mechanical damage.",
        "Network Vulnerability: Connection dropouts cause blind spots in machine health monitoring.",
        "Rigid Static Thresholds: Voltage ripples & supply noise trigger costly false alarms.",
        "High Bandwidth Overhead: Streaming raw high-frequency waveforms to servers is expensive."
    ], ACCENT_RED)
    add_glass_card(s2, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.4), "✅ Our Renesas RA6E2 Edge AI Solution", [
        "Deterministic Sub-20ms Latency: Immediate on-chip fault isolation and emergency siren triggering.",
        "100% Autonomous on Silicon: Operates standalone with zero internet or cloud subscription costs.",
        "Adaptive Gaussian ML: Dynamic Z-Score model separates harmless electrical drift from true faults.",
        "Dual-Domain Diagnostics: Simultaneously covers internal electromechanical health & optical obstacles."
    ], ACCENT_GREEN)

    # 3. PIPELINE BLOCK DIAGRAM
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_slide_header(s3, "End-to-End System Block Diagram & Flow", "4-STAGE DIAGNOSTIC PIPELINE")
    add_glass_card(s3, Inches(0.6), Inches(1.5), Inches(2.6), Inches(4.5), "1. PHYSICAL LOAD", [
        "12V DC Brushless Fan",
        "Rotating motor dynamics",
        "Back-EMF electrical line",
        "Physical 12V switch control"
    ], ACCENT_CYAN)
    add_glass_card(s3, Inches(3.8), Inches(1.5), Inches(2.6), Inches(4.5), "2. SENSOR INTERFACE", [
        "Precision Voltage Divider",
        "12-Bit Fast ADC0 (P000)",
        "Active-Low IR Sensor (P001)",
        "On-Chip TSN Temp Sensor"
    ], ACCENT_SKY)
    add_glass_card(s3, Inches(7.0), Inches(1.5), Inches(2.6), Inches(4.5), "3. RENESAS RA6E2", [
        "Arm Cortex-M33 @ 200 MHz",
        "50 Hz True RMS Math",
        "Dynamic Power (0.91 W)",
        "Gaussian Z-Score ML Model"
    ], ACCENT_GREEN)
    add_glass_card(s3, Inches(10.2), Inches(1.5), Inches(2.5), Inches(4.5), "4. 60 FPS COCKPIT", [
        "Single-Trace Oscilloscope",
        "Quad Telemetry Cards",
        "Z-Score Arc Dial Gauge",
        "1400 Hz Emergency Siren"
    ], RGBColor(168, 85, 247))

    # 4. RENESAS PERIPHERALS
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_slide_header(s4, "Renesas FPB-RA6E2 Hardware & Silicon Architecture", "MICROCONTROLLER SPECIFICATIONS")
    add_glass_card(s4, Inches(0.6), Inches(1.5), Inches(5.8), Inches(2.6), "⚡ Arm® Cortex®-M33 Core @ 200 MHz", [
        "Hardware Single-Precision FPU & DSP instructions for single-cycle float32 RMS math.",
        "512 KB Dual-Bank Flash & 128 KB SRAM enabling zero-wait state execution."
    ], ACCENT_CYAN)
    add_glass_card(s4, Inches(6.8), Inches(1.5), Inches(5.9), Inches(2.6), "📊 12-Bit Fast ADC0 Module", [
        "Dedicated 12-bit successive approximation ADC with < 1 us conversion speed.",
        "4096 discrete quantization steps (0.805 mV per code resolution) for back-EMF."
    ], ACCENT_SKY)
    add_glass_card(s4, Inches(0.6), Inches(4.3), Inches(5.8), Inches(2.6), "🌡️ On-Chip Silicon TSN Sensor", [
        "Internal 12-bit sensor tracking core junction temperature (nominal 29.4 °C).",
        "Guards against thermal runaway without requiring external thermistors."
    ], ACCENT_GREEN)
    add_glass_card(s4, Inches(6.8), Inches(4.3), Inches(5.9), Inches(2.6), "🛠️ Renesas e² studio & FSP Ecosystem", [
        "Built with official Flexible Software Package (FSP) production HAL drivers.",
        "Port Function Select (PFS) configuring digital pull-ups on Port P001."
    ], RGBColor(168, 85, 247))

    # 5. STATE MACHINE MATRIX
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_slide_header(s5, "Verified Operational State Machine Matrix", "PHYSICAL HARDWARE TEST RESULTS")
    add_glass_card(s5, Inches(0.6), Inches(1.5), Inches(3.8), Inches(5.4), "🔌 State 1: Appliance OFF", [
        "Physical 12V Power Switch is turned OFF.",
        "Voltage Level: 0.0 mV (Zero load).",
        "Waveform: Strict 0.0 mV Flat Zero Line.",
        "Telemetry: 0.00 W Power | 29.4 °C | 0.00 sigma.",
        "Acoustic State: Completely Silent (0 Faults)."
    ], TEXT_MUTED)
    add_glass_card(s5, Inches(4.7), Inches(1.5), Inches(3.8), Inches(5.4), "⚡ State 2: Normal Free-Spin", [
        "Fan spinning freely at full speed.",
        "Voltage Level: Nominal ~1085.0 mV.",
        "Waveform: 100% Constant Solid Cyan Sine Wave.",
        "Telemetry: 0.91 W Power | 29.4 °C | 0.35 sigma.",
        "Acoustic State: Completely Silent (NOMINAL)."
    ], ACCENT_GREEN)
    add_glass_card(s5, Inches(8.8), Inches(1.5), Inches(3.9), Inches(5.4), "🚨 State 3: Anomaly / Obstacle", [
        "IR Sensor Obstruction or Blade Drag.",
        "Trigger Event: Sensor Pin = LOW or Voltage < 500 mV.",
        "Waveform: Solid Violent Red Spike Harmonics.",
        "Acoustic Alert: Continuous 1400 Hz Siren + Fault +1.",
        "Recovery: Siren mutes instantly upon obstacle removal."
    ], ACCENT_RED)

    # 6. CONCLUSION & ACKNOWLEDGMENTS
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_slide_header(s6, "Conclusion & Formal Acknowledgments", "SUMMARY & INSTITUTIONAL MENTORSHIP")
    add_glass_card(s6, Inches(0.6), Inches(1.5), Inches(5.8), Inches(5.4), "🏆 Project Achievements", [
        "Full Hardware Integration: Completed on Renesas FPB-RA6E2 with 12V fan & IR sensor.",
        "Deterministic Edge Execution: Proven sub-20ms latency with zero cloud dependency.",
        "100% Verified States: Perfect reliability across OFF, Normal Free-Spin, and Anomaly.",
        "Industry 4.0 Ready: Scalable foundation for commercial predictive maintenance."
    ], ACCENT_CYAN)
    add_glass_card(s6, Inches(6.8), Inches(1.5), Inches(5.9), Inches(5.4), "🙏 Formal Acknowledgments", [
        "Academic Leadership & Guidance:",
        "  • Dr. Deiva Sundari P (Principal, Easwari Engineering College)",
        "  • Dr. Senthamizh Selvi R (HOD, Department of ECE)",
        "  • Dr. Diana D (Associate Professor, Department of ECE)",
        "  • Easwari Engineering College (SRM Group).",
        "Industry Mentorship & Support:",
        "  • Renesas Electronics Team & Altium",
        "  • Surendra, Ashish Kumar, and Sweta Yadav for step-by-step technical guidance."
    ], ACCENT_SKY)

    out_ppt = r"C:\Users\WELCOME\Desktop\Embedded_EdgeAI_AnomalyDetection_Visual_Master.pptx"
    prs.save(out_ppt)
    print("Modern Deck Saved to Desktop.")

if __name__ == "__main__":
    build_modern_deck()
