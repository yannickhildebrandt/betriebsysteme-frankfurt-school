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

# --- CSS Styles ---
st.markdown("""
<style>
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
    }
    
    .dos-line {
        margin: 3px 0;
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
        padding: 30px;
        padding-bottom: 80px;
    }
    
    .windows-icon {
        display: inline-block;
        width: 80px;
        text-align: center;
        margin: 10px;
        vertical-align: top;
    }
    
    .windows-icon-emoji {
        font-size: 48px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 8px;
    }
    
    .windows-icon-label {
        font-size: 12px;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .windows-window {
        background: white;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        overflow: hidden;
        margin: 20px 0;
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
    }
    
    .windows-taskbar {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 48px;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        padding: 0 15px;
        border-top: 1px solid rgba(255,255,255,0.1);
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
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        padding: 0 15px;
        font-size: 13px;
        color: white;
        gap: 15px;
    }
    
    .macos-desktop-content {
        padding: 30px;
        min-height: 560px;
    }
    
    .macos-window {
        background: white;
        border-radius: 10px;
        box-shadow: 0 12px 48px rgba(0,0,0,0.3);
        overflow: hidden;
        margin: 20px 0;
    }
    
    .macos-titlebar {
        background: #f6f6f6;
        height: 40px;
        display: flex;
        align-items: center;
        padding: 0 15px;
        border-bottom: 1px solid #e0e0e0;
        gap: 10px;
    }
    
    .macos-traffic-lights {
        display: flex;
        gap: 8px;
    }
    
    .macos-traffic-light {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    
    .macos-dock {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(40px);
        border-radius: 16px;
        padding: 8px;
        display: flex;
        gap: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .macos-dock-icon {
        width: 52px;
        height: 52px;
        background: rgba(255,255,255,0.4);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
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
    
    .command-input-area {
        margin-top: 20px;
        padding: 15px;
        background: rgba(0,0,0,0.05);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- OS Daten ---
os_data = {
    "DOS": {"icon": "💾", "color": "#0000AA", "name": "MS-DOS"},
    "Windows": {"icon": "🪟", "color": "#0078D4", "name": "Windows"},
    "macOS": {"icon": "", "color": "#000000", "name": "macOS"},
    "Linux": {"icon": "🐧", "color": "#FCC624", "name": "Linux"},
    "Android": {"icon": "🤖", "color": "#3DDC84", "name": "Android"},
    "iOS": {"icon": "", "color": "#007AFF", "name": "iOS"}
}

def get_current_time():
    return datetime.now().strftime("%H:%M")

def get_current_date():
    return datetime.now().strftime("%a, %d. %B")

# --- Header ---
st.markdown("""
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
    
    st.markdown("---")
    show_hints = st.checkbox("💡 Hilfestellungen anzeigen", value=True)
    realistic_delays = st.checkbox("⏱️ Realistische Verzögerungen", value=False)

# --- Hauptbereich ---
selected_os_info = os_data[selected_os_name]

st.markdown(f"""
<div style='background: linear-gradient(135deg, {selected_os_info['color']}22, {selected_os_info['color']}44); 
     padding: 20px; border-radius: 10px; border-left: 4px solid {selected_os_info['color']}; margin-bottom: 20px;'>
    <h2 style='margin: 0; color: {selected_os_info['color']};'>{selected_os_info['icon']} {selected_os_name}</h2>
</div>
""", unsafe_allow_html=True)

# === DOS Simulation ===
if selected_os_name == "DOS":
    if show_hints:
        st.info("🕹️ **DOS** - Probieren Sie: `dir`, `cd`, `cls`, `ver`, `help`, `date`, `time`")
    
    if 'dos_history' not in st.session_state:
        st.session_state.dos_history = [
            "Microsoft(R) MS-DOS(R) Version 6.22",
            "             (C)Copyright Microsoft Corp 1981-1994.",
            "",
            "C:\\&gt;"
        ]
    
    dos_html = '<div class="dos-screen">'
    for line in st.session_state.dos_history:
        dos_html += f'<div class="dos-line">{line}</div>'
    dos_html += '<div class="dos-line"><span class="dos-cursor"></span></div>'
    dos_html += '</div>'
    
    st.markdown(dos_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        dos_command = st.text_input("DOS Befehl:", key="dos_cmd", placeholder="z.B. dir", label_visibility="collapsed")
    with col2:
        execute_button = st.button("⏎", key="dos_exec", use_container_width=True)
    
    if execute_button and dos_command:
        cmd = dos_command.lower().strip()
        st.session_state.dos_history.append(f"C:\\&gt;{dos_command}")
        
        if cmd == "dir":
            st.session_state.dos_history.extend([
                " Volume in Laufwerk C: hat keine Bezeichnung.",
                " Volumeseriennummer: 1A2B-3C4D",
                "",
                " Verzeichnis von C:\\",
                "",
                "DOS          &lt;DIR&gt;     01.01.1994   9:00",
                "WINDOWS      &lt;DIR&gt;     01.01.1994   9:30",
                "COMMAND  COM    54,645 01.01.1994  10:00",
                "               3 Datei(en)     55,029 Bytes",
                ""
            ])
        elif cmd == "cls":
            st.session_state.dos_history = ["C:\\&gt;"]
        elif cmd == "ver":
            st.session_state.dos_history.extend(["", "MS-DOS Version 6.22", ""])
        elif cmd == "help":
            st.session_state.dos_history.extend([
                "", "Verfügbare Befehle:",
                "  DIR  - Verzeichnis anzeigen",
                "  CLS  - Bildschirm löschen",
                "  VER  - Version anzeigen", ""
            ])
        elif cmd == "date":
            st.session_state.dos_history.extend([f"Aktuelles Datum: {datetime.now().strftime('%d.%m.%Y')}", ""])
        elif cmd == "time":
            st.session_state.dos_history.extend([f"Aktuelle Zeit: {datetime.now().strftime('%H:%M:%S')}", ""])
        else:
            st.session_state.dos_history.extend([f"Ungültiger Befehl: {dos_command}", ""])
        
        st.session_state.dos_history.append("C:\\&gt;")
        st.rerun()

# === Windows Simulation ===
elif selected_os_name == "Windows":
    if show_hints:
        st.info("🖱️ **Windows** - Klicken Sie auf die Buttons, um Fenster zu öffnen!")
    
    if 'win_explorer_open' not in st.session_state:
        st.session_state.win_explorer_open = False
    if 'win_edge_open' not in st.session_state:
        st.session_state.win_edge_open = False
    
    windows_html = '<div class="windows-screen">'
    
    # Desktop Icons
    windows_html += '''
    <div>
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
    
    if st.session_state.win_explorer_open:
        windows_html += '''
        <div class="windows-window">
            <div class="windows-titlebar">
                <div><span>📁</span> Datei-Explorer</div>
                <div>─ □ ✕</div>
            </div>
            <div class="windows-window-content">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center;">
                    <div><div style="font-size: 48px;">📄</div>Dokumente</div>
                    <div><div style="font-size: 48px;">🖼️</div>Bilder</div>
                    <div><div style="font-size: 48px;">🎵</div>Musik</div>
                    <div><div style="font-size: 48px;">🎬</div>Videos</div>
                </div>
            </div>
        </div>
        '''
    
    if st.session_state.win_edge_open:
        windows_html += '''
        <div class="windows-window">
            <div class="windows-titlebar">
                <div><span>🌐</span> Microsoft Edge</div>
                <div>─ □ ✕</div>
            </div>
            <div class="windows-window-content" style="text-align: center; padding: 40px;">
                <h2 style="color: #0078D4;">Willkommen bei Microsoft Edge</h2>
                <p>Der schnelle und sichere Browser für Windows</p>
            </div>
        </div>
        '''
    
    windows_html += f'''
    <div class="windows-taskbar">
        <div style="font-size: 24px;">🪟</div>
        <div style="flex-grow: 1; display: flex; gap: 10px; margin-left: 15px;">
            <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">📁</div>
            <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">🌐</div>
        </div>
        <div style="display: flex; gap: 15px; color: white; font-size: 13px;">
            <span>🔊</span>
            <span>📶</span>
            <span>{get_current_time()}</span>
        </div>
    </div>
    '''
    
    windows_html += '</div>'
    st.markdown(windows_html, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📁 Explorer", key="win_exp", use_container_width=True):
            st.session_state.win_explorer_open = True
            st.rerun()
    with col2:
        if st.button("🌐 Edge", key="win_edge", use_container_width=True):
            st.session_state.win_edge_open = True
            st.rerun()
    with col3:
        if st.button("⚙️ Einstellungen", key="win_set", use_container_width=True):
            st.toast("⚙️ Einstellungen")
    with col4:
        if st.button("🔄 Reset", key="win_reset", use_container_width=True):
            st.session_state.win_explorer_open = False
            st.session_state.win_edge_open = False
            st.rerun()

# === macOS Simulation ===
elif selected_os_name == "macOS":
    if show_hints:
        st.info("🍎 **macOS** - Nutzen Sie die Buttons, um Apps zu öffnen!")
    
    if 'mac_finder_open' not in st.session_state:
        st.session_state.mac_finder_open = False
    if 'mac_safari_open' not in st.session_state:
        st.session_state.mac_safari_open = False
    
    macos_html = '<div class="macos-screen">'
    
    macos_html += f'''
    <div class="macos-menubar">
        <div style="font-weight: 600;"></div>
        <div>Finder</div>
        <div>Ablage</div>
        <div>Darstellung</div>
        <div style="flex-grow: 1;"></div>
        <div>{get_current_time()}</div>
    </div>
    '''
    
    macos_html += '<div class="macos-desktop-content">'
    
    if st.session_state.mac_finder_open:
        macos_html += '''
        <div class="macos-window">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light" style="background: #ff605c;"></div>
                    <div class="macos-traffic-light" style="background: #ffbd44;"></div>
                    <div class="macos-traffic-light" style="background: #00ca4e;"></div>
                </div>
                <div style="flex-grow: 1; text-align: center; font-weight: 600;">Finder</div>
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
        <div class="macos-window">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light" style="background: #ff605c;"></div>
                    <div class="macos-traffic-light" style="background: #ffbd44;"></div>
                    <div class="macos-traffic-light" style="background: #00ca4e;"></div>
                </div>
                <div style="flex-grow: 1; text-align: center; font-weight: 600;">Safari</div>
            </div>
            <div style="padding: 40px; text-align: center;">
                <div style="font-size: 48px;"></div>
                <h3>Safari</h3>
                <p>Der schnellste Browser für Mac</p>
            </div>
        </div>
        '''
    
    macos_html += '</div>'
    
    macos_html += '''
    <div class="macos-dock">
        <div class="macos-dock-icon">📁</div>
        <div class="macos-dock-icon">🌐</div>
        <div class="macos-dock-icon">✉️</div>
        <div class="macos-dock-icon">🎵</div>
        <div class="macos-dock-icon">⚙️</div>
    </div>
    '''
    
    macos_html += '</div>'
    st.markdown(macos_html, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📁 Finder", key="mac_find", use_container_width=True):
            st.session_state.mac_finder_open = True
            st.rerun()
    with col2:
        if st.button("🌐 Safari", key="mac_saf", use_container_width=True):
            st.session_state.mac_safari_open = True
            st.rerun()
    with col3:
        if st.button("✉️ Mail", key="mac_mail", use_container_width=True):
            st.toast("📧 Mail")
    with col4:
        if st.button("🔄 Reset", key="mac_reset", use_container_width=True):
            st.session_state.mac_finder_open = False
            st.session_state.mac_safari_open = False
            st.rerun()

# === Linux Simulation ===
elif selected_os_name == "Linux":
    if show_hints:
        st.info("🐧 **Linux** - Probieren Sie: `ls`, `pwd`, `whoami`, `uname -a`, `clear`")
    
    if 'linux_history' not in st.session_state:
        st.session_state.linux_history = [
            "Welcome to Ubuntu 22.04.3 LTS",
            "",
            f"Last login: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}",
            "",
            "user@ubuntu:~$"
        ]
    
    linux_html = '<div class="linux-screen">'
    for line in st.session_state.linux_history:
        if "user@ubuntu" in line:
            linux_html += f'<div><span class="linux-prompt">user@ubuntu:</span>~$</div>'
        else:
            linux_html += f'<div>{line}</div>'
    linux_html += '</div>'
    
    st.markdown(linux_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        linux_cmd = st.text_input("Linux Befehl:", key="linux_cmd", placeholder="z.B. ls", label_visibility="collapsed")
    with col2:
        if st.button("⏎", key="linux_exec", use_container_width=True):
            if linux_cmd:
                st.session_state.linux_history.append(f"user@ubuntu:~$ {linux_cmd}")
                
                if linux_cmd == "ls":
                    st.session_state.linux_history.extend(["Desktop  Documents  Downloads  Music  Pictures", ""])
                elif linux_cmd == "pwd":
                    st.session_state.linux_history.extend(["/home/user", ""])
                elif linux_cmd == "whoami":
                    st.session_state.linux_history.extend(["user", ""])
                elif linux_cmd == "uname -a":
                    st.session_state.linux_history.extend(["Linux ubuntu 5.15.0-91-generic x86_64 GNU/Linux", ""])
                elif linux_cmd == "clear":
                    st.session_state.linux_history = []
                else:
                    st.session_state.linux_history.extend([f"bash: {linux_cmd}: command not found", ""])
                
                st.session_state.linux_history.append("user@ubuntu:~$")
                st.rerun()

# === Android Simulation ===
elif selected_os_name == "Android":
    if show_hints:
        st.info("📱 **Android** - Nutzen Sie die Buttons für App-Interaktionen!")
    
    android_html = f'''
    <div class="phone-container">
        <div class="phone-screen android-screen">
            <div class="phone-statusbar">
                <span>{get_current_time()}</span>
                <div style="display: flex; gap: 8px;">
                    <span>📶</span>
                    <span>🔋 {st.session_state.battery_level}%</span>
                </div>
            </div>
            
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
                        <div class="app-label">Settings</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    st.markdown(android_html, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📞 Anruf", key="and_call", use_container_width=True):
            st.toast("📞 Anruf wird getätigt...")
    with col2:
        if st.button("📸 Foto", key="and_photo", use_container_width=True):
            st.success("✓ Foto gespeichert")
    with col3:
        if st.button("💬 Nachricht", key="and_msg", use_container_width=True):
            st.success("✓ Nachricht gesendet")

# === iOS Simulation ===
elif selected_os_name == "iOS":
    if show_hints:
        st.info(" **iOS** - Erleben Sie das Apple-Ökosystem!")
    
    ios_html = f'''
    <div class="phone-container">
        <div class="phone-screen ios-screen">
            <div class="phone-statusbar">
                <span>{get_current_time()}</span>
                <div style="display: flex; gap: 8px;">
                    <span>📶</span>
                    <span>🔋</span>
                </div>
            </div>
            
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
                        <div class="app-label">Settings</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    st.markdown(ios_html, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔐 Face ID", key="ios_face", use_container_width=True):
            st.success("✓ iPhone entsperrt")
    with col2:
        if st.button("🎙️ Siri", key="ios_siri", use_container_width=True):
            st.info("🎙️ Wie kann ich helfen?")
    with col3:
        if st.button("📱 AirDrop", key="ios_air", use_container_width=True):
            st.success("✓ Datei gesendet")

# === Footer ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea22, #764ba244); border-radius: 10px;'>
    <p style='margin: 0; color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • Erstellt mit Streamlit • © 2024
    </p>
</div>
""", unsafe_allow_html=True)
