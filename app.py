import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="Betriebssystem-Simulator Pro",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialisierung ---
if 'terminal_history' not in st.session_state:
    st.session_state.terminal_history = []
if 'current_directory' not in st.session_state:
    st.session_state.current_directory = "C:\\"
if 'battery_level' not in st.session_state:
    st.session_state.battery_level = random.randint(60, 100)

# --- Erweiterte CSS Styles ---
st.markdown("""
<style>
    /* Globale Styles */
    .main {
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* DOS Terminal */
    .dos-screen {
        background-color: #0000AA;
        color: #FFFFFF;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        font-size: 16px;
        line-height: 1.3;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        position: relative;
    }
    
    .dos-screen::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.15),
            rgba(0, 0, 0, 0.15) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
    }
    
    .dos-line {
        margin: 3px 0;
        position: relative;
        z-index: 1;
    }
    
    .dos-cursor {
        display: inline-block;
        width: 10px;
        height: 16px;
        background-color: #FFFFFF;
        animation: blink 1s infinite;
        margin-left: 5px;
    }
    
    @keyframes blink {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
    }
    
    /* Windows Desktop */
    .windows-screen {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 600px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        padding-bottom: 60px;
    }
    
    .windows-desktop-content {
        padding: 30px;
        min-height: 540px;
    }
    
    .windows-taskbar {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 48px;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(20px) saturate(180%);
        display: flex;
        align-items: center;
        padding: 0 10px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .windows-icon {
        width: 80px;
        height: 80px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        cursor: pointer;
        transition: all 0.2s;
        margin: 10px;
    }
    
    .windows-icon:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .windows-icon-emoji {
        font-size: 36px;
    }
    
    .windows-icon-label {
        font-size: 11px;
        color: white;
        text-align: center;
    }
    
    .windows-window {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(40px);
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        overflow: hidden;
        margin: 20px;
        animation: windowOpen 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes windowOpen {
        from {
            transform: scale(0.9);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .windows-titlebar {
        background: #f3f3f3;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .windows-window-content {
        padding: 20px;
        background: white;
    }
    
    /* macOS Desktop */
    .macos-screen {
        background: linear-gradient(180deg, #4A90E2 0%, #7B68EE 100%);
        min-height: 650px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .macos-menubar {
        height: 28px;
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(20px) saturate(180%);
        display: flex;
        align-items: center;
        padding: 0 15px;
        font-size: 13px;
        color: white;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    .macos-menu-item {
        padding: 0 12px;
        cursor: pointer;
        border-radius: 4px;
        height: 22px;
        display: flex;
        align-items: center;
    }
    
    .macos-menu-item:hover {
        background-color: rgba(255,255,255,0.2);
    }
    
    .macos-desktop-content {
        padding: 40px 30px;
        min-height: 550px;
    }
    
    .macos-dock {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(40px) saturate(180%);
        border-radius: 16px;
        padding: 8px;
        display: flex;
        gap: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.18);
    }
    
    .macos-dock-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(145deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .macos-dock-icon:hover {
        transform: translateY(-10px) scale(1.1);
    }
    
    .macos-window {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(40px);
        border-radius: 10px;
        box-shadow: 0 12px 48px rgba(0,0,0,0.3);
        overflow: hidden;
        margin: 20px;
        animation: macWindowOpen 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes macWindowOpen {
        from {
            transform: scale(0.8);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .macos-titlebar {
        background: #f6f6f6;
        height: 40px;
        display: flex;
        align-items: center;
        padding: 0 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .macos-traffic-lights {
        display: flex;
        gap: 8px;
    }
    
    .macos-traffic-light {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 0.5px solid rgba(0,0,0,0.1);
    }
    
    .macos-traffic-light.close {
        background: linear-gradient(145deg, #ff605c, #ff3b30);
    }
    
    .macos-traffic-light.minimize {
        background: linear-gradient(145deg, #ffbd44, #ff9500);
    }
    
    .macos-traffic-light.maximize {
        background: linear-gradient(145deg, #00ca4e, #28cd41);
    }
    
    .macos-window-title {
        flex-grow: 1;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        color: #333;
    }
    
    /* Linux Terminal */
    .linux-screen {
        background-color: #300A24;
        color: #FFFFFF;
        font-family: 'Ubuntu Mono', 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        font-size: 14px;
        line-height: 1.5;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .linux-prompt {
        color: #8AE234;
        font-weight: bold;
    }
    
    .linux-path {
        color: #729FCF;
    }
    
    /* Mobile Screens */
    .phone-container {
        max-width: 375px;
        margin: 20px auto;
        background: #1a1a1a;
        border-radius: 40px;
        padding: 12px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .phone-screen {
        width: 100%;
        height: 700px;
        border-radius: 32px;
        overflow: hidden;
        position: relative;
        display: flex;
        flex-direction: column;
    }
    
    .android-screen {
        background: linear-gradient(180deg, #1a73e8 0%, #4285f4 100%);
    }
    
    .ios-screen {
        background: linear-gradient(180deg, #000428 0%, #004e92 100%);
    }
    
    .phone-statusbar {
        height: 28px;
        background: rgba(0,0,0,0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 15px;
        font-size: 11px;
        color: white;
    }
    
    .phone-content {
        flex-grow: 1;
        padding: 20px;
        overflow-y: auto;
    }
    
    .app-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-top: 20px;
    }
    
    .app-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    
    .app-icon-circle {
        width: 60px;
        height: 60px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .app-label {
        font-size: 11px;
        color: white;
        text-align: center;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0,0,0,0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0,0,0,0.5);
    }
    
    /* Command Input Area */
    .command-input-area {
        margin-top: 20px;
        padding: 15px;
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- OS Daten ---
os_data = {
    "DOS": {
        "Hersteller": "Microsoft",
        "Einsatzbereich": "Desktop",
        "Besonderheiten": "Kommandozeilenbasiert, Grundlage für frühe Windows-Versionen",
        "Unterscheidungsmerkmale": "Einfach, stabil, keine grafische Benutzeroberfläche",
        "Betriebsarten": "Singletasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "1981",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor",
        "icon": "💾",
        "color": "#0000AA"
    },
    "Windows": {
        "Hersteller": "Microsoft",
        "Einsatzbereich": "Desktop, Server",
        "Besonderheiten": "Weit verbreitet, benutzerfreundlich, viele Anwendungen verfügbar",
        "Unterscheidungsmerkmale": "Benutzerfreundliche Oberfläche, breite Hardware-Kompatibilität",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1985",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor",
        "icon": "🪟",
        "color": "#0078D4"
    },
    "macOS": {
        "Hersteller": "Apple",
        "Einsatzbereich": "Desktop, Laptop",
        "Besonderheiten": "Nahtlose Integration mit Apple-Produkten",
        "Unterscheidungsmerkmale": "Elegantes Design, hohe Sicherheit",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2001",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Mehrprozessor",
        "icon": "",
        "color": "#000000"
    },
    "Linux": {
        "Hersteller": "Open Source Community",
        "Einsatzbereich": "Desktop, Server, Embedded",
        "Besonderheiten": "Open Source, hochgradig anpassbar",
        "Unterscheidungsmerkmale": "Freie Software, starke Community",
        "Betriebsarten": "Multitasking, Timesharing, Echtzeit",
        "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1991",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Mehrprozessor",
        "icon": "🐧",
        "color": "#FCC624"
    },
    "Android": {
        "Hersteller": "Google",
        "Einsatzbereich": "Mobile Geräte",
        "Besonderheiten": "Marktführer bei mobilen OS",
        "Unterscheidungsmerkmale": "Open Source, riesige App-Auswahl",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2008",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Mehrprozessor",
        "icon": "🤖",
        "color": "#3DDC84"
    },
    "iOS": {
        "Hersteller": "Apple",
        "Einsatzbereich": "Mobile Geräte",
        "Besonderheiten": "Exklusiv für iPhone/iPad",
        "Unterscheidungsmerkmale": "Geschlossenes System, höchste Sicherheit",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2007",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Mehrprozessor",
        "icon": "",
        "color": "#007AFF"
    }
}

def get_current_time():
    return datetime.now().strftime("%H:%M")

def get_current_date():
    return datetime.now().strftime("%a, %d. %B")

# --- Header ---
st.markdown(f"""
<div style='text-align: center; padding: 20px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
     border-radius: 10px; margin-bottom: 30px; color: white;'>
    <h1 style='margin: 0; font-size: 2.5em;'>💻 Betriebssystem-Simulator Pro</h1>
    <p style='margin: 10px 0 0 0; opacity: 0.9;'>Erleben Sie die Evolution der Betriebssysteme</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎮 Betriebssystem wählen")
    
    selected_os_name = st.selectbox(
        "Betriebssystem:",
        list(os_data.keys()),
        format_func=lambda x: f"{os_data[x]['icon']} {x}",
        key="os_selector"
    )
    
    selected_os_info = os_data[selected_os_name]
    
    st.markdown("---")
    st.markdown("### 📊 Systeminformationen")
    
    with st.expander("Details anzeigen", expanded=False):
        for key, value in selected_os_info.items():
            if key not in ['icon', 'color']:
                st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    show_hints = st.checkbox("💡 Hilfestellungen anzeigen", value=True)
    realistic_delays = st.checkbox("⏱️ Realistische Verzögerungen", value=False)

# --- Hauptbereich ---
selected_os_info = os_data[selected_os_name]

# System-Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {selected_os_info['color']}22, {selected_os_info['color']}44); 
         padding: 20px; border-radius: 10px; border-left: 4px solid {selected_os_info['color']};'>
        <h2 style='margin: 0; color: {selected_os_info['color']};'>{selected_os_info['icon']} {selected_os_name}</h2>
        <p style='margin: 5px 0 0 0; opacity: 0.8;'>{selected_os_info['Besonderheiten']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Erscheinungsjahr", selected_os_info['Erst-erscheinung'])

with col3:
    st.metric("Hersteller", selected_os_info['Hersteller'])

st.markdown("---")

# === DOS Simulation ===
if selected_os_name == "DOS":
    if show_hints:
        st.info("🕹️ **DOS** - Probieren Sie: `dir`, `cd`, `type`, `cls`, `ver`, `help`, `date`, `time`")
    
    # Initialize DOS history
    if 'dos_history' not in st.session_state:
        st.session_state.dos_history = [
            "Microsoft(R) MS-DOS(R) Version 6.22",
            "             (C)Copyright Microsoft Corp 1981-1994.",
            "",
            "C:\\>"
        ]
    
    # DOS Screen
    dos_html = '<div class="dos-screen">'
    for line in st.session_state.dos_history:
        dos_html += f'<div class="dos-line">{line}</div>'
    dos_html += '<div class="dos-line"><span class="dos-cursor"></span></div>'
    dos_html += '</div>'
    
    st.markdown(dos_html, unsafe_allow_html=True)
    
    # Command Input below the screen
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        dos_command = st.text_input(
            "DOS Befehl:",
            key="dos_cmd",
            placeholder="Befehl eingeben (z.B. dir)...",
            label_visibility="collapsed"
        )
    with col2:
        execute_button = st.button("⏎", key="dos_exec", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if execute_button and dos_command:
        cmd = dos_command.lower().strip()
        st.session_state.dos_history.append(f"C:\\>{dos_command}")
        
        if realistic_delays:
            time.sleep(0.3)
        
        # DOS Befehle
        if cmd == "dir":
            st.session_state.dos_history.extend([
                " Volume in Laufwerk C: hat keine Bezeichnung.",
                " Volumeseriennummer: 1A2B-3C4D",
                "",
                " Verzeichnis von C:\\",
                "",
                "DOS          <DIR>     01.01.1994   9:00",
                "WINDOWS      <DIR>     01.01.1994   9:30",
                "COMMAND  COM    54,645 01.01.1994  10:00",
                "AUTOEXEC BAT       128 01.01.1994  10:00",
                "CONFIG   SYS       256 01.01.1994  10:00",
                "               3 Datei(en)     55,029 Bytes",
                "               2 Verzeichnis(se) 10,240,000 Bytes frei",
                ""
            ])
        elif cmd == "cls":
            st.session_state.dos_history = ["C:\\>"]
        elif cmd == "ver":
            st.session_state.dos_history.extend(["", "MS-DOS Version 6.22", ""])
        elif cmd == "help":
            st.session_state.dos_history.extend([
                "",
                "Verfügbare Befehle:",
                "  DIR  - Verzeichnis anzeigen",
                "  CD   - Verzeichnis wechseln",
                "  TYPE - Dateiinhalt anzeigen",
                "  CLS  - Bildschirm löschen",
                "  VER  - Version anzeigen",
                "  DATE - Datum anzeigen",
                "  TIME - Zeit anzeigen",
                ""
            ])
        elif cmd == "date":
            st.session_state.dos_history.extend([
                f"Aktuelles Datum: {datetime.now().strftime('%d.%m.%Y')}", ""
            ])
        elif cmd == "time":
            st.session_state.dos_history.extend([
                f"Aktuelle Zeit: {datetime.now().strftime('%H:%M:%S')}", ""
            ])
        else:
            st.session_state.dos_history.extend([
                f"Ungültiger Befehl oder Dateiname: {dos_command}", ""
            ])
        
        st.session_state.dos_history.append("C:\\>")
        st.rerun()

# === Windows Simulation ===
elif selected_os_name == "Windows":
    if show_hints:
        st.info("🖱️ **Windows** - Klicken Sie auf die Buttons unterhalb des Desktops, um Fenster zu öffnen!")
    
    # Initialize states
    if 'win_explorer_open' not in st.session_state:
        st.session_state.win_explorer_open = False
    if 'win_edge_open' not in st.session_state:
        st.session_state.win_edge_open = False
    
    # Windows Screen
    windows_html = '<div class="windows-screen">'
    windows_html += '<div class="windows-desktop-content">'
    
    # Desktop Icons (decorative)
    windows_html += '''
    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div class="windows-icon">
            <div class="windows-icon-emoji">📁</div>
            <div class="windows-icon-label">Dieser PC</div>
        </div>
        <div class="windows-icon">
            <div class="windows-icon-emoji">🗑️</div>
            <div class="windows-icon-label">Papierkorb</div>
        </div>
        <div class="windows-icon">
            <div class="windows-icon-emoji">📄</div>
            <div class="windows-icon-label">Dokumente</div>
        </div>
    </div>
    '''
    
    # Windows
    if st.session_state.win_explorer_open:
        windows_html += '''
        <div class="windows-window">
            <div class="windows-titlebar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>📁</span>
                    <span>Datei-Explorer</span>
                </div>
                <div>─ □ ✕</div>
            </div>
            <div class="windows-window-content">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px;">📄</div>
                        <div>Dokumente</div>
                    </div>
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px;">🖼️</div>
                        <div>Bilder</div>
                    </div>
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px;">🎵</div>
                        <div>Musik</div>
                    </div>
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px;">🎬</div>
                        <div>Videos</div>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    if st.session_state.win_edge_open:
        windows_html += '''
        <div class="windows-window" style="margin-top: 30px;">
            <div class="windows-titlebar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>🌐</span>
                    <span>Microsoft Edge</span>
                </div>
                <div>─ □ ✕</div>
            </div>
            <div class="windows-window-content" style="text-align: center; padding: 40px;">
                <h2 style="color: #0078D4;">Willkommen bei Microsoft Edge</h2>
                <p>Der schnelle und sichere Browser für Windows</p>
            </div>
        </div>
        '''
    
    windows_html += '</div>'  # End desktop-content
    
    # Taskbar
    windows_html += f'''
    <div class="windows-taskbar">
        <div style="font-size: 24px; padding: 0 10px; cursor: pointer;">🪟</div>
        <div style="flex-grow: 1; display: flex; gap: 5px; margin-left: 15px;">
            <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">📁</div>
            <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">🌐</div>
        </div>
        <div style="display: flex; gap: 15px; color: white; font-size: 13px; align-items: center;">
            <span>🔊</span>
            <span>📶</span>
            <span>🔋</span>
            <span>{get_current_time()}</span>
        </div>
    </div>
    '''
    
    windows_html += '</div>'  # End windows-screen
    
    st.markdown(windows_html, unsafe_allow_html=True)
    
    # Control Buttons below the screen
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📁 Explorer öffnen", key="win_explorer_btn", use_container_width=True):
            st.session_state.win_explorer_open = True
            st.rerun()
    with col2:
        if st.button("🌐 Edge öffnen", key="win_edge_btn", use_container_width=True):
            st.session_state.win_edge_open = True
            st.rerun()
    with col3:
        if st.button("⚙️ Einstellungen", key="win_settings_btn", use_container_width=True):
            st.toast("⚙️ Einstellungen geöffnet")
    with col4:
        if st.button("🔄 Zurücksetzen", key="win_reset_btn", use_container_width=True):
            st.session_state.win_explorer_open = False
            st.session_state.win_edge_open = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# === macOS Simulation ===
elif selected_os_name == "macOS":
    if show_hints:
        st.info("🍎 **macOS** - Nutzen Sie die Buttons unten, um Apps zu öffnen!")
    
    # Initialize states
    if 'mac_finder_open' not in st.session_state:
        st.session_state.mac_finder_open = False
    if 'mac_safari_open' not in st.session_state:
        st.session_state.mac_safari_open = False
    
    # macOS Screen
    macos_html = '<div class="macos-screen">'
    
    # Menu Bar
    macos_html += f'''
    <div class="macos-menubar">
        <div class="macos-menu-item" style="font-weight: 600;"></div>
        <div class="macos-menu-item">Finder</div>
        <div class="macos-menu-item">Ablage</div>
        <div class="macos-menu-item">Darstellung</div>
        <div style="flex-grow: 1;"></div>
        <div style="display: flex; gap: 12px;">
            <span>🔋</span>
            <span>📶</span>
            <span>{get_current_time()}</span>
        </div>
    </div>
    '''
    
    macos_html += '<div class="macos-desktop-content">'
    
    # Windows
    if st.session_state.mac_finder_open:
        macos_html += '''
        <div class="macos-window">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light close"></div>
                    <div class="macos-traffic-light minimize"></div>
                    <div class="macos-traffic-light maximize"></div>
                </div>
                <div class="macos-window-title">Finder</div>
                <div style="width: 60px;"></div>
            </div>
            <div style="padding: 30px; text-align: center;">
                <h3>📁 Finder</h3>
                <div style="display: flex; justify-content: center; gap: 30px; margin-top: 20px;">
                    <div><div style="font-size: 48px;">📄</div>Dokumente</div>
                    <div><div style="font-size: 48px;">🖼️</div>Bilder</div>
                    <div><div style="font-size: 48px;">💾</div>Downloads</div>
                </div>
            </div>
        </div>
        '''
    
    if st.session_state.mac_safari_open:
        macos_html += '''
        <div class="macos-window" style="margin-top: 50px;">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light close"></div>
                    <div class="macos-traffic-light minimize"></div>
                    <div class="macos-traffic-light maximize"></div>
                </div>
                <div class="macos-window-title">Safari</div>
                <div style="width: 60px;"></div>
            </div>
            <div style="padding: 40px; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 15px;"></div>
                <h3>Safari</h3>
                <p>Der schnellste Browser für Mac</p>
            </div>
        </div>
        '''
    
    macos_html += '</div>'  # End desktop-content
    
    # Dock
    macos_html += '''
    <div class="macos-dock">
        <div class="macos-dock-icon">📁</div>
        <div class="macos-dock-icon">🌐</div>
        <div class="macos-dock-icon">✉️</div>
        <div class="macos-dock-icon">📅</div>
        <div class="macos-dock-icon">🎵</div>
        <div style="width: 1px; height: 48px; background: rgba(255,255,255,0.3);"></div>
        <div class="macos-dock-icon">⚙️</div>
    </div>
    '''
    
    macos_html += '</div>'  # End macos-screen
    
    st.markdown(macos_html, unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📁 Finder", key="mac_finder_btn", use_container_width=True):
            st.session_state.mac_finder_open = True
            st.rerun()
    with col2:
        if st.button("🌐 Safari", key="mac_safari_btn", use_container_width=True):
            st.session_state.mac_safari_open = True
            st.rerun()
    with col3:
        if st.button("✉️ Mail", key="mac_mail_btn", use_container_width=True):
            st.toast("📧 Mail geöffnet")
    with col4:
        if st.button("🔄 Zurücksetzen", key="mac_reset_btn", use_container_width=True):
            st.session_state.mac_finder_open = False
            st.session_state.mac_safari_open = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# === Linux Simulation ===
elif selected_os_name == "Linux":
    if show_hints:
        st.info("🐧 **Linux** - Probieren Sie: `ls`, `pwd`, `whoami`, `uname -a`, `df -h`, `neofetch`, `clear`")
    
    # Initialize Linux history
    if 'linux_history' not in st.session_state:
        st.session_state.linux_history = [
            "Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)",
            "",
            f"Last login: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}",
            "",
            "user@ubuntu:~$"
        ]
    
    # Linux Screen
    linux_html = '<div class="linux-screen">'
    for line in st.session_state.linux_history:
        if "user@ubuntu" in line:
            linux_html += f'<div><span class="linux-prompt">user@ubuntu:</span><span class="linux-path">~$</span></div>'
        else:
            linux_html += f'<div>{line}</div>'
    linux_html += '</div>'
    
    st.markdown(linux_html, unsafe_allow_html=True)
    
    # Command Input
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        linux_cmd = st.text_input(
            "Linux Befehl:",
            key="linux_cmd",
            placeholder="Befehl eingeben...",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("⏎", key="linux_exec", use_container_width=True):
            if linux_cmd:
                st.session_state.linux_history.append(f"user@ubuntu:~$ {linux_cmd}")
                
                cmd = linux_cmd.strip()
                
                if cmd == "ls":
                    st.session_state.linux_history.extend([
                        "Desktop  Documents  Downloads  Music  Pictures  Videos",
                        ""
                    ])
                elif cmd == "pwd":
                    st.session_state.linux_history.extend(["/home/user", ""])
                elif cmd == "whoami":
                    st.session_state.linux_history.extend(["user", ""])
                elif cmd == "uname -a":
                    st.session_state.linux_history.extend([
                        "Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux",
                        ""
                    ])
                elif cmd == "clear":
                    st.session_state.linux_history = []
                elif cmd == "neofetch":
                    st.session_state.linux_history.extend([
                        "       _,met$$$$$gg.",
                        "    ,g$$$$$$$$$$$$$$$P.",
                        "  OS: Ubuntu 22.04.3 LTS x86_64",
                        "  Kernel: 5.15.0-91-generic",
                        "  Shell: bash 5.1.16",
                        ""
                    ])
                else:
                    st.session_state.linux_history.extend([
                        f"bash: {cmd}: command not found",
                        ""
                    ])
                
                st.session_state.linux_history.append("user@ubuntu:~$")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# === Android Simulation ===
elif selected_os_name == "Android":
    if show_hints:
        st.info("📱 **Android** - Nutzen Sie die Buttons unten, um Apps zu starten!")
    
    android_html = '<div class="phone-container">'
    android_html += '<div class="phone-screen android-screen">'
    
    # Status Bar
    android_html += f'''
    <div class="phone-statusbar">
        <span>{get_current_time()}</span>
        <div style="display: flex; gap: 8px;">
            <span>📶</span>
            <span>🔋 {st.session_state.battery_level}%</span>
        </div>
    </div>
    '''
    
    # Content
    android_html += f'''
    <div class="phone-content">
        <div style="color: white; margin-bottom: 40px;">
            <div style="font-size: 64px; font-weight: 300;">{get_current_time()}</div>
            <div style="font-size: 18px; opacity: 0.9;">{get_current_date()}</div>
        </div>
        
        <div class="app-grid">
            <div class="app-icon">
                <div class="app-icon-circle">📞</div>
                <div class="app-label">Telefon</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">💬</div>
                <div class="app-label">Nachrichten</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">🌐</div>
                <div class="app-label">Chrome</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">📧</div>
                <div class="app-label">Gmail</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">📷</div>
                <div class="app-label">Kamera</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">🗺️</div>
                <div class="app-label">Maps</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">▶️</div>
                <div class="app-label">YouTube</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle">⚙️</div>
                <div class="app-label">Einstellungen</div>
            </div>
        </div>
    </div>
    '''
    
    android_html += '</div></div>'
    st.markdown(android_html, unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📞 Anruf", key="android_call", use_container_width=True):
            st.toast("📞 Anruf wird getätigt...")
    with col2:
        if st.button("📸 Foto", key="android_photo", use_container_width=True):
            st.success("✓ Foto gespeichert")
    with col3:
        if st.button("💬 Nachricht", key="android_msg", use_container_width=True):
            st.success("✓ Nachricht gesendet")
    st.markdown('</div>', unsafe_allow_html=True)

# === iOS Simulation ===
elif selected_os_name == "iOS":
    if show_hints:
        st.info(" **iOS** - Erleben Sie das Apple-Ökosystem!")
    
    ios_html = '<div class="phone-container">'
    ios_html += '<div class="phone-screen ios-screen">'
    
    # Status Bar
    ios_html += f'''
    <div class="phone-statusbar">
        <span>{get_current_time()}</span>
        <div style="display: flex; gap: 8px;">
            <span>📶</span>
            <span>🔋</span>
        </div>
    </div>
    '''
    
    # Content
    ios_html += '''
    <div class="phone-content">
        <div class="app-grid">
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">📱</div>
                <div class="app-label">Telefon</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">🌐</div>
                <div class="app-label">Safari</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">✉️</div>
                <div class="app-label">Mail</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">🎵</div>
                <div class="app-label">Musik</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">📅</div>
                <div class="app-label">Kalender</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">📸</div>
                <div class="app-label">Fotos</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">📷</div>
                <div class="app-label">Kamera</div>
            </div>
            <div class="app-icon">
                <div class="app-icon-circle" style="border-radius: 22%;">⚙️</div>
                <div class="app-label">Einstellungen</div>
            </div>
        </div>
    </div>
    '''
    
    ios_html += '</div></div>'
    st.markdown(ios_html, unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown('<div class="command-input-area">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔐 Face ID", key="ios_faceid", use_container_width=True):
            st.success("✓ iPhone entsperrt")
    with col2:
        if st.button("🎙️ Siri", key="ios_siri", use_container_width=True):
            st.info("🎙️ Wie kann ich helfen?")
    with col3:
        if st.button("📱 AirDrop", key="ios_airdrop", use_container_width=True):
            st.success("✓ Datei gesendet")
    st.markdown('</div>', unsafe_allow_html=True)

# === Footer ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea22, #764ba244); border-radius: 10px;'>
    <p style='margin: 0; color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • Erstellt mit Streamlit • © 2024
    </p>
</div>
""", unsafe_allow_html=True)
