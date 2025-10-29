import streamlit as st
from datetime import datetime
import random
from textwrap import dedent # <-- WICHTIGER IMPORT

# --- Konfiguration ---
st.set_page_config(
    page_title="Betriebssystem-Simulator Pro",
    page_icon="💻",
    layout="wide"
)
# --- Einfaches CSS ---
st.markdown("""
<style>
    .dos-box {
        background-color: #0000AA;
        color: white;
        font-family: 'Courier New', monospace;
        padding: 30px;
        border-radius: 10px;
        font-size: 16px;
        line-height: 1.6;
        min-height: 400px;
    }
    .linux-box {
        background-color: #300A24;
        color: white;
        font-family: 'Ubuntu Mono', 'Courier New', monospace;
        padding: 30px;
        border-radius: 10px;
        font-size: 14px;
        line-height: 1.8;
        min-height: 400px;
    }
    .os-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        min-height: 500px;
        color: white;
    }
    .phone-box {
        background: linear-gradient(180deg, #1a73e8 0%, #4285f4 100%);
        padding: 30px;
        border-radius: 40px;
        min-height: 600px;
        max-width: 400px;
        margin: 0 auto;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
# --- Header ---
st.title("💻 Betriebssystem-Simulator Pro")
st.markdown("---")
# --- Sidebar ---
with st.sidebar:
    st.header("🎮 Betriebssystem wählen")
    os_choice = st.selectbox(
        "Wähle ein OS:",
        ["DOS", "Windows", "macOS", "Linux", "Android", "iOS"]
    )
    st.markdown("---")
    st.info("Wähle ein Betriebssystem aus, um eine visuelle Darstellung zu sehen.")
# --- Hauptbereich ---
if os_choice == "DOS":
    st.header("💾 MS-DOS")
    st.info("**MS-DOS** - Das Kommandozeilen-Betriebssystem der 1980er Jahre")
    st.markdown("""
    <div class="dos-box">
    Microsoft(R) MS-DOS(R) Version 6.22<br>
    (C)Copyright Microsoft Corp 1981-1994.<br>
    <br>
    C:\\>dir<br>
    <br>
    Volume in Laufwerk C: hat keine Bezeichnung.<br>
    Volumeseriennummer: 1A2B-3C4D<br>
    <br>
    Verzeichnis von C:\\<br>
    <br>
    DOS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DIR]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01.01.1994&nbsp;&nbsp;&nbsp;9:00<br>
    WINDOWS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DIR]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;01.01.1994&nbsp;&nbsp;&nbsp;9:30<br>
    COMMAND&nbsp;&nbsp;COM&nbsp;&nbsp;&nbsp;&nbsp;54,645 01.01.1994&nbsp;&nbsp;10:00<br>
    AUTOEXEC&nbsp;BAT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;128 01.01.1994&nbsp;&nbsp;10:00<br>
    CONFIG&nbsp;&nbsp;&nbsp;SYS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;256 01.01.1994&nbsp;&nbsp;10:00<br>
    <br>
    3 Datei(en)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;55,029 Bytes<br>
    2 Verzeichnis(se) 10,240,000 Bytes frei<br>
    <br>
    C:\\>_
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 📝 Typische DOS-Befehle")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("DIR")
        st.caption("Verzeichnis anzeigen")
    with col2:
        st.code("CD")
        st.caption("Verzeichnis wechseln")
    with col3:
        st.code("COPY")
        st.caption("Dateien kopieren")

elif os_choice == "Windows":
    st.header("🪟 Windows 11")
    st.info("**Windows** - Das meistgenutzte Desktop-Betriebssystem weltweit")
    # KORREKTUR: Verwende dedent, um die Einrückung aus dem HTML-String zu entfernen
    windows_html = dedent("""
        <div class="os-box">
            <h2 style='text-align: center; margin-bottom: 30px;'>🖥️ Windows Desktop</h2>
            <div style='display: flex; gap: 30px; justify-content: center; margin-bottom: 40px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 64px;'>📁</div>
                    <div>Dieser PC</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 64px;'>🗑️</div>
                    <div>Papierkorb</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 64px;'>📄</div>
                    <div>Dokumente</div>
                </div>
            </div>
            <div style='background: white; color: black; padding: 30px; border-radius: 10px; margin-top: 50px;'>
                <div style='border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 20px;'>
                    <strong>📁 Datei-Explorer</strong>
                </div>
                <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center;'>
                    <div>
                        <div style='font-size: 48px;'>📄</div>
                        <div>Dokumente</div>
                        <small>15 Dateien</small>
                    </div>
                    <div>
                        <div style='font-size: 48px;'>🖼️</div>
                        <div>Bilder</div>
                        <small>127 Dateien</small>
                    </div>
                    <div>
                        <div style='font-size: 48px;'>🎵</div>
                        <div>Musik</div>
                        <small>42 Dateien</small>
                    </div>
                    <div>
                        <div style='font-size: 48px;'>🎬</div>
                        <div>Videos</div>
                        <small>8 Dateien</small>
                    </div>
                </div>
            </div>
        </div>
    """)
    st.markdown(windows_html, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Marktanteil", "75%")
    with col2:
        st.metric("Erscheinungsjahr", "1985")
    with col3:
        st.metric("Hersteller", "Microsoft")

elif os_choice == "macOS":
    st.header(" macOS")
    st.info("**macOS** - Apples elegantes Desktop-Betriebssystem")
    # KORREKTUR: Verwende dedent für den f-String
    mac_html = dedent(f"""
        <div style='background: linear-gradient(180deg, #4A90E2 0%, #7B68EE 100%); padding: 40px; border-radius: 15px; min-height: 500px; color: white; position: relative;'>
            <div style='background: rgba(0,0,0,0.3); padding: 10px 20px; border-radius: 8px; margin-bottom: 30px; display: flex; justify-content: space-between;'>
                <div><strong> Finder</strong></div>
                <div>Ablage · Bearbeiten · Darstellung</div>
                <div>🔋 📶 {datetime.now().strftime('%H:%M')}</div>
            </div>
            <div style='background: white; color: black; padding: 30px; border-radius: 10px; margin-top: 50px;'>
                <div style='border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;'>
                    <div style='display: flex; gap: 8px;'>
                        <div style='width: 12px; height: 12px; border-radius: 50%; background: #ff605c;'></div>
                        <div style='width: 12px; height: 12px; border-radius: 50%; background: #ffbd44;'></div>
                        <div style='width: 12px; height: 12px; border-radius: 50%; background: #00ca4e;'></div>
                    </div>
                    <strong>Finder</strong>
                </div>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; text-align: center;'>
                    <div>
                        <div style='font-size: 64px;'>📁</div>
                        <div>Projekte</div>
                    </div>
                    <div>
                        <div style='font-size: 64px;'>📄</div>
                        <div>Präsentation.key</div>
                    </div>
                    <div>
                        <div style='font-size: 64px;'>🖼️</div>
                        <div>Urlaub2024.jpg</div>
                    </div>
                </div>
            </div>
            <div style='position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(255,255,255,0.2); backdrop-filter: blur(20px); padding: 15px; border-radius: 20px; display: flex; gap: 15px;'>
                <div style='font-size: 36px;'>📁</div>
                <div style='font-size: 36px;'>🌐</div>
                <div style='font-size: 36px;'>✉️</div>
                <div style='font-size: 36px;'>🎵</div>
                <div style='font-size: 36px;'>⚙️</div>
            </div>
        </div>
    """)
    st.markdown(mac_html, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Erscheinungsjahr", "2001")
    with col2:
        st.metric("Basis", "Unix")
    with col3:
        st.metric("Hersteller", "Apple")

elif os_choice == "Linux":
    st.header("🐧 Linux (Ubuntu)")
    st.info("**Linux** - Open-Source-Betriebssystem mit maximaler Freiheit")
    st.markdown("""
    <div class="linux-box">
    Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)<br>
    <br>
    * Documentation:&nbsp;&nbsp;https://help.ubuntu.com<br>
    * Management:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://landscape.canonical.com<br>
    * Support:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://ubuntu.com/advantage<br>
    <br>
    <span style='color: #8AE234; font-weight: bold;'>user@ubuntu</span>:<span style='color: #729FCF;'>~</span>$ ls -la<br>
    total 48<br>
    drwxr-xr-x&nbsp;&nbsp;8 user user 4096 Jan 15 10:30 .<br>
    drwxr-xr-x&nbsp;&nbsp;3 root root 4096 Dec&nbsp;&nbsp;1 09:15 ..<br>
    drwxr-xr-x&nbsp;&nbsp;2 user user 4096 Jan 10 14:22 Desktop<br>
    drwxr-xr-x&nbsp;&nbsp;3 user user 4096 Jan 12 16:45 Documents<br>
    drwxr-xr-x&nbsp;&nbsp;2 user user 4096 Jan 14 11:30 Downloads<br>
    drwxr-xr-x&nbsp;&nbsp;2 user user 4096 Dec 28 08:15 Music<br>
    <br>
    <span style='color: #8AE234; font-weight: bold;'>user@ubuntu</span>:<span style='color: #729FCF;'>~</span>$ uname -a<br>
    Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP x86_64 x86_64 x86_64 GNU/Linux<br>
    <br>
    <span style='color: #8AE234; font-weight: bold;'>user@ubuntu</span>:<span style='color: #729FCF;'>~</span>$ _
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🐧 Beliebte Distributionen")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Ubuntu**\n\nBenutzerfreundlich")
    with col2:
        st.info("**Fedora**\n\nModern & aktuell")
    with col3:
        st.warning("**Arch**\n\nFür Experten")

elif os_choice == "Android":
    st.header("🤖 Android")
    st.info("**Android** - Das meistgenutzte mobile Betriebssystem weltweit")
    # KORREKTUR: Verwende dedent für den f-String
    android_html = dedent(f"""
        <div class="phone-box">
            <div style='display: flex; justify-content: space-between; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px; margin-bottom: 40px;'>
                <div style='font-weight: bold;'>{datetime.now().strftime('%H:%M')}</div>
                <div>📶 🔋 87%</div>
            </div>
            <div style='text-align: center; margin-bottom: 50px;'>
                <div style='font-size: 72px; font-weight: 300;'>{datetime.now().strftime('%H:%M')}</div>
                <div style='font-size: 20px; opacity: 0.9;'>{datetime.now().strftime('%A, %d. %B')}</div>
            </div>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; text-align: center;'>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📞</div>
                    <div style='font-size: 12px;'>Telefon</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>💬</div>
                    <div style='font-size: 12px;'>Nachrichten</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>🌐</div>
                    <div style='font-size: 12px;'>Chrome</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📧</div>
                    <div style='font-size: 12px;'>Gmail</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📷</div>
                    <div style='font-size: 12px;'>Kamera</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>🗺️</div>
                    <div style='font-size: 12px;'>Maps</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>▶️</div>
                    <div style='font-size: 12px;'>YouTube</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 50%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>⚙️</div>
                    <div style='font-size: 12px;'>Einstellungen</div>
                </div>
            </div>
        </div>
    """)
    st.markdown(android_html, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Marktanteil", "71%")
    with col2:
        st.metric("Apps", "3,5 Mio")
    with col3:
        st.metric("Hersteller", "Google")
elif os_choice == "iOS":
    st.header("📱 iOS")
    st.info("**iOS** - Apples mobiles Betriebssystem für iPhone und iPad")
    # KORREKTUR: Verwende dedent für den f-String
    ios_html = dedent(f"""
        <div style='background: linear-gradient(180deg, #000428 0%, #004e92 100%); padding: 30px; border-radius: 40px; min-height: 600px; max-width: 400px; margin: 0 auto; color: white;'>
            <div style='display: flex; justify-content: space-between; padding: 15px; margin-bottom: 40px;'>
                <div style='font-weight: bold;'>{datetime.now().strftime('%H:%M')}</div>
                <div>📶 🔋</div>
            </div>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; text-align: center; margin-top: 50px;'>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📱</div>
                    <div style='font-size: 11px;'>Telefon</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>🌐</div>
                    <div style='font-size: 11px;'>Safari</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>✉️</div>
                    <div style='font-size: 11px;'>Mail</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>🎵</div>
                    <div style='font-size: 11px;'>Musik</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📅</div>
                    <div style='font-size: 11px;'>Kalender</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📸</div>
                    <div style='font-size: 11px;'>Fotos</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>📷</div>
                    <div style='font-size: 11px;'>Kamera</div>
                </div>
                <div>
                    <div style='font-size: 48px; background: rgba(255,255,255,0.2); border-radius: 20%; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;'>⚙️</div>
                    <div style='font-size: 11px;'>Einstellungen</div>
                </div>
            </div>
            <div style='margin-top: 80px; text-align: center;'>
                <div style='background: rgba(255,255,255,0.15); border-radius: 20px; padding: 15px; display: inline-flex; gap: 25px;'>
                    <div style='font-size: 36px;'>📞</div>
                    <div style='font-size: 36px;'>🌐</div>
                    <div style='font-size: 36px;'>💬</div>
                    <div style='font-size: 36px;'>🎵</div>
                </div>
            </div>
        </div>
    """)
    st.markdown(ios_html, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Marktanteil", "28%")
    with col2:
        st.metric("Apps", "1,8 Mio")
    with col3:
        st.metric("Sicherheit", "Sehr hoch")
# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • Erstellt mit Streamlit • © 2024
    </p>
</div>
""", unsafe_allow_html=True)
