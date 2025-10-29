import streamlit as st
from datetime import datetime
import random

# --- Konfiguration ---
st.set_page_config(
    page_title="Betriebssystem-Simulator Pro",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State ---
if 'dos_history' not in st.session_state:
    st.session_state.dos_history = [
        "Microsoft(R) MS-DOS(R) Version 6.22",
        "             (C)Copyright Microsoft Corp 1981-1994.",
        "",
        "C:\\>"
    ]
if 'linux_history' not in st.session_state:
    st.session_state.linux_history = [
        "Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)",
        "",
        f"Last login: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}",
        "",
        "user@ubuntu:~$"
    ]
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
        margin-bottom: 20px;
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
        margin-bottom: 20px;
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
        margin-bottom: 20px;
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
        margin-bottom: 20px;
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
    "DOS": {"icon": "💾", "color": "#0000AA"},
    "Windows": {"icon": "🪟", "color": "#0078D4"},
    "macOS": {"icon": "", "color": "#000000"},
    "Linux": {"icon": "🐧", "color": "#FCC624"},
    "Android": {"icon": "🤖", "color": "#3DDC84"},
    "iOS": {"icon": "", "color": "#007AFF"}
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
        st.info("🕹️ **DOS** - Kommandozeilenbasiertes Betriebssystem aus den 1980er Jahren. Alle Befehle wurden über Text eingegeben.")
    
    dos_html = """
    <div class="dos-screen">
        Microsoft(R) MS-DOS(R) Version 6.22<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(C)Copyright Microsoft Corp 1981-1994.<br>
        <br>
        C:\\&gt;dir<br>
        &nbsp;Volume in Laufwerk C: hat keine Bezeichnung.<br>
        &nbsp;Volumeseriennummer: 1A2B-3C4D<br>
        <br>
        &nbsp;Verzeichnis von C:\\<br>
        <br>
        DOS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;DIR&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01.01.1994&nbsp;&nbsp;&nbsp;9:00<br>
        WINDOWS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;DIR&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01.01.1994&nbsp;&nbsp;&nbsp;9:30<br>
        COMMAND&nbsp;&nbsp;COM&nbsp;&nbsp;&nbsp;&nbsp;54,645 01.01.1994&nbsp;&nbsp;10:00<br>
        AUTOEXEC&nbsp;BAT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;128 01.01.1994&nbsp;&nbsp;10:00<br>
        CONFIG&nbsp;&nbsp;&nbsp;SYS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;256 01.01.1994&nbsp;&nbsp;10:00<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 Datei(en)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;55,029 Bytes<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 Verzeichnis(se) 10,240,000 Bytes frei<br>
        <br>
        C:\\&gt;<span class="dos-cursor"></span>
    </div>
    """
    
    st.markdown(dos_html, unsafe_allow_html=True)
    
    st.markdown("### 📝 Typische DOS-Befehle")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("DIR - Verzeichnis anzeigen")
        st.code("CD - Verzeichnis wechseln")
        st.code("COPY - Dateien kopieren")
    with col2:
        st.code("DEL - Dateien löschen")
        st.code("TYPE - Datei anzeigen")
        st.code("CLS - Bildschirm löschen")
    with col3:
        st.code("FORMAT - Datenträger formatieren")
        st.code("EDIT - Text-Editor")
        st.code("VER - Version anzeigen")

# === Windows Simulation ===
elif selected_os_name == "Windows":
    if show_hints:
        st.info("🖱️ **Windows** - Das erste Mainstream-Betriebssystem mit grafischer Oberfläche. Revolutionierte die PC-Bedienung mit Maus und Fenstern.")
    
    windows_html = f"""
    <div class="windows-screen">
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
        
        <div class="windows-window" style="margin-top: 50px;">
            <div class="windows-titlebar">
                <div><span>📁</span> Datei-Explorer</div>
                <div>─ □ ✕</div>
            </div>
            <div class="windows-window-content">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center;">
                    <div><div style="font-size: 48px;">📄</div>Dokumente<br><small>15 Dateien</small></div>
                    <div><div style="font-size: 48px;">🖼️</div>Bilder<br><small>127 Dateien</small></div>
                    <div><div style="font-size: 48px;">🎵</div>Musik<br><small>42 Dateien</small></div>
                    <div><div style="font-size: 48px;">🎬</div>Videos<br><small>8 Dateien</small></div>
                </div>
            </div>
        </div>
        
        <div class="windows-taskbar">
            <div style="font-size: 24px;">🪟</div>
            <div style="flex-grow: 1; display: flex; gap: 10px; margin-left: 15px;">
                <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">📁</div>
                <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">🌐</div>
                <div style="padding: 8px 12px; background: rgba(255,255,255,0.1); border-radius: 4px;">📧</div>
            </div>
            <div style="display: flex; gap: 15px; color: white; font-size: 13px;">
                <span>🔊</span>
                <span>📶</span>
                <span>🔋</span>
                <span>{get_current_time()}</span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(windows_html, unsafe_allow_html=True)
    
    st.markdown("### ✨ Windows-Merkmale")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Benutzerfreundlich**\n\nIntutive grafische Oberfläche")
    with col2:
        st.info("**Große Auswahl**\n\nMillionen verfügbare Programme")
    with col3:
        st.warning("**Weit verbreitet**\n\n75% Marktanteil bei Desktop-PCs")

# === macOS Simulation ===
elif selected_os_name == "macOS":
    if show_hints:
        st.info("🍎 **macOS** - Apples elegantes Betriebssystem, bekannt für Design-Exzellenz und nahtlose Integration mit dem Apple-Ökosystem.")
    
    macos_html = f"""
    <div class="macos-screen">
        <div class="macos-menubar">
            <div style="font-weight: 600;"></div>
            <div>Finder</div>
            <div>Ablage</div>
            <div>Bearbeiten</div>
            <div>Darstellung</div>
            <div style="flex-grow: 1;"></div>
            <div>🔋</div>
            <div>📶</div>
            <div>🔍</div>
            <div>{get_current_time()}</div>
        </div>
        
        <div class="macos-desktop-content">
            <div class="macos-window" style="margin-top: 30px;">
                <div class="macos-titlebar">
                    <div class="macos-traffic-lights">
                        <div class="macos-traffic-light" style="background: #ff605c;"></div>
                        <div class="macos-traffic-light" style="background: #ffbd44;"></div>
                        <div class="macos-traffic-light" style="background: #00ca4e;"></div>
                    </div>
                    <div style="flex-grow: 1; text-align: center; font-weight: 600;">Finder</div>
                </div>
                <div style="display: flex; height: 300px;">
                    <div style="width: 150px; background: #f5f5f7; padding: 15px; border-right: 1px solid #e0e0e0;">
                        <div style="font-size: 11px; color: #86868b; font-weight: 600; margin-bottom: 8px;">FAVORITEN</div>
                        <div style="padding: 6px 8px; background: #e8e8ed; border-radius: 6px; margin-bottom: 4px;">
                            <span>🏠</span> Schreibtisch
                        </div>
                        <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px;">
                            <span>📄</span> Dokumente
                        </div>
                        <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px;">
                            <span>💾</span> Downloads
                        </div>
                    </div>
                    <div style="flex-grow: 1; padding: 20px;">
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
                            <div><div style="font-size: 48px;">📁</div>Projekte</div>
                            <div><div style="font-size: 48px;">📄</div>Präsentation.key</div>
                            <div><div style="font-size: 48px;">🖼️</div>Urlaub2024.jpg</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="macos-dock">
            <div class="macos-dock-icon">📁</div>
            <div class="macos-dock-icon">🌐</div>
            <div class="macos-dock-icon">✉️</div>
            <div class="macos-dock-icon">📅</div>
            <div class="macos-dock-icon">🎵</div>
            <div style="width: 1px; height: 48px; background: rgba(255,255,255,0.3);"></div>
            <div class="macos-dock-icon">⚙️</div>
        </div>
    </div>
    """
    
    st.markdown(macos_html, unsafe_allow_html=True)
    
    st.markdown("### ✨ macOS-Merkmale")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Elegantes Design**\n\nMinimalistisch und durchdacht")
    with col2:
        st.info("**Apple-Ökosystem**\n\niPhone, iPad, Mac nahtlos integriert")
    with col3:
        st.warning("**Hohe Sicherheit**\n\nUnix-Basis, weniger Malware")

# === Linux Simulation ===
elif selected_os_name == "Linux":
    if show_hints:
        st.info("🐧 **Linux** - Open-Source-Betriebssystem mit maximaler Anpassbarkeit. Grundlage für Android und viele Server weltweit.")
    
    linux_html = """
    <div class="linux-screen">
        <div style="background: rgba(0,0,0,0.3); padding: 8px 12px; margin: -20px -20px 15px -20px; display: flex; justify-content: space-between; border-radius: 8px 8px 0 0;">
            <div style="display: flex; gap: 8px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #fc5753;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #fdbc40;"></div>
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #33c948;"></div>
            </div>
            <div style="font-size: 12px; color: #8AE234;">user@ubuntu: ~</div>
        </div>
        
        Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)<br>
        <br>
        &nbsp;* Documentation:&nbsp;&nbsp;https://help.ubuntu.com<br>
        &nbsp;* Management:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://landscape.canonical.com<br>
        &nbsp;* Support:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://ubuntu.com/advantage<br>
        <br>
        <span class="linux-prompt">user@ubuntu:~$</span> ls -la<br>
        total 48<br>
        drwxr-xr-x&nbsp;&nbsp;8 user user 4096 Jan 15 10:30 .<br>
        drwxr-xr-x&nbsp;&nbsp;3 root root 4096 Dec&nbsp;&nbsp;1 09:15 ..<br>
        drwxr-xr-x&nbsp;&nbsp;2 user user 4096 Jan 10 14:22 Desktop<br>
        drwxr-xr-x&nbsp;&nbsp;3 user user 4096 Jan 12 16:45 Documents<br>
        drwxr-xr-x&nbsp;&nbsp;2 user user 4096 Jan 14 11:30 Downloads<br>
        <br>
        <span class="linux-prompt">user@ubuntu:~$</span> uname -a<br>
        Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP x86_64 x86_64 x86_64 GNU/Linux<br>
        <br>
        <span class="linux-prompt">user@ubuntu:~$</span> <span style="display: inline-block; width: 8px; height: 14px; background: white; animation: blink 1s infinite;"></span>
    </div>
    """
    
    st.markdown(linux_html, unsafe_allow_html=True)
    
    st.markdown("### 🐧 Linux-Distributionen")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Ubuntu**\n\nBenutzerfreundlich, ideal für Einsteiger")
    with col2:
        st.info("**Fedora**\n\nModerne Software, für Entwickler")
    with col3:
        st.warning("**Arch Linux**\n\nMaximale Kontrolle, für Experten")

# === Android Simulation ===
elif selected_os_name == "Android":
    if show_hints:
        st.info("📱 **Android** - Das weltweit am meisten genutzte mobile Betriebssystem. Basiert auf Linux und ist Open Source.")
    
    android_html = f"""
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
                        <div class="app-label">Einstellungen</div>
                    </div>
                </div>
            </div>
            
            <div style="height: 50px; background: rgba(0,0,0,0.3); display: flex; justify-content: space-around; align-items: center;">
                <div style="font-size: 24px; color: white;">◁</div>
                <div style="font-size: 24px; color: white;">⚪</div>
                <div style="font-size: 24px; color: white;">▢</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(android_html, unsafe_allow_html=True)
    
    st.markdown("### 📊 Android Fakten")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Marktanteil", "71%", "Global")
    with col2:
        st.metric("Apps verfügbar", "3,5 Mio", "Play Store")
    with col3:
        st.metric("Hersteller", "1000+", "Weltweit")

# === iOS Simulation ===
elif selected_os_name == "iOS":
    if show_hints:
        st.info(" **iOS** - Apples mobiles Betriebssystem, exklusiv für iPhone und iPad. Bekannt für Sicherheit und nahtlose Hardware-Integration.")
    
    ios_html = f"""
    <div class="phone-container">
        <div class="phone-screen ios-screen">
            <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 180px; height: 30px; background: #1a1a1a; border-radius: 0 0 20px 20px; z-index: 100;"></div>
            
            <div class="phone-statusbar" style="padding-top: 8px;">
                <span>{get_current_time()}</span>
                <div style="display: flex; gap: 8px;">
                    <span>📶</span>
                    <span>🔋</span>
                </div>
            </div>
            
            <div class="phone-content" style="padding-top: 30px;">
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
            
            <div style="position: absolute; bottom: 70px; left: 0; right: 0; background: rgba(255,255,255,0.15); backdrop-filter: blur(30px); margin: 0 10px; border-radius: 20px; padding: 10px; display: flex; justify-content: space-around;">
                <div style="font-size: 28px;">📞</div>
                <div style="font-size: 28px;">🌐</div>
                <div style="font-size: 28px;">💬</div>
                <div style="font-size: 28px;">🎵</div>
            </div>
            
            <div style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); width: 134px; height: 5px; background: rgba(255,255,255,0.4); border-radius: 2.5px;"></div>
        </div>
    </div>
    """
    
    st.markdown(ios_html, unsafe_allow_html=True)
    
    st.markdown("### 📊 iOS Fakten")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Marktanteil", "28%", "Global")
    with col2:
        st.metric("Apps verfügbar", "1,8 Mio", "App Store")
    with col3:
        st.metric("Sicherheit", "Sehr hoch", "Face ID, Verschlüsselung")

# === Footer ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea22, #764ba244); border-radius: 10px;'>
    <p style='margin: 0; color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • Erstellt mit Streamlit • © 2024
    </p>
    <p style='margin: 10px 0 0 0; font-size: 12px; color: #888;'>
        Alle Betriebssystem-Namen und Logos sind Eigentum ihrer jeweiligen Inhaber
    </p>
</div>
""", unsafe_allow_html=True)
