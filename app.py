import streamlit as st
import pandas as pd
import time

# --- Konfiguration der Seite ---
st.set_page_config(
    page_title="Betriebssystem-Simulator",
    page_icon="💻",
    layout="wide"
)

# --- Daten aus der Tabelle (leicht angepasst für bessere Lesbarkeit/Verarbeitung) ---
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
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "Windows": {
        "Hersteller": "Microsoft",
        "Einsatzbereich": "Desktop, Server",
        "Besonderheiten": "Weit verbreitet, benutzerfreundlich, viele Anwendungen verfügbar",
        "Unterscheidungsmerkmale": "Benutzerfreundliche Oberfläche, breite Hardware-Kompatibilität, hohe Verbreitung",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1985",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "macOS": {
        "Hersteller": "Apple",
        "Einsatzbereich": "Desktop, Laptop",
        "Besonderheiten": "Nahtlose Integration mit anderen Apple-Produkten, exklusiv für Apple-Hardware",
        "Unterscheidungsmerkmale": "Exklusiv für Apple-Hardware, hohe Sicherheit, nahtlose Integration mit Apple-Ökosystem",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2001",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Linux": {
        "Hersteller": "Versch.",
        "Einsatzbereich": "Desktop, Server",
        "Besonderheiten": "Open Source, hohe Anpassbarkeit, viele Distributionen (z.B. Ubuntu, Fedora)",
        "Unterscheidungsmerkmale": "Open Source, hohe Anpassbarkeit, viele Distributionen, starke Community-Unterstützung",
        "Betriebsarten": "Multitasking, Timesharing, Echtzeit",
        "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1991",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Android": {
        "Hersteller": "Google",
        "Einsatzbereich": "Mobile Geräte",
        "Besonderheiten": "Weit verbreitet auf Smartphones und Tablets, basiert auf Linux",
        "Unterscheidungsmerkmale": "Open Source, hohe App-Auswahl, weit verbreitet auf mobilen Geräten",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2008",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "iOS": {
        "Hersteller": "Apple",
        "Einsatzbereich": "Mobile Geräte",
        "Besonderheiten": "Exklusiv für iPhones und iPads, nahtlose Integration mit Apple-Ökosystem",
        "Unterscheidungsmerkmale": "Exklusiv für Apple-Hardware, hohe Sicherheit, nahtlose Integration mit Apple-Ökosystem",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2007",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "Unix": {
        "Hersteller": "Versch.",
        "Einsatzbereich": "Server, Workstations",
        "Besonderheiten": "Stabil, sicher, Grundlage für viele andere Betriebssysteme (z.B. macOS, Linux)",
        "Unterscheidungsmerkmale": "Hohe Stabilität und Sicherheit, Grundlage für viele andere Betriebssysteme, Multiuser-Fähigkeit",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1969",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    },
    "Chrome OS": {
        "Hersteller": "Google",
        "Einsatzbereich": "Laptops (Chromebooks)",
        "Besonderheiten": "Leichtgewichtig, basiert auf Linux, stark auf Cloud-Dienste ausgerichtet",
        "Unterscheidungsmerkmale": "Leichtgewichtig, stark auf Cloud-Dienste ausgerichtet, schnelle Boot-Zeiten",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2011",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor"
    },
    "FreeBSD": {
        "Hersteller": "FreeBSD Project",
        "Einsatzbereich": "Server, Desktop",
        "Besonderheiten": "Open Source, bekannt für Stabilität und Sicherheit",
        "Unterscheidungsmerkmale": "Hohe Stabilität und Sicherheit, Open Source, starke Netzwerkfähigkeiten",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1993",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor"
    }
}

df_os_data = pd.DataFrame.from_dict(os_data, orient='index')

# --- Header ---
st.title("Betriebssysteme - Interaktiver Simulator 💻")
st.markdown("""
Erkunden Sie verschiedene Betriebssysteme und bekommen Sie ein Gefühl für deren Kernfunktionen und Charakteristiken.
Wählen Sie ein Betriebssystem aus der Sidebar, um mehr darüber zu erfahren und eine kleine Simulation zu starten.
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
st.write(f"**Hersteller:** {selected_os_info['Hersteller']}")
st.write(f"**Einsatzbereich:** {selected_os_info['Einsatzbereich']}")
st.write(f"**Besonderheiten:** {selected_os_info['Besonderheiten']}")
st.write(f"**Unterscheidungsmerkmale:** {selected_os_info['Unterscheidungsmerkmale']}")
st.write(f"**Betriebsarten:** {selected_os_info['Betriebsarten']}")
st.write(f"**Single-User/Multi-User:** {selected_os_info['Single-User/Multi-User']}")
st.write(f"**Erst-erscheinung:** {selected_os_info['Erst-erscheinung']}")
st.write(f"**Dialog/Batch:** {selected_os_info['Dialog/Batch']}")
st.write(f"**Einprozessor/Mehrprozessor:** {selected_os_info['Einprozessor/Mehrprozessor']}")

st.markdown("---")

# --- Interaktive Simulation ---
st.header(f"Erleben Sie {selected_os_name}")

if selected_os_name == "DOS":
    st.markdown("""
    **DOS (Disk Operating System)** war ein kommandozeilenbasiertes System. 
    Hier interagieren Sie direkt durch Eingabe von Befehlen.
    """)
    st.markdown("<div style='background-color:#0000AA; color:white; padding:10px; border-radius:5px;'>", unsafe_allow_html=True)
    st.write("`C:\\>` Bitte geben Sie einen Befehl ein:")
    command = st.text_input("", key="dos_command_input", help="Probieren Sie 'dir', 'echo Hello World', 'cd ..', 'exit'")
    
    if command:
        command = command.lower().strip()
        if command == "dir":
            st.write("`Volume in drive C has no label.`")
            st.write("`Volume Serial Number is 1234-5678`")
            st.write("`Directory of C:\\`")
            st.write("`01/01/1981  12:00 PM        0 COMMAND.COM`")
            st.write("`01/01/1981  12:00 PM        0 AUTOEXEC.BAT`")
            st.write("`01/01/1981  12:00 PM        0 CONFIG.SYS`")
            st.write("`        3 File(s)              0 bytes`")
            st.write("`        0 Dir(s)         1457664 bytes free`")
        elif command.startswith("echo "):
            st.write(command[5:])
        elif command == "cd ..":
            st.write("`C:\\>`")
        elif command == "exit":
            st.error("`DOS-Sitzung beendet. Bitte starten Sie neu.`")
        else:
            st.warning(f"`Bad command or file name: {command}`")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_os_name == "Windows":
    st.markdown("""
    **Windows** zeichnet sich durch seine grafische Benutzeroberfläche und Multitasking-Fähigkeit aus.
    Hier können Sie versuchen, mehrere "Anwendungen" gleichzeitig zu öffnen.
    """)

    st.markdown(
        """
        <style>
        .windows-desktop {
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Windows_XP_Desktop.png/1280px-Windows_XP_Desktop.png');
            background-size: cover;
            background-position: center;
            height: 400px; /* Adjust height as needed */
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            position: relative;
        }
        .windows-icon {
            text-align: center;
            margin: 10px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
        .windows-icon img {
            width: 48px;
            height: 48px;
            display: block;
            margin: auto;
            border: 1px solid transparent;
            border-radius: 5px;
            transition: all 0.2s ease-in-out;
        }
        .windows-icon img:hover {
            border: 1px solid lightblue;
            background-color: rgba(173, 216, 230, 0.3);
        }
        .windows-window {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid #777;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            position: absolute; /* Allows overlaying */
            min-width: 200px;
            z-index: 100;
        }
        .windows-window-titlebar {
            background-color: #337ab7;
            color: white;
            padding: 5px;
            border-radius: 3px 3px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -10px -10px 10px -10px; /* Adjust for padding */
        }
        .windows-window-close {
            background-color: #f00;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            padding: 0 5px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='windows-desktop'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📁 Eigene Dateien", key="win_files", help="Öffnet ein Dateifenster"):
            st.session_state["win_files_open"] = not st.session_state.get("win_files_open", False)
        
    with col2:
        if st.button("🌐 Browser", key="win_browser", help="Öffnet einen Webbrowser"):
            st.session_state["win_browser_open"] = not st.session_state.get("win_browser_open", False)
            
    with col3:
        if st.button("📝 Editor", key="win_editor", help="Öffnet einen einfachen Texteditor"):
            st.session_state["win_editor_open"] = not st.session_state.get("win_editor_open", False)
            
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("win_files_open"):
        st.markdown(f"""
            <div class='windows-window' style='top:100px; left:50px;'>
                <div class='windows-window-titlebar'>
                    <span>📁 Eigene Dateien</span>
                    <button class='windows-window-close' onclick="parent.window.location.href = '/?{time.time()}#win_files_close'">X</button>
                </div>
                <p>Inhalt von 'Eigene Dateien':</p>
                <ul>
                    <li>Dokument.docx</li>
                    <li>Bild.jpg</li>
                    <li>Präsentation.pptx</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        if "#win_files_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["win_files_open"] = False
            st.experimental_set_query_params() # Clear query param

    if st.session_state.get("win_browser_open"):
        st.markdown(f"""
            <div class='windows-window' style='top:150px; left:250px;'>
                <div class='windows-window-titlebar'>
                    <span>🌐 Internet Browser</span>
                     <button class='windows-window-close' onclick="parent.window.location.href = '/?{time.time()}#win_browser_close'">X</button>
                </div>
                <p>Willkommen im Streamlit-Browser!</p>
                <a href='https://streamlit.io' target='_blank'>Besuchen Sie Streamlit.io</a>
            </div>
            """, unsafe_allow_html=True)
        if "#win_browser_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["win_browser_open"] = False
            st.experimental_set_query_params() # Clear query param

    if st.session_state.get("win_editor_open"):
        st.markdown(f"""
            <div class='windows-window' style='top:200px; left:450px;'>
                <div class='windows-window-titlebar'>
                    <span>📝 Editor</span>
                     <button class='windows-window-close' onclick="parent.window.location.href = '/?{time.time()}#win_editor_close'">X</button>
                </div>
                <textarea style='width:100%; height:100px; border:1px solid #ccc; padding:5px;'>Dies ist ein einfacher Texteditor. Hier können Sie etwas tippen.</textarea>
            </div>
            """, unsafe_allow_html=True)
        if "#win_editor_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["win_editor_open"] = False
            st.experimental_set_query_params() # Clear query param


elif selected_os_name == "macOS":
    st.markdown("""
    **macOS** (früher OS X) bietet eine elegante, intuitive grafische Oberfläche und ist bekannt für seine nahtlose Integration im Apple-Ökosystem.
    Hier sehen Sie eine stilisierte Oberfläche mit einem "Dock".
    """)

    st.markdown(
        """
        <style>
        .mac-desktop {
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Mojave_Desktop.jpg/1280px-Mojave_Desktop.jpg');
            background-size: cover;
            background-position: center;
            height: 400px; /* Adjust height as needed */
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end; /* Dock at bottom */
            position: relative;
        }
        .mac-dock {
            background-color: rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 10px 20px;
            margin: 10px auto;
            display: flex;
            gap: 15px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .mac-dock-icon button {
            background: none;
            border: none;
            padding: 0;
            cursor: pointer;
            transition: transform 0.2s ease-in-out;
        }
        .mac-dock-icon button:hover {
            transform: scale(1.1);
        }
        .mac-dock-icon img {
            width: 48px;
            height: 48px;
            display: block;
        }
        .mac-window {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid #bbb;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border-radius: 8px;
            padding: 15px;
            position: absolute;
            min-width: 250px;
            z-index: 100;
        }
        .mac-window-titlebar {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .mac-window-traffic-lights {
            display: flex;
            gap: 6px;
        }
        .mac-window-traffic-lights div {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 1px solid rgba(0,0,0,0.1);
        }
        .mac-window-traffic-lights .close { background-color: #ff5f56; }
        .mac-window-traffic-lights .minimize { background-color: #ffbd2e; }
        .mac-window-traffic-lights .maximize { background-color: #27c93f; }
        .mac-window-title {
            flex-grow: 1;
            text-align: center;
            font-weight: bold;
            color: #444;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='mac-desktop'>", unsafe_allow_html=True)
    st.markdown("<div class='mac-dock'>", unsafe_allow_html=True)
    
    col_icons = st.columns(3)
    
    with col_icons[0]:
        if st.button("✉️ Mail", key="mac_mail", help="Öffnet die Mail App"):
            st.session_state["mac_mail_open"] = not st.session_state.get("mac_mail_open", False)
    with col_icons[1]:
        if st.button("🌐 Safari", key="mac_safari", help="Öffnet den Safari Browser"):
            st.session_state["mac_safari_open"] = not st.session_state.get("mac_safari_open", False)
    with col_icons[2]:
        if st.button("🎵 Music", key="mac_music", help="Öffnet die Musik App"):
            st.session_state["mac_music_open"] = not st.session_state.get("mac_music_open", False)
            
    st.markdown("</div>", unsafe_allow_html=True) # End mac-dock
    st.markdown("</div>", unsafe_allow_html=True) # End mac-desktop

    # Simplified window closing with query params
    if st.session_state.get("mac_mail_open"):
        st.markdown(f"""
            <div class='mac-window' style='top:80px; left:100px;'>
                <div class='mac-window-titlebar'>
                    <div class='mac-window-traffic-lights'>
                        <div class='close' onclick="parent.window.location.href = '/?{time.time()}#mac_mail_close'"></div>
                        <div class='minimize'></div>
                        <div class='maximize'></div>
                    </div>
                    <span class='mac-window-title'>✉️ Mail</span>
                </div>
                <p>Willkommen in Ihrer Mail App!</p>
                <p>_Neue E-Mail von Apple Support_</p>
            </div>
            """, unsafe_allow_html=True)
        if "#mac_mail_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["mac_mail_open"] = False
            st.experimental_set_query_params()

    if st.session_state.get("mac_safari_open"):
        st.markdown(f"""
            <div class='mac-window' style='top:150px; left:300px;'>
                <div class='mac-window-titlebar'>
                    <div class='mac-window-traffic-lights'>
                        <div class='close' onclick="parent.window.location.href = '/?{time.time()}#mac_safari_close'"></div>
                        <div class='minimize'></div>
                        <div class='maximize'></div>
                    </div>
                    <span class='mac-window-title'>🌐 Safari</span>
                </div>
                <p>Surfen Sie mit Safari!</p>
                <a href='https://www.apple.com' target='_blank'>Besuchen Sie Apple.com</a>
            </div>
            """, unsafe_allow_html=True)
        if "#mac_safari_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["mac_safari_open"] = False
            st.experimental_set_query_params()

    if st.session_state.get("mac_music_open"):
        st.markdown(f"""
            <div class='mac-window' style='top:220px; left:50px;'>
                <div class='mac-window-titlebar'>
                    <div class='mac-window-traffic-lights'>
                        <div class='close' onclick="parent.window.location.href = '/?{time.time()}#mac_music_close'"></div>
                        <div class='minimize'></div>
                        <div class='maximize'></div>
                    </div>
                    <span class='mac-window-title'>🎵 Musik</span>
                </div>
                <p>Ihre Lieblingssongs hier!</p>
                <p>_Aktueller Titel: "Feeling Good" (N. Simone)_</p>
            </div>
            """, unsafe_allow_html=True)
        if "#mac_music_close" in st.experimental_get_query_params().get("",[]):
            st.session_state["mac_music_open"] = False
            st.experimental_set_query_params()


elif selected_os_name == "Linux":
    st.markdown("""
    **Linux** ist bekannt für seine Open-Source-Natur, hohe Anpassbarkeit und eine breite Palette an Distributionen und Desktop-Umgebungen.
    Hier können Sie zwischen verschiedenen 'Desktop-Umgebungen' wählen und einen Terminal-Befehl ausführen.
    """)

    desktop_env = st.selectbox(
        "Wählen Sie eine Desktop-Umgebung:",
        ["GNOME (modern)", "KDE Plasma (anpassbar)", "XFCE (leichtgewichtig)"],
        key="linux_desktop_env"
    )

    st.info(f"Sie erleben gerade die {desktop_env}-Umgebung.")

    st.markdown("<div style='background-color:#2e3436; color:#eeeeec; padding:10px; border-radius:5px;'>", unsafe_allow_html=True)
    st.write("`user@linux-pc:~$` Geben Sie einen Befehl ein:")
    command = st.text_input("", key="linux_command_input", help="Probieren Sie 'ls', 'pwd', 'sudo apt update', 'uname -a'")
    
    if command:
        command = command.lower().strip()
        if command == "ls":
            st.write("`Documents  Downloads  Music  Pictures  Videos  Public  Templates`")
        elif command == "pwd":
            st.write("`/home/user`")
        elif command == "sudo apt update":
            st.write("`[sudo] password for user: *******`")
            st.write("`Hit:1 http://archive.ubuntu.com/ubuntu focal InRelease`")
            st.write("`...Package lists updated. Done.`")
        elif command == "uname -a":
            st.write("`Linux linux-pc 5.4.0-77-generic #86-Ubuntu SMP Thu Jun 17 00:00:00 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux`")
        else:
            st.warning(f"`bash: {command}: command not found`")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_os_name == "Android":
    st.markdown("""
    **Android** ist das dominierende Betriebssystem für mobile Geräte, bekannt für seine Offenheit und große App-Auswahl.
    Simulieren Sie hier grundlegende Interaktionen eines Android-Smartphones.
    """)
    
    st.markdown(
        """
        <style>
        .android-phone {
            width: 300px;
            height: 550px;
            border: 12px solid #333;
            border-radius: 30px;
            background-color: #f0f0f0;
            margin: 20px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            position: relative;
        }
        .android-screen {
            width: 100%;
            height: 100%;
            background-image: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf_b_K1K8w2s-9K8x9F0v5hK3W3f6J6k_2w&s'); /* Placeholder background */
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 15px 5px;
        }
        .android-app-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 50px; /* Push apps down */
        }
        .android-app-icon {
            text-align: center;
            font-size: 12px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
        .android-app-icon button {
            background-color: rgba(255,255,255,0.2);
            border: none;
            border-radius: 10px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .android-app-icon button:hover {
            background-color: rgba(255,255,255,0.4);
        }
        .android-notification {
            background-color: #2196F3;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 14px;
            margin-top: 10px;
            width: 80%;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='android-phone'>", unsafe_allow_html=True)
    st.markdown("<div class='android-screen'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞", key="android_phone"):
            st.session_state["android_notification"] = "Anruf getätigt!"
        st.markdown("<div class='android-app-icon'>Anruf</div>", unsafe_allow_html=True)
    with col2:
        if st.button("📸", key="android_camera"):
            st.session_state["android_notification"] = "Foto aufgenommen!"
        st.markdown("<div class='android-app-icon'>Kamera</div>", unsafe_allow_html=True)
    with col3:
        if st.button("✉️", key="android_message"):
            st.session_state["android_notification"] = "Nachricht gesendet!"
        st.markdown("<div class='android-app-icon'>Nachrichten</div>", unsafe_allow_html=True)

    if st.session_state.get("android_notification"):
        st.markdown(f"<div class='android-notification'>{st.session_state['android_notification']}</div>", unsafe_allow_html=True)
        # Clear notification after a short delay (Streamlit makes this a bit tricky without a callback)
        # For simplicity, it stays until another action or refresh.

    st.markdown("</div>", unsafe_allow_html=True) # End android-screen
    st.markdown("</div>", unsafe_allow_html=True) # End android-phone

elif selected_os_name == "iOS":
    st.markdown("""
    **iOS** ist Apples Betriebssystem für iPhones und iPads, bekannt für seine Einfachheit, Sicherheit und die tiefe Integration in das Apple-Ökosystem.
    Erleben Sie hier die typische, minimalistische iOS-Benutzeroberfläche.
    """)

    st.markdown(
        """
        <style>
        .ios-phone {
            width: 300px;
            height: 550px;
            border: 12px solid #555;
            border-radius: 30px;
            background-color: #eee;
            margin: 20px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            position: relative;
        }
        .ios-screen {
            width: 100%;
            height: 100%;
            background-image: url('https://i.stack.imgur.com/b3T6W.png'); /* iOS 14 default background */
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 15px 5px;
        }
        .ios-app-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        .ios-app-icon {
            text-align: center;
            font-size: 10px;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
        .ios-app-icon button {
            background-color: rgba(255,255,255,0.2); /* Transparent white */
            border: none;
            border-radius: 15px; /* Rounded square */
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            cursor: pointer;
            transition: transform 0.1s;
        }
        .ios-app-icon button:active {
            transform: scale(0.95);
        }
        .ios-dock {
            background-color: rgba(255,255,255,0.3);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 8px;
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='ios-phone'>", unsafe_allow_html=True)
    st.markdown("<div class='ios-screen'>", unsafe_allow_html=True)

    # App grid
    app_col1, app_col2, app_col3, app_col4 = st.columns(4)
    with app_col1:
        if st.button("📱", key="ios_phone"): st.info("Anruf-App geöffnet.")
        st.markdown("<div class='ios-app-icon'>Telefon</div>", unsafe_allow_html=True)
    with app_col2:
        if st.button("🌐", key="ios_safari"): st.info("Safari geöffnet.")
        st.markdown("<div class='ios-app-icon'>Safari</div>", unsafe_allow_html=True)
    with app_col3:
        if st.button("✉️", key="ios_mail"): st.info("Mail geöffnet.")
        st.markdown("<div class='ios-app-icon'>Mail</div>", unsafe_allow_html=True)
    with app_col4:
        if st.button("📸", key="ios_camera"): st.info("Kamera geöffnet. Lächeln!")
        st.markdown("<div class='ios-app-icon'>Kamera</div>", unsafe_allow_html=True)
        
    # Spacer to push dock to bottom
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)

    # iOS Dock
    st.markdown("<div class='ios-dock'>", unsafe_allow_html=True)
    dock_col1, dock_col2, dock_col3, dock_col4 = st.columns(4)
    with dock_col1:
        if st.button("💬", key="ios_messages_dock"): st.info("Nachrichten-App geöffnet.")
    with dock_col2:
        if st.button("🎵", key="ios_music_dock"): st.info("Musik-App geöffnet.")
    with dock_col3:
        if st.button("🗓️", key="ios_calendar_dock"): st.info("Kalender geöffnet.")
    with dock_col4:
        if st.button("⚙️", key="ios_settings_dock"): st.info("Einstellungen geöffnet.")
    st.markdown("</div>", unsafe_allow_html=True) # End ios-dock

    st.markdown("</div>", unsafe_allow_html=True) # End ios-screen
    st.markdown("</div>", unsafe_allow_html=True) # End ios-phone

elif selected_os_name == "Unix":
    st.markdown("""
    **Unix** ist ein stabiles, multiuser-fähiges System, das die Grundlage für viele moderne Betriebssysteme bildet.
    Fokus liegt auf der Kommandozeile und Systemverwaltung.
    """)
    st.markdown("<div style='background-color:#000; color:#00FF00; padding:15px; border-radius:5px;'>", unsafe_allow_html=True)
    st.write("```bash")
    st.write("# Willkommen im Unix-System. Typische Server-Interaktionen.")
    st.write("# Hier sind einige simulierte Befehle:")
    st.write("# user@server:~# ls -l")
    st.write("# user@server:~# ping google.com")
    st.write("```")
    
    command = st.text_input("`user@server:~#`", key="unix_command_input", help="Probieren Sie 'ls -l', 'ping google.com', 'whoami'")
    
    if command:
        command = command.lower().strip()
        if command == "ls -l":
            st.write("```")
            st.write("total 16")
            st.write("drwxr-xr-x 2 user user 4096 Jan  1 00:00 bin")
            st.write("drwxr-xr-x 2 user user 4096 Jan  1 00:00 etc")
            st.write("drwxr-xr-x 2 user user 4096 Jan  1 00:00 home")
            st.write("drwxr-xr-x 2 user user 4096 Jan  1 00:00 var")
            st.write("```")
        elif command == "ping google.com":
            st.write("```")
            st.write("PING google.com (142.250.186.78) 56(84) bytes of data.")
            st.write("64 bytes from fra16s31-in-f14.1e100.net (142.250.186.78): icmp_seq=1 ttl=117 time=9.24 ms")
            st.write("64 bytes from fra16s31-in-f14.1e100.net (142.250.186.78): icmp_seq=2 ttl=117 time=9.18 ms")
            st.write("--- google.com ping statistics ---")
            st.write("2 packets transmitted, 2 received, 0% packet loss, time 1001ms")
            st.write("```")
        elif command == "whoami":
            st.write("`user`")
        else:
            st.warning(f"`bash: {command}: command not found`")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_os_name == "Chrome OS":
    st.markdown("""
    **Chrome OS** ist ein leichtgewichtiges, Cloud-basiertes Betriebssystem von Google. Es ist stark auf Webanwendungen und schnelle Bootzeiten ausgerichtet.
    Hier erleben Sie eine Oberfläche, die primär auf den Browser setzt.
    """)
    
    st.markdown(
        """
        <style>
        .chromeos-desktop {
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e0/Chrome_OS_desktop_after_OOBE.png'); /* Placeholder Chrome OS background */
            background-size: cover;
            background-position: center;
            height: 400px;
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }
        .chromeos-browser-window {
            background-color: white;
            border: 1px solid #aaa;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            border-radius: 8px;
            width: 90%;
            height: 80%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
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
        .chromeos-content {
            flex-grow: 1;
            padding: 15px;
            text-align: center;
            color: #3c4043;
            overflow-y: auto;
        }
        .chromeos-shelf {
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
            padding: 5px 10px;
            border-radius: 10px;
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        .chromeos-shelf button {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div class='chromeos-desktop'>", unsafe_allow_html=True)
    st.markdown("<div class='chromeos-browser-window'>", unsafe_allow_html=True)
    st.markdown("""
        <div class='chromeos-browser-toolbar'>
            <button>←</button>
            <button>→</button>
            <span class='chromeos-address-bar'>https://www.google.com</span>
            <button>⋮</button>
        </div>
        <div class='chromeos-content'>
            <h3>Willkommen bei Google Chrome!</h3>
            <p>Ihr gesamtes digitales Leben in der Cloud.</p>
            <p>Suchen Sie etwas?</p>
            <input type='text' placeholder='Google durchsuchen oder Adresse eingeben' style='width:80%; padding:8px; border:1px solid #ccc; border-radius:20px;' disabled>
            <div style='margin-top:20px;'>
                <button style='background-color:#4285F4; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer;'>Google Suche</button>
                <button style='background-color:#f8f9fa; color:#3c4043; border:1px solid #dadce0; padding:10px 15px; border-radius:5px; cursor:pointer;'>Auf gut Glück</button>
            </div>
            <p style='margin-top:20px;'>_Simuliert einen schnellen Bootvorgang_</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # End chromeos-browser-window

    st.markdown("<div class='chromeos-shelf'>", unsafe_allow_html=True)
    shelf_col1, shelf_col2, shelf_col3 = st.columns(3)
    with shelf_col1: st.button("🌐", key="chromeos_browser_shelf")
    with shelf_col2: st.button("📧", key="chromeos_gmail_shelf")
    with shelf_col3: st.button("📁", key="chromeos_files_shelf")
    st.markdown("</div>", unsafe_allow_html=True) # End chromeos-shelf
    st.markdown("</div>", unsafe_allow_html=True) # End chromeos-desktop

    st.warning("Hinweis: Da Cloud-Dienste nicht direkt simuliert werden können, zeigt dies eine browserzentrierte Oberfläche.")


elif selected_os_name == "FreeBSD":
    st.markdown("""
    **FreeBSD** ist ein leistungsstarkes, stabiles und sicheres Open-Source-Unix-System, oft in Servern und für spezialisierte Anwendungen eingesetzt.
    Fokus liegt auf Systemstabilität, Sicherheit und Netzwerkfähigkeiten.
    """)
    st.markdown("<div style='background-color:#222222; color:#bada55; padding:15px; border-radius:5px;'>", unsafe_allow_html=True)
    st.write("```bash")
    st.write("# Willkommen bei FreeBSD. Ein System für Stabilität und Sicherheit.")
    st.write("# Hier sind einige simulierte Befehle:")
    st.write("# root@freebsd:~# dmesg | grep -i cpu")
    st.write("# root@freebsd:~# top -o cpu")
    st.write("```")
    
    command = st.text_input("`root@freebsd:~#`", key="freebsd_command_input", help="Probieren Sie 'pkg info', 'ifconfig', 'sysctl kern.ipc.somaxconn'")
    
    if command:
        command = command.lower().strip()
        if command == "pkg info":
            st.write("```")
            st.write("apache24-2.4.52               Apache HTTP server")
            st.write("nginx-1.20.1_2,2              Robust and small-footprint HTTP(S) server")
            st.write("php80-8.0.15                  PHP Scripting Language")
            st.write("```")
        elif command == "ifconfig":
            st.write("```")
            st.write("em0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500")
            st.write("        options=209b<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,VLAN_HWCSUM,WOL_MAGIC>")
            st.write("        inet 192.168.1.10 netmask 0xffffff00 broadcast 192.168.1.255 ")
            st.write("        ether 00:0c:29:1c:2c:1a")
            st.write("lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384")
            st.write("        options=600003<RXCSUM,TXCSUM,RXCSUM_IPV6,TXCSUM_IPV6>")
            st.write("        inet 127.0.0.1 netmask 0xff000000 ")
            st.write("```")
        elif command == "sysctl kern.ipc.somaxconn":
            st.write("`kern.ipc.somaxconn: 128`")
        else:
            st.warning(f"`{command}: Command not found.`")
    st.markdown("</div>", unsafe_allow_html=True)


# --- Fußzeile (optional) ---
st.sidebar.markdown("---")
st.sidebar.info("Diese App ist ein Lernwerkzeug und simuliert die Betriebssysteme auf einer grundlegenden Ebene.")

st.markdown("---")
st.markdown("Alle Informationen basieren auf der bereitgestellten Übersichtstabelle.")
