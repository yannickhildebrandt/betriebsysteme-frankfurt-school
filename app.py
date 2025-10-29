import streamlit as st
import time
from datetime import datetime

# Seitenkonfiguration
st.set_page_config(
    page_title="Betriebssystem-Simulator",
    page_icon="💻",
    layout="wide"
)

# CSS für besseres Styling
st.markdown("""
<style>
    .os-window {
        border: 2px solid #333;
        border-radius: 10px;
        padding: 20px;
        background-color: #f0f0f0;
        margin: 10px 0;
    }
    .terminal {
        background-color: #000;
        color: #0f0;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        min-height: 200px;
    }
    .mac-window {
        background: linear-gradient(to bottom, #e8e8e8, #d0d0d0);
        border-radius: 10px;
        padding: 10px;
    }
    .windows-taskbar {
        background-color: #1e1e1e;
        color: white;
        padding: 10px;
        margin-top: 20px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisierung des Session States
if 'terminal_history' not in st.session_state:
    st.session_state.terminal_history = []
if 'file_system' not in st.session_state:
    st.session_state.file_system = {
        'Dokumente': ['brief.txt', 'rechnung.pdf'],
        'Bilder': ['urlaub.jpg', 'familie.png'],
        'Programme': ['app.exe', 'tool.app']
    }

# Haupttitel
st.title("💻 Interaktiver Betriebssystem-Simulator")
st.markdown("Erlebe die Unterschiede zwischen verschiedenen Betriebssystemen!")

# Sidebar für OS-Auswahl
st.sidebar.title("Betriebssystem wählen")
os_choice = st.sidebar.selectbox(
    "Wähle ein Betriebssystem:",
    ["DOS", "Windows", "macOS", "Linux", "Android", "iOS", "Unix", "Chrome OS", "FreeBSD"]
)

# Informationsbereich in Sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**Lernziele:**
- Unterschiede zwischen Betriebssystemen verstehen
- Bedienkonzepte kennenlernen
- Einsatzbereiche erkennen
""")

# =====================
# DOS SIMULATION
# =====================
def simulate_dos():
    st.header("🖥️ DOS (Disk Operating System)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Kommandozeilenbasiert
        - Single-User, Single-Tasking
        - Einprozessor
        - Erscheinungsjahr: 1981
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Kommandozeile")
        st.markdown('<div class="terminal">', unsafe_allow_html=True)
        
        # DOS-Befehle
        dos_command = st.text_input("C:\\>", key="dos_input")
        
        if dos_command:
            output = f"C:\\> {dos_command}\n"
            
            if dos_command.lower() == "dir":
                output += """
 Volume in Laufwerk C: hat keine Bezeichnung
 Verzeichnis von C:\\

COMMAND  COM     25.307  01.01.1981  12:00
AUTOEXEC BAT        128  01.01.1981  12:00
CONFIG   SYS         64  01.01.1981  12:00
        3 Datei(en)     25.499 Bytes
        """
            elif dos_command.lower() == "help":
                output += """
Verfügbare Befehle:
DIR     - Verzeichnis anzeigen
COPY    - Dateien kopieren
DEL     - Dateien löschen
CLS     - Bildschirm löschen
DATE    - Datum anzeigen/ändern
TIME    - Uhrzeit anzeigen/ändern
                """
            elif dos_command.lower() == "date":
                output += f"\nAktuelles Datum: {datetime.now().strftime('%d.%m.%Y')}"
            elif dos_command.lower() == "cls":
                output = "Bildschirm gelöscht...\nC:\\>"
            else:
                output += f"\nFehler: '{dos_command}' ist kein bekannter Befehl.\nGeben Sie 'HELP' ein für verfügbare Befehle."
            
            st.code(output, language=None)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Single-Tasking")
        st.metric("Benutzer", "Single-User")
        st.metric("Dialog/Batch", "Dialog")
        st.metric("Prozessoren", "1")
        
        st.markdown("### Typische Anwendung")
        st.write("Grundlage für frühe Windows-Versionen, einfache Dateiverwaltung")

# =====================
# WINDOWS SIMULATION
# =====================
def simulate_windows():
    st.header("🪟 Windows")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Benutzerfreundliche Oberfläche
        - Multi-User, Multitasking, Timesharing
        - Weit verbreitet
        - Erscheinungsjahr: 1985
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simulierter Desktop
        st.markdown("### Desktop-Oberfläche")
        
        tab1, tab2, tab3 = st.tabs(["📁 Datei-Explorer", "⚙️ Einstellungen", "🎮 Programme"])
        
        with tab1:
            st.subheader("Dieser PC")
            selected_folder = st.selectbox("Ordner:", list(st.session_state.file_system.keys()))
            
            st.write(f"**Inhalt von {selected_folder}:**")
            for file in st.session_state.file_system[selected_folder]:
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"📄 {file}")
                with col_b:
                    if st.button("Öffnen", key=f"open_{file}"):
                        st.success(f"{file} wird geöffnet...")
                with col_c:
                    if st.button("Löschen", key=f"del_{file}"):
                        st.warning(f"{file} wurde gelöscht!")
        
        with tab2:
            st.subheader("System-Einstellungen")
            st.slider("Bildschirmhelligkeit", 0, 100, 75)
            st.selectbox("Design", ["Hell", "Dunkel", "Automatisch"])
            st.checkbox("Automatische Updates aktivieren", value=True)
        
        with tab3:
            st.subheader("Installierte Programme")
            programs = ["Microsoft Word", "Excel", "Browser", "E-Mail-Client", "Media Player"]
            for prog in programs:
                if st.button(f"▶️ {prog}", key=f"prog_{prog}"):
                    st.success(f"{prog} wird gestartet...")
        
        # Taskleiste
        st.markdown('<div class="windows-taskbar">🪟 Start | 📁 Dateien | 🌐 Browser | ⚙️ Einstellungen | ' + 
                   datetime.now().strftime('%H:%M') + '</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Multi-User")
        st.metric("Dialog/Batch", "Beides")
        st.metric("Prozessoren", "Mehrere")
        
        st.markdown("### Vorteile")
        st.success("✓ Große Software-Auswahl")
        st.success("✓ Hardware-Kompatibilität")
        st.success("✓ Benutzerfreundlich")

# =====================
# macOS SIMULATION
# =====================
def simulate_macos():
    st.header("🍎 macOS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Nahtlose Integration mit Apple-Produkten
        - Exklusiv für Apple-Hardware
        - Single-User, Multitasking
        - Erscheinungsjahr: 2001
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # macOS Dock
        st.markdown('<div class="mac-window">', unsafe_allow_html=True)
        st.markdown("### 🍎 Mac Desktop")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("#### 📱 Finder")
            if st.button("Finder öffnen", key="mac_finder"):
                st.info("Finder zeigt alle Dateien und Ordner übersichtlich an")
                for folder, files in st.session_state.file_system.items():
                    with st.expander(f"📁 {folder}"):
                        for f in files:
                            st.write(f"• {f}")
        
        with col_b:
            st.markdown("#### 🚀 Launchpad")
            if st.button("Apps anzeigen", key="mac_launch"):
                apps = ["Safari", "Mail", "Fotos", "Musik", "iMovie", "GarageBand", "Pages"]
                st.write("**Verfügbare Apps:**")
                for app in apps:
                    st.write(f"🔵 {app}")
        
        with col_c:
            st.markdown("#### 🔧 Systemeinstellungen")
            if st.button("Einstellungen", key="mac_settings"):
                st.write("**macOS Einstellungen:**")
                st.checkbox("iCloud Synchronisation", value=True)
                st.checkbox("AirDrop aktiviert", value=True)
                st.checkbox("Handoff aktiviert", value=True)
        
        # Menüleiste
        st.markdown("---")
        st.markdown("🍎 Finder | Ablage | Bearbeiten | Darstellung | Gehe zu | Fenster | Hilfe" + 
                   " " * 50 + "🔋 🔊 " + datetime.now().strftime('%H:%M'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Single-User")
        st.metric("Dialog/Batch", "Dialog")
        st.metric("Prozessoren", "Mehrere")
        
        st.markdown("### Apple-Ökosystem")
        st.success("✓ iPhone Integration")
        st.success("✓ iCloud Synchronisation")
        st.success("✓ AirDrop")
        st.success("✓ Handoff")

# =====================
# LINUX SIMULATION
# =====================
def simulate_linux():
    st.header("🐧 Linux")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Open Source, hohe Anpassbarkeit
        - Viele Distributionen (Ubuntu, Fedora, etc.)
        - Multi-User, Multitasking, Echtzeit
        - Erscheinungsjahr: 1991
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Linux Terminal
        st.markdown("### 💻 Terminal (bash)")
        st.markdown('<div class="terminal">', unsafe_allow_html=True)
        
        linux_cmd = st.text_input("user@linux:~$", key="linux_input")
        
        if linux_cmd:
            output = f"user@linux:~$ {linux_cmd}\n"
            
            if linux_cmd.lower().startswith("ls"):
                output += "Dokumente  Bilder  Downloads  Programme\n"
                output += "musik.mp3  notizen.txt  script.sh"
            elif linux_cmd.lower().startswith("pwd"):
                output += "/home/user"
            elif linux_cmd.lower().startswith("whoami"):
                output += "user"
            elif linux_cmd.lower().startswith("uname"):
                output += "Linux"
            elif linux_cmd.lower().startswith("date"):
                output += datetime.now().strftime('%a %d %b %Y %H:%M:%S')
            elif linux_cmd.lower() == "help" or linux_cmd.lower() == "--help":
                output += """
Häufige Linux-Befehle:
ls      - Dateien auflisten
pwd     - aktuelles Verzeichnis
cd      - Verzeichnis wechseln
cp      - Dateien kopieren
mv      - Dateien verschieben
rm      - Dateien löschen
mkdir   - Verzeichnis erstellen
cat     - Dateiinhalt anzeigen
grep    - Text suchen
sudo    - als Administrator ausführen
                """
            elif linux_cmd.lower().startswith("sudo"):
                output += "[sudo] Passwort für user:\n"
                output += "Root-Rechte erforderlich!"
            else:
                output += f"bash: {linux_cmd}: Befehl nicht gefunden"
            
            st.code(output, language="bash")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Distributionsauswahl
        st.markdown("### 📦 Beliebte Distributionen")
        distro = st.selectbox("Wähle eine Distribution:", 
                             ["Ubuntu", "Fedora", "Debian", "Arch Linux", "Linux Mint"])
        
        distro_info = {
            "Ubuntu": "Benutzerfreundlich, große Community, ideal für Einsteiger",
            "Fedora": "Cutting-edge, von Red Hat gesponsert",
            "Debian": "Sehr stabil, Grundlage für Ubuntu",
            "Arch Linux": "Für Fortgeschrittene, Rolling Release",
            "Linux Mint": "Besonders einsteigerfreundlich, basiert auf Ubuntu"
        }
        st.info(distro_info[distro])
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking + Echtzeit")
        st.metric("Benutzer", "Multi-User")
        st.metric("Dialog/Batch", "Beides")
        st.metric("Prozessoren", "Mehrere")
        
        st.markdown("### Vorteile")
        st.success("✓ Open Source")
        st.success("✓ Kostenlos")
        st.success("✓ Sehr sicher")
        st.success("✓ Hoch anpassbar")
        st.success("✓ Starke Community")

# =====================
# ANDROID SIMULATION
# =====================
def simulate_android():
    st.header("📱 Android")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Weit verbreitet auf Smartphones und Tablets
        - Basiert auf Linux
        - Open Source, große App-Auswahl
        - Erscheinungsjahr: 2008
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Android Home Screen
        st.markdown("### 📱 Home Screen")
        
        # Status Bar
        st.markdown("🔋 95% | 📶 4G | 🕐 " + datetime.now().strftime('%H:%M'))
        
        # App Grid
        col_a, col_b, col_c, col_d = st.columns(4)
        
        apps = [
            ("📞", "Telefon"),
            ("💬", "Nachrichten"),
            ("📧", "Gmail"),
            ("🌐", "Chrome"),
            ("📷", "Kamera"),
            ("🗺️", "Maps"),
            ("▶️", "YouTube"),
            ("🎵", "Musik"),
            ("📱", "Einstellungen"),
            ("📸", "Galerie"),
            ("📅", "Kalender"),
            ("⏰", "Uhr")
        ]
        
        for i, (icon, name) in enumerate(apps):
            col = [col_a, col_b, col_c, col_d][i % 4]
            with col:
                if st.button(f"{icon}\n{name}", key=f"android_{name}"):
                    st.toast(f"{name} wird geöffnet...")
        
        st.markdown("---")
        
        # Quick Settings
        with st.expander("⚙️ Schnelleinstellungen"):
            col1a, col2a, col3a, col4a = st.columns(4)
            with col1a:
                st.checkbox("📶 WLAN", value=True)
            with col2a:
                st.checkbox("📱 Mobile Daten", value=True)
            with col3a:
                st.checkbox("🔇 Stumm", value=False)
            with col4a:
                st.checkbox("✈️ Flugmodus", value=False)
        
        # Google Play Store
        st.markdown("### 🏪 Google Play Store")
        st.write("**Empfohlene Apps:**")
        play_apps = ["WhatsApp", "Instagram", "Spotify", "Netflix", "TikTok"]
        for app in play_apps:
            col_x, col_y = st.columns([3, 1])
            with col_x:
                st.write(f"📱 {app}")
            with col_y:
                if st.button("Installieren", key=f"install_{app}"):
                    st.success(f"{app} installiert!")
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Single-User")
        st.metric("Dialog/Batch", "Dialog")
        st.metric("Prozessoren", "1")
        
        st.markdown("### Besonderheiten")
        st.success("✓ Millionen Apps")
        st.success("✓ Google-Integration")
        st.success("✓ Anpassbar")
        st.success("✓ Viele Hersteller")

# =====================
# iOS SIMULATION
# =====================
def simulate_ios():
    st.header("📱 iOS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Exklusiv für iPhones und iPads
        - Nahtlose Integration mit Apple-Ökosystem
        - Hohe Sicherheit
        - Erscheinungsjahr: 2007
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # iOS Home Screen
        st.markdown("### 📱 iPhone Home Screen")
        
        # Status Bar
        st.markdown("🕐 " + datetime.now().strftime('%H:%M') + " | 📶 5G | 🔋 92%")
        
        # App Icons
        col_a, col_b, col_c, col_d = st.columns(4)
        
        ios_apps = [
            ("📱", "Telefon"),
            ("💬", "Nachrichten"),
            ("📧", "Mail"),
            ("🌐", "Safari"),
            ("📷", "Kamera"),
            ("📸", "Fotos"),
            ("🗺️", "Karten"),
            ("🎵", "Musik"),
            ("⚙️", "Einstellungen"),
            ("📺", "TV"),
            ("📅", "Kalender"),
            ("⏰", "Uhr")
        ]
        
        for i, (icon, name) in enumerate(ios_apps):
            col = [col_a, col_b, col_c, col_d][i % 4]
            with col:
                if st.button(f"{icon}\n{name}", key=f"ios_{name}"):
                    st.toast(f"{name} geöffnet", icon=icon)
        
        st.markdown("---")
        
        # Control Center
        with st.expander("🎛️ Kontrollzentrum"):
            col1a, col2a = st.columns(2)
            with col1a:
                st.slider("🔆 Helligkeit", 0, 100, 80, key="ios_brightness")
                st.slider("🔊 Lautstärke", 0, 100, 60, key="ios_volume")
            with col2a:
                st.checkbox("📶 WLAN", value=True, key="ios_wifi")
                st.checkbox("📱 Mobile Daten", value=True, key="ios_data")
                st.checkbox("🔵 Bluetooth", value=True, key="ios_bt")
        
        # App Store
        st.markdown("### 🏪 App Store")
        st.write("**Top-Charts:**")
        ios_store_apps = ["iMessage", "FaceTime", "Pages", "Keynote", "GarageBand"]
        for app in ios_store_apps:
            col_x, col_y = st.columns([3, 1])
            with col_x:
                st.write(f"📱 {app}")
            with col_y:
                if st.button("Laden", key=f"download_{app}"):
                    with st.spinner("Laden..."):
                        time.sleep(1)
                    st.success("Installiert!")
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Single-User")
        st.metric("Dialog/Batch", "Dialog")
        st.metric("Prozessoren", "1")
        
        st.markdown("### Apple-Ökosystem")
        st.success("✓ iCloud")
        st.success("✓ AirDrop")
        st.success("✓ Handoff")
        st.success("✓ FaceTime")
        st.success("✓ iMessage")

# =====================
# UNIX SIMULATION
# =====================
def simulate_unix():
    st.header("🖥️ Unix")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Stabil, sicher, Grundlage für viele andere Betriebssysteme
        - Multi-User, Multitasking
        - Vor allem auf Servern und Workstations
        - Erscheinungsjahr: 1969
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Unix Terminal
        st.markdown("### 💻 Unix Shell")
        st.markdown('<div class="terminal">', unsafe_allow_html=True)
        
        unix_cmd = st.text_input("root@unix:/#", key="unix_input")
        
        if unix_cmd:
            output = f"root@unix:/# {unix_cmd}\n"
            
            if unix_cmd.lower().startswith("ls"):
                output += "bin  boot  dev  etc  home  lib  mnt  opt  proc  root  sbin  tmp  usr  var"
            elif unix_cmd.lower().startswith("ps"):
                output += """
PID   TTY      TIME CMD
1     tty1     0:00 init
125   tty1     0:01 bash
342   tty1     0:00 ps
                """
            elif unix_cmd.lower().startswith("top"):
                output += "System-Monitor gestartet...\nCPU: 15% | RAM: 2.1GB/8GB | Prozesse: 143"
            elif unix_cmd.lower().startswith("who"):
                output += "root     tty1     " + datetime.now().strftime('%Y-%m-%d %H:%M')
            elif unix_cmd.lower().startswith("uptime"):
                output += "System läuft seit 45 Tagen, 12:34"
            else:
                output += f"command not found: {unix_cmd}"
            
            st.code(output, language="bash")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔧 Typische Unix-Eigenschaften")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Multiuser-Fähigkeit:**")
            st.code("""
$ users
root admin user1 user2

$ finger user1
Login: user1
Name: John Doe
Last login: Mon Jan 15 09:23
            """)
        
        with col_b:
            st.write("**Prozessverwaltung:**")
            st.code("""
$ ps aux | grep apache
apache  1234  0.5  2.1
apache  1235  0.3  1.8

$ kill -9 1234
Prozess beendet
            """)
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Multi-User")
        st.metric("Dialog/Batch", "Beides")
        st.metric("Prozessoren", "Mehrere")
        
        st.markdown("### Einsatzgebiete")
        st.info("🖥️ Server")
        st.info("💼 Workstations")
        st.info("🏢 Enterprise-Systeme")
        
        st.markdown("### Ableger")
        st.write("• Linux")
        st.write("• macOS")
        st.write("• BSD-Systeme")

# =====================
# CHROME OS SIMULATION
# =====================
def simulate_chromeos():
    st.header("🌐 Chrome OS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Leichtgewichtig, basiert auf Linux
        - Stark auf Cloud-Dienste ausgerichtet
        - Schnelle Boot-Zeiten
        - Erscheinungsjahr: 2011
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chrome OS Desktop
        st.markdown("### 💻 Chrome OS Desktop")
        
        # Browser-zentrierte Oberfläche
        st.markdown("#### 🌐 Google Chrome Browser")
        
        tab1, tab2, tab3 = st.tabs(["🏠 Startseite", "☁️ Google Drive", "🛠️ Einstellungen"])
        
        with tab1:
            url = st.text_input("🔍", placeholder="Suchen oder URL eingeben...", key="chrome_url")
            if url:
                st.info(f"Navigiere zu: {url}")
            
            st.markdown("#### Häufig besucht:")
            col_a, col_b, col_c, col_d = st.columns(4)
            websites = ["Gmail", "Google Docs", "YouTube", "Google Drive"]
            for i, site in enumerate(websites):
                col = [col_a, col_b, col_c, col_d][i]
                with col:
                    if st.button(f"🌐\n{site}", key=f"site_{site}"):
                        st.success(f"{site} wird geöffnet...")
        
        with tab2:
            st.markdown("#### ☁️ Google Drive")
            st.info("Alle Dateien werden automatisch in der Cloud gespeichert")
            
            cloud_files = {
                "Dokumente": ["Präsentation.pptx", "Bericht.docx"],
                "Tabellen": ["Budget.xlsx", "Daten.csv"],
                "Formulare": ["Umfrage.form"]
            }
            
            for folder, files in cloud_files.items():
                with st.expander(f"📁 {folder}"):
                    for f in files:
                        col_x, col_y = st.columns([3, 1])
                        with col_x:
                            st.write(f"📄 {f}")
                        with col_y:
                            if st.button("Öffnen", key=f"cloud_{f}"):
                                st.success("In Google Docs geöffnet!")
        
        with tab3:
            st.markdown("#### ⚙️ Chrome OS Einstellungen")
            st.checkbox("Google-Konto synchronisieren", value=True)
            st.checkbox("Offline-Zugriff aktivieren", value=True)
            st.selectbox("Standard-Suchmaschine", ["Google", "Bing", "DuckDuckGo"])
            st.slider("Zoom-Stufe", 50, 200, 100, step=25, format="%d%%")
        
        st.markdown("---")
        st.markdown("🌐 Chrome | 📁 Dateien | ⚙️ Einstellungen | " + datetime.now().strftime('%H:%M'))
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Single-User")
        st.metric("Dialog/Batch", "Dialog")
        st.metric("Prozessoren", "1")
        
        st.markdown("### Vorteile")
        st.success("✓ Sehr schnell")
        st.success("✓ Cloud-basiert")
        st.success("✓ Günstige Hardware")
        st.success("✓ Automatische Updates")
        st.success("✓ Sicher")

# =====================
# FreeBSD SIMULATION
# =====================
def simulate_freebsd():
    st.header("😈 FreeBSD")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        **Besonderheiten:**
        - Open Source, bekannt für Stabilität und Sicherheit
        - Starke Netzwerkfähigkeiten
        - Multi-User, Multitasking
        - Erscheinungsjahr: 1993
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # FreeBSD Terminal
        st.markdown("### 💻 FreeBSD Shell")
        st.markdown('<div class="terminal">', unsafe_allow_html=True)
        
        bsd_cmd = st.text_input("freebsd%", key="bsd_input")
        
        if bsd_cmd:
            output = f"freebsd% {bsd_cmd}\n"
            
            if bsd_cmd.lower().startswith("uname"):
                output += "FreeBSD 13.2-RELEASE"
            elif bsd_cmd.lower().startswith("pkg"):
                output += """
FreeBSD Package Manager
Installierte Pakete: 342
Verfügbare Updates: 12
Verwenden Sie 'pkg install <name>' zum Installieren
                """
            elif bsd_cmd.lower().startswith("sockstat"):
                output += """
USER    COMMAND    PID   FD PROTO  LOCAL ADDRESS         FOREIGN ADDRESS
root    sshd       645   3  tcp4   *:22                  *:*
www     httpd      892   4  tcp4   *:80                  *:*
                """
            elif bsd_cmd.lower().startswith("jls"):
                output += """
JID  IP Address      Hostname      Path
1    192.168.1.10    jail1         /usr/jails/jail1
2    192.168.1.11    jail2         /usr/jails/jail2
                """
                st.info("FreeBSD Jails: Lightweight Virtualisierung für erhöhte Sicherheit")
            else:
                output += f"{bsd_cmd}: command not found"
            
            st.code(output, language="bash")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔒 Sicherheitsfeatures")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Jails (Container):**")
            st.code("""
# Jail erstellen
jail -c name=testjail \\
  path=/jails/test \\
  host.hostname=test.local \\
  ip4.addr=192.168.1.100
            """)
        
        with col_b:
            st.write("**Firewall (pf):**")
            st.code("""
# Firewall-Regeln
block all
pass in on em0 proto tcp \\
  from any to any port 22
pass out all keep state
            """)
        
        st.markdown("### 📦 Ports Collection")
        st.info("FreeBSD Ports: Über 30.000 Software-Pakete als Quellcode verfügbar")
    
    with col2:
        st.markdown("### Eigenschaften")
        st.metric("Betriebsart", "Multitasking")
        st.metric("Benutzer", "Multi-User")
        st.metric("Dialog/Batch", "Beides")
        st.metric("Prozessoren", "Mehrere")
        
        st.markdown("### Stärken")
        st.success("✓ Sehr stabil")
        st.success("✓ Hohe Sicherheit")
        st.success("✓ Exzellentes Networking")
        st.success("✓ ZFS Dateisystem")
        
        st.markdown("### Einsatz")
        st.write("• Webserver")
        st.write("• Storage-Systeme (z.B. Netflix)")
        st.write("• Firewalls")

# =====================
# VERGLEICHSTABELLE
# =====================
def show_comparison():
    st.header("📊 Vergleichsübersicht")
    
    st.markdown("""
    Diese Tabelle zeigt die wichtigsten Unterschiede zwischen den Betriebssystemen auf einen Blick:
    """)
    
    comparison_data = {
        "Betriebssystem": ["DOS", "Windows", "macOS", "Linux", "Android", "iOS", "Unix", "Chrome OS", "FreeBSD"],
        "Jahr": [1981, 1985, 2001, 1991, 2008, 2007, 1969, 2011, 1993],
        "Hersteller": ["Microsoft", "Microsoft", "Apple", "Versch.", "Google", "Apple", "Versch.", "Google", "FreeBSD Project"],
        "Einsatzbereich": ["Desktop", "Desktop/Server", "Desktop", "Desktop/Server", "Mobile", "Mobile", "Server", "Laptops", "Server"],
        "Single/Multi-User": ["Single", "Multi", "Single", "Multi", "Single", "Single", "Multi", "Single", "Multi"],
        "Single/Multi-tasking": ["Single", "Multi", "Multi", "Multi", "Multi", "Multi", "Multi", "Multi", "Multi"],
        "Open Source": ["❌", "❌", "❌", "✅", "✅", "❌", "Teils", "❌", "✅"]
    }
    
    st.dataframe(comparison_data, use_container_width=True)
    
    # Interaktiver Vergleich
    st.markdown("### 🔍 Detailvergleich")
    
    col1, col2 = st.columns(2)
    
    with col1:
        os1 = st.selectbox("Betriebssystem 1:", 
                          ["DOS", "Windows", "macOS", "Linux", "Android", "iOS", "Unix", "Chrome OS", "FreeBSD"],
                          index=1, key="comp1")
    
    with col2:
        os2 = st.selectbox("Betriebssystem 2:", 
                          ["DOS", "Windows", "macOS", "Linux", "Android", "iOS", "Unix", "Chrome OS", "FreeBSD"],
                          index=3, key="comp2")
    
    if os1 != os2:
        comparison_details = {
            "Windows": {"Benutzerfreundlichkeit": 9, "Anpassbarkeit": 6, "Sicherheit": 6, "Performance": 7, "Software-Auswahl": 10},
            "macOS": {"Benutzerfreundlichkeit": 9, "Anpassbarkeit": 4, "Sicherheit": 9, "Performance": 9, "Software-Auswahl": 7},
            "Linux": {"Benutzerfreundlichkeit": 6, "Anpassbarkeit": 10, "Sicherheit": 9, "Performance": 9, "Software-Auswahl": 7},
            "Android": {"Benutzerfreundlichkeit": 8, "Anpassbarkeit": 8, "Sicherheit": 6, "Performance": 7, "Software-Auswahl": 10},
            "iOS": {"Benutzerfreundlichkeit": 10, "Anpassbarkeit": 3, "Sicherheit": 10, "Performance": 9, "Software-Auswahl": 9},
            "DOS": {"Benutzerfreundlichkeit": 2, "Anpassbarkeit": 2, "Sicherheit": 3, "Performance": 5, "Software-Auswahl": 2},
            "Unix": {"Benutzerfreundlichkeit": 5, "Anpassbarkeit": 9, "Sicherheit": 10, "Performance": 10, "Software-Auswahl": 6},
            "Chrome OS": {"Benutzerfreundlichkeit": 9, "Anpassbarkeit": 4, "Sicherheit": 8, "Performance": 8, "Software-Auswahl": 6},
            "FreeBSD": {"Benutzerfreundlichkeit": 5, "Anpassbarkeit": 9, "Sicherheit": 10, "Performance": 10, "Software-Auswahl": 7}
        }
        
        st.markdown(f"#### Vergleich: {os1} vs {os2}")
        
        for criterion in ["Benutzerfreundlichkeit", "Anpassbarkeit", "Sicherheit", "Performance", "Software-Auswahl"]:
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_a:
                st.metric(os1, comparison_details[os1][criterion])
            with col_b:
                st.write(f"**{criterion}**")
            with col_c:
                st.metric(os2, comparison_details[os2][criterion])

# =====================
# QUIZ
# =====================
def show_quiz():
    st.header("🎯 Wissenstest")
    
    st.markdown("""
    Teste dein Wissen über Betriebssysteme!
    """)
    
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    if not st.session_state.quiz_started:
        if st.button("Quiz starten", type="primary"):
            st.session_state.quiz_started = True
            st.session_state.quiz_score = 0
            st.rerun()
    else:
        questions = [
            {
                "question": "Welches Betriebssystem ist Open Source?",
                "options": ["Windows", "macOS", "Linux", "iOS"],
                "correct": "Linux"
            },
            {
                "question": "Welches Betriebssystem verwendet Jails für Sicherheit?",
                "options": ["Linux", "Windows", "FreeBSD", "Android"],
                "correct": "FreeBSD"
            },
            {
                "question": "Welches war das erste Betriebssystem in der Liste?",
                "options": ["DOS", "Unix", "Windows", "Linux"],
                "correct": "Unix"
            },
            {
                "question": "Welches Betriebssystem ist stark Cloud-orientiert?",
                "options": ["DOS", "Chrome OS", "FreeBSD", "Unix"],
                "correct": "Chrome OS"
            },
            {
                "question": "Welches Betriebssystem unterstützt Single-Tasking?",
                "options": ["DOS", "Windows", "Linux", "macOS"],
                "correct": "DOS"
            }
        ]
        
        for i, q in enumerate(questions):
            st.markdown(f"**Frage {i+1}:** {q['question']}")
            answer = st.radio("", q['options'], key=f"q{i}", label_visibility="collapsed")
            
            if st.button(f"Prüfen", key=f"check{i}"):
                if answer == q['correct']:
                    st.success("✅ Richtig!")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"❌ Falsch! Die richtige Antwort ist: {q['correct']}")
            
            st.markdown("---")
        
        if st.button("Quiz beenden"):
            st.balloons()
            st.success(f"🎉 Du hast {st.session_state.quiz_score} von {len(questions)} Punkten erreicht!")
            st.session_state.quiz_started = False

# =====================
# HAUPTNAVIGATION
# =====================

# Hauptbereich basierend auf Auswahl
if os_choice == "DOS":
    simulate_dos()
elif os_choice == "Windows":
    simulate_windows()
elif os_choice == "macOS":
    simulate_macos()
elif os_choice == "Linux":
    simulate_linux()
elif os_choice == "Android":
    simulate_android()
elif os_choice == "iOS":
    simulate_ios()
elif os_choice == "Unix":
    simulate_unix()
elif os_choice == "Chrome OS":
    simulate_chromeos()
elif os_choice == "FreeBSD":
    simulate_freebsd()

# Zusätzliche Funktionen am Ende
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Vergleichstabelle anzeigen", use_container_width=True):
        show_comparison()

with col2:
    if st.button("🎯 Wissenstest starten", use_container_width=True):
        show_quiz()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💻 Interaktiver Betriebssystem-Simulator | Erstellt für Lernzwecke</p>
    <p><small>Hinweis: Dies ist eine Simulation zu Lernzwecken. Die dargestellten Funktionen sind vereinfacht.</small></p>
</div>
""", unsafe_allow_html=True)
