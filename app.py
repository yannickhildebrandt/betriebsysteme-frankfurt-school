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
    st.session_state.current_directory = "C:\\" if st.session_state.get('selected_os') == "DOS" else "~"
if 'running_processes' not in st.session_state:
    st.session_state.running_processes = []
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'battery_level' not in st.session_state:
    st.session_state.battery_level = random.randint(60, 100)
if 'wifi_connected' not in st.session_state:
    st.session_state.wifi_connected = True

# --- Erweiterte CSS Styles ---
st.markdown("""
<style>
    /* Globale Styles */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=SF+Pro+Display:wght@300;400;600;700&family=Consolas&display=swap');
    
    .main {
        padding: 0;
    }
    
    /* DOS Terminal */
    .dos-terminal {
        background-color: #0000AA;
        color: #FFFFFF;
        font-family: 'Perfect DOS VGA 437', 'Courier New', monospace;
        padding: 20px;
        border-radius: 0;
        min-height: 500px;
        font-size: 16px;
        line-height: 1.2;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    .dos-terminal::before {
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
    
    .dos-cursor {
        display: inline-block;
        width: 10px;
        height: 16px;
        background-color: #FFFFFF;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 49% { opacity: 1; }
        50%, 100% { opacity: 0; }
    }
    
    /* Windows 10/11 Style */
    .windows-desktop {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 600px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
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
        z-index: 1000;
    }
    
    .windows-start-button {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        transition: background-color 0.2s;
        border-radius: 4px;
    }
    
    .windows-start-button:hover {
        background-color: rgba(255,255,255,0.1);
    }
    
    .windows-window {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(40px);
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        overflow: hidden;
        position: absolute;
        min-width: 400px;
        min-height: 300px;
        z-index: 100;
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
        cursor: move;
    }
    
    .windows-titlebar-buttons {
        display: flex;
        gap: 10px;
    }
    
    .windows-titlebar-button {
        width: 46px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background-color 0.1s;
        font-size: 10px;
    }
    
    .windows-titlebar-button:hover {
        background-color: #e0e0e0;
    }
    
    .windows-titlebar-button.close:hover {
        background-color: #e81123;
        color: white;
    }
    
    /* macOS Style */
    .macos-desktop {
        background: linear-gradient(180deg, #4A90E2 0%, #7B68EE 100%);
        min-height: 650px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .macos-menubar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 28px;
        background: rgba(0,0,0,0.3);
        backdrop-filter: blur(20px) saturate(180%);
        display: flex;
        align-items: center;
        padding: 0 15px;
        font-size: 13px;
        color: white;
        z-index: 1001;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    .macos-menu-item {
        padding: 0 12px;
        cursor: pointer;
        transition: background-color 0.2s;
        border-radius: 4px;
        height: 22px;
        display: flex;
        align-items: center;
    }
    
    .macos-menu-item:hover {
        background-color: rgba(255,255,255,0.2);
    }
    
    .macos-dock {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(40px) saturate(180%);
        border-radius: 16px;
        padding: 6px;
        display: flex;
        gap: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.18);
        z-index: 1000;
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
        position: relative;
    }
    
    .macos-dock-icon:hover {
        transform: translateY(-10px) scale(1.1);
    }
    
    .macos-dock-icon::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 4px;
        height: 4px;
        background: rgba(255,255,255,0.8);
        border-radius: 50%;
        opacity: 0;
    }
    
    .macos-dock-icon.active::after {
        opacity: 1;
    }
    
    .macos-window {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(40px);
        border-radius: 10px;
        box-shadow: 0 12px 48px rgba(0,0,0,0.3);
        overflow: hidden;
        position: absolute;
        min-width: 500px;
        min-height: 350px;
        z-index: 100;
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
        cursor: pointer;
        transition: all 0.2s;
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
    
    .macos-traffic-light:hover {
        transform: scale(1.1);
    }
    
    .macos-window-title {
        flex-grow: 1;
        text-align: center;
        font-weight: 600;
        font-size: 13px;
        color: #333;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    /* Linux Terminal */
    .linux-terminal {
        background-color: #300A24;
        color: #FFFFFF;
        font-family: 'Ubuntu Mono', 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 500px;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        position: relative;
    }
    
    .linux-prompt {
        color: #8AE234;
        font-weight: bold;
    }
    
    .linux-path {
        color: #729FCF;
    }
    
    .linux-cursor {
        display: inline-block;
        width: 8px;
        height: 16px;
        background-color: #FFFFFF;
        animation: blink 1s infinite;
    }
    
    /* Android Phone */
    .android-phone {
        width: 360px;
        height: 720px;
        background: #1a1a1a;
        border-radius: 36px;
        padding: 12px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        margin: 20px auto;
        position: relative;
    }
    
    .android-screen {
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, #1a73e8 0%, #4285f4 100%);
        border-radius: 28px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .android-statusbar {
        height: 28px;
        background: rgba(0,0,0,0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 15px;
        font-size: 11px;
        color: white;
    }
    
    .android-notch {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 24px;
        background: #1a1a1a;
        border-radius: 0 0 16px 16px;
        z-index: 100;
    }
    
    .android-home-screen {
        flex-grow: 1;
        padding: 40px 20px 20px 20px;
        display: flex;
        flex-direction: column;
    }
    
    .android-time-widget {
        color: white;
        text-align: left;
        margin-bottom: 30px;
    }
    
    .android-time {
        font-size: 72px;
        font-weight: 300;
        line-height: 1;
        margin-bottom: 5px;
    }
    
    .android-date {
        font-size: 18px;
        opacity: 0.9;
    }
    
    .android-app-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-top: auto;
        padding-bottom: 20px;
    }
    
    .android-app-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        cursor: pointer;
    }
    
    .android-app-icon-circle {
        width: 60px;
        height: 60px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .android-app-icon:active .android-app-icon-circle {
        transform: scale(0.9);
    }
    
    .android-app-label {
        font-size: 11px;
        color: white;
        text-align: center;
    }
    
    .android-navbar {
        height: 50px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: rgba(0,0,0,0.3);
    }
    
    .android-nav-button {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        cursor: pointer;
        transition: transform 0.1s;
    }
    
    .android-nav-button:active {
        transform: scale(0.9);
    }
    
    /* iOS Style */
    .ios-phone {
        width: 375px;
        height: 812px;
        background: #1a1a1a;
        border-radius: 40px;
        padding: 8px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        margin: 20px auto;
        position: relative;
    }
    
    .ios-screen {
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, #000428 0%, #004e92 100%);
        border-radius: 36px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .ios-notch {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 180px;
        height: 30px;
        background: #1a1a1a;
        border-radius: 0 0 20px 20px;
        z-index: 100;
    }
    
    .ios-statusbar {
        height: 44px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 30px;
        padding-top: 8px;
        color: white;
        font-size: 15px;
        font-weight: 600;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    .ios-home-screen {
        flex-grow: 1;
        padding: 20px;
        padding-top: 30px;
        display: flex;
        flex-direction: column;
    }
    
    .ios-app-pages {
        flex-grow: 1;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px 16px;
        align-content: start;
    }
    
    .ios-app-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        cursor: pointer;
    }
    
    .ios-app-icon-rounded {
        width: 60px;
        height: 60px;
        background: linear-gradient(145deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-radius: 13.33px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 0.5px solid rgba(255,255,255,0.2);
    }
    
    .ios-app-icon:active .ios-app-icon-rounded {
        transform: scale(0.85);
        opacity: 0.8;
    }
    
    .ios-app-label {
        font-size: 11px;
        color: white;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    .ios-dock {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(30px) saturate(180%);
        border-radius: 20px;
        margin: 0 10px 20px 10px;
        padding: 10px;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    
    .ios-home-indicator {
        width: 134px;
        height: 5px;
        background: rgba(255,255,255,0.4);
        border-radius: 2.5px;
        margin: 8px auto;
    }
    
    /* Chrome OS Style */
    .chromeos-desktop {
        background: #f1f3f4;
        min-height: 600px;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .chromeos-shelf {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(20px);
        border-radius: 12px 12px 0 0;
        padding: 8px 16px;
        display: flex;
        gap: 8px;
        box-shadow: 0 -2px 12px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .chromeos-shelf-icon {
        width: 48px;
        height: 48px;
        background: rgba(0,0,0,0.05);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .chromeos-shelf-icon:hover {
        background: rgba(0,0,0,0.1);
        transform: translateY(-4px);
    }
    
    /* Unix Terminal */
    .unix-terminal {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 500px;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .unix-prompt {
        color: #00FF00;
        font-weight: bold;
    }
    
    /* FreeBSD Terminal */
    .freebsd-terminal {
        background-color: #1a1a1a;
        color: #c0c0c0;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        min-height: 500px;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .freebsd-prompt {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    /* Notification */
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0,0,0,0.9);
        backdrop-filter: blur(20px);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        max-width: 320px;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
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
        "Besonderheiten": "Nahtlose Integration mit Apple-Produkten, exklusiv für Apple-Hardware",
        "Unterscheidungsmerkmale": "Elegantes Design, hohe Sicherheit, Apple-Ökosystem",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2001",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor",
        "icon": "",
        "color": "#000000"
    },
    "Linux": {
        "Hersteller": "Open Source Community",
        "Einsatzbereich": "Desktop, Server, Embedded",
        "Besonderheiten": "Open Source, hochgradig anpassbar, viele Distributionen",
        "Unterscheidungsmerkmale": "Freie Software, starke Community, maximale Kontrolle",
        "Betriebsarten": "Multitasking, Timesharing, Echtzeit",
        "Single-User/Multi-User": "Single-User, Multi-User",
        "Erst-erscheinung": "1991",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor",
        "icon": "🐧",
        "color": "#FCC624"
    },
    "Android": {
        "Hersteller": "Google",
        "Einsatzbereich": "Mobile Geräte",
        "Besonderheiten": "Marktführer bei mobilen OS, basiert auf Linux",
        "Unterscheidungsmerkmale": "Open Source, riesige App-Auswahl, hohe Anpassbarkeit",
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
        "Besonderheiten": "Exklusiv für iPhone/iPad, höchste Sicherheitsstandards",
        "Unterscheidungsmerkmale": "Geschlossenes System, nahtlose Hardware-Integration",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2007",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Mehrprozessor",
        "icon": "",
        "color": "#007AFF"
    },
    "Unix": {
        "Hersteller": "AT&T Bell Labs",
        "Einsatzbereich": "Server,Workstations",
        "Besonderheiten": "Urväter moderner Betriebssysteme, hochstabil",
        "Unterscheidungsmerkmale": "Multiuser-System, Grundlage für macOS und Linux",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1969",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor",
        "icon": "🖥️",
        "color": "#000000"
    },
    "Chrome OS": {
        "Hersteller": "Google",
        "Einsatzbereich": "Laptops (Chromebooks)",
        "Besonderheiten": "Cloud-zentriert, sehr schnell, sicher",
        "Unterscheidungsmerkmale": "Browser-basiert, automatische Updates, günstige Hardware",
        "Betriebsarten": "Multitasking",
        "Single-User/Multi-User": "Single-User",
        "Erst-erscheinung": "2011",
        "Dialog/Batch": "Dialog",
        "Einprozessor/Mehrprozessor": "Einprozessor",
        "icon": "🌐",
        "color": "#4285F4"
    },
    "FreeBSD": {
        "Hersteller": "FreeBSD Project",
        "Einsatzbereich": "Server, Desktop",
        "Besonderheiten": "Extrem stabil, hohe Performance, BSD-Lizenz",
        "Unterscheidungsmerkmale": "Komplettes System aus einer Hand, ZFS-Support",
        "Betriebsarten": "Multitasking, Timesharing",
        "Single-User/Multi-User": "Multi-User",
        "Erst-erscheinung": "1993",
        "Dialog/Batch": "Dialog, Batch",
        "Einprozessor/Mehrprozessor": "Einprozessor, Mehrprozessor",
        "icon": "👹",
        "color": "#AB2B28"
    }
}

# --- Hilfsfunktionen ---
def show_notification(message, duration=3):
    """Zeigt eine Benachrichtigung an"""
    notification_placeholder = st.empty()
    notification_placeholder.markdown(
        f"""
        <div class="notification">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(duration)
    notification_placeholder.empty()

def get_current_time():
    """Gibt die aktuelle Zeit zurück"""
    return datetime.now().strftime("%H:%M")

def get_current_date():
    """Gibt das aktuelle Datum zurück"""
    return datetime.now().strftime("%a, %d. %B")

# --- Header ---
st.markdown(f"""
<div style='text-align: center; padding: 20px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
     border-radius: 10px; margin-bottom: 30px; color: white;'>
    <h1 style='margin: 0; font-size: 2.5em;'>💻 Betriebssystem-Simulator Pro</h1>
    <p style='margin: 10px 0 0 0; opacity: 0.9;'>Erleben Sie die Evolution der Betriebssysteme - von DOS bis moderne Mobile OS</p>
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
    
    info_expander = st.expander("Details anzeigen", expanded=False)
    with info_expander:
        for key, value in selected_os_info.items():
            if key not in ['icon', 'color']:
                st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Simulator-Einstellungen")
    
    show_hints = st.checkbox("💡 Hilfestellungen anzeigen", value=True)
    realistic_delays = st.checkbox("⏱️ Realistische Verzögerungen", value=True)
    sound_effects = st.checkbox("🔊 Soundeffekte (simuliert)", value=False)
    
    st.markdown("---")
    st.info("💡 **Tipp:** Interagieren Sie mit den Oberflächen, um die jeweiligen Betriebssysteme zu erkunden!")

# --- Hauptbereich ---
selected_os_info = os_data[selected_os_name]

# System-Header
col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
with col_header1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {selected_os_info['color']}22, {selected_os_info['color']}44); 
         padding: 20px; border-radius: 10px; border-left: 4px solid {selected_os_info['color']};'>
        <h2 style='margin: 0; color: {selected_os_info['color']};'>{selected_os_info['icon']} {selected_os_name}</h2>
        <p style='margin: 5px 0 0 0; opacity: 0.8;'>{selected_os_info['Besonderheiten']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    st.metric("Erscheinungsjahr", selected_os_info['Erst-erscheinung'])

with col_header3:
    st.metric("Hersteller", selected_os_info['Hersteller'])

st.markdown("---")

# === DOS Simulation ===
if selected_os_name == "DOS":
    st.markdown("### 💾 MS-DOS Simulation")
    
    if show_hints:
        st.info("🕹️ **DOS** war das dominierende Betriebssystem in den 1980ern. Alle Interaktionen erfolgten über Textbefehle. Probieren Sie: `dir`, `cd`, `type`, `cls`, `ver`, `help`")
    
    # DOS Terminal
    terminal_container = st.container()
    
    with terminal_container:
        st.markdown('<div class="dos-terminal">', unsafe_allow_html=True)
        
        # Terminal History anzeigen
        if 'dos_history' not in st.session_state:
            st.session_state.dos_history = [
                "Microsoft(R) MS-DOS(R) Version 6.22",
                "             (C)Copyright Microsoft Corp 1981-1994.",
                "",
                "C:\\>"
            ]
        
        # History anzeigen
        for line in st.session_state.dos_history:
            st.markdown(f"<div style='margin: 2px 0;'>{line}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Command Input
    col_cmd1, col_cmd2 = st.columns([5, 1])
    with col_cmd1:
        dos_command = st.text_input(
            "DOS Command:",
            key="dos_cmd",
            placeholder="Geben Sie einen Befehl ein...",
            label_visibility="collapsed"
        )
    with col_cmd2:
        execute_button = st.button("⏎ Execute", use_container_width=True)
    
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
            st.session_state.dos_history.extend([
                "",
                "MS-DOS Version 6.22",
                ""
            ])
        
        elif cmd == "help":
            st.session_state.dos_history.extend([
                "",
                "Verfügbare Befehle:",
                "  DIR     - Verzeichnis anzeigen",
                "  CD      - Verzeichnis wechseln",
                "  TYPE    - Dateiinhalt anzeigen",
                "  CLS     - Bildschirm löschen",
                "  VER     - Version anzeigen",
                "  DATE    - Datum anzeigen/ändern",
                "  TIME    - Zeit anzeigen/ändern",
                "  HELP    - Diese Hilfe",
                ""
            ])
        
        elif cmd == "date":
            st.session_state.dos_history.extend([
                f"Aktuelles Datum: {datetime.now().strftime('%d.%m.%Y')}",
                ""
            ])
        
        elif cmd == "time":
            st.session_state.dos_history.extend([
                f"Aktuelle Zeit: {datetime.now().strftime('%H:%M:%S')}",
                ""
            ])
        
        elif cmd.startswith("type "):
            filename = cmd[5:]
            st.session_state.dos_history.extend([
                "",
                f"Inhalt von {filename.upper()}:",
                "Dies ist eine Beispieldatei.",
                "MS-DOS Version 6.22",
                ""
            ])
        
        elif cmd.startswith("cd "):
            path = cmd[3:]
            st.session_state.dos_history.extend([
                f"C:\\{path.upper()}>",
                ""
            ])
        
        else:
            st.session_state.dos_history.extend([
                f"Ungültiger Befehl oder Dateiname: {dos_command}",
                ""
            ])
        
        st.session_state.dos_history.append("C:\\>")
        st.rerun()

# === Windows Simulation ===
elif selected_os_name == "Windows":
    st.markdown("### 🪟 Windows 11 Simulation")
    
    if show_hints:
        st.info("🖱️ **Windows** revolutionierte die PC-Bedienung mit grafischer Oberfläche. Klicken Sie auf Icons im Startmenü oder der Taskleiste!")
    
    # Initialize window states
    if 'win_explorer_open' not in st.session_state:
        st.session_state.win_explorer_open = False
    if 'win_edge_open' not in st.session_state:
        st.session_state.win_edge_open = False
    if 'win_settings_open' not in st.session_state:
        st.session_state.win_settings_open = False
    if 'win_start_open' not in st.session_state:
        st.session_state.win_start_open = False
    
    # Desktop
    st.markdown('<div class="windows-desktop">', unsafe_allow_html=True)
    
    # Desktop Icons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📁\nDieser PC", key="win_this_pc"):
            st.session_state.win_explorer_open = not st.session_state.win_explorer_open
            if sound_effects:
                st.toast("🔊 *Click*")
    
    with col2:
        if st.button("🗑️\nPapierkorb", key="win_recycle"):
            st.toast("🗑️ Papierkorb ist leer")
    
    # Windows
    if st.session_state.win_explorer_open:
        st.markdown("""
        <div class="windows-window" style="top: 100px; left: 100px;">
            <div class="windows-titlebar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>📁</span>
                    <span>Datei-Explorer</span>
                </div>
                <div class="windows-titlebar-buttons">
                    <div class="windows-titlebar-button">─</div>
                    <div class="windows-titlebar-button">□</div>
                    <div class="windows-titlebar-button close">✕</div>
                </div>
            </div>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px; padding: 10px; background: #f0f0f0; border-radius: 4px;">
                    <strong>Schnellzugriff</strong>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">📄</div>
                        <div style="margin-top: 8px; font-size: 12px;">Dokumente</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">🖼️</div>
                        <div style="margin-top: 8px; font-size: 12px;">Bilder</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">🎵</div>
                        <div style="margin-top: 8px; font-size: 12px;">Musik</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">🎬</div>
                        <div style="margin-top: 8px; font-size: 12px;">Videos</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">💾</div>
                        <div style="margin-top: 8px; font-size: 12px;">Downloads</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="font-size: 32px;">💻</div>
                        <div style="margin-top: 8px; font-size: 12px;">Desktop</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.win_edge_open:
        st.markdown("""
        <div class="windows-window" style="top: 150px; left: 200px; min-width: 600px; min-height: 400px;">
            <div class="windows-titlebar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span>🌐</span>
                    <span>Microsoft Edge</span>
                </div>
                <div class="windows-titlebar-buttons">
                    <div class="windows-titlebar-button">─</div>
                    <div class="windows-titlebar-button">□</div>
                    <div class="windows-titlebar-button close">✕</div>
                </div>
            </div>
            <div style="padding: 0;">
                <div style="background: #f3f3f3; padding: 10px; border-bottom: 1px solid #e0e0e0; display: flex; gap: 10px; align-items: center;">
                    <button style="background: none; border: none; padding: 5px 10px; cursor: pointer;">←</button>
                    <button style="background: none; border: none; padding: 5px 10px; cursor: pointer;">→</button>
                    <button style="background: none; border: none; padding: 5px 10px; cursor: pointer;">↻</button>
                    <div style="flex-grow: 1; background: white; padding: 8px 15px; border-radius: 20px; border: 1px solid #e0e0e0;">
                        🔒 https://www.microsoft.com
                    </div>
                </div>
                <div style="padding: 40px; text-align: center;">
                    <h2 style="color: #0078D4; margin-bottom: 20px;">Willkommen bei Microsoft Edge</h2>
                    <p style="color: #666; margin-bottom: 30px;">Der schnelle und sichere Browser für Windows</p>
                    <div style="display: flex; justify-content: center; gap: 20px;">
                        <div style="padding: 20px; background: #f5f5f5; border-radius: 8px; width: 150px;">
                            <div style="font-size: 32px; margin-bottom: 10px;">⚡</div>
                            <div style="font-size: 14px; color: #333;">Schnell</div>
                        </div>
                        <div style="padding: 20px; background: #f5f5f5; border-radius: 8px; width: 150px;">
                            <div style="font-size: 32px; margin-bottom: 10px;">🔒</div>
                            <div style="font-size: 14px; color: #333;">Sicher</div>
                        </div>
                        <div style="padding: 20px; background: #f5f5f5; border-radius: 8px; width: 150px;">
                            <div style="font-size: 32px; margin-bottom: 10px;">🌐</div>
                            <div style="font-size: 14px; color: #333;">Modern</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Taskbar
    st.markdown("""
    <div class="windows-taskbar">
        <div class="windows-start-button">🪟</div>
        <div style="flex-grow: 1; display: flex; gap: 5px; margin-left: 10px;">
            <div style="padding: 0 12px; height: 32px; display: flex; align-items: center; background: rgba(255,255,255,0.1); border-radius: 4px; cursor: pointer;">
                📁
            </div>
            <div style="padding: 0 12px; height: 32px; display: flex; align-items: center; background: rgba(255,255,255,0.1); border-radius: 4px; cursor: pointer;">
                🌐
            </div>
            <div style="padding: 0 12px; height: 32px; display: flex; align-items: center; background: rgba(255,255,255,0.1); border-radius: 4px; cursor: pointer;">
                📧
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 15px; color: white; font-size: 12px;">
            <div>🔊</div>
            <div>📶</div>
            <div>🔋 87%</div>
            <div>{}</div>
        </div>
    </div>
    """.format(get_current_time()), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown("---")
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)
    with col_ctrl1:
        if st.button("📁 Datei-Explorer öffnen", use_container_width=True):
            st.session_state.win_explorer_open = True
            st.rerun()
    with col_ctrl2:
        if st.button("🌐 Edge Browser öffnen", use_container_width=True):
            st.session_state.win_edge_open = True
            st.rerun()
    with col_ctrl3:
        if st.button("⚙️ Einstellungen", use_container_width=True):
            st.session_state.win_settings_open = True
            st.toast("⚙️ Einstellungen geöffnet")
    with col_ctrl4:
        if st.button("🔄 Desktop zurücksetzen", use_container_width=True):
            st.session_state.win_explorer_open = False
            st.session_state.win_edge_open = False
            st.session_state.win_settings_open = False
            st.rerun()

# === macOS Simulation ===
elif selected_os_name == "macOS":
    st.markdown("### macOS Ventura Simulation")
    
    if show_hints:
        st.info("🍎 **macOS** ist bekannt für sein elegantes Design und die nahtlose Integration im Apple-Ökosystem. Nutzen Sie das Dock am unteren Bildschirmrand!")
    
    # Initialize states
    if 'mac_finder_open' not in st.session_state:
        st.session_state.mac_finder_open = False
    if 'mac_safari_open' not in st.session_state:
        st.session_state.mac_safari_open = False
    if 'mac_mail_open' not in st.session_state:
        st.session_state.mac_mail_open = False
    
    # Desktop
    st.markdown('<div class="macos-desktop">', unsafe_allow_html=True)
    
    # Menu Bar
    st.markdown(f"""
    <div class="macos-menubar">
        <div class="macos-menu-item" style="font-weight: 600;"></div>
        <div class="macos-menu-item">Finder</div>
        <div class="macos-menu-item">Ablage</div>
        <div class="macos-menu-item">Bearbeiten</div>
        <div class="macos-menu-item">Darstellung</div>
        <div class="macos-menu-item">Gehe zu</div>
        <div class="macos-menu-item">Fenster</div>
        <div class="macos-menu-item">Hilfe</div>
        <div style="flex-grow: 1;"></div>
        <div style="display: flex; gap: 15px; align-items: center;">
            <div>🔋</div>
            <div>📶</div>
            <div>🔍</div>
            <div>{get_current_time()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Windows
    if st.session_state.mac_finder_open:
        st.markdown("""
        <div class="macos-window" style="top: 80px; left: 100px;">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light close"></div>
                    <div class="macos-traffic-light minimize"></div>
                    <div class="macos-traffic-light maximize"></div>
                </div>
                <div class="macos-window-title">Finder</div>
                <div style="width: 80px;"></div>
            </div>
            <div style="display: flex; height: 400px;">
                <div style="width: 180px; background: #f5f5f7; border-right: 1px solid #e0e0e0; padding: 15px;">
                    <div style="font-size: 11px; color: #86868b; font-weight: 600; margin-bottom: 8px;">FAVORITEN</div>
                    <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px; cursor: pointer; background: #e8e8ed;">
                        <span style="margin-right: 8px;">🏠</span>Schreibtisch
                    </div>
                    <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px; cursor: pointer;">
                        <span style="margin-right: 8px;">📄</span>Dokumente
                    </div>
                    <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px; cursor: pointer;">
                        <span style="margin-right: 8px;">💾</span>Downloads
                    </div>
                    <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px; cursor: pointer;">
                        <span style="margin-right: 8px;">🖼️</span>Bilder
                    </div>
                    <div style="font-size: 11px; color: #86868b; font-weight: 600; margin: 15px 0 8px 0;">GERÄTE</div>
                    <div style="padding: 6px 8px; border-radius: 6px; margin-bottom: 4px; cursor: pointer;">
                        <span style="margin-right: 8px;">💻</span>Macintosh HD
                    </div>
                </div>
                <div style="flex-grow: 1; padding: 20px;">
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                        <div style="text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 8px;">📁</div>
                            <div style="font-size: 12px;">Projekte</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 8px;">📄</div>
                            <div style="font-size: 12px;">Präsentation.key</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 8px;">🖼️</div>
                            <div style="font-size: 12px;">Urlaub2024.jpg</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 48px; margin-bottom: 8px;">🎵</div>
                            <div style="font-size: 12px;">Playlist.m4a</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.mac_safari_open:
        st.markdown("""
        <div class="macos-window" style="top: 120px; left: 200px; min-width: 700px;">
            <div class="macos-titlebar">
                <div class="macos-traffic-lights">
                    <div class="macos-traffic-light close"></div>
                    <div class="macos-traffic-light minimize"></div>
                    <div class="macos-traffic-light maximize"></div>
                </div>
                <div class="macos-window-title">Apple – Safari</div>
                <div style="width: 80px;"></div>
            </div>
            <div style="padding: 0;">
                <div style="background: #f5f5f7; padding: 10px 15px; border-bottom: 1px solid #e0e0e0; display: flex; gap: 12px; align-items: center;">
                    <button style="background: none; border: none; font-size: 16px; cursor: pointer; color: #666;">←</button>
                    <button style="background: none; border: none; font-size: 16px; cursor: pointer; color: #666;">→</button>
                    <div style="flex-grow: 1; background: white; padding: 6px 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px; border: 1px solid #d0d0d0;">
                        <span>🔒</span>
                        <span style="color: #666; font-size: 13px;">apple.com</span>
                    </div>
                    <button style="background: none; border: none; font-size: 16px; cursor: pointer;">⋯</button>
                </div>
                <div style="padding: 50px; text-align: center; background: white;">
                    <div style="font-size: 56px; margin-bottom: 20px;"></div>
                    <h2 style="font-size: 32px; font-weight: 600; margin-bottom: 15px; color: #1d1d1f;">Safari</h2>
                    <p style="font-size: 16px; color: #666; max-width: 400px; margin: 0 auto;">Der schnellste Browser der Welt. Entwickelt von Apple für Mac, iPhone und iPad.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dock
    st.markdown("""
    <div class="macos-dock">
        <div class="macos-dock-icon active">📁</div>
        <div class="macos-dock-icon">🌐</div>
        <div class="macos-dock-icon">✉️</div>
        <div class="macos-dock-icon">📅</div>
        <div class="macos-dock-icon">🎵</div>
        <div class="macos-dock-icon">📺</div>
        <div style="width: 1px; height: 48px; background: rgba(255,255,255,0.3); margin: 0 4px;"></div>
        <div class="macos-dock-icon">⚙️</div>
        <div class="macos-dock-icon">🗑️</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown("---")
    col_mac1, col_mac2, col_mac3, col_mac4 = st.columns(4)
    with col_mac1:
        if st.button("📁 Finder öffnen", use_container_width=True):
            st.session_state.mac_finder_open = True
            st.rerun()
    with col_mac2:
        if st.button("🌐 Safari öffnen", use_container_width=True):
            st.session_state.mac_safari_open = True
            st.rerun()
    with col_mac3:
        if st.button("✉️ Mail öffnen", use_container_width=True):
            st.session_state.mac_mail_open = True
            st.toast("📧 Mail geöffnet")
    with col_mac4:
        if st.button("🔄 Desktop zurücksetzen", use_container_width=True):
            st.session_state.mac_finder_open = False
            st.session_state.mac_safari_open = False
            st.session_state.mac_mail_open = False
            st.rerun()

# === Linux Simulation ===
elif selected_os_name == "Linux":
    st.markdown("### 🐧 Linux (Ubuntu) Simulation")
    
    if show_hints:
        st.info("🐧 **Linux** bietet maximale Kontrolle über Ihr System. Probieren Sie Befehle wie: `ls`, `pwd`, `whoami`, `uname -a`, `df -h`, `top`, `neofetch`")
    
    # Desktop Environment Selector
    de_col1, de_col2 = st.columns([3, 1])
    with de_col1:
        desktop_env = st.selectbox(
            "Desktop-Umgebung:",
            ["GNOME (Standard)", "KDE Plasma", "XFCE", "i3 (Tiling WM)"],
            key="linux_de"
        )
    with de_col2:
        terminal_theme = st.selectbox(
            "Terminal-Theme:",
            ["Ubuntu", "Dracula", "Solarized"],
            key="linux_theme"
        )
    
    # Terminal
    st.markdown('<div class="linux-terminal">', unsafe_allow_html=True)
    
    # Terminal Header
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); padding: 8px 12px; margin: -20px -20px 15px -20px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px 8px 0 0;">
        <div style="display: flex; gap: 8px;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: #fc5753;"></div>
            <div style="width: 12px; height: 12px; border-radius: 50%; background: #fdbc40;"></div>
            <div style="width: 12px; height: 12px; border-radius: 50%; background: #33c948;"></div>
        </div>
        <div style="font-size: 12px; color: #8AE234;">user@ubuntu: ~</div>
        <div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Linux history
    if 'linux_history' not in st.session_state:
        st.session_state.linux_history = [
            "Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-91-generic x86_64)",
            "",
            " * Documentation:  https://help.ubuntu.com",
            " * Management:     https://landscape.canonical.com",
            " * Support:        https://ubuntu.com/advantage",
            "",
            f"Last login: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')} from 192.168.1.100",
            ""
        ]
    
    # Display history
    for line in st.session_state.linux_history:
        if line.startswith("user@ubuntu"):
            st.markdown(f"<div><span class='linux-prompt'>{line.split(':')[0]}:</span><span class='linux-path'>{line.split(':')[1] if ':' in line else ''}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div>{line}</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Command Input
    col_linux1, col_linux2 = st.columns([5, 1])
    with col_linux1:
        linux_command = st.text_input(
            "Linux Command:",
            key="linux_cmd",
            placeholder="Geben Sie einen Befehl ein...",
            label_visibility="collapsed"
        )
    with col_linux2:
        if st.button("⏎ Enter", use_container_width=True):
            if linux_command:
                cmd = linux_command.strip()
                st.session_state.linux_history.append(f"user@ubuntu:~$ {cmd}")
                
                if realistic_delays:
                    time.sleep(0.2)
                
                # Linux Commands
                if cmd == "ls" or cmd == "ls -la":
                    st.session_state.linux_history.extend([
                        "total 48",
                        "drwxr-xr-x  8 user user 4096 Jan 15 10:30 .",
                        "drwxr-xr-x  3 root root 4096 Dec  1 09:15 ..",
                        "drwxr-xr-x  2 user user 4096 Jan 10 14:22 Desktop",
                        "drwxr-xr-x  3 user user 4096 Jan 12 16:45 Documents",
                        "drwxr-xr-x  2 user user 4096 Jan 14 11:30 Downloads",
                        "drwxr-xr-x  2 user user 4096 Dec 28 08:15 Music",
                        "drwxr-xr-x  3 user user 4096 Jan  5 19:20 Pictures",
                        "-rw-r--r--  1 user user  220 Dec  1 09:15 .bash_logout",
                        "-rw-r--r--  1 user user 3526 Dec  1 09:15 .bashrc",
                        ""
                    ])
                
                elif cmd == "pwd":
                    st.session_state.linux_history.extend([
                        "/home/user",
                        ""
                    ])
                
                elif cmd == "whoami":
                    st.session_state.linux_history.extend([
                        "user",
                        ""
                    ])
                
                elif cmd == "uname -a":
                    st.session_state.linux_history.extend([
                        "Linux ubuntu 5.15.0-91-generic #101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux",
                        ""
                    ])
                
                elif cmd == "df -h":
                    st.session_state.linux_history.extend([
                        "Filesystem      Size  Used Avail Use% Mounted on",
                        "/dev/sda1       100G   45G   50G  48% /",
                        "tmpfs           7.8G  1.2M  7.8G   1% /dev/shm",
                        "/dev/sda2       200G   78G  112G  42% /home",
                        ""
                    ])
                
                elif cmd == "top":
                    st.session_state.linux_history.extend([
                        "top - 14:23:45 up 3 days,  2:15,  1 user,  load average: 0.52, 0.58, 0.59",
                        "Tasks: 247 total,   1 running, 246 sleeping,   0 stopped,   0 zombie",
                        "%Cpu(s):  5.2 us,  2.1 sy,  0.0 ni, 92.1 id,  0.3 wa,  0.0 hi,  0.3 si,  0.0 st",
                        "MiB Mem :  15976.2 total,   8234.1 free,   4512.3 used,   3229.8 buff/cache",
                        "",
                        "  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND",
                        " 1234 user      20   0 3234556 456789  12345 S   8.3   2.9   5:23.45 firefox",
                        " 5678 user      20   0 1234567 234567  56789 S   4.2   1.5   2:45.67 code",
                        ""
                    ])
                
                elif cmd == "neofetch":
                    st.session_state.linux_history.extend([
                        "            .-/+oossssoo+/-.",
                        "        `:+ssssssssssssssssss+:`",
                        "      -+ssssssssssssssssssyyssss+-",
                        "    .ossssssssssssssssssdMMMNysssso.",
                        "   /ssssssssssshdmmNNmmyNMMMMhssssss/",
                        "  +ssssssssshmydMMMMMMMNddddyssssssss+",
                        "",
                        f"user@ubuntu",
                        "-----------",
                        "OS: Ubuntu 22.04.3 LTS x86_64",
                        "Host: Virtual Machine",
                        "Kernel: 5.15.0-91-generic",
                        "Uptime: 3 days, 2 hours, 15 mins",
                        "Packages: 2847 (dpkg), 12 (snap)",
                        "Shell: bash 5.1.16",
                        f"DE: {desktop_env}",
                        "CPU: Intel i7-9700K (8) @ 3.600GHz",
                        "GPU: NVIDIA GeForce RTX 2070",
                        "Memory: 4512MiB / 15976MiB",
                        ""
                    ])
                
                elif cmd == "clear":
                    st.session_state.linux_history = []
                
                elif cmd.startswith("sudo "):
                    st.session_state.linux_history.extend([
                        "[sudo] password for user: ",
                        "✓ Command executed successfully",
                        ""
                    ])
                
                else:
                    st.session_state.linux_history.extend([
                        f"bash: {cmd}: command not found",
                        "Try 'help' for a list of available commands",
                        ""
                    ])
                
                st.session_state.linux_history.append("")
                st.rerun()

# === Android Simulation ===
elif selected_os_name == "Android":
    st.markdown("### 🤖 Android 14 Simulation")
    
    if show_hints:
        st.info("📱 **Android** ist das meistgenutzte mobile Betriebssystem weltweit. Tippen Sie auf App-Icons oder nutzen Sie die Navigationsleiste!")
    
    # Phone Container
    st.markdown('<div class="android-phone">', unsafe_allow_html=True)
    st.markdown('<div class="android-screen">', unsafe_allow_html=True)
    st.markdown('<div class="android-notch"></div>', unsafe_allow_html=True)
    
    # Status Bar
    current_time = get_current_time()
    st.markdown(f"""
    <div class="android-statusbar">
        <div style="display: flex; gap: 8px; align-items: center;">
            <span>{current_time}</span>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span>📶</span>
            <span>📡</span>
            <span>🔋 {st.session_state.battery_level}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Home Screen
    st.markdown('<div class="android-home-screen">', unsafe_allow_html=True)
    
    # Time Widget
    current_date = get_current_date()
    st.markdown(f"""
    <div class="android-time-widget">
        <div class="android-time">{current_time}</div>
        <div class="android-date">{current_date}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # App Grid
    st.markdown('<div class="android-app-grid">', unsafe_allow_html=True)
    
    apps = [
        ("📞", "Telefon"),
        ("💬", "Nachrichten"),
        ("🌐", "Chrome"),
        ("📧", "Gmail"),
        ("📷", "Kamera"),
        ("🗺️", "Maps"),
        ("▶️", "YouTube"),
        ("📸", "Fotos"),
        ("🎵", "Musik"),
        ("⚙️", "Einstellungen"),
        ("📱", "Play Store"),
        ("📅", "Kalender")
    ]
    
    for emoji, name in apps:
        st.markdown(f"""
        <div class="android-app-icon">
            <div class="android-app-icon-circle">{emoji}</div>
            <div class="android-app-label">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End app-grid
    st.markdown('</div>', unsafe_allow_html=True)  # End home-screen
    
    # Navigation Bar
    st.markdown("""
    <div class="android-navbar">
        <div class="android-nav-button">◁</div>
        <div class="android-nav-button">⚪</div>
        <div class="android-nav-button">▢</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End screen
    st.markdown('</div>', unsafe_allow_html=True)  # End phone
    
    # App Controls
    st.markdown("---")
    st.markdown("### 📱 App-Interakt ionen")
    col_and1, col_and2, col_and3, col_and4 = st.columns(4)
    
    with col_and1:
        if st.button("📞 Anruf starten", use_container_width=True):
            st.toast("📞 Anruf wird getätigt...")
            if realistic_delays:
                time.sleep(1)
            st.success("✓ Anruf beendet")
    
    with col_and2:
        if st.button("📸 Foto aufnehmen", use_container_width=True):
            st.toast("📸 Kamera wird geöffnet...")
            if realistic_delays:
                time.sleep(0.5)
            st.success("✓ Foto gespeichert in Galerie")
    
    with col_and3:
        if st.button("💬 Nachricht senden", use_container_width=True):
            st.toast("💬 Nachricht wird gesendet...")
            if realistic_delays:
                time.sleep(0.7)
            st.success("✓ Nachricht zugestellt")
    
    with col_and4:
        if st.button("🔋 Akku anzeigen", use_container_width=True):
            st.info(f"🔋 Akkustand: {st.session_state.battery_level}%")

# === iOS Simulation ===
elif selected_os_name == "iOS":
    st.markdown("### iOS 17 Simulation")
    
    if show_hints:
        st.info("📱 **iOS** bietet eine intuitive, flüssige Bedienung und ist bekannt für höchste Sicherheitsstandards. Wischen Sie von unten nach oben für das Kontrollzentrum!")
    
    # Phone Container
    st.markdown('<div class="ios-phone">', unsafe_allow_html=True)
    st.markdown('<div class="ios-screen">', unsafe_allow_html=True)
    st.markdown('<div class="ios-notch"></div>', unsafe_allow_html=True)
    
    # Status Bar
    current_time = get_current_time()
    st.markdown(f"""
    <div class="ios-statusbar">
        <div>{current_time}</div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span>📶</span>
            <span>📡</span>
            <span>🔋</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Home Screen
    st.markdown('<div class="ios-home-screen">', unsafe_allow_html=True)
    st.markdown('<div class="ios-app-pages">', unsafe_allow_html=True)
    
    ios_apps = [
        ("📱", "Telefon"),
        ("📧", "Mail"),
        ("🌐", "Safari"),
        ("🎵", "Musik"),
        ("💬", "Nachrichten"),
        ("📅", "Kalender"),
        ("📸", "Fotos"),
        ("📷", "Kamera"),
        ("⚙️", "Einstellungen"),
        ("🗺️", "Karten"),
        ("🎬", "TV"),
        ("📰", "News"),
        ("📚", "Bücher"),
        ("🏪", "App Store"),
        ("💳", "Wallet"),
        ("⏰", "Uhr")
    ]
    
    for emoji, name in ios_apps:
        st.markdown(f"""
        <div class="ios-app-icon">
            <div class="ios-app-icon-rounded">{emoji}</div>
            <div class="ios-app-label">{name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End app-pages
    
    # Dock
    st.markdown("""
    <div class="ios-dock">
        <div class="ios-app-icon-rounded" style="width: 60px; height: 60px; font-size: 30px;">📞</div>
        <div class="ios-app-icon-rounded" style="width: 60px; height: 60px; font-size: 30px;">🌐</div>
        <div class="ios-app-icon-rounded" style="width: 60px; height: 60px; font-size: 30px;">💬</div>
        <div class="ios-app-icon-rounded" style="width: 60px; height: 60px; font-size: 30px;">🎵</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Home Indicator
    st.markdown('<div class="ios-home-indicator"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End home-screen
    st.markdown('</div>', unsafe_allow_html=True)  # End screen
    st.markdown('</div>', unsafe_allow_html=True)  # End phone
    
    # App Controls
    st.markdown("---")
    st.markdown("### 📱 iOS Features")
    
    col_ios1, col_ios2, col_ios3 = st.columns(3)
    
    with col_ios1:
        if st.button("🔐 Face ID entsperren", use_container_width=True):
            st.toast("🔐 Gesicht wird erkannt...")
            if realistic_delays:
                time.sleep(1.5)
            st.success("✓ iPhone entsperrt")
    
    with col_ios2:
        if st.button("🎙️ Siri aktivieren", use_container_width=True):
            st.toast("🎙️ 'Hey Siri' erkannt...")
            if realistic_delays:
                time.sleep(1)
            st.info("🎙️ Wie kann ich helfen?")
    
    with col_ios3:
        if st.button("📱 AirDrop teilen", use_container_width=True):
            st.toast("📱 Suche nach Geräten in der Nähe...")
            if realistic_delays:
                time.sleep(1)
            st.success("✓ Datei gesendet")

# === Unix/Chrome OS/FreeBSD Simulationen (ähnlich wie vorher, aber mit verbessertem Styling) ===
elif selected_os_name == "Unix":
    st.markdown("### 🖥️ Unix System V Simulation")
    
    if show_hints:
        st.info("🖥️ **Unix** ist der Vater moderner Betriebssysteme. Probieren Sie Befehle wie: `ls -l`, `ps aux`, `netstat`, `top`")
    
    st.markdown('<div class="unix-terminal">', unsafe_allow_html=True)
    
    if 'unix_history' not in st.session_state:
        st.session_state.unix_history = [
            "UNIX System V Release 4.0 (localhost)",
            f"login: root",
            f"Password: ",
            f"Last login: {datetime.now().strftime('%a %b %d %H:%M:%S')} on console",
            "#"
        ]
    
    for line in st.session_state.unix_history:
        st.markdown(f"<div>{line}</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    unix_cmd = st.text_input("Unix Command:", key="unix_cmd", placeholder="Enter command...")
    
    if st.button("Execute", key="unix_exec") and unix_cmd:
        st.session_state.unix_history.append(f"# {unix_cmd}")
        
        if unix_cmd == "ls -l":
            st.session_state.unix_history.extend([
                "total 24",
                "drwxr-xr-x  2 root  wheel   512 Jan  1 00:00 bin",
                "drwxr-xr-x  2 root  wheel   512 Jan  1 00:00 etc",
                "drwxr-xr-x  2 root  wheel   512 Jan  1 00:00 usr",
                "drwxr-xr-x  2 root  wheel   512 Jan  1 00:00 var",
                ""
            ])
        elif unix_cmd == "ps aux":
            st.session_state.unix_history.extend([
                "USER  PID  %CPU %MEM    VSZ   RSS  TT  STAT STARTED      TIME COMMAND",
                "root    1   0.0  0.1   1234   567  ?   Ss   00:00     0:01 /sbin/init",
                "root  123   0.0  0.2   2345   678  ?   S    00:01     0:00 syslogd",
                ""
            ])
        else:
            st.session_state.unix_history.append(f"{unix_cmd}: command not found")
        
        st.session_state.unix_history.append("#")
        st.rerun()

elif selected_os_name == "Chrome OS":
    st.markdown("### 🌐 Chrome OS Simulation")
    
    if show_hints:
        st.info("🌐 **Chrome OS** ist vollständig auf den Chrome-Browser und Cloud-Dienste ausgerichtet. Alles läuft im Browser!")
    
    st.markdown('<div class="chromeos-desktop">', unsafe_allow_html=True)
    
    # Chrome Browser Window
    st.markdown("""
    <div style="background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); margin: 20px; height: 500px; display: flex; flex-direction: column;">
        <div style="background: #f1f3f4; padding: 12px; border-bottom: 1px solid #dadce0; border-radius: 8px 8px 0 0; display: flex; gap: 10px; align-items: center;">
            <div style="display: flex; gap: 15px;">
                <span style="cursor: pointer; color: #666;">←</span>
                <span style="cursor: pointer; color: #666;">→</span>
                <span style="cursor: pointer; color: #666;">↻</span>
            </div>
            <div style="flex-grow: 1; background: white; padding: 8px 15px; border-radius: 24px; border: 1px solid #dadce0; display: flex; align-items: center; gap: 10px;">
                <span>🔒</span>
                <input type="text" value="https://www.google.com" style="border: none; outline: none; width: 100%; font-size: 14px;" />
            </div>
            <span style="cursor: pointer; font-size: 20px; color: #666;">⋮</span>
        </div>
        <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px;">
            <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" alt="Google" style="width: 272px; margin-bottom: 30px;"/>
            <div style="width: 100%; max-width: 600px; position: relative;">
                <input type="text" placeholder="In Google suchen oder URL eingeben" style="width: 100%; padding: 12px 45px 12px 45px; border: 1px solid #dfe1e5; border-radius: 24px; font-size: 14px; box-shadow: 0 1px 6px rgba(32,33,36,.28);"/>
                <span style="position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: #9aa0a6;">🔍</span>
                <span style="position: absolute; right: 15px; top: 50%; transform: translateY(-50%); color: #4285f4;">🎤</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Shelf
    st.markdown("""
    <div class="chromeos-shelf">
        <div class="chromeos-shelf-icon">🔍</div>
        <div class="chromeos-shelf-icon" style="background: rgba(66,133,244,0.2);">🌐</div>
        <div class="chromeos-shelf-icon">📧</div>
        <div class="chromeos-shelf-icon">📁</div>
        <div class="chromeos-shelf-icon">⚙️</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col_chrome1, col_chrome2, col_chrome3 = st.columns(3)
    with col_chrome1:
        if st.button("🌐 Neuer Tab", use_container_width=True):
            st.toast("🌐 Neuer Tab geöffnet")
    with col_chrome2:
        if st.button("📧 Gmail öffnen", use_container_width=True):
            st.toast("📧 Gmail wird geladen...")
    with col_chrome3:
        if st.button("📁 Dateien", use_container_width=True):
            st.toast("📁 Datei-Manager geöffnet")

elif selected_os_name == "FreeBSD":
    st.markdown("### 👹 FreeBSD Simulation")
    
    if show_hints:
        st.info("👹 **FreeBSD** ist bekannt für Stabilität und Performance. Ideal für Server und fortgeschrittene Nutzer. Probieren Sie: `pkg info`, `freebsd-version`, `sysctl`")
    
    st.markdown('<div class="freebsd-terminal">', unsafe_allow_html=True)
    
    if 'freebsd_history' not in st.session_state:
        st.session_state.freebsd_history = [
            "FreeBSD 13.2-RELEASE (GENERIC) #0: Fri Apr 21 08:02:32 UTC 2023",
            "",
            "Welcome to FreeBSD!",
            "",
            f"root@freebsd:~ #"
        ]
    
    for line in st.session_state.freebsd_history:
        if line.startswith("root@"):
            st.markdown(f"<div><span class='freebsd-prompt'>{line}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div>{line}</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    freebsd_cmd = st.text_input("FreeBSD Command:", key="freebsd_cmd", placeholder="Enter command...")
    
    if st.button("Execute", key="freebsd_exec") and freebsd_cmd:
        st.session_state.freebsd_history.append(f"root@freebsd:~ # {freebsd_cmd}")
        
        if freebsd_cmd == "freebsd-version":
            st.session_state.freebsd_history.append("13.2-RELEASE")
        elif freebsd_cmd == "pkg info":
            st.session_state.freebsd_history.extend([
                "bash-5.2.15                    The GNU Project's Bourne Again SHell",
                "nginx-1.24.0,3                 Robust and small WWW server",
                "python39-3.9.18                Interpreted object-oriented programming language",
                ""
            ])
        elif freebsd_cmd == "uname -a":
            st.session_state.freebsd_history.append("FreeBSD freebsd 13.2-RELEASE FreeBSD 13.2-RELEASE #0: Fri Apr 21 08:02:32 UTC 2023 amd64")
        else:
            st.session_state.freebsd_history.append(f"{freebsd_cmd}: Command not found.")
        
        st.session_state.freebsd_history.append("")
        st.session_state.freebsd_history.append("root@freebsd:~ #")
        st.rerun()

# === Footer ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea22, #764ba244); border-radius: 10px;'>
    <p style='margin: 0; color: #666;'>
        <strong>Betriebssystem-Simulator Pro</strong> • 
        Erstellt mit Streamlit • 
        © 2024 • 
        Alle Simulationen dienen ausschließlich Lernzwecken
    </p>
    <p style='margin: 10px 0 0 0; font-size: 12px; color: #888;'>
        Produktnamen und Logos sind Eigentum ihrer jeweiligen Inhaber
    </p>
</div>
""", unsafe_allow_html=True)
