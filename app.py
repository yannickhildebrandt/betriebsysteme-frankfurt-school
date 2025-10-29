import streamlit as st
from datetime import datetime
import random

# --- Konfiguration ---
st.set_page_config(
    page_title="Betriebssystem-Simulator Pro",
    page_icon="💻",
    layout="wide"
)

# --- Session State ---
if 'dos_history' not in st.session_state:
    st.session_state.dos_history = ["Microsoft(R) MS-DOS(R) Version 6.22", "(C)Copyright Microsoft Corp 1981-1994.", "", "C:\\>"]
if 'linux_history' not in st.session_state:
    st.session_state.linux_history = ["Welcome to Ubuntu 22.04.3 LTS", "", "user@ubuntu:~$"]
if 'win_explorer_open' not in st.session_state:
    st.session_state.win_explorer_open = False
if 'win_edge_open' not in st.session_state:
    st.session_state.win_edge_open = False
if 'mac_finder_open' not in st.session_state:
    st.session_state.mac_finder_open = False
if 'mac_safari_open' not in st.session_state:
    st.session_state.mac_safari_open = False
if 'battery_level' not in st.session_state:
    st.session_state.battery_level = random.randint(60, 100)

# --- CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* DOS Terminal */
    .dos-terminal {
        background-color: #0000AA;
        color: #FFFFFF;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 400px;
        font-size: 14px;
        line-height: 1.4;
        white-space: pre-wrap;
        overflow-y: auto;
        max-height: 500px;
    }
    
    /* Linux Terminal */
    .linux-terminal {
        background-color: #300A24;
        color: #FFFFFF;
        font-family: 'Ubuntu Mono', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 400px;
        font-size: 14px;
        line-height: 1.5;
        white-space: pre-wrap;
        overflow-y: auto;
        max-height: 500px;
    }
    
    .linux-prompt {
        color: #8AE234;
    }
    
    /* Card Styles */
    .os-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .icon-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .icon-item {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    
    .icon-item:hover {
        background: rgba(0,0,0,0.05);
    }
    
    .icon-emoji {
        font-size: 40px;
        margin-bottom: 5px;
    }
    
    .icon-label {
        font-size: 11px;
        color: #333;
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

# --- Header ---
st.markdown("""
<div style='text-align: center; padding: 30px 0; color: white;'>
    <h1 style='font-size: 3em; margin: 0;'>💻 Betriebssystem-Simulator Pro</h1>
    <p style='font-size: 1.2em; opacity: 0.9; margin-top: 10px;'>Erleben Sie die Evolution der Betriebssysteme</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🎮 Steuerung")
    selected_os = st.selectbox(
        "Betriebssystem:",
        list(os_data.keys()),
        format_func=lambda x: f"{os_data[x]['icon']} {x}"
    )
    
    st.markdown("---")
    show_hints = st.checkbox("💡 Hilfestellungen", value=True)
    
    st.markdown("---")
    st.info("💡 Nutzen Sie die interaktiven Elemente, um die Betriebssysteme zu erkunden!")

# --- Hauptbereich ---

# ==================== DOS ====================
if selected_os == "DOS":
    st.markdown(f"## 💾 MS-DOS Simulation")
    
    if show_hints:
        st.info("📝 Verfügbare Befehle: `dir`, `cls`, `ver`, `help`, `date`, `time`")
    
    # Terminal Display
    terminal_text = "\n".join(st.session_state.dos_history)
    st.markdown(f'<div class="dos-terminal">{terminal_text}\n█</div>', unsafe_allow_html=True)
    
    # Command Input
    st.markdown("### Befehlseingabe")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        dos_cmd = st.text_input("DOS Befehl:", key="dos_input", placeholder="Befehl eingeben...")
    
    with col2:
        st.write("")
        st.write("")
        execute = st.button("▶️ Enter", key="dos_exec", use_container_width=True)
    
    if execute and dos_cmd:
        st.session_state.dos_history.append(f"C:\\>{dos_cmd}")
        
        cmd = dos_cmd.lower().strip()
        
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
                "               3 Datei(en)     55,029 Bytes",
                ""
            ])
        elif cmd == "cls":
            st.session_state.dos_history = ["C:\\>"]
        elif cmd == "ver":
            st.session_state.dos_history.extend(["", "MS-DOS Version 6.22", ""])
        elif cmd == "help":
            st.session_state.dos_history.extend([
                "", "Verfügbare Befehle:",
                "  DIR   - Verzeichnis anzeigen",
                "  CLS   - Bildschirm löschen",
                "  VER   - Version anzeigen",
                "  DATE  - Datum anzeigen",
                "  TIME  - Zeit anzeigen",
                "  HELP  - Diese Hilfe", ""
            ])
        elif cmd == "date":
            st.session_state.dos_history.extend([f"Aktuelles Datum: {datetime.now().strftime('%d.%m.%Y')}", ""])
        elif cmd == "time":
            st.session_state.dos_history.extend([f"Aktuelle Zeit: {datetime.now().strftime('%H:%M:%S')}", ""])
        else:
            st.session_state.dos_history.extend([f"Ungültiger Befehl oder Dateiname: {dos_cmd}", ""])
        
        st.session_state.dos_history.append("C:\\>")
        st.rerun()

# ==================== WINDOWS ====================
elif selected_os == "Windows":
    st.markdown("## 🪟 Windows 11 Simulation")
    
    if show_hints:
        st.info("🖱️ Klicken Sie auf die Buttons, um Fenster zu öffnen und zu schließen!")
    
    # Desktop
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("### 🖥️ Desktop")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="icon-item"><div class="icon-emoji">📁</div><div class="icon-label">Dieser PC</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="icon-item"><div class="icon-emoji">🗑️</div><div class="icon-label">Papierkorb</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="icon-item"><div class="icon-emoji">📄</div><div class="icon-label">Dokumente</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="icon-item"><div class="icon-emoji">🖼️</div><div class="icon-label">Bilder</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Windows
    if st.session_state.win_explorer_open:
        st.markdown('<div class="os-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Datei-Explorer")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**📄 Dokumente**")
            st.caption("15 Dateien")
        with col2:
            st.markdown("**🖼️ Bilder**")
            st.caption("127 Dateien")
        with col3:
            st.markdown("**🎵 Musik**")
            st.caption("42 Dateien")
        with col4:
            st.markdown("**🎬 Videos**")
            st.caption("8 Dateien")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.win_edge_open:
        st.markdown('<div class="os-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 Microsoft Edge")
        st.markdown("#### Willkommen bei Microsoft Edge")
        st.write("Der schnelle und sichere Browser für Windows")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚡ Geschwindigkeit", "Sehr schnell")
        with col2:
            st.metric("🔒 Sicherheit", "Sehr hoch")
        with col3:
            st.metric("🌐 Kompatibilität", "100%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Taskbar
    st.markdown("---")
    st.markdown("### ⬇️ Taskleiste")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📁 Datei-Explorer", key="win_explorer", use_container_width=True):
            st.session_state.win_explorer_open = not st.session_state.win_explorer_open
            st.rerun()
    
    with col2:
        if st.button("🌐 Edge Browser", key="win_edge", use_container_width=True):
            st.session_state.win_edge_open = not st.session_state.win_edge_open
            st.rerun()
    
    with col3:
        if st.button("⚙️ Einstellungen", key="win_settings", use_container_width=True):
            st.toast("⚙️ Einstellungen geöffnet")
    
    with col4:
        if st.button("🔄 Alle schließen", key="win_reset", use_container_width=True):
            st.session_state.win_explorer_open = False
            st.session_state.win_edge_open = False
            st.rerun()

# ==================== macOS ====================
elif selected_os == "macOS":
    st.markdown("##  macOS Ventura Simulation")
    
    if show_hints:
        st.info("🍎 Nutzen Sie das Dock am unteren Rand, um Apps zu starten!")
    
    # Menu Bar
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown("** Finder**")
    with col2:
        st.markdown("**Ablage · Bearbeiten · Darstellung · Gehe zu · Fenster**")
    with col3:
        st.markdown(f"**🔋 📶 {datetime.now().strftime('%H:%M')}**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Desktop
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("### 🖥️ Schreibtisch")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Windows
    if st.session_state.mac_finder_open:
        st.markdown('<div class="os-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Finder")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📄 Dokumente**")
            st.caption("Zuletzt verwendet")
        with col2:
            st.markdown("**🖼️ Bilder**")
            st.caption("Fotos Mediathek")
        with col3:
            st.markdown("**💾 Downloads**")
            st.caption("Neueste Dateien")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.mac_safari_open:
        st.markdown('<div class="os-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 Safari")
        st.markdown("#### Der schnellste Browser der Welt")
        st.write("Entwickelt von Apple für Mac, iPhone und iPad.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dock
    st.markdown("---")
    st.markdown("### 📱 Dock")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("📁", key="mac_finder", use_container_width=True):
            st.session_state.mac_finder_open = not st.session_state.mac_finder_open
            st.rerun()
        st.caption("Finder")
    
    with col2:
        if st.button("🌐", key="mac_safari", use_container_width=True):
            st.session_state.mac_safari_open = not st.session_state.mac_safari_open
            st.rerun()
        st.caption("Safari")
    
    with col3:
        if st.button("✉️", key="mac_mail", use_container_width=True):
            st.toast("📧 Mail geöffnet")
        st.caption("Mail")
    
    with col4:
        if st.button("🎵", key="mac_music", use_container_width=True):
            st.toast("🎵 Musik geöffnet")
        st.caption("Musik")
    
    with col5:
        if st.button("⚙️", key="mac_settings", use_container_width=True):
            st.toast("⚙️ Systemeinstellungen")
        st.caption("Einstellungen")
    
    with col6:
        if st.button("🔄", key="mac_reset", use_container_width=True):
            st.session_state.mac_finder_open = False
            st.session_state.mac_safari_open = False
            st.rerun()
        st.caption("Zurücksetzen")

# ==================== LINUX ====================
elif selected_os == "Linux":
    st.markdown("## 🐧 Linux (Ubuntu) Simulation")
    
    if show_hints:
        st.info("⌨️ Verfügbare Befehle: `ls`, `pwd`, `whoami`, `uname -a`, `df -h`, `clear`, `neofetch`")
    
    # Terminal Display
    terminal_text = "\n".join(st.session_state.linux_history)
    st.markdown(f'<div class="linux-terminal"><span class="linux-prompt">{terminal_text}</span>\n█</div>', unsafe_allow_html=True)
    
    # Command Input
    st.markdown("### Befehlseingabe")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        linux_cmd = st.text_input("Linux Befehl:", key="linux_input", placeholder="Befehl eingeben...")
    
    with col2:
        st.write("")
        st.write("")
        execute = st.button("▶️ Enter", key="linux_exec", use_container_width=True)
    
    if execute and linux_cmd:
        st.session_state.linux_history.append(f"user@ubuntu:~$ {linux_cmd}")
        
        cmd = linux_cmd.strip()
        
        if cmd == "ls":
            st.session_state.linux_history.extend(["Desktop  Documents  Downloads  Music  Pictures  Videos", ""])
        elif cmd == "pwd":
            st.session_state.linux_history.extend(["/home/user", ""])
        elif cmd == "whoami":
            st.session_state.linux_history.extend(["user", ""])
        elif cmd == "uname -a":
            st.session_state.linux_history.extend(["Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux", ""])
        elif cmd == "df -h":
            st.session_state.linux_history.extend([
                "Filesystem      Size  Used Avail Use% Mounted on",
                "/dev/sda1       100G   45G   50G  48% /",
                "/dev/sda2       200G   78G  112G  42% /home", ""
            ])
        elif cmd == "clear":
            st.session_state.linux_history = []
        elif cmd == "neofetch":
            st.session_state.linux_history.extend([
                "OS: Ubuntu 22.04.3 LTS x86_64",
                "Kernel: 5.15.0-91-generic",
                "Shell: bash 5.1.16",
                "CPU: Intel i7 (8) @ 3.600GHz",
                "Memory: 4512MiB / 15976MiB", ""
            ])
        else:
            st.session_state.linux_history.extend([f"bash: {cmd}: command not found", ""])
        
        st.session_state.linux_history.append("user@ubuntu:~$")
        st.rerun()

# ==================== ANDROID ====================
elif selected_os == "Android":
    st.markdown("## 🤖 Android 14 Simulation")
    
    if show_hints:
        st.info("📱 Tippen Sie auf die App-Buttons, um Aktionen auszuführen!")
    
    # Status Bar
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**{datetime.now().strftime('%H:%M')}**")
    with col2:
        st.markdown(f"**📶 🔋 {st.session_state.battery_level}%**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Home Screen
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown(f"### {datetime.now().strftime('%H:%M')}")
    st.caption(datetime.now().strftime('%A, %d. %B %Y'))
    
    st.markdown("#### Apps")
    
    col1, col2, col3, col4 = st.columns(4)
    
    apps = [
        ("📞", "Telefon", "call"),
        ("💬", "Nachrichten", "msg"),
        ("🌐", "Chrome", "chrome"),
        ("📧", "Gmail", "gmail"),
        ("📷", "Kamera", "camera"),
        ("🗺️", "Maps", "maps"),
        ("▶️", "YouTube", "youtube"),
        ("⚙️", "Einstellungen", "settings")
    ]
    
    cols = [col1, col2, col3, col4] * 2
    
    for i, (emoji, name, key) in enumerate(apps):
        with cols[i]:
            if st.button(f"{emoji}\n{name}", key=f"android_{key}", use_container_width=True):
                st.toast(f"{emoji} {name} gestartet!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== iOS ====================
elif selected_os == "iOS":
    st.markdown("##  iOS 17 Simulation")
    
    if show_hints:
        st.info(" Erleben Sie das intuitive iOS-Interface!")
    
    # Status Bar
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**{datetime.now().strftime('%H:%M')}**")
    with col2:
        st.markdown("**📶 🔋 87%**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Home Screen
    st.markdown('<div class="os-card">', unsafe_allow_html=True)
    st.markdown("#### Apps")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ios_apps = [
        ("📱", "Telefon", "phone"),
        ("🌐", "Safari", "safari"),
        ("✉️", "Mail", "mail"),
        ("🎵", "Musik", "music"),
        ("📅", "Kalender", "cal"),
        ("📸", "Fotos", "photos"),
        ("📷", "Kamera", "camera"),
        ("⚙️", "Einstellungen", "set")
    ]
    
    cols = [col1, col2, col3, col4] * 2
    
    for i, (emoji, name, key) in enumerate(ios_apps):
        with cols[i]:
            if st.button(f"{emoji}\n{name}", key=f"ios_{key}", use_container_width=True):
                st.toast(f"{emoji} {name} gestartet!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔐 Face ID entsperren", use_container_width=True):
            st.success("✓ iPhone entsperrt")
    
    with col2:
        if st.button("🎙️ Siri aktivieren", use_container_width=True):
            st.info("🎙️ Wie kann ich helfen?")
    
    with col3:
        if st.button("📱 AirDrop", use_container_width=True):
            st.success("✓ Datei gesendet")

# === Footer ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.9); border-radius: 10px;'>
    <p style='margin: 0; color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • Erstellt mit Streamlit • © 2024
    </p>
</div>
""", unsafe_allow_html=True)
