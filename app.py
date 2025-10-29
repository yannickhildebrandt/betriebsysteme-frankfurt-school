import streamlit as st
import pandas as pd
from streamlit_elements import elements, html, sync
import time # For unique keys and timestamps

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="Betriebssystem-Simulator (Realistisch)",
    page_icon="💻",
    layout="wide"
)

# --- Daten aus der Tabelle ---
os_data = {
    "DOS": {
        "Hersteller": "Microsoft", "Einsatzbereich": "Desktop", "Besonderheiten": "Kommandozeilenbasiert, Grundlage für frühe Windows-Versionen",
        "Unterscheidungsmerkmale": "Einfach, stabil, keine grafische Benutzeroberfläche", "Betriebsarten": "Singletasking",
        "Single-User/Multi-User": "Single-User", "Erst-erscheinung": "1981", "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "Windows": {
        "Hersteller": "Microsoft", "Einsatzbereich": "Desktop, Server", "Besonderheiten": "Weit verbreitet, benutzerfreundlich, viele Anwendungen verfügbar",
        "Unterscheidungsmerkmale": "Benutzerfreundliche Oberfläche, breite Hardware-Kompatibilität, hohe Verbreitung",
        "Betriebsarten": "Multitasking, Timesharing", "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1985", "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "macOS": {
        "Hersteller": "Apple", "Einsatzbereich": "Desktop, Laptop", "Besonderheiten": "Nahtlose Integration mit anderen Apple-Produkten, exklusiv für Apple-Hardware",
        "Unterscheidungsmerkmale": "Exklusiv für Apple-Hardware, hohe Sicherheit, nahtlose Integration mit Apple-Ökosystem",
        "Betriebsarten": "Multitasking, Timesharing", "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2001", "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Linux": {
        "Hersteller": "Versch.", "Einsatzbereich": "Desktop, Server", "Besonderheiten": "Open Source, hohe Anpassbarkeit, viele Distributionen (z.B. Ubuntu, Fedora)",
        "Unterscheidungsmerkmale": "Open Source, hohe Anpassbarkeit, viele Distributionen, starke Community-Unterstützung",
        "Betriebsarten": "Multitasking, Timesharing, Echtzeit", "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1991", "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Android": {
        "Hersteller": "Google", "Einsatzbereich": "Mobile Geräte", "Besonderheiten": "Weit verbreitet auf Smartphones und Tablets, basiert auf Linux",
        "Unterscheidungsmerkmale": "Open Source, hohe App-Auswahl, weit verbreitet auf mobilen Geräten",
        "Betriebsarten": "Multitasking", "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2008", "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "iOS": {
        "Hersteller": "Apple", "Einsatzbereich": "Mobile Geräte", "Besonderheiten": "Exklusiv für iPhones und iPads, nahtlose Integration mit Apple-Ökosystem",
        "Unterscheidungsmerkmale": "Exklusiv für Apple-Hardware, hohe Sicherheit, nahtlose Integration mit Apple-Ökosystem",
        "Betriebsarten": "Multitasking", "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2007", "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "Unix": {
        "Hersteller": "Versch.", "Einsatzbereich": "Server, Workstations", "Besonderheiten": "Stabil, sicher, Grundlage für viele andere Betriebssysteme (z.B. macOS, Linux)",
        "Unterscheidungsmerkmale": "Hohe Stabilität und Sicherheit, Grundlage für viele andere Betriebssysteme, Multiuser-Fähigkeit",
        "Betriebsarten": "Multitasking, Timesharing", "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1969", "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Chrome OS": {
        "Hersteller": "Google", "Einsatzbereich": "Laptops (Chromebooks)", "Besonderheiten": "Leichtgewichtig, basiert auf Linux, stark auf Cloud-Dienste ausgerichtet",
        "Unterscheidungsmerkmale": "Leichtgewichtig, stark auf Cloud-Dienste ausgerichtet, schnelle Boot-Zeiten",
        "Betriebsarten": "Multitasking", "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2011", "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "FreeBSD": {
        "Hersteller": "FreeBSD Project", "Einsatzbereich": "Server, Desktop", "Besonderheiten": "Open Source, bekannt für Stabilität und Sicherheit",
        "Unterscheidungsmerkmale": "Hohe Stabilität und Sicherheit, Open Source, starke Netzwerkfähigkeiten",
        "Betriebsarten": "Multitasking", "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1993", "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    }
}

# Initialisiere den Session State für Fensterpositionen und -größen
if "window_states" not in st.session_state:
    st.session_state["window_states"] = {
        "Windows_Explorer": {"x": 50, "y": 50, "width": 400, "height": 300, "open": False},
        "Windows_Browser": {"x": 100, "y": 100, "width": 500, "height": 400, "open": False},
        "Windows_Notepad": {"x": 150, "y": 150, "width": 350, "height": 250, "open": False},
        "macOS_Finder": {"x": 50, "y": 50, "width": 450, "height": 350, "open": False},
        "macOS_Safari": {"x": 100, "y": 100, "width": 600, "height": 450, "open": False},
        "macOS_TextEdit": {"x": 150, "y": 150, "width": 400, "height": 300, "open": False},
        "Linux_Files": {"x": 50, "y": 50, "width": 400, "height": 300, "open": False},
        "ChromeOS_Browser": {"x": 100, "y": 100, "width": 600, "height": 450, "open": True}, # Default open for ChromeOS
    }

def update_window_state(window_id, x=None, y=None, width=None, height=None, open=None):
    if x is not None: st.session_state["window_states"][window_id]["x"] = x
    if y is not None: st.session_state["window_states"][window_id]["y"] = y
    if width is not None: st.session_state["window_states"][window_id]["width"] = width
    if height is not None: st.session_state["window_states"][window_id]["height"] = height
    if open is not None: st.session_state["window_states"][window_id]["open"] = open

# --- Header ---
st.title("Betriebssysteme - Interaktiver Simulator 💻")
st.markdown("""
Erkunden Sie verschiedene Betriebssysteme und bekommen Sie ein realistischeres Gefühl für deren Kernfunktionen und Charakteristiken.
Wählen Sie ein Betriebssystem aus der Sidebar, um mehr darüber zu erfahren und eine verbesserte Simulation zu starten.
""")

# --- Sidebar für die Auswahl ---
st.sidebar.header("Wählen Sie ein Betriebssystem")
selected_os_name = st.sidebar.selectbox(
    "Betriebssystem:",
    list(os_data.keys()),
    key="os_selector"
)

selected_os_info = os_data[selected_os_name]

# --- Anzeige der grundlegenden Informationen ---
st.subheader(f"Informationen zu {selected_os_name}")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.write(f"**Hersteller:** {selected_os_info['Hersteller']}")
    st.write(f"**Einsatzbereich:** {selected_os_info['Einsatzbereich']}")
    st.write(f"**Besonderheiten:** {selected_os_info['Besonderheiten']}")
    st.write(f"**Unterscheidungsmerkmale:** {selected_os_info['Unterscheidungsmerkmale']}")
with col_info2:
    st.write(f"**Betriebsarten:** {selected_os_info['Betriebsarten']}")
    st.write(f"**Single-User/Multi-User:** {selected_os_info['Single-User/Multi-User']}")
    st.write(f"**Erst-erscheinung:** {selected_os_info['Erst-erscheinung']}")
    st.write(f"**Dialog/Batch:** {selected_os_info['Dialog/Batch']}")
    st.write(f"**Einprozessor/Mehrprozessor:** {selected_os_info['Einprozessor/Mehrprozessor']}")

st.markdown("---")

# --- Interaktive Simulation ---
st.header(f"Erleben Sie {selected_os_name}")

# Global CSS for elements windows
st.markdown("""
<style>
.st-emotion-cache-1f19sfk { /* Target main block for elements */
    min-height: 600px; /* Ensure enough space for windows */
    position: relative; /* Needed for absolute positioning of draggable elements */
}

/* Base style for elements windows */
.os-window {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #ccc;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    overflow: hidden; /* Hide content overflow for resizing */
    z-index: 100;
}

.os-window-titlebar {
    padding: 8px 12px;
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    font-weight: bold;
    user-select: none;
}

.os-window-content {
    flex-grow: 1;
    padding: 10px;
    overflow: auto; /* Enable scrolling for window content */
}

.os-window-close-btn {
    background: none;
    border: none;
    font-size: 1.2em;
    cursor: pointer;
    line-height: 1;
    padding: 0 5px;
    color: #555;
}

.os-window-close-btn:hover {
    color: #f00;
}

/* Specific styles for Windows */
.windows-desktop {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Windows_XP_Bliss.jpg/1920px-Windows_XP_Bliss.jpg');
    background-size: cover;
    background-position: center;
    height: 600px;
    width: 100%;
    border-radius: 8px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.windows-taskbar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    background: linear-gradient(to bottom, #2458a2, #297be2);
    border-top: 1px solid #1a3c71;
    display: flex;
    align-items: center;
    padding: 0 5px;
    z-index: 200;
}

.windows-start-button {
    background: linear-gradient(to right, #46960f, #326b0a);
    border: 1px solid #234d07;
    border-radius: 3px;
    color: white;
    font-weight: bold;
    padding: 5px 15px;
    margin-right: 10px;
    cursor: pointer;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.3);
    transition: background 0.1s;
}

.windows-start-button:hover {
    background: linear-gradient(to right, #54ac17, #3a7c0d);
}

.windows-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px;
    color: white;
    text-shadow: 1px 1px 2px black;
    font-size: 0.8em;
}

.windows-icon img {
    width: 48px;
    height: 48px;
    margin-bottom: 5px;
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: 5px;
    transition: all 0.2s ease-in-out;
}

.windows-icon img:hover {
    border-color: rgba(173, 216, 230, 0.5);
    background-color: rgba(173, 216, 230, 0.2);
}

.windows-titlebar-bg {
    background: linear-gradient(to bottom, #2c6eb5, #225a97);
    color: white;
}

.windows-close-traffic {
    background-color: #f00;
    color: white;
    border: 1px solid #a00;
    border-radius: 3px;
    padding: 0 7px;
    font-weight: bold;
    cursor: pointer;
}


/* Specific styles for macOS */
.mac-desktop {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/b/b3/MacOS_Ventura_wallpaper.jpg'); /* macOS Ventura */
    background-size: cover;
    background-position: center;
    height: 600px;
    width: 100%;
    border-radius: 8px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.mac-menubar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 22px;
    background-color: rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    color: white;
    display: flex;
    align-items: center;
    padding: 0 10px;
    font-size: 0.9em;
    z-index: 200;
}

.mac-menubar-item {
    padding: 0 8px;
    cursor: pointer;
}

.mac-menubar-item:hover {
    background-color: rgba(255,255,255,0.2);
    border-radius: 3px;
}

.mac-dock {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0,0,0,0.3);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 8px 15px;
    display: flex;
    gap: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    z-index: 200;
}

.mac-dock-icon {
    width: 48px;
    height: 48px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
}

.mac-dock-icon:hover {
    transform: scale(1.1);
}

.mac-window-titlebar {
    background: rgba(255,255,255,0.9);
    color: #444;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: center;
    padding: 5px 10px;
    cursor: grab;
}

.mac-traffic-lights {
    display: flex;
    gap: 7px;
    margin-right: 10px;
}

.mac-traffic-lights div {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 0.5px solid rgba(0,0,0,0.2);
}
.mac-traffic-lights .close { background-color: #ff5f56; }
.mac-traffic-lights .minimize { background-color: #ffbd2e; }
.mac-traffic-lights .maximize { background-color: #27c93f; }

.mac-window-title {
    flex-grow: 1;
    text-align: center;
    font-weight: bold;
    color: #333;
}


/* Mobile device frames (Android/iOS) */
.mobile-frame {
    width: 320px;
    height: 600px;
    border: 10px solid #222;
    border-radius: 40px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    margin: 20px auto;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.mobile-notch {
    width: 120px;
    height: 25px;
    background: #222;
    border-radius: 0 0 15px 15px;
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
}
.mobile-home-button {
    width: 35px;
    height: 35px;
    border: 1px solid #ccc;
    border-radius: 50%;
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    background: #eee;
    cursor: pointer;
    z-index: 10;
}
.mobile-screen {
    flex-grow: 1;
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 10px;
}
.mobile-status-bar {
    display: flex;
    justify-content: space-between;
    color: white;
    font-size: 0.8em;
    padding: 5px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
.mobile-app-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    padding: 10px;
}
.mobile-app-icon {
    text-align: center;
    color: white;
    font-size: 0.7em;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
}
.mobile-app-icon img {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    transition: transform 0.1s;
}
.mobile-app-icon img:active {
    transform: scale(0.95);
}
.mobile-dock {
    display: flex;
    justify-content: space-around;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 8px;
    margin: 0 10px 10px 10px;
}
.mobile-notification {
    position: absolute;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0,0,0,0.7);
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 0.9em;
    z-index: 10;
    min-width: 80%;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* Chrome OS */
.chromeos-desktop {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e0/Chrome_OS_desktop_after_OOBE.png'); /* Placeholder Chrome OS background */
    background-size: cover;
    background-position: center;
    height: 600px;
    width: 100%;
    border-radius: 8px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}
.chromeos-shelf {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50px;
    background-color: rgba(0,0,0,0.5);
    backdrop-filter: blur(5px);
    display: flex;
    align-items: center;
    padding: 0 10px;
    border-radius: 0 0 8px 8px; /* Match desktop border radius */
    z-index: 100;
}
.chromeos-shelf-icon {
    width: 40px;
    height: 40px;
    margin: 0 5px;
    border-radius: 50%;
    cursor: pointer;
    background-color: rgba(255,255,255,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5em;
    color: white;
    transition: background-color 0.1s;
}
.chromeos-shelf-icon:hover {
    background-color: rgba(255,255,255,0.4);
}
.chromeos-browser-content {
    flex-grow: 1;
    padding: 15px;
    text-align: center;
    color: #3c4043;
    overflow-y: auto;
    background-color: white;
}
.chromeos-browser-toolbar {
    background-color: #f1f3f4;
    padding: 8px 10px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #dadce0;
}
.chromeos-address-bar {
    background-color: white;
    border: 1px solid #dadce0;
    border-radius: 20px;
    padding: 5px 10px;
    flex-grow: 1;
    margin: 0 10px;
    color: #3c4043;
    font-size: 14px;
}
.chromeos-browser-btn {
    background: none;
    border: none;
    font-size: 1.2em;
    cursor: pointer;
    color: #5f6368;
    padding: 0 5px;
}

</style>
""", unsafe_allow_html=True)


# --- OS-spezifische Simulationen ---

if selected_os_name == "DOS":
    st.markdown("""
    **DOS (Disk Operating System)** war ein kommandozeilenbasiertes System.
    Hier interagieren Sie direkt durch Eingabe von Befehlen in einem simulierten Terminal.
    """)
    st.markdown("<div style='background-color:#000080; color:#CCCCCC; padding:20px; border-radius:8px; font-family:\"Lucida Console\", \"Courier New\", monospace; font-size:1.1em; line-height:1.4;'>", unsafe_allow_html=True)
    st.write("`Microsoft(R) MS-DOS(R) Version 6.22`")
    st.write("`(C)Copyright Microsoft Corp 1981-1994.`")
    st.write("")
    
    if "dos_history" not in st.session_state:
        st.session_state["dos_history"] = []
    
    for entry in st.session_state["dos_history"]:
        st.write(entry)
    
    command = st.text_input("`C:\\>`", key="dos_command_input", help="Probieren Sie 'dir', 'echo Hello World', 'cd ..', 'help', 'exit'")
    
    if st.button("Ausführen", key="dos_execute_btn"):
        st.session_state["dos_history"].append(f"`C:\\>{command}`")
        command = command.lower().strip()
        
        output = ""
        if command == "dir":
            output = """` Volume in drive C has no label.
 Volume Serial Number is 1234-5678
 
 Directory of C:\\
 
 COMMAND  COM     54,645  06-25-93  6:22a
 AUTOEXEC BAT          34  06-25-93  6:22a
 CONFIG   SYS          21  06-25-93  6:22a
         3 file(s)     54,700 bytes
                       14,576,640 bytes free`"""
        elif command.startswith("echo "):
            output = f"`{command[5:]}`"
        elif command == "cd ..":
            output = "`C:\\>`"
        elif command == "help":
            output = """`DIR        Displays a list of files and subdirectories.
ECHO       Displays messages, or turns command echoing on or off.
CD         Changes the current directory.
EXIT       Exits the MS-DOS command interpreter.`"""
        elif command == "exit":
            output = "`DOS-Sitzung beendet. Bitte starten Sie neu.`"
            st.session_state["dos_history"] = [] # Clear history on exit
        else:
            output = f"`Bad command or file name: {command}`"
        
        st.session_state["dos_history"].append(output)
        st.rerun() # Rerun to display updated history
    
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_os_name == "Windows":
    st.markdown("""
    **Windows** zeichnet sich durch seine grafische Benutzeroberfläche und Multitasking-Fähigkeit aus.
    Hier können Sie bewegliche und in der Größe veränderbare "Anwendungsfenster" erleben.
    """)

    if st.button("📁 Explorer öffnen", key="win_explorer_btn"):
        update_window_state("Windows_Explorer", open=not st.session_state["window_states"]["Windows_Explorer"]["open"])
    if st.button("🌐 Browser öffnen", key="win_browser_btn"):
        update_window_state("Windows_Browser", open=not st.session_state["window_states"]["Windows_Browser"]["open"])
    if st.button("📝 Notizblock öffnen", key="win_notepad_btn"):
        update_window_state("Windows_Notepad", open=not st.session_state["window_states"]["Windows_Notepad"]["open"])

    with elements("windows_desktop_elements"):
        html.div(
            html.div(
                # Desktop Icons
                html.div(
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/My_Computer_icon.svg/48px-My_Computer_icon.svg.png", alt="My Computer"),
                    html.div("Arbeitsplatz"),
                    className="windows-icon",
                    onClick=sync(lambda: update_window_state("Windows_Explorer", open=not st.session_state["window_states"]["Windows_Explorer"]["open"]))
                ),
                html.div(
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Internet_Explorer_7_Icon.svg/48px-Internet_Explorer_7_Icon.svg.png", alt="Internet Explorer"),
                    html.div("Internet Explorer"),
                    className="windows-icon",
                    onClick=sync(lambda: update_window_state("Windows_Browser", open=not st.session_state["window_states"]["Windows_Browser"]["open"]))
                ),
                html.div(
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Nuvola_apps_kedit.png/48px-Nuvola_apps_kedit.png", alt="Notepad"),
                    html.div("Notizblock"),
                    className="windows-icon",
                    onClick=sync(lambda: update_window_state("Windows_Notepad", open=not st.session_state["window_states"]["Windows_Notepad"]["open"]))
                ),
                style={"display": "flex", "flex-wrap": "wrap", "align-content": "flex-start", "height": "calc(100% - 40px)", "padding-top": "15px"}
            ),
            # Taskbar
            html.div(
                html.button("Start", className="windows-start-button"),
                className="windows-taskbar",
            ),
            className="windows-desktop",
        )

        # Windows Explorer Window
        explorer_state = st.session_state["window_states"]["Windows_Explorer"]
        if explorer_state["open"]:
            html.div(
                html.div("📁 Eigene Dateien", className="os-window-titlebar windows-titlebar-bg"),
                html.div("""
                    <p>Inhalt von 'Eigene Dateien':</p>
                    <ul>
                        <li>Dokument.docx</li>
                        <li>Bild.jpg</li>
                        <li>Präsentation.pptx</li>
                        <li>(Dies ist ein simulierter Dateibrowser)</li>
                    </ul>
                """, className="os-window-content"),
                key="Windows_Explorer_Win",
                css=(
                    ".os-window { background: white; }" # Override default window background
                    f"transform: translate({explorer_state['x']}px, {explorer_state['y']}px);"
                ),
                style={
                    "position": "absolute",
                    "width": explorer_state['width'],
                    "height": explorer_state['height'],
                    "top": 0, "left": 0, # Controlled by transform
                },
                className="os-window",
                draggable={"handle": ".os-window-titlebar", "default": {"x": explorer_state["x"], "y": explorer_state["y"]}, "onStop": sync.set_state("Windows_Explorer", "x", "y")},
                resizable={"default": {"width": explorer_state["width"], "height": explorer_state["height"]}, "onStop": sync.set_state("Windows_Explorer", "width", "height")}
            )
        
        # Windows Browser Window
        browser_state = st.session_state["window_states"]["Windows_Browser"]
        if browser_state["open"]:
            html.div(
                html.div("🌐 Internet Browser", className="os-window-titlebar windows-titlebar-bg"),
                html.iframe(src="https://streamlit.io", style={"height": "100%", "width": "100%", "border": "none"}),
                key="Windows_Browser_Win",
                css=f"transform: translate({browser_state['x']}px, {browser_state['y']}px);",
                style={
                    "position": "absolute",
                    "width": browser_state['width'],
                    "height": browser_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".os-window-titlebar", "default": {"x": browser_state["x"], "y": browser_state["y"]}, "onStop": sync.set_state("Windows_Browser", "x", "y")},
                resizable={"default": {"width": browser_state["width"], "height": browser_state["height"]}, "onStop": sync.set_state("Windows_Browser", "width", "height")}
            )

        # Windows Notepad Window
        notepad_state = st.session_state["window_states"]["Windows_Notepad"]
        if notepad_state["open"]:
            html.div(
                html.div("📝 Notizblock", className="os-window-titlebar windows-titlebar-bg"),
                html.textarea("Dies ist ein simulierter Notizblock. Sie können hier Text eingeben.",
                              style={"width": "100%", "height": "100%", "border": "none", "padding": "10px", "resize": "none", "font-family": "monospace"}),
                key="Windows_Notepad_Win",
                css=f"transform: translate({notepad_state['x']}px, {notepad_state['y']}px);",
                style={
                    "position": "absolute",
                    "width": notepad_state['width'],
                    "height": notepad_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".os-window-titlebar", "default": {"x": notepad_state["x"], "y": notepad_state["y"]}, "onStop": sync.set_state("Windows_Notepad", "x", "y")},
                resizable={"default": {"width": notepad_state["width"], "height": notepad_state["height"]}, "onStop": sync.set_state("Windows_Notepad", "width", "height")}
            )

elif selected_os_name == "macOS":
    st.markdown("""
    **macOS** (früher OS X) bietet eine elegante, intuitive grafische Oberfläche und ist bekannt für seine nahtlose Integration im Apple-Ökosystem.
    Hier sehen Sie eine stilisierte Oberfläche mit einem "Dock" und beweglichen Fenstern.
    """)

    if st.button("📁 Finder öffnen", key="mac_finder_btn"):
        update_window_state("macOS_Finder", open=not st.session_state["window_states"]["macOS_Finder"]["open"])
    if st.button("🌐 Safari öffnen", key="mac_safari_btn"):
        update_window_state("macOS_Safari", open=not st.session_state["window_states"]["macOS_Safari"]["open"])
    if st.button("📝 TextEdit öffnen", key="mac_textedit_btn"):
        update_window_state("macOS_TextEdit", open=not st.session_state["window_states"]["macOS_TextEdit"]["open"])

    with elements("mac_desktop_elements"):
        html.div(
            # Menu Bar
            html.div(
                html.div("", className="mac-menubar-item"),
                html.div("Finder", className="mac-menubar-item", style={"font-weight": "bold"}),
                html.div("Ablage", className="mac-menubar-item"),
                html.div("Bearbeiten", className="mac-menubar-item"),
                html.div("Darstellung", className="mac-menubar-item"),
                style={"flex-grow": 1, "display": "flex"},
                html.div(f"{time.strftime('%H:%M')} {time.strftime('%a %d.%m.')}", className="mac-menubar-item"), # Current time
                className="mac-menubar",
            ),
            # Dock
            html.div(
                html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Finder_icon.svg/48px-Finder_icon.svg.png", alt="Finder", className="mac-dock-icon",
                         onClick=sync(lambda: update_window_state("macOS_Finder", open=not st.session_state["window_states"]["macOS_Finder"]["open"]))
                ),
                html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Safari_icon_%28iOS%29.svg/48px-Safari_icon_%28iOS%29.svg.png", alt="Safari", className="mac-dock-icon",
                         onClick=sync(lambda: update_window_state("macOS_Safari", open=not st.session_state["window_states"]["macOS_Safari"]["open"]))
                ),
                html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Apple_Mail_icon.svg/48px-Apple_Mail_icon.svg.png", alt="Mail", className="mac-dock-icon"),
                html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/App_Store_iOS_11.png/48px-App_Store_iOS_11.png", alt="App Store", className="mac-dock-icon"),
                className="mac-dock",
            ),
            className="mac-desktop",
        )

        # macOS Finder Window
        finder_state = st.session_state["window_states"]["macOS_Finder"]
        if finder_state["open"]:
            html.div(
                html.div(
                    html.div(
                        html.div(onClick=sync(lambda: update_window_state("macOS_Finder", open=False)), className="close"),
                        html.div(className="minimize"),
                        html.div(className="maximize"),
                        className="mac-traffic-lights"
                    ),
                    html.span("📁 Finder", className="mac-window-title"),
                    className="mac-window-titlebar"
                ),
                html.div("""
                    <p>Willkommen im Finder!</p>
                    <ul>
                        <li>Programme</li>
                        <li>Dokumente</li>
                        <li>Downloads</li>
                        <li>Schreibtisch</li>
                    </ul>
                    <p>(Ein simulierter Dateibrowser für macOS)</p>
                """, className="os-window-content"),
                key="macOS_Finder_Win",
                css=(
                    ".os-window { background: rgba(230, 230, 230, 0.95); border: 1px solid #bbb; }" # Override default window background
                    f"transform: translate({finder_state['x']}px, {finder_state['y']}px);"
                ),
                style={
                    "position": "absolute",
                    "width": finder_state['width'],
                    "height": finder_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".mac-window-titlebar", "default": {"x": finder_state["x"], "y": finder_state["y"]}, "onStop": sync.set_state("macOS_Finder", "x", "y")},
                resizable={"default": {"width": finder_state["width"], "height": finder_state["height"]}, "onStop": sync.set_state("macOS_Finder", "width", "height")}
            )

        # macOS Safari Window
        safari_state = st.session_state["window_states"]["macOS_Safari"]
        if safari_state["open"]:
            html.div(
                html.div(
                    html.div(
                        html.div(onClick=sync(lambda: update_window_state("macOS_Safari", open=False)), className="close"),
                        html.div(className="minimize"),
                        html.div(className="maximize"),
                        className="mac-traffic-lights"
                    ),
                    html.span("🌐 Safari", className="mac-window-title"),
                    className="mac-window-titlebar"
                ),
                html.iframe(src="https://www.apple.com", style={"height": "100%", "width": "100%", "border": "none"}),
                key="macOS_Safari_Win",
                css=f"transform: translate({safari_state['x']}px, {safari_state['y']}px);",
                style={
                    "position": "absolute",
                    "width": safari_state['width'],
                    "height": safari_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".mac-window-titlebar", "default": {"x": safari_state["x"], "y": safari_state["y"]}, "onStop": sync.set_state("macOS_Safari", "x", "y")},
                resizable={"default": {"width": safari_state["width"], "height": safari_state["height"]}, "onStop": sync.set_state("macOS_Safari", "width", "height")}
            )
        
        # macOS TextEdit Window
        textedit_state = st.session_state["window_states"]["macOS_TextEdit"]
        if textedit_state["open"]:
            html.div(
                html.div(
                    html.div(
                        html.div(onClick=sync(lambda: update_window_state("macOS_TextEdit", open=False)), className="close"),
                        html.div(className="minimize"),
                        html.div(className="maximize"),
                        className="mac-traffic-lights"
                    ),
                    html.span("📝 TextEdit", className="mac-window-title"),
                    className="mac-window-titlebar"
                ),
                html.textarea("Ein einfaches Textdokument für Ihre Notizen auf macOS.",
                              style={"width": "100%", "height": "100%", "border": "none", "padding": "10px", "resize": "none", "font-family": "monospace"}),
                key="macOS_TextEdit_Win",
                css=f"transform: translate({textedit_state['x']}px, {textedit_state['y']}px);",
                style={
                    "position": "absolute",
                    "width": textedit_state['width'],
                    "height": textedit_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".mac-window-titlebar", "default": {"x": textedit_state["x"], "y": textedit_state["y"]}, "onStop": sync.set_state("macOS_TextEdit", "x", "y")},
                resizable={"default": {"width": textedit_state["width"], "height": textedit_state["height"]}, "onStop": sync.set_state("macOS_TextEdit", "width", "height")}
            )


elif selected_os_name == "Linux":
    st.markdown("""
    **Linux** ist bekannt für seine Open-Source-Natur, hohe Anpassbarkeit und eine breite Palette an Distributionen und Desktop-Umgebungen.
    Hier können Sie zwischen verschiedenen 'Desktop-Umgebungen' wählen und einen Terminal-Befehl ausführen, sowie einen simulierten Dateimanager öffnen.
    """)

    desktop_env = st.selectbox(
        "Wählen Sie eine Desktop-Umgebung:",
        ["GNOME (modern)", "KDE Plasma (anpassbar)", "XFCE (leichtgewichtig)"],
        key="linux_desktop_env"
    )

    st.info(f"Sie erleben gerade die {desktop_env}-Umgebung. (Visuell nur durch Hintergrundbild angedeutet)")
    
    linux_bg_image = {
        "GNOME (modern)": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Ubuntu_20.04_LTS_Focal_Fossa_desktop.png/1920px-Ubuntu_20.04_LTS_Focal_Fossa_desktop.png",
        "KDE Plasma (anpassbar)": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Kubuntu_22.04_LTS_desktop.png/1920px-Kubuntu_22.04_LTS_desktop.png",
        "XFCE (leichtgewichtig)": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Xubuntu_22.04_LTS_desktop.png/1920px-Xubuntu_22.04_LTS_desktop.png"
    }.get(desktop_env, "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Ubuntu_20.04_LTS_Focal_Fossa_desktop.png/1920px-Ubuntu_20.04_LTS_Focal_Fossa_desktop.png")


    if st.button("📁 Dateimanager öffnen", key="linux_files_btn"):
        update_window_state("Linux_Files", open=not st.session_state["window_states"]["Linux_Files"]["open"])

    with elements("linux_desktop_elements"):
        html.div(
            # Top Bar (simplified)
            html.div(
                html.div(f"Aktivitäten", style={"font-weight": "bold", "cursor": "pointer"}),
                style={"flex-grow": 1, "text-align": "center"},
                html.div(f"{time.strftime('%a, %d. %B %H:%M')}", style={"cursor": "pointer"}),
                html.div("⚙️", style={"cursor": "pointer"}),
                style={
                    "display": "flex", "justify-content": "space-between", "align-items": "center",
                    "background-color": "rgba(0,0,0,0.3)", "backdrop-filter": "blur(5px)",
                    "height": "30px", "padding": "0 15px", "color": "white", "font-size": "0.9em",
                    "position": "absolute", "top": 0, "left": 0, "right": 0, "z-index": 150
                }
            ),
            # Terminal Simulation
            html.div(
                html.div("`user@linux-pc:~$` Geben Sie einen Befehl ein:", style={"padding": "10px", "color": "#aaffaa"}),
                html.div(
                    id="linux_terminal_output",
                    style={"padding": "10px", "background-color": "#2e3436", "color": "#eeeeec", "border-radius": "5px", "overflow-y": "auto", "height": "calc(100% - 70px)"}
                ),
                key="linux_terminal",
                css=f"""
                    transform: translate(calc(50% - 250px), calc(50% - 150px)); /* Center it */
                    background-color: rgba(46, 52, 54, 0.9);
                    border: 1px solid rgba(0,0,0,0.5);
                    box-shadow: 0 5px 20px rgba(0,0,0,0.5);
                    border-radius: 8px;
                    width: 600px;
                    height: 350px;
                    position: absolute;
                    z-index: 120;
                    display: flex;
                    flex-direction: column;
                    font-family: monospace;
                    font-size: 1.0em;
                """,
                draggable={"handle": ".os-window-titlebar", "default": {"x": 50, "y": 50}}, # Simplified positioning for terminal
            ),
            className="windows-desktop", # Reusing desktop base for background
            style={"background-image": f"url('{linux_bg_image}')"}
        )

        # Linux Files Window
        linux_files_state = st.session_state["window_states"]["Linux_Files"]
        if linux_files_state["open"]:
            html.div(
                html.div(
                    html.div(
                        html.div(onClick=sync(lambda: update_window_state("Linux_Files", open=False)), style={"width": "12px", "height": "12px", "border-radius": "50%", "background-color": "#ff5f56", "border": "0.5px solid rgba(0,0,0,0.2)", "cursor": "pointer"}),
                        style={"display": "flex", "gap": "7px", "margin-right": "10px"}
                    ),
                    html.span("📁 Dateien", style={"flex-grow": 1, "text-align": "center", "font-weight": "bold", "color": "#333"}),
                    style={"display": "flex", "align-items": "center", "padding": "5px 10px", "border-bottom": "1px solid #ddd", "background": "rgba(255,255,255,0.9)", "cursor": "grab"}
                ),
                html.div("""
                    <p>Inhalt von '/home/user':</p>
                    <ul>
                        <li>Dokumente</li>
                        <li>Bilder</li>
                        <li>Musik</li>
                        <li>Videos</li>
                        <li>(Simulierter Linux Dateimanager)</li>
                    </ul>
                """, className="os-window-content", style={"background-color": "white"}),
                key="Linux_Files_Win",
                css=f"transform: translate({linux_files_state['x']}px, {linux_files_state['y']}px);",
                style={
                    "position": "absolute",
                    "width": linux_files_state['width'],
                    "height": linux_files_state['height'],
                    "top": 0, "left": 0,
                },
                className="os-window",
                draggable={"handle": ".os-window-titlebar", "default": {"x": linux_files_state["x"], "y": linux_files_state["y"]}, "onStop": sync.set_state("Linux_Files", "x", "y")},
                resizable={"default": {"width": linux_files_state["width"], "height": linux_files_state["height"]}, "onStop": sync.set_state("Linux_Files", "width", "height")}
            )

    # Streamlit native part for terminal input
    st.markdown("<div style='background-color:#2e3436; color:#eeeeec; padding:10px; border-radius:5px; margin-top:20px;'>", unsafe_allow_html=True)
    st.write("`user@linux-pc:~$` Geben Sie einen Befehl ein (im Terminal oben angezeigt):")
    command = st.text_input("", key="linux_command_input", help="Probieren Sie 'ls', 'pwd', 'sudo apt update', 'uname -a'")
    
    if st.button("Terminal-Befehl ausführen", key="linux_execute_btn"):
        command = command.lower().strip()
        output = ""
        if command == "ls":
            output = "`Documents  Downloads  Music  Pictures  Videos  Public  Templates`"
        elif command == "pwd":
            output = "`/home/user`"
        elif command == "sudo apt update":
            output = """`[sudo] password for user: *******
Hit:1 http://archive.ubuntu.com/ubuntu focal InRelease
...Package lists updated. Done.`"""
        elif command == "uname -a":
            output = "`Linux linux-pc 5.4.0-77-generic #86-Ubuntu SMP Thu Jun 17 00:00:00 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux`"
        else:
            output = f"`bash: {command}: command not found`"
        
        # This will be appended to the output div in the elements context
        with elements("linux_desktop_elements"):
            html.script(f"""
                var outputDiv = document.getElementById('linux_terminal_output');
                outputDiv.innerHTML += '<p><code>user@linux-pc:~$ {command}</code></p><p><code>{output.replace(/`/g, '')}</code></p>';
                outputDiv.scrollTop = outputDiv.scrollHeight; // Scroll to bottom
            """)
        st.rerun() # Rerun to ensure elements updates

    st.markdown("</div>", unsafe_allow_html=True)


elif selected_os_name == "Android":
    st.markdown("""
    **Android** ist das dominierende Betriebssystem für mobile Geräte, bekannt für seine Offenheit und große App-Auswahl.
    Simulieren Sie hier grundlegende Interaktionen eines Android-Smartphones.
    """)
    
    if "android_notification_text" not in st.session_state:
        st.session_state["android_notification_text"] = None
    
    def show_android_notification(text):
        st.session_state["android_notification_text"] = text

    with elements("android_phone_elements"):
        html.div(
            html.div(className="mobile-notch"),
            html.div(
                html.div(
                    html.span("10:30"),
                    html.span("📶 🔋"),
                    className="mobile-status-bar"
                ),
                html.div(
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Google_Phone_icon.svg/48px-Google_Phone_icon.svg.png", alt="Phone",
                                 onClick=sync(lambda: show_android_notification("Anruf-App geöffnet"))),
                        html.div("Telefon"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Google_Messages_icon.svg/48px-Google_Messages_icon.svg.png", alt="Messages",
                                 onClick=sync(lambda: show_android_notification("Nachricht gesendet!"))),
                        html.div("Nachrichten"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Google_Chrome_icon_%282011%29.svg/48px-Google_Chrome_icon_%282011%29.svg.png", alt="Chrome",
                                 onClick=sync(lambda: show_android_notification("Chrome geöffnet"))),
                        html.div("Chrome"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Android_Settings_Icon.png/48px-Android_Settings_Icon.png", alt="Settings",
                                 onClick=sync(lambda: show_android_notification("Einstellungen geöffnet"))),
                        html.div("Einstellungen"),
                        className="mobile-app-icon"
                    ),
                    className="mobile-app-grid"
                ),
                html.div(
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Google_Play_Store_icon.svg/48px-Google_Play_Store_icon.svg.png", alt="Play Store", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Google-Apps-Calendar-icon.png/48px-Google-Apps-Calendar-icon.png", alt="Calendar", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Google_Maps_icon.svg/48px-Google_Maps_icon.svg.png", alt="Maps", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Google_Photos_icon.svg/48px-Google_Photos_icon.svg.png", alt="Photos", className="mobile-app-icon"),
                    className="mobile-dock"
                ),
                className="mobile-screen",
                style={"background-image": "url('https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Android_12_wallpaper.png/1280px-Android_12_wallpaper.png')"} # Android 12 wallpaper
            ),
            html.div(className="mobile-home-button"),
            className="mobile-frame"
        )
        if st.session_state["android_notification_text"]:
            html.div(st.session_state["android_notification_text"], className="mobile-notification")
            # This notification will stay until another action updates it or rerun clears it.
            # For a fade-out, would need more complex JS.

elif selected_os_name == "iOS":
    st.markdown("""
    **iOS** ist Apples Betriebssystem für iPhones und iPads, bekannt für seine Einfachheit, Sicherheit und die tiefe Integration in das Apple-Ökosystem.
    Erleben Sie hier die typische, minimalistische iOS-Benutzeroberfläche.
    """)

    if "ios_notification_text" not in st.session_state:
        st.session_state["ios_notification_text"] = None

    def show_ios_notification(text):
        st.session_state["ios_notification_text"] = text

    with elements("ios_phone_elements"):
        html.div(
            # No notch for simplicity, could add if desired
            html.div(
                html.div(
                    html.span("Provider"), # Carrier name
                    html.span("10:30"),
                    html.span("📶 🔋"),
                    className="mobile-status-bar"
                ),
                html.div(
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Apple_phone_icon.svg/48px-Apple_phone_icon.svg.png", alt="Phone",
                                 onClick=sync(lambda: show_ios_notification("Telefon-App geöffnet"))),
                        html.div("Telefon"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Safari_icon_%28iOS%29.svg/48px-Safari_icon_%28iOS%29.svg.png", alt="Safari",
                                 onClick=sync(lambda: show_ios_notification("Safari geöffnet"))),
                        html.div("Safari"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Apple_Mail_icon.svg/48px-Apple_Mail_icon.svg.png", alt="Mail",
                                 onClick=sync(lambda: show_ios_notification("Mail geöffnet"))),
                        html.div("Mail"),
                        className="mobile-app-icon"
                    ),
                    html.div(
                        html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/IOS_Messages_App_Icon.svg/48px-IOS_Messages_App_Icon.svg.png", alt="Messages",
                                 onClick=sync(lambda: show_ios_notification("Nachricht gesendet!"))),
                        html.div("Nachrichten"),
                        className="mobile-app-icon"
                    ),
                    className="mobile-app-grid"
                ),
                html.div(
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/App_Store_icon.svg/48px-App_Store_icon.svg.png", alt="App Store", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Apple_Music_icon_%282015%29.svg/48px-Apple_Music_icon_%282015%29.svg.png", alt="Music", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Apple_Photos_icon.svg/48px-Apple_Photos_icon.svg.png", alt="Photos", className="mobile-app-icon"),
                    html.img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Apple_Settings_icon.svg/48px-Apple_Settings_icon.svg.png", alt="Settings", className="mobile-app-icon"),
                    className="mobile-dock"
                ),
                className="mobile-screen",
                style={"background-image": "url('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/IOS_17_Wallpaper.png/1280px-IOS_17_Wallpaper.png')"} # iOS 17 wallpaper
            ),
            html.div(className="mobile-home-button"), # No actual button, just visual
            className="mobile-frame"
        )
        if st.session_state["ios_notification_text"]:
            html.div(st.session_state["ios_notification_text"], className="mobile-notification")

elif selected_os_name == "Unix":
    st.markdown("""
    **Unix** ist ein stabiles, multiuser-fähiges System, das die Grundlage für viele moderne Betriebssysteme bildet.
    Fokus liegt auf der Kommandozeile und Systemverwaltung.
    """)
    st.markdown("<div style='background-color:#000; color:#00FF00; padding:20px; border-radius:8px; font-family:\"Courier New\", monospace; font-size:1.1em; line-height:1.4;'>", unsafe_allow_html=True)
    st.write("`Login: root`")
    st.write("`Password:` ************")
    st.write("`Welcome to Unix System V Release 4.0`")
    st.write("")
    
    if "unix_history" not in st.session_state:
        st.session_state["unix_history"] = []
    
    for entry in st.session_state["unix_history"]:
        st.write(entry)
    
    command = st.text_input("`root@server:~#`", key="unix_command_input", help="Probieren Sie 'ls -l', 'ping google.com', 'whoami', 'man ls'")
    
    if st.button("Ausführen", key="unix_execute_btn"):
        st.session_state["unix_history"].append(f"`root@server:~# {command}`")
        command = command.lower().strip()
        
        output = ""
        if command == "ls -l":
            output = """`total 16
drwxr-xr-x 2 user root 4096 Jan  1 00:00 bin
drwxr-xr-x 2 user root 4096 Jan  1 00:00 etc
drwxr-xr-x 2 user root 4096 Jan  1 00:00 home
drwxr-xr-x 2 user root 4096 Jan  1 00:00 var`"""
        elif command == "ping google.com":
            output = """`PING google.com (142.250.186.78): 56 data bytes
64 bytes from 142.250.186.78: icmp_seq=0 ttl=117 time=9.24 ms
64 bytes from 142.250.186.78: icmp_seq=1 ttl=117 time=9.18 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 9.18/9.21/9.24/0.03 ms`"""
        elif command == "whoami":
            output = "`root`"
        elif command == "man ls":
            output = """`LS(1)                                     User Commands                                     LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List  information  about  the FILEs (the current directory by default). Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

       -a, --all
              do not ignore entries starting with .

       -l     use a long listing format`"""
        else:
            output = f"`{command}: command not found`"
        
        st.session_state["unix_history"].append(output)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_os_name == "Chrome OS":
    st.markdown("""
    **Chrome OS** ist ein leichtgewichtiges, Cloud-basiertes Betriebssystem von Google. Es ist stark auf Webanwendungen und schnelle Bootzeiten ausgerichtet.
    Hier erleben Sie eine Oberfläche, die primär auf den Browser setzt.
    """)

    # Default open state for the browser in Chrome OS
    if not st.session_state["window_states"]["ChromeOS_Browser"]["open"]:
        update_window_state("ChromeOS_Browser", open=True)

    with elements("chromeos_desktop_elements"):
        html.div(
            # Browser Window (fixed in place for Chrome OS main experience)
            html.div(
                html.div(
                    html.button("←", className="chromeos-browser-btn"),
                    html.button("→", className="chromeos-browser-btn"),
                    html.span("https://www.google.com", className="chromeos-address-bar"),
                    html.button("⋮", className="chromeos-browser-btn"),
                    className="chromeos-browser-toolbar"
                ),
                html.div("""
                    <h3>Willkommen bei Google Chrome!</h3>
                    <p>Ihr gesamtes digitales Leben in der Cloud.</p>
                    <p>Suchen Sie etwas?</p>
                    <input type='text' placeholder='Google durchsuchen oder Adresse eingeben' style='width:80%; padding:8px; border:1px solid #ccc; border-radius:20px;' disabled>
                    <div style='margin-top:20px;'>
                        <button style='background-color:#4285F4; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer;'>Google Suche</button>
                        <button style='background-color:#f8f9fa; color:#3c4043; border:1px solid #dadce0; padding:10px 15px; border-radius:5px; cursor:pointer;'>Auf gut Glück</button>
                    </div>
                    <p style='margin-top:20px; font-size:0.8em; color:#666;'>_Simuliert einen schnellen Bootvorgang und die Browser-Zentrierung_</p>
                """, className="chromeos-browser-content"),
                key="ChromeOS_Browser_Win",
                css="""
                    background: white;
                    border: 1px solid #aaa;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                    border-radius: 8px;
                    width: calc(100% - 40px);
                    height: calc(100% - 100px); /* Account for shelf and some top margin */
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    z-index: 90;
                """
            ),
            # Shelf
            html.div(
                html.div("🌐", className="chromeos-shelf-icon"),
                html.div("📧", className="chromeos-shelf-icon"),
                html.div("📁", className="chromeos-shelf-icon"),
                className="chromeos-shelf",
            ),
            className="chromeos-desktop",
        )

elif selected_os_name == "FreeBSD":
    st.markdown("""
    **FreeBSD** ist ein leistungsstarkes, stabiles und sicheres Open-Source-Unix-System, oft in Servern und für spezialisierte Anwendungen eingesetzt.
    Fokus liegt auf Systemstabilität, Sicherheit und Netzwerkfähigkeiten.
    """)
    st.markdown("<div style='background-color:#222222; color:#bada55; padding:20px; border-radius:8px; font-family:\"Hack\", \"Source Code Pro\", monospace; font-size:1.1em; line-height:1.4;'>", unsafe_allow_html=True)
    st.write("`FreeBSD/x86-64 (localhost) (ttyv0)`")
    st.write("`login:` `root`")
    st.write("`Password:` ************")
    st.write("`Last login: Mon Jan 1 00:00:00 on ttyv0`")
    st.write("`Welcome to FreeBSD!`")
    st.write("")
    
    if "freebsd_history" not in st.session_state:
        st.session_state["freebsd_history"] = []
    
    for entry in st.session_state["freebsd_history"]:
        st.write(entry)
    
    command = st.text_input("`root@freebsd:~#`", key="freebsd_command_input", help="Probieren Sie 'pkg info', 'ifconfig', 'sysctl kern.ipc.somaxconn', 'top'")
    
    if st.button("Ausführen", key="freebsd_execute_btn"):
        st.session_state["freebsd_history"].append(f"`root@freebsd:~# {command}`")
        command = command.lower().strip()
        
        output = ""
        if command == "pkg info":
            output = """`apache24-2.4.52               Apache HTTP server
nginx-1.20.1_2,2              Robust and small-footprint HTTP(S) server
php80-8.0.15                  PHP Scripting Language`"""
        elif command == "ifconfig":
            output = """`em0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=209b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,WOL_MAGIC>
        inet 192.168.1.10 netmask 0xffffff00 broadcast 192.168.1.255 
        ether 00:0c:29:1c:2c:1a
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=600003<RXCSUM,TXCSUM,RXCSUM_IPV6,TXCSUM_IPV6>
        inet 127.0.0.1 netmask 0xff000000 `"""
        elif command == "sysctl kern.ipc.somaxconn":
            output = "`kern.ipc.somaxconn: 128`"
        elif command == "top":
            output = """`last pid: 12345;  load averages: 0.10, 0.15, 0.20  up 0+01:23:45 00:00:00
11 processes:  1 running, 10 sleeping
CPU:  0.0% user,  0.0% nice,  0.0% system,  0.0% interrupt, 100% idle
Mem: 123M Active, 234M Inact, 56M Wired, 128M Cache, 512M Buf, 2048M Free
Swap: 4096M Total, 0B Used, 4096M Free
 
  PID USERNAME    THR PRI NICE   SIZE    RES STATE    C   TIME    WCPU COMMAND
 101 root          1  20    0    12M    2M idle     0  0:00   0.00% init
 202 www           1  20    0    20M    5M sleep    1  0:00   0.00% httpd
 ...`"""
        else:
            output = f"`{command}: Command not found.`"
        
        st.session_state["freebsd_history"].append(output)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# --- Fußzeile (optional) ---
st.sidebar.markdown("---")
st.sidebar.info("""
Diese App ist ein erweitertes Lernwerkzeug. 
Die Simulationen sind auf der Benutzeroberflächenebene und nutzen `streamlit-elements`
für interaktivere Fenster. Es handelt sich nicht um echte Betriebssystem-Emulationen.
""")
st.markdown("---")
st.markdown("Alle Informationen und simulierten Interaktionen basieren auf der bereitgestellten Übersichtstabelle und allgemeinen Kenntnissen der jeweiligen Betriebssysteme.")
