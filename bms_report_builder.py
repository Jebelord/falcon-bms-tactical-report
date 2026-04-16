import sys
import math

try:
    print("[TACTICAL INFO] Starting system...")
    
    import re
    import os
    import glob
    from datetime import datetime
    import tkinter as tk 
    from tkinter import filedialog, messagebox, ttk 
    import threading 
    import queue 
    import time 

    # ==========================================
    # PYINSTALLER RESOURCE PATH FINDER
    # ==========================================
    def get_resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    # ==========================================
    # MILITARY ASSETS AND SILHOUETTES (SVG)
    # ==========================================
    LOGO_URL = "" 

    REPORT_LOGO_SVG = '''
    <svg viewBox="0 0 256 256" style="height: 100px; display: block; margin: 0 auto 20px auto; fill: #83a5c2; opacity: 0.9;">
        <path d="M127.7,246.78c-.03.67-1.19,1.96-1.74,1.87s-1.33-1.23-1.35-1.86l-.21-6.66-7.69-.04-.84-12.92c-.14-.13-1.45.17-1.45.52v7.1s-5.98.07-5.98.07l-.33,2.94h-23.06s-2.41-4.03-2.41-4.03l.17-10.09c.02-1.44,2.53-3.37,3.56-4.21l14.39-11.8c2.37-1.94,5.77-4.55,5.98-7.9.34-5.45.21-10.64.14-16.11h-50.45s-.77,2.41-.77,2.41c-2.6.78-5.35,1.02-8.24.34-.44-1.81-.56-3.94-.3-5.55l2.13-1.62.09-27.28-1.02-1.69c-.19-.32.83-1.16.93-1.59,1.25-5.33,1.2-11.78,2.58-10.04,1.6,2.01.25,6.33,2.35,11.43l-1.07,1.77c.05,4.25.09,8.41.46,13l49.7-37.84c.78-2.03.71-4.72.95-7,.91-8.58,3.01-16.6,5.76-24.78,4.24-12.6,6.93-24.99,8.01-38.28.71-8.74,2.11-16.87,4.92-25.23,1.55-4.59,2.37-9.28,2.37-14.09l.17-1.28c.05-.35,1.31.46,1.3.93-.23,10.08,5,19.54,6.07,28.62l2.1,17.87c.91,7.73,2.27,15.17,4.54,22.62l5.03,16.54c2.38,7.81,3.54,15.59,3.92,23.72l49.97,38.02,1.01-12.5c-1.51-1.37-1.59-3.1-.38-4.69l.79-8.67,1.63.03c-.09,6.75,3.35,11.54,1.34,13.02l-.05,25.25c0,1.39,1.12,2.68,1.82,3.85.5,1.34.29,3.66.15,5.79l-7.86-.21-.95-2.88h-50.47s.18,17.73.18,17.73c3.16,4.65,7.97,8.02,12.2,11.56l11.56,9.67.02,11.68-2.52,3.47h-22.94s-.24-2.91-.24-2.91l-5.99-.15-.19-7.68-1.25-.04-.67,12.92-7.63.21-.28,6.63Z"/>
    </svg>
    '''

    SVG_ICON_MISSIONS = '<svg class="mil-icon-svg" viewBox="0 0 24 24"><path d="M19,3H14.82C14.4,1.84 13.3,1 12,1C10.7,1 9.6,1.84 9.18,3H5C3.9,3 3,3.9 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.9 20.1,3 19,3M12,3A1,1 0 0,1 13,4A1,1 0 0,1 12,5A1,1 0 0,1 11,4A1,1 0 0,1 12,3M7,7H17V9H7V7M7,11H17V13H7V11M7,15H15V17H7V15Z"></path></svg>'
    SVG_ICON_AA = '<svg class="mil-icon-svg" viewBox="0 0 256 256"><path d="M82.59,249.6c-2.94-7.25-4.7-10.54-.36-15.61l25.13-29.36.82-13.49c-9.07,1.64-17.32,2.77-25.87,4.77-6,1.4-11.99,2.48-18.02,3.15l-10.43,1.15.07-13.3c.02-2.9,1.84-6.28,4.07-8.31l52.07-47.5.48-4.91c2.1-12.93,5.23-25.24,9.13-37.74,2.39-7.68,4.83-14.86,6.67-22.67,1.14-4.83.57-10.04.84-14.93.28-5.14.47-9.95,1.03-15,.5-4.49,2.96-8.53,3.88-12.93.58-2.77.8-6.08.97-8.94l.46-7.71c.73,5.66-.28,11.63,1.27,17.36,1.3,4.83,3.7,9.22,3.98,14.27l1.47,26.7c.38,6.87,12.5,37.52,15.97,62.51l.57,4.11,50.86,46.39c3.22,2.94,5.23,6.2,5.2,10.63l-.09,11.95-10.5-1.17c-6.06-.68-12-2.02-18.1-3.15l-25.73-4.78.88,13.42,25.83,30.29c1.49,1.75,2.47,4.19,1.82,6.39l-2.51,8.55-26.08-12.33-1.2-8.01c-.42.06-1.73.03-1.94-.35l-1.88-3.52c-.29,1.49-.69,3.48-1.59,4.08l-12.58.12-.86-6.77-1.93,1.45-1.06-3.29c-.55.52-1.36,1.39-1.81,1.25l-2.39-.75-.63,2.45c-.14.56-1.85-.75-2.25-1.21l-.68,6.86-12.12-.04c-1.36,0-1.95-2.87-1.87-4.59l-2.44,4.39-1.71-.11-.96,7.99-25.87,12.25Z"></path></svg>'
    SVG_ICON_AG = '<svg class="mil-icon-svg" viewBox="0 0 256 256"><path d="M8.52,115.41v-3.99c1.01.23,3.16-.96,4.29-.96l17.52-.1,2.46.86,34.27-.09-.14-2.2c-1.34-.25-2.35-.97-3.14-1.81l-10.32-1.13-18.98-2,.22-10.05c.13-.49,1.16-1.44,1.71-1.44l19.02-.08.29-20.35c.27,1.17.74,3.03.75,4.22l.13,14.15c1.29-1.23,2.32-1.87,3.38-1.46.94.37,1.31,1.92,1.23,3.39l8.03.03.54-3,27.17.03c1.04.83,2.08,1.38,3.63,1.76l1.17-4.8,5.02.19.34,4.13,10.59.31,5.49,3.98,3.41,3.06,11.84.08c2.24,1.36,4.08,2.13,6.57,3.27l40.82.7,7.95-.46-.02,2.89-4.98-.23-3.21-.38-40.28.11-2.66,1.36-1.22,2.86c-3.87.55-5.77,2.78-10.92,1.57-.53-.74-1.37-1.6-1.9-1.46-.44.12-.97,1-1.1,1.44l-.93,3.05,1.15,1.52c.6-.85,1.42-2.24,2.11-2.25l7.76-.06,2.31,2.19,1.96-.13,18.43.07,1.02,1.03c4.3-.61,9.3.95,14.39.76,3.55-.14,7.03-1.59,10.45.52,1.19.73,1.93.31,3.35.01,2.09-.44,5-.14,7.26-.04-.11,1.37.05,2.09.81,2.77.71.63,2.22.38,2.99.65l11.5,4.02,3.66,1.52,28.5,10.6c1.42.53,2.56.84,3.95.41.85-.27,2.19,1.89,1.68,2.63l-29.38,24.75c-1.75.62-4.91.89-6.38.11-2.04-1.09-4.77-2.13-6.42-.45,1.09,2.13.65,5.54-.06,8.09-1.42,5.1-4.54,9.01-9.41,11.58-1.18.62-2.28,1.13-3.53,1.26l-3.83.4c-1.7.18-6.03-.48-7.26-1.04l-3.53-1.6c-1.61-.73-4.6-3.69-5.46-5.36l-1.76-3.41c-.6-1.16-1.01-2.48-1.02-3.7v-3.19s-.24-5.8-.24-5.8l-5.31-.19.64,3.32c1.48,7.67-2.64,15.54-9.8,19.28-1.16.61-2.21,1.16-3.46,1.29l-3.83.41c-1.78.19-6.24-.51-7.6-1.14l-3.2-1.49c-3.96-1.84-8.31-8.91-8.31-12.48v-3.89s.26-3.36.26-3.36l-15.2.15c-.29.22-.93.79-.79,1.03l.59,1.05v2.98c.01,6.05-4.31,12.51-9.87,15.3-1.19.6-2.37,1.24-3.71,1.38l-3.5.35c-2.03.2-5.9-.4-7.6-1.16l-3.4-1.53c-4.27-1.93-9.22-10.31-8.06-15.89l-.02-3.52-3.35.38c.8,2.51.83,2.88.58,4.66l-.56,3.86c-.18,1.22-.77,2.25-1.37,3.43-2.03,3.98-4.45,6.21-8.32,8.24-1.02.54-2.14,1.08-3.23,1.19l-3.76.4c-1.85.2-6.23-.48-7.59-1.11l-3.48-1.62c-1.71-.8-4.41-3.52-5.29-5.22l-1.76-3.38c-.64-1.23-1.02-2.44-1.03-3.79l-.03-3.54.08-3.69-20.06-.26c1.06-5.7-3.23-8.1-3.35-12.11-.07-2.33-.23-4.15-.78-6.28l-7.55-28.31Z"/></svg>'
    SVG_ICON_KIA = '<svg class="mil-icon-svg" viewBox="0 0 256 256"><path d="M128.33,233.63c-3.58,1.91-7.86,1.18-10.57-1.42-2.06.44-4.51.87-6.33.58-1.43-.23-3.19-2.6-4.04-3.82l-4.83.62c-1.1.14-2.47-1.91-2.98-2.54-1.87,1.26-4.72,1.02-5.97-.21-1.62-1.59-2.36-4.52-2.12-6.62l1.57-13.45c-6.82-10.03-15.66-18.2-25.9-9.85l-13.22-24.01c8.25-11.25,14.41-27.63,5.14-37.09-.58,6.03-.49,11.08-.46,17.04-8.37-7.74-10.55-18.09-11.47-28.54-1.41-15.99-1.54-31.34,2.3-46.84,5.52-22.3,20.03-40.17,41.43-48.98s47.36-9.57,70.18-1.59,38.87,25.83,45.08,49.18c4.23,15.87,4.21,31.74,2.69,48.24-.96,10.44-3.09,20.8-11.48,28.56.04-5.95.22-11.05-.55-17.03-9.48,10.24-2.38,25.82,5.12,37.39l-13.09,23.48c-5.31-3.57-10.04-4.8-15.05-1.3-3.91,2.73-9.03,7.38-10.7,11.66l1.41,13.1c.23,2.14-.46,4.94-2.14,6.67-1.23,1.25-4.34,1.13-5.95.28-1.67,2.2-4.56,3.35-7.53,1.6-1.15,1.4-2.49,3.19-3.76,3.82-1.64.82-5.01.21-6.86-.42-2.7,2.7-6.47,3.56-9.92,1.5ZM113.09,165.75c2.93-11.67,1.49-23.6-8.65-26.27-12.02-3.16-28.35-6.34-32.11,2.54-5.27,12.42-.49,27.16,4.99,28.09,12.29,2.08,24.02.49,35.78-4.35ZM174.08,170.93c4.57-.12,7.9-2.14,9.55-6.01,5.25-12.29,1.6-28.95-9.04-28.67-8.32.22-15.89,1.15-23.72,3.51-9.67,2.92-11,15.36-7.78,26.02,9.85,4.46,19.8,5.43,31,5.15ZM128.57,183.01l1.99,12.52c2.27.88,6.83.53,9.18-.4.63-6.13-2.21-9.16-4.69-13.88-2.72-5.19-4.7-16.07-7.41-14.26-3.94,2.63-3.7,8.67-6.7,14.3-2.34,4.4-5.53,8.24-4.56,13.55,1.87,1.68,7.78,2.09,9.24.09.91-4.2-.42-7.76,2.95-11.92Z"/><path d="M113.09,165.75c-11.75,4.84-23.48,6.43-35.78,4.35-5.47-.93-10.25-15.67-4.99-28.09,3.77-8.88,20.09-5.71,32.11-2.54,10.14,2.67,11.58,14.6,8.65,26.27Z"/><path d="M174.08,170.93c-11.2.29-21.15-.69-31-5.15-3.22-10.66-1.89-23.1,7.78-26.02,7.83-2.36,15.4-3.3,23.72-3.51,10.64-.28,14.29,16.38,9.04,28.67-1.65,3.86-4.97,5.89-9.55,6.01Z"/><path d="M128.57,183.01c-3.38,4.15-2.05,7.71-2.95,11.92-1.45,2-7.37,1.59-9.24-.09-.97-5.31,2.22-9.15,4.56-13.55,3-5.63,2.76-11.67,6.7-14.3,2.7-1.81,4.68,9.07,7.41,14.26,2.48,4.72,5.32,7.75,4.69,13.88-2.34.92-6.91,1.28-9.18.4l-1.99-12.52Z"/></svg>'
    SVG_ICON_MIA = '<svg class="mil-icon-svg" viewBox="0 0 256 256"><path d="M243.66,131.48c-26.65,38.61-68.28,62.84-116.01,60.98-47.39,1.77-89.32-22.87-115.56-61.41-1.2-1.76-.94-4.79.23-6.48,26.6-38.63,68.6-63.03,116.26-61,47.55-1.62,88.61,22.71,115.22,61.13,1.16,2.18,1.26,4.75-.15,6.79ZM174.88,128c0-25.89-20.99-46.89-46.89-46.89s-46.89,20.99-46.89-46.89,20.99-46.89,46.89-46.89,46.89-20.99,46.89-46.89Z"/><path d="M174.88,128c0,25.89-20.99,46.89-46.89,46.89s-46.89-20.99-46.89-46.89,20.99-46.89,46.89-46.89,46.89,20.99,46.89,46.89ZM162.46,127.99c0-19.03-15.43-34.46-34.46-34.46s-34.46,15.43-34.46,34.46,15.43,34.46,34.46,34.46,34.46-15.43,34.46-34.46Z"/><circle cx="128" cy="127.99" r="34.46"/></svg>'
    SVG_ICON_HINT = '<svg class="search-hint-svg" viewBox="0 0 24 24"><path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11,15.41,12.59,14.44,13.73L14.71,14H15.5,20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41,11.11,16,9.5,16A6.5,6.5 0 0,1,3,9.5A6.5,6.5 0 0,1,9.5,3M9.5,5C7,5,5,7,5,9.5C5,12,7,14,9.5,14C12,14,14,12,14,9.5C14,7,12,5,9.5,5Z"></path></svg>'
    
    # ==========================================
    # EMBEDDED TACTICAL CSS
    # ==========================================
    CSS_CORE = """
    body { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', 'Courier New', monospace; margin: 0; padding: 20px; }
    .container { max-width: 1000px; margin: 0 auto; background-color: #12151c; padding: 30px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.8); border: 1px solid #222; position: relative; }

    h1, h2 { text-transform: uppercase; letter-spacing: 1.5px; margin-top: 30px; font-family: 'Consolas', monospace; }
    h1 { color: #fff; font-size: 1.8em; border-bottom: 1px dashed #333; padding-bottom: 15px; text-align: center; margin-bottom: 25px; }
    h2 { color: #83a5c2; font-size: 1.2em; margin-bottom: 20px; }

    /* Tab System CSS */
    .tab-container { display: flex; border-bottom: 2px solid #333; margin-bottom: 20px; gap: 10px; justify-content: center;}
    .tab { background: #1e1e1e; padding: 12px 25px; cursor: pointer; color: #888; font-weight: bold; text-transform: uppercase; font-family: 'Consolas', monospace; border: 1px solid #333; border-bottom: none; border-radius: 5px 5px 0 0; transition: 0.3s;}
    .tab:hover { background: #252525; color: #c9d1d9; }
    .tab.active { background: #83a5c2; color: #1a1e24; border-color: #83a5c2; }
    .tab-content { display: none; animation: fadeInStat 0.4s ease forwards;}
    .tab-content.active { display: block; }

    .hl-cyan { color: #00bcd4; font-weight: bold; }
    .hl-orange { color: #ff9800; font-weight: bold; }
    .hl-green { color: #4caf50; font-weight: bold; }
    .hl-white { color: #ffffff; font-weight: bold; }
    .hl-red { color: #ff4444; font-weight: bold; }
    .hl-light-red { color: #ff6b6b; font-weight: bold; }
    .hl-yellow { color: #f1fa8c; font-weight: bold; }
    .hl-pink { color: #ff79c6; font-weight: bold; }

    .print-btn { position: absolute; top: 30px; right: 30px; float: none; margin: 0; background-color: #333; color: #fff; border: 1px solid #555; padding: 8px 15px; cursor: pointer; font-family: 'Consolas', monospace; text-transform: uppercase; transition: 0.2s; }
    .print-btn:hover { background-color: #83a5c2; color: #000; border-color: #83a5c2; }
    @media print { .print-btn, .tab-container { display: none; } .tab-content { display: block !important; } .container { box-shadow: none; border: none; padding: 0; } }

    .campaign-info-banner { display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px; background: #1a1e24; border-top: 2px solid #83a5c2; border-bottom: 2px solid #83a5c2; padding: 15px; color: #aaa; font-weight: bold; letter-spacing: 1px; font-size: 1.1em; text-transform: uppercase; margin-bottom: 20px; }
    .campaign-info-banner span { color: #fff; }

    .global-stats { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px; margin-bottom: 30px; }
    .campaign-stats { border-bottom: 2px solid #83a5c2; background-color: #1a1e24; padding-bottom: 15px; margin-bottom: 20px; }
    
    .stat-box { background: #151515; border: 1px solid #2a2a2a; border-top: 3px solid #222; padding: 15px; border-radius: 4px; flex: 1; min-width: 130px; text-align: center; transition: all 0.2s; }
    .stat-title { color: #888; font-size: 0.85em; text-transform: uppercase; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; gap: 5px; }
    .stat-value { font-size: 1.8em; font-weight: bold; font-family: 'Consolas', monospace; }

    .pilot-summary-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;}
    .pilot-summary-card { background: #151515; border: 1px solid #333; border-left: 4px solid #83a5c2; padding: 20px; border-radius: 4px; }
    .pilot-summary-name { font-size: 1.3em; color: #fff; font-weight: bold; margin-bottom: 15px; border-bottom: 1px dashed #444; padding-bottom: 10px; display: flex; justify-content: space-between;}
    .pilot-summary-callsign { color: #888; font-size: 0.8em; font-weight: normal;}
    .summary-stat-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.95em; color: #aaa;}
    .summary-stat-val { color: #fff; font-weight: bold; font-family: 'Consolas', monospace;}

    .pilot-hours-container { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 30px; }
    .pilot-hour-box { background: #151515; border: 1px solid #333; border-left: 3px solid #83a5c2; padding: 12px 15px; border-radius: 4px; flex: 1; min-width: 140px; text-align: center; }
    .pilot-hour-name { color: #aaa; font-size: 0.8em; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .pilot-hour-time { color: #fff; font-size: 1.4em; font-weight: bold; }

    details.mission-log { margin-bottom: 20px; border: 1px solid #333; background: #151515; border-radius: 4px; }
    details.mission-log > summary { display: block; padding: 15px 20px; background: #1e1e1e; cursor: pointer; list-style: none; outline: none; border-bottom: 1px solid #333; transition: 0.3s; border-radius: 4px; }
    details.mission-log > summary:hover { background: #252525; }
    details.mission-log > summary::-webkit-details-marker { display: none; }

    .summary-header { display: flex; justify-content: space-between; align-items: center; width: 100%; }
    .mission-summary-title { font-size: 1.1em; color: #83a5c2; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .mission-summary-meta { font-size: 0.85em; color: #777; font-weight: normal; letter-spacing: 0.5px; }
    .mission-summary-meta b { color: #ccc; }
    
    details.mission-log[open] > summary .mission-summary-title::after { content: ' ▲'; font-size: 0.8em; color: #888; margin-left: 10px; }
    details.mission-log:not([open]) > summary .mission-summary-title::after { content: ' ▼'; font-size: 0.8em; color: #888; margin-left: 10px; }

    .mission-container { padding: 20px; }

    .header-info { display: flex; justify-content: space-between; font-size: 0.9em; color: #888; margin-bottom: 20px; line-height: 1.6; }
    .header-info span { color: #ddd; font-weight: bold; }

    details.briefing-log { background: #111; border-left: 3px solid #83a5c2; margin-top: 20px; margin-bottom: 25px; border-radius: 0 4px 4px 0; transition: all 0.3s ease; }
    details.briefing-log summary { cursor: pointer; padding: 15px; outline: none; list-style: none; transition: background 0.3s; }
    details.briefing-log summary::-webkit-details-marker { display: none; }
    details.briefing-log summary:hover { background: #1a1a1a; }
    .briefing-title { color: #83a5c2; font-weight: bold; font-size: 0.9em; letter-spacing: 1px; display: inline-block; text-transform: uppercase; }
    
    details.briefing-log summary .briefing-title::after { content: ' ▼ (CLICK TO READ)'; font-size: 0.85em; color: #fffae6; margin-left: 10px; font-weight: bold; letter-spacing: 0.5px; text-shadow: 0 0 5px rgba(255, 250, 230, 0.4); }
    details.events-log summary h2::after { content: ' ▼ (CLICK TO EXPAND)'; font-size: 0.6em; color: #fffae6; margin-left: 10px; vertical-align: middle; font-weight: bold; letter-spacing: 0.5px; text-shadow: 0 0 5px rgba(255, 250, 230, 0.4); }
    details.loadouts-log summary .weapon-summary-title::after { content: ' ▼ (CLICK TO EXPAND)'; font-size: 0.8em; color: #fffae6; margin-left: 10px; font-weight: bold; letter-spacing: 0.5px; text-shadow: 0 0 5px rgba(255, 250, 230, 0.4); }
    
    details.briefing-log[open] summary .briefing-title::after { content: ' ▲ (COLLAPSE)'; color: #555; text-shadow: none; font-weight: normal; }
    details.events-log[open] summary h2::after { content: ' ▲ (COLLAPSE)'; color: #555; text-shadow: none; font-weight: normal; }
    details.loadouts-log[open] summary .weapon-summary-title::after { content: ' ▲ (COLLAPSE)'; color: #555; text-shadow: none; font-weight: normal; }

    .briefing-text { font-family: 'Consolas', 'Courier New', monospace; font-size: 0.9em; white-space: pre-wrap; line-height: 1.6; padding: 15px; margin: 0 15px 15px 15px; background-color: #0d1117; color: #d1d5db; border: 1px solid #30363d; border-radius: 4px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }

    details.events-log summary { cursor: pointer; list-style: none; outline: none; margin-top: 10px; }
    details.events-log summary::-webkit-details-marker { display: none; }
    details.events-log summary h2 { display: inline-block; transition: 0.3s; user-select: none; border-bottom: none; margin-bottom: 0; }
    details.events-log summary:hover h2 { color: #fff; border-bottom-color: #888; }

    details.loadouts-log { margin-top: 15px; }
    details.loadouts-log summary { cursor: pointer; list-style: none; outline: none; background: #222; padding: 10px; border: 1px solid #333; transition: 0.3s; border-radius: 4px; }
    details.loadouts-log summary::-webkit-details-marker { display: none; }
    details.loadouts-log summary:hover { background: #2a2a2a; }
    .weapon-summary-title { display: inline-block; color: #888; font-weight: bold; font-size: 0.9em; letter-spacing: 1px; }

    .pilot-card { background: #1a1e24; border: 1px solid #333; border-radius: 4px; margin-bottom: 20px; padding: 20px; }
    .pilot-header { font-size: 1.1em; color: #fff; margin-bottom: 15px; border-bottom: 1px dashed #444; padding-bottom: 10px; text-transform: uppercase; font-weight: bold;}
    .pilot-stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin-bottom: 15px; }
    .pilot-stat-item { background: #12151c; padding: 10px; border-radius: 4px; border: 1px solid #222; text-align: center; font-size: 0.85em; color: #888; text-transform: uppercase; transition: all 0.2s; }
    .pilot-stat-value { display: block; font-size: 1.4em; margin-top: 5px; font-family: 'Consolas', monospace; font-weight: bold;}

    .loadouts-container { padding-top: 15px; }
    .weapon-box { background: #12151c; border: 1px solid #333; border-radius: 4px; padding: 12px; margin-bottom: 10px; border-left: 3px solid #555; }
    .weapon-title { font-weight: bold; color: #ddd; margin-bottom: 8px; font-size: 0.9em; text-transform: uppercase; border-bottom: 1px dashed #333; padding-bottom: 5px; }
    .weapon-data-row { display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.85em; color: #888; margin-bottom: 8px; }
    .weapon-events { list-style-type: none; padding-left: 0; margin: 0; font-family: 'Consolas', monospace; font-size: 0.85em; color: #aaa; }
    .weapon-events li { margin-bottom: 4px; border-left: 2px solid #83a5c2; padding-left: 10px; }

    table { width: 100%; border-collapse: collapse; margin-top: 15px; font-family: 'Consolas', monospace; font-size: 0.9em; background: #161b22; border-radius: 4px; overflow: hidden; border: 1px solid #333; }
    th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #222; }
    th { background-color: #1a1e24; color: #888; text-transform: uppercase; border-bottom: 2px solid #333; }
    tr:hover { background-color: #1c2128; }

    .mil-icon-svg { height: 1.5em; fill: currentColor; vertical-align: middle; margin-right: 8px; opacity: 0.8; }
    .stat-box .stat-title svg { height: 1.2em; } 
    .search-hint-svg { height: 0.9em; fill: currentColor; margin-left: 5px; vertical-align: middle; opacity: 0.7; }

    .clickable-box { cursor: pointer; position: relative; transition: all 0.2s; }
    .clickable-box:hover { background: #222; transform: translateY(-3px); border-color: #fffae6 !important; box-shadow: 0 5px 15px rgba(255, 250, 230, 0.2); }
    .clickable-box:hover * { color: #fffae6 !important; }
    
    @keyframes tacticalPulse { 0% { box-shadow: 0 0 0 0 rgba(255, 250, 230, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(255, 250, 230, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 250, 230, 0); } }
    .clickable-box:active { animation: tacticalPulse 0.4s linear; }
    
    .clickable-kia { cursor: pointer; text-decoration: underline; text-decoration-style: dashed; transition: 0.2s;}
    .clickable-kia:hover { background: #331111; color: #ff6b6b !important;}

    @keyframes fadeInStat { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }
    .stat-box { opacity: 0; animation: fadeInStat 0.6s ease forwards; }

    @keyframes modalIn { 0% { opacity: 0; transform: scale(0.9) translateY(-30px); } 100% { opacity: 1; transform: scale(1) translateY(0); } }
    @keyframes modalOut { 0% { opacity: 1; transform: scale(1) translateY(0); } 100% { opacity: 0; transform: scale(0.9) translateY(30px); } }

    dialog.tactical-modal { background: #1a1e24; border: 1px solid #83a5c2; color: #c5c5c5; border-radius: 5px; padding: 25px; width: 90%; max-width: 450px; box-shadow: 0 0 30px rgba(0,0,0,0.9); margin: auto; font-family: 'Consolas', monospace; }
    dialog.tactical-modal::backdrop { background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(4px); }
    dialog.tactical-modal[open] { animation: modalIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    dialog.tactical-modal.closing { animation: modalOut 0.25s ease-in forwards; }

    .modal-header { font-size: 1.2em; color: #83a5c2; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
    .modal-header svg { height: 1.1em; }
    .close-btn { background: none; border: none; color: #aaa; cursor: pointer; font-size: 1.5em; line-height: 1; outline: none; transition: 0.2s; }
    .close-btn:hover { color: #fff; transform: scale(1.2); }
    .target-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #2a2a2a; font-size: 0.95em; }
    .target-row:last-child { border-bottom: none; }
    .target-name { color: #ddd; text-transform: uppercase; }
    
    .delete-btn { background: transparent; color: #555; border: 1px dashed #333; padding: 4px 10px; border-radius: 3px; cursor: pointer; font-family: 'Consolas', monospace; font-weight: bold; margin-left: 15px; font-size: 0.8em; transition: 0.2s; }
    .delete-btn:hover { color: #ff6b6b; border: 1px solid #ff6b6b; background: #1a1111; box-shadow: 0 0 8px rgba(255, 107, 107, 0.2); }

    /* REFINED PACKAGE STYLING */
    details.package-log { margin-bottom: 30px; border-left: 4px solid #5c7c99; padding-left: 10px; }
    details.package-log > summary { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: #161b22; cursor: pointer; list-style: none; outline: none; border: 1px solid #222; border-radius: 3px; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.5); }
    details.package-log > summary:hover { background: #1c2128; border-color: #5c7c99; }
    details.package-log > summary::-webkit-details-marker { display: none; }
    .package-summary-title { font-size: 1.1em; color: #83a5c2; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }
    details.package-log[open] > summary .package-summary-title::after { content: ' ▲'; font-size: 0.7em; color: #555; margin-left: 10px; }
    details.package-log:not([open]) > summary .package-summary-title::after { content: ' ▼'; font-size: 0.7em; color: #555; margin-left: 10px; }
    .package-content { padding-top: 15px; border-left: 2px dashed #222; margin-left: 10px; padding-left: 15px; }

    @media (max-width: 768px) {
        body { padding: 5px; } .container { padding: 15px; }
        .campaign-info-banner { flex-direction: column; text-align: center; font-size: 1em; }
        .global-stats { display: flex; flex-wrap: wrap; gap: 8px; border: none; background: transparent; padding: 0; }
        .stat-box { flex: 1 1 45%; border: 1px solid #2a2a2a !important; background: #151515; border-radius: 5px; padding: 12px 0; margin: 0; opacity: 1; animation: none; } 
        .campaign-stats { border: none; margin-bottom: 20px; }
        .summary-header { flex-direction: column; align-items: flex-start; gap: 5px; }
        .mission-summary-meta { line-height: 1.5; } .hide-mobile { display: none; } 
        .header-info { display: flex; flex-direction: column; gap: 10px; }
        .weapon-data-row { flex-wrap: wrap; gap: 5px; }
        details.events-log table { display: block; overflow-x: auto; white-space: nowrap; }
        .print-btn { position: relative; top: 0; right: 0; width: 100%; margin-bottom: 20px; }
    }
    """

    # ==========================================
    # TACTICAL PROCESSING ENGINE
    # ==========================================
    def parse_time(t_str):
        try:
            h, m, s = map(int, t_str.split(':'))
            return h * 3600 + m * 60 + s
        except:
            return 0

    def format_time(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        return f"{h}h {m}m"

    def extract_bms_date(text):
        match = re.search(r'RECORD BEGIN TIMESTAMP.*?(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})\s+(\d{1,2}:\d{2}:\d{2})', text, re.IGNORECASE)
        if match:
            date_str = f"{match.group(1).replace('-', '/')} {match.group(2)}"
            formats = ["%m/%d/%Y %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"]
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    pass
        return datetime.min

    def process_report(mission_folder, date_start_str="", date_end_str="", user_theater="Auto-Detect", user_campaign="Auto-Detect", user_network="All Missions", output_file="Final_Campaign_Report.html"):
        
        # --- BULLETPROOF OMNIVOROUS AUTO-ARCHIVER LOGIC ---
        master_briefing_path = os.path.join(mission_folder, 'master_briefings.txt')
        master_briefing_map = {}
        
        if os.path.exists(master_briefing_path):
            with open(master_briefing_path, 'r', encoding='utf-8', errors='ignore') as mf:
                content = mf.read()
                for bb in re.split(r'(?=BRIEFING RECORD|Flight Unique Id:)', content, flags=re.IGNORECASE):
                    if not bb.strip(): continue
                    m_id = re.search(r'Flight Unique Id:\s*([^\n\r]+)', bb, re.IGNORECASE)
                    if m_id: 
                        master_briefing_map[m_id.group(1).strip()] = bb 
                    else:
                        m_call = re.search(r'Mission Overview:\s*([A-Za-z0-9]+)', bb, re.IGNORECASE)
                        if m_call: master_briefing_map[m_call.group(1).strip()] = bb 

        for file_name in os.listdir(mission_folder):
            if file_name.lower().endswith('.txt') and "master" not in file_name.lower():
                current_path = os.path.join(mission_folder, file_name)
                
                curr_content = ""
                encodings_to_try = ['utf-8', 'utf-16', 'latin-1']
                for enc in encodings_to_try:
                    try:
                        with open(current_path, 'r', encoding=enc) as cf:
                            curr_content = cf.read().replace('\x00', '')
                        if "BRIEFING" in curr_content.upper() or "Mission Overview" in curr_content: 
                            break
                    except Exception:
                        continue
                
                is_briefing_record = "BRIEFING RECORD" in curr_content.upper()
                has_mission_overview = "Mission Overview:" in curr_content
                is_pure_briefing = "FLIGHT EVENTS" not in curr_content.upper()
                is_literal_file = ("briefing" in file_name.lower() and "debrief" not in file_name.lower())

                if (is_briefing_record or has_mission_overview or is_literal_file) and is_pure_briefing:
                    curr_id = None
                    id_match = re.search(r'Flight Unique Id:\s*([^\n\r]+)', curr_content, re.IGNORECASE)
                    if id_match:
                        curr_id = id_match.group(1).strip()
                    else:
                        alt_match = re.search(r'Mission Overview:\s*([A-Za-z0-9]+)', curr_content, re.IGNORECASE)
                        if alt_match: curr_id = alt_match.group(1).strip()

                    if curr_id and curr_id not in master_briefing_map:
                        try:
                            with open(master_briefing_path, 'a', encoding='utf-8') as mf:
                                mf.write("\n\n" + "="*50 + "\n\n")
                                mf.write(curr_content)
                            master_briefing_map[curr_id] = curr_content 
                        except Exception:
                            pass
        # ---------------------------------------------------------

        txt_files = glob.glob(os.path.join(mission_folder, '*.txt'))
        if not txt_files:
            return False, f"No .txt files found in:\n{mission_folder}"

        cutoff_start = None
        if date_start_str.strip():
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
                try:
                    cutoff_start = datetime.strptime(date_start_str.strip(), fmt)
                    break
                except ValueError: continue

        cutoff_end = None
        if date_end_str.strip():
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
                try:
                    cutoff_end = datetime.strptime(date_end_str.strip() + " 23:59:59", fmt + " %H:%M:%S")
                    break
                except ValueError: continue

        briefing_dict = {}
        master_briefing = ""
        total_blocks = []
        
        for file in txt_files:
            base_name = os.path.basename(file).lower()
            
            if base_name in ["master_briefings.txt", "campaign_briefings.txt"]:
                continue
                
            try:
                with open(file, 'r', encoding='latin-1', errors='ignore') as f:
                    full_content = f.read().replace('\x00', '')
            except:
                continue
            
            if "briefing" in base_name and "debrief" not in base_name:
                if base_name == "briefing.txt":
                    master_briefing = full_content
                else:
                    key = base_name.replace("briefing", "").replace(".txt", "").strip(" _-")
                    briefing_dict[key] = full_content
                continue 
            
            file_blocks = re.split(r'(?=RECORD BEGIN TIMESTAMP)', full_content, flags=re.IGNORECASE)
            for b in file_blocks:
                if "RECORD BEGIN TIMESTAMP" in b.upper():
                    total_blocks.append((base_name, b))

        missions_data = []
        campaign_pilot_hours = {}
        global_pilot_stats = {} 
        global_aa_targets = {}
        global_ag_targets = {}
        all_modals_html = "" 
        
        global_campaign_name = ""
        global_theater = ""
        if total_blocks:
            camp_match = re.search(r'(?:Campaign|Campaign Name|TE Name)\s*:\s*([^\n\r]+)', total_blocks[0][1], re.IGNORECASE)
            if camp_match: global_campaign_name = camp_match.group(1).strip()
            thea_match = re.search(r'(?:Theater|Theatre)\s*:\s*([^\n\r]+)', total_blocks[0][1], re.IGNORECASE)
            if thea_match: global_theater = thea_match.group(1).strip()

        for idx, (base_name, block) in enumerate(total_blocks):
            
            is_networked = bool(re.search(r'\bNetworked\b', block, re.IGNORECASE))
            is_local = bool(re.search(r'\bLocal\b', block, re.IGNORECASE))
            
            if user_network == "Multiplayer (Networked)" and not is_networked: continue
            if user_network == "Single Player (Local)" and not is_local: continue

            date_obj = extract_bms_date(block)
            
            if date_obj != datetime.min:
                if cutoff_start and date_obj < cutoff_start: continue
                if cutoff_end and date_obj > cutoff_end: continue

            parts = re.split(r'FLIGHT\s*EVENTS|PILOT\s*SLOT', block, maxsplit=1, flags=re.IGNORECASE)
            top_section = parts[0] if parts else block

            mission_type_match = re.search(r'Mission Type:\s*([^\n]+)', top_section, re.IGNORECASE)
            flight_id_match = re.search(r'Flight Unique Id:\s*([^\n]+)', top_section, re.IGNORECASE)
            ac_type_match = re.search(r'Ac type:\s*([^\n]+)', top_section, re.IGNORECASE)
            country_match = re.search(r'Country:\s*([^\n]+)', top_section, re.IGNORECASE)

            # --- BULLETPROOF PACKAGE PARSER ---
            pkg_match = re.search(r'Package\s*(?:#|Number)?\s*:\s*(\d+)', top_section, re.IGNORECASE)
            if not pkg_match:
                pkg_match = re.search(r'Package\s*(?:#|Number)?\s*:\s*(\d+)', block, re.IGNORECASE)
            package_id = pkg_match.group(1).strip() if pkg_match else "INDIVIDUAL / UNKNOWN"

            mission_type = mission_type_match.group(1).strip() if mission_type_match else "UNKNOWN"
            
            # --- TRAINING MISSION FILTER ---
            if "training" in mission_type.lower():
                continue

            flight_id = flight_id_match.group(1).strip() if flight_id_match else "UNKNOWN FLIGHT"
            ac_type = ac_type_match.group(1).strip() if ac_type_match else "UNKNOWN"
            country = country_match.group(1).strip() if country_match else "UNKNOWN"

            fired = sum(map(int, re.findall(r'Fired\s+(\d+)', block)))
            m_aa_kills = sum(map(int, re.findall(r'AA Kills\s*(\d+)', block)))
            m_ag_kills = sum(map(int, re.findall(r'AG Kills\s*(\d+)', block)))
            
            m_damaged = len(re.findall(r'damaged', block, re.IGNORECASE))
            m_kia = 0; m_mia = 0  

            events_match = re.search(r'FLIGHT\s*EVENTS(.*?)(?:-{5,}|\Z)', block, re.DOTALL | re.IGNORECASE)
            events_html = ""
            events_list = [] 
            
            mission_aa_targets = {}
            mission_ag_targets = {}

            if events_match:
                for line in events_match.group(1).strip().split('\n'):
                    line = line.strip()
                    if not line: continue
                    time_match = re.search(r'(\d{2}:\d{2}:\d{2})', line)
                    if not time_match: continue 
                    
                    time_str = time_match.group(1)
                    desc_clean = re.sub(r'(?i)^Event\s+', '', line)
                    desc_clean = re.sub(rf'(?i)\s*at\s*{time_str}', '', desc_clean)
                    desc_clean = desc_clean.replace(time_str, '').strip()
                    events_list.append((desc_clean, time_str))

                    match_aa = re.search(r'^(.*?)\s+downed by', desc_clean, re.IGNORECASE)
                    if match_aa: 
                        tgt = match_aa.group(1).strip()
                        global_aa_targets[tgt] = global_aa_targets.get(tgt, 0) + 1
                        mission_aa_targets[tgt] = mission_aa_targets.get(tgt, 0) + 1

                    match_ag = re.search(r'^(.*?)\s+destroyed by', desc_clean, re.IGNORECASE)
                    if match_ag: 
                        tgt = match_ag.group(1).strip()
                        global_ag_targets[tgt] = global_ag_targets.get(tgt, 0) + 1
                        mission_ag_targets[tgt] = mission_ag_targets.get(tgt, 0) + 1

                    desc_colored = re.sub(r'(?i)(downed)', r'<span class="hl-red">\1</span>', desc_clean) 
                    desc_colored = re.sub(r'(?i)(destroyed)', r'<span class="hl-light-red">\1</span>', desc_colored) 
                    desc_colored = re.sub(r'(?i)([A-Za-z0-9-\(\)\s]+ launched)', r'<span class="hl-yellow">\1</span>', desc_colored)
                    events_html += f"<tr><td>{time_str}</td><td>{desc_colored}</td></tr>\n"
            else:
                events_html = "<tr><td colspan='2'>No events logged for this flight.</td></tr>"

            m_aa_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(mission_aa_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No A-A kills recorded for this flight.</div>"
            m_ag_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(mission_ag_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No Surface kills recorded for this flight.</div>"
            
            all_modals_html += f"""
            <dialog id="modal-aa-m{idx}" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AA} FLIGHT A-A BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-aa-m{idx}')">×</button></div><div class="modal-body">{m_aa_rows}</div></dialog>
            <dialog id="modal-ag-m{idx}" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AG} FLIGHT A-G BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-ag-m{idx}')">×</button></div><div class="modal-body">{m_ag_rows}</div></dialog>
            """

            pilots_html = ""
            callsign_to_player = {}
            mission_kia_mia_callsigns = [] 
            pilot_parts = re.split(r'-{5,}', block)
            
            for p_idx, p in enumerate(pilot_parts):
                if "PILOT SLOT" not in p.upper(): continue

                slot = re.search(r'PILOT SLOT\s*(\d+)', p).group(1) if re.search(r'PILOT SLOT\s*(\d+)', p) else "?"
                callsign = re.search(r'Callsign:\s*(.*)', p).group(1).strip() if re.search(r'Callsign:\s*(.*)', p) else "?"
                player = re.search(r'Human Player:\s*(.*)', p).group(1).strip() if re.search(r'Human Player:\s*(.*)', p) else "?"
                
                if player and player != "?":
                    player = re.sub(r'^(?:Rec\.|2Lt\.|1Lt\.|Capt\.|Maj\.|LtC\.|Col\.|BG\.|MG\.|LG\.|Gen\.)\s+', '', player, flags=re.IGNORECASE).strip()
                
                if player and player != "?":
                    callsign_to_player[callsign] = player
                    if player not in global_pilot_stats:
                        global_pilot_stats[player] = {'callsign': callsign, 'aa': 0, 'ag': 0, 'kia': 0, 'mia': 0, 'missions': 0}
                    global_pilot_stats[player]['missions'] += 1

                aa_k = re.search(r'AA Kills\s*(\d+)', p).group(1) if re.search(r'AA Kills\s*(\d+)', p) else "0"
                ag_k = re.search(r'AG Kills\s*(\d+)', p).group(1) if re.search(r'AG Kills\s*(\d+)', p) else "0"
                shoot = re.search(r'Shoot At\s*(\d+)', p).group(1) if re.search(r'Shoot At\s*(\d+)', p) else "0"

                p_status_match = re.search(r'Pilot status\s*-\s*([^\n]+)', p)
                p_status = p_status_match.group(1).strip() if p_status_match else "UNKNOWN"
                p_color_hex = "#4caf50" if p_status.upper() == "OK" else "#cc3333" 

                is_kia_mia = False
                if p_status.upper() == "KIA": 
                    m_kia += 1
                    is_kia_mia = True
                    if player and player != "?": global_pilot_stats[player]['kia'] += 1
                elif p_status.upper() == "MIA": 
                    m_mia += 1
                    is_kia_mia = True
                    if player and player != "?": global_pilot_stats[player]['mia'] += 1
                
                if is_kia_mia and callsign != "?":
                    mission_kia_mia_callsigns.append((callsign, p_status.upper()))

                if player and player != "?":
                    global_pilot_stats[player]['aa'] += int(aa_k)
                    global_pilot_stats[player]['ag'] += int(ag_k)

                ac_status_match = re.search(r'Aircraft status\s*-\s*([^\n]+)', p)
                ac_status = ac_status_match.group(1).strip() if ac_status_match else "UNKNOWN"
                ac_color_hex = "#4caf50" if ac_status.upper() == "OK" else "#cc3333" 

                pilot_aa_targets = {}
                pilot_ag_targets = {}
                for desc, t_str in events_list:
                    if callsign and callsign != "?":
                        match_aa = re.search(r'^(.*?)\s+downed by\s+(.*)', desc, re.IGNORECASE)
                        if match_aa:
                            tgt = match_aa.group(1).strip()
                            shooter = match_aa.group(2).strip()
                            if re.search(rf'\b{re.escape(callsign)}\b', shooter, re.IGNORECASE):
                                pilot_aa_targets[tgt] = pilot_aa_targets.get(tgt, 0) + 1
                        
                        match_ag = re.search(r'^(.*?)\s+destroyed by\s+(.*)', desc, re.IGNORECASE)
                        if match_ag:
                            tgt = match_ag.group(1).strip()
                            shooter = match_ag.group(2).strip()
                            if re.search(rf'\b{re.escape(callsign)}\b', shooter, re.IGNORECASE):
                                pilot_ag_targets[tgt] = pilot_ag_targets.get(tgt, 0) + 1

                p_aa_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(pilot_aa_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No A-A kills recorded for this pilot.</div>"
                p_ag_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(pilot_ag_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No Surface kills recorded for this pilot.</div>"
                
                all_modals_html += f"""
                <dialog id="modal-aa-m{idx}-p{p_idx}" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AA} PILOT A-A BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-aa-m{idx}-p{p_idx}')">×</button></div><div class="modal-body">{p_aa_rows}</div></dialog>
                <dialog id="modal-ag-m{idx}-p{p_idx}" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AG} PILOT A-G BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-ag-m{idx}-p{p_idx}')">×</button></div><div class="modal-body">{p_ag_rows}</div></dialog>
                """

                pilots_html += f'''
                <div class="pilot-card">
                    <div class="pilot-header">Slot {slot}: {player} (Callsign: {callsign})</div>
                    <div class="pilot-stats-grid">
                        <div class="pilot-stat-item">Status<span class="pilot-stat-value" style="color: {p_color_hex};">{p_status}</span></div>
                        <div class="pilot-stat-item">Aircraft<span class="pilot-stat-value" style="color: {ac_color_hex};">{ac_status}</span></div>
                        <div class="pilot-stat-item clickable-box" onclick="document.getElementById('modal-aa-m{idx}-p{p_idx}').showModal()">AA Kills {SVG_ICON_HINT}<span class="pilot-stat-value hl-white">{aa_k}</span></div>
                        <div class="pilot-stat-item clickable-box" onclick="document.getElementById('modal-ag-m{idx}-p{p_idx}').showModal()">AG Kills {SVG_ICON_HINT}<span class="pilot-stat-value hl-white">{ag_k}</span></div>
                        <div class="pilot-stat-item">Shoot At<span class="pilot-stat-value hl-white">{shoot}</span></div>
                    </div>
                    <details class="loadouts-log">
                        <summary><div class="weapon-summary-title">WEAPON LOADOUTS & EVENTS</div></summary>
                        <div class="loadouts-container">'''

                pattern = r'LOADOUT (\d+):\s*(.*?)\s*\nStarting Load\s*(\d+)\s*\nFired\s*(\d+)\s*\nMissed\s*(\d+)\s*\nHit\s*(\d+)\s*(.*?)(?=LOADOUT|\Z)'
                loadouts = re.finditer(pattern, p, re.DOTALL)
                
                for lo in loadouts:
                    l_num, l_name, l_start, l_fired, l_missed, l_hit, l_events = lo.groups()
                    ev_lines = ""
                    for el in l_events.strip().split('\n'):
                        if not el.strip() or 'Event' not in el: continue
                        t_match = re.search(r'at (\d{2}:\d{2}:\d{2})', el)
                        time_str = t_match.group(1) if t_match else "00:00:00"
                        clean_el = el.replace('Event ', '')
                        if '@72hit' in clean_el: action_str = f"Hit {clean_el.split('@72hit')[1].strip()}"
                        elif '@72miss' in clean_el: action_str = "Miss"
                        else: action_str = clean_el.split(' at ')[0] if ' at ' in clean_el else clean_el
                        action_str = re.sub(r'-\s*destroyed', r'(<span class="hl-light-red">destroyed</span>)', action_str)
                        action_str = re.sub(r'-\s*damaged', r'(<span class="hl-pink">damaged</span>)', action_str)
                        if 'MiG' in action_str: action_str = action_str.replace('hl-light-red', 'hl-red')
                        ev_lines += f"<li>{time_str} - {action_str}</li>\n"
                    
                    ul_tag = f'<ul class="weapon-events">\n{ev_lines}</ul>' if ev_lines else ""
                    if int(l_start) > 0 or int(l_fired) > 0 or ev_lines:
                        pilots_html += f'''
                            <div class="weapon-box">
                                <div class="weapon-title">LOADOUT {l_num}: {l_name.strip()}</div>
                                <div class="weapon-data-row">
                                    <span>Load: <span class="hl-white">{l_start}</span></span>
                                    <span>Fired: <span class="hl-white">{l_fired}</span></span>
                                    <span>Hit: <span class="hl-white">{l_hit}</span></span>
                                    <span>Missed: <span class="hl-white">{l_missed}</span></span>
                                </div>
                                {ul_tag}
                            </div>'''
                pilots_html += '''</div></details></div>\n''' 

            for callsign, player in callsign_to_player.items():
                pilot_times = []
                for desc, t_str in events_list:
                    if callsign in desc: pilot_times.append(parse_time(t_str))
                if pilot_times:
                    duration = max(pilot_times) - min(pilot_times)
                    if duration < 0: duration += 86400 
                    if player not in campaign_pilot_hours: campaign_pilot_hours[player] = 0
                    campaign_pilot_hours[player] += duration

            raw_briefing = block 
            if "BRIEFING RECORD" not in block.upper():
                if flight_id and flight_id in master_briefing_map:
                    raw_briefing = master_briefing_map[flight_id]
                else:
                    key_debrief = base_name.replace("debrief", "").replace(".txt", "").strip(" _-")
                    if key_debrief in briefing_dict and briefing_dict[key_debrief]:
                        raw_briefing = briefing_dict[key_debrief]
                    elif master_briefing:
                        raw_briefing = master_briefing
                    
            # --- PACKAGE PARSER FALLBACK IN RAW BRIEFING ---
            if package_id == "INDIVIDUAL / UNKNOWN" and raw_briefing:
                pkg_match_fallback = re.search(r'Package\s*(?:#|Number)?\s*:\s*(\d+)', raw_briefing, re.IGNORECASE)
                if pkg_match_fallback:
                    package_id = pkg_match_fallback.group(1).strip()

            match_slice = re.search(r'(BRIEFING RECORD.*?)(?=Threat Analysis)', raw_briefing, re.DOTALL | re.IGNORECASE)
            if match_slice:
                m_briefing = match_slice.group(1).strip()
            else:
                match_slice_alt = re.search(r'(BRIEFING RECORD.*?)(?=FLIGHT\s*EVENTS|PILOT\s*SLOT|\Z)', raw_briefing, re.DOTALL | re.IGNORECASE)
                if match_slice_alt: m_briefing = match_slice_alt.group(1).strip()
                else: m_briefing = raw_briefing 
            
            formatted_briefing = m_briefing
            formatted_briefing = re.sub(r'(?i)(Package\s+\d+)', r'<span class="hl-cyan">\1</span>', formatted_briefing)
            formatted_briefing = re.sub(r'(?im)^([ \t]*)(Target[s]?|Objective[s]?|Mission):', r'\1<span class="hl-orange">\2:</span>', formatted_briefing)
            formatted_briefing = re.sub(r'(?im)^([ \t]*)(Threat[s]?|Air Threats|Surface Threats):', r'\1<span class="hl-red">\2:</span>', formatted_briefing)
            if flight_id and flight_id != "UNKNOWN FLIGHT":
                safe_flight = re.escape(flight_id)
                formatted_briefing = re.sub(rf'(?i)\b({safe_flight})\b', r'<span class="hl-yellow">\1</span>', formatted_briefing)
            
            for callsign in callsign_to_player.keys():
                if callsign and callsign != "?":
                    safe_call = re.escape(callsign)
                    kia_mia_status = next((status for cs, status in mission_kia_mia_callsigns if cs == callsign), None)
                    
                    if kia_mia_status:
                        modal_id = f"modal-kia-m{idx}-{callsign.replace(' ', '')}"
                        formatted_briefing = re.sub(rf'(?i)\b({safe_call})\b', rf'<span class="hl-red clickable-kia" onclick="document.getElementById(\'{modal_id}\').showModal()">\1</span>', formatted_briefing)
                        icon = SVG_ICON_KIA if kia_mia_status == "KIA" else SVG_ICON_MIA
                        all_modals_html += f"""
                        <dialog id="{modal_id}" class="tactical-modal">
                            <div class="modal-header"><span class="hl-red">{icon} PILOT {kia_mia_status} STATUS</span><button class="close-btn" onclick="closeTacticalModal('{modal_id}')">×</button></div>
                            <div class="modal-body" style="text-align: center; padding: 20px;">
                                <div style="font-size: 1.2em; color: #fff; margin-bottom: 10px;">Callsign: <b>{callsign}</b></div>
                                <div style="color: #888;">This pilot was confirmed <span class="hl-red">{kia_mia_status}</span> during this flight operation.</div>
                                <div style="color: #666; font-size: 0.8em; margin-top: 15px;">Check the Flight Events Log below for exact timestamps of ejection or destruction.</div>
                            </div>
                        </dialog>
                        """
                    else:
                        formatted_briefing = re.sub(rf'(?i)\b({safe_call})\b', r'<span class="hl-green">\1</span>', formatted_briefing)

            date_str_formatted = date_obj.strftime("%Y/%m/%d %H:%M:%S") if date_obj != datetime.min else "UNKNOWN DATE"
            just_date_str = date_obj.strftime("%Y/%m/%d") if date_obj != datetime.min else "UNKNOWN DATE"
            
            mission_html_block = f"""
            <details class="mission-log" id="mission-{idx}">
                <summary>
                    <div class="summary-header">
                        <div class="mission-summary-title">FLIGHT ID: <span style="color: #baddf9;">{flight_id}</span></div>
                        <div class="mission-summary-meta" style="display: flex; align-items: center;">
                            <span>START: <b>{date_str_formatted}</b> &nbsp;|&nbsp; 
                            A/C: <b>{ac_type}</b> <span class="hide-mobile">&nbsp;|&nbsp; TYPE: <b>{mission_type}</b></span></span>
                            <button class="delete-btn" onclick="removeMission(event, 'mission-{idx}', {m_aa_kills}, {m_ag_kills}, {m_kia}, {m_mia})">X SCRUB</button>
                        </div>
                    </div>
                </summary>
                
                <div class="mission-container">
                    <div class="header-info">
                        <div>CLASSIFICATION: <span>UNCLASSIFIED / TACTICAL</span><br>RECORD START: <span>{date_str_formatted}</span><br>MISSION TYPE: <span>{mission_type}</span></div>
                        <div>FLIGHT ID: <span>{flight_id}</span><br>AIRCRAFT: <span>{ac_type}</span><br>COALITION: <span>{country}</span></div>
                    </div>

                    <details class="briefing-log">
                        <summary><div class="briefing-title">MISSION BRIEFING / SUMMARY</div></summary>
                        <div class="briefing-text">{formatted_briefing}</div>
                    </details>

                    <div class="global-stats">
                        <div class="stat-box"><div class="stat-title">WPN Fired</div><div class="stat-value hl-white">{fired}</div></div>
                        <div class="stat-box clickable-box" onclick="document.getElementById('modal-aa-m{idx}').showModal()"><div class="stat-title">A-A Kills {SVG_ICON_HINT}</div><div class="stat-value hl-white">{m_aa_kills}</div></div>
                        <div class="stat-box clickable-box" onclick="document.getElementById('modal-ag-m{idx}').showModal()"><div class="stat-title">A-G Kills {SVG_ICON_HINT}</div><div class="stat-value hl-white">{m_ag_kills}</div></div>
                        <div class="stat-box"><div class="stat-title">KIA</div><div class="stat-value hl-white">{m_kia}</div></div>
                        <div class="stat-box"><div class="stat-title">MIA</div><div class="stat-value hl-white">{m_mia}</div></div>
                    </div>
                    
                    <h2>Pilot Dossiers</h2>
                    {pilots_html}

                    <details class="events-log">
                        <summary><h2>Flight Events Log</h2></summary>
                        <table>
                            <thead><tr><th style="width: 100px;">Time</th><th>Event Description</th></tr></thead>
                            <tbody>{events_html}</tbody>
                        </table>
                    </details>
                </div>
            </details>
            """

            missions_data.append({
                'date_obj': date_obj, 
                'html': mission_html_block, 
                'aa': m_aa_kills, 
                'ag': m_ag_kills, 
                'dam': m_damaged, 
                'kia': m_kia, 
                'mia': m_mia, 
                'package_id': package_id, 
                'just_date': just_date_str,
                'footprint': m_briefing 
            })

        if not missions_data: 
            msg = "No valid flight reports found."
            if date_start_str or date_end_str or user_network != "All Missions": 
                msg = f"No flights found matching the specified filters."
            return False, msg

        # --- RESTORED GLOBAL STATS CALCULATIONS ---
        total_missions = len(missions_data)
        camp_aa_kills = sum(m['aa'] for m in missions_data)
        camp_ag_kills = sum(m['ag'] for m in missions_data)
        camp_kia = sum(m['kia'] for m in missions_data)
        camp_mia = sum(m['mia'] for m in missions_data)

        # --- THE BRIEFING-FOOTPRINT PACKAGE GROUPER ENGINE ---
        grouped_packages = {}
        for m in missions_data:
            pid = m['package_id']
            # We group by Package ID and the exact text of the briefing footprint.
            footprint_hash = hash(m['footprint']) if m['footprint'] else hash(m['flight_id']) 
            
            group_key = (pid, footprint_hash)
            
            if group_key not in grouped_packages:
                grouped_packages[group_key] = []
            grouped_packages[group_key].append(m)

        # Build list for sorting
        package_list = []
        for (pid, f_hash), flights in grouped_packages.items():
            flights.sort(key=lambda x: x['date_obj']) # Sort flights chronologically inside package
            package_list.append((pid, flights))

        # Sort the actual package blocks so the newest operations are at the top
        package_list.sort(key=lambda x: x[1][0]['date_obj'], reverse=True)

        final_missions_html = ""
        for pid, flights in package_list:
            first_flight = flights[0]
            pdate = first_flight['just_date']
            first_flight_time = first_flight['date_obj'].strftime("%H:%M") if first_flight['date_obj'] != datetime.min else "00:00"
            
            if pid != "INDIVIDUAL / UNKNOWN":
                pkg_title = f"PACKAGE <span style='color: #baddf9;'>{pid}</span> <span style='font-size: 0.75em; color: #777; margin-left: 20px; font-weight: normal; letter-spacing: 1px;'>DATE: {pdate} @ {first_flight_time}</span>"
            else:
                pkg_title = f"INDEPENDENT FLIGHTS <span style='font-size: 0.75em; color: #777; margin-left: 20px; font-weight: normal; letter-spacing: 1px;'>DATE: {pdate} @ {first_flight_time}</span>"
            
            pkg_html = f"""
            <details class="package-log">
                <summary>
                    <div class="package-summary-title">{pkg_title}</div>
                    <div class="mission-summary-meta" style="color: #aaa;">Contains <b>{len(flights)}</b> Flight(s)</div>
                </summary>
                <div class="package-content">
            """
            
            # Sort flights newest to oldest inside the package drawer
            flights.sort(key=lambda x: x['date_obj'], reverse=True)
            for f in flights:
                pkg_html += f['html']
            
            pkg_html += "</div></details>"
            final_missions_html += pkg_html

        pilot_hours_html = ""
        if campaign_pilot_hours:
            pilot_hours_html += "<h2 style='margin-top: 30px; font-size: 1em; color: #888;'>FLIGHT HOURS BY PILOT</h2><div class='pilot-hours-container'>"
            for player, seconds in sorted(campaign_pilot_hours.items(), key=lambda item: item[1], reverse=True):
                pilot_hours_html += f"<div class='pilot-hour-box'><div class='pilot-hour-name'>{player}</div><div class='pilot-hour-time'>{format_time(seconds)}</div></div>"
            pilot_hours_html += "</div>"

        pilot_summary_html = "<div class='pilot-summary-grid'>"
        for player, stats in sorted(global_pilot_stats.items()):
            time_flown = format_time(campaign_pilot_hours.get(player, 0))
            pilot_summary_html += f"""
            <div class='pilot-summary-card'>
                <div class='pilot-summary-name'>{player} <span class='pilot-summary-callsign'>[{stats['callsign']}]</span></div>
                <div class='summary-stat-row'><span>Total Missions:</span> <span class='summary-stat-val'>{stats['missions']}</span></div>
                <div class='summary-stat-row'><span>Flight Time:</span> <span class='summary-stat-val hl-cyan'>{time_flown}</span></div>
                <div style="border-top: 1px dashed #333; margin: 10px 0;"></div>
                <div class='summary-stat-row'><span>Air-to-Air Kills:</span> <span class='summary-stat-val hl-white'>{stats['aa']}</span></div>
                <div class='summary-stat-row'><span>Air-to-Ground Kills:</span> <span class='summary-stat-val hl-white'>{stats['ag']}</span></div>
                <div style="border-top: 1px dashed #333; margin: 10px 0;"></div>
                <div class='summary-stat-row'><span>KIA:</span> <span class='summary-stat-val hl-white'>{stats['kia']}</span></div>
                <div class='summary-stat-row'><span>MIA:</span> <span class='summary-stat-val hl-white'>{stats['mia']}</span></div>
            </div>
            """
        pilot_summary_html += "</div>"

        aa_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(global_aa_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No A-A kills recorded.</div>"
        ag_rows = "".join([f'<div class="target-row"><span class="target-name">{tgt}</span><span class="hl-white">{count}</span></div>' for tgt, count in sorted(global_ag_targets.items(), key=lambda x: x[1], reverse=True)]) or "<div class='target-row'>No Surface kills recorded.</div>"
        
        modals_html = f"""
        <dialog id="modal-aa" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AA} OVERALL AIR-TO-AIR BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-aa')">×</button></div><div class="modal-body">{aa_rows}</div></dialog>
        <dialog id="modal-ag" class="tactical-modal"><div class="modal-header"><span>{SVG_ICON_AG} OVERALL SURFACE BREAKDOWN</span><button class="close-btn" onclick="closeTacticalModal('modal-ag')">×</button></div><div class="modal-body">{ag_rows}</div></dialog>
        {all_modals_html}
        """

        thea_str = user_theater if user_theater and user_theater != "Auto-Detect" else (global_theater if global_theater else "N/A")
        camp_str = user_campaign if user_campaign and user_campaign != "Auto-Detect" else (global_campaign_name if global_campaign_name else "TACTICAL ENGAGEMENT")

        logo_block = REPORT_LOGO_SVG

        final_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Campaign After Action Report</title>
        <style>{CSS_CORE}</style>
    </head>
    <body>
        <div class="container">
            <button class="print-btn" onclick="window.print()">[ Export PDF ]</button>
            {logo_block}
            <h1>Campaign After Action Report</h1>
            
            <div class="tab-container">
                <div class="tab active" onclick="switchTab('tab-campaign')">Campaign Operations</div>
                <div class="tab" onclick="switchTab('tab-pilots')">Pilot Dossiers Summary</div>
            </div>

            <div id="tab-campaign" class="tab-content active">
                <h2>OVERALL CAMPAIGN PERFORMANCE</h2>
                <div class="campaign-info-banner">
                    <div>THEATER: <span>{thea_str}</span></div>
                    <div>CAMPAIGN: <span>{camp_str}</span></div>
                </div>

                <div class="global-stats campaign-stats">
                    <div class="stat-box"><div class="stat-title">{SVG_ICON_MISSIONS} Missions</div><div class="stat-value hl-white" id="stat-missions">{total_missions}</div></div>
                    <div class="stat-box clickable-box" onclick="document.getElementById('modal-aa').showModal()"><div class="stat-title">{SVG_ICON_AA} A-A Kills {SVG_ICON_HINT}</div><div class="stat-value hl-white" id="stat-aa">{camp_aa_kills}</div></div>
                    <div class="stat-box clickable-box" onclick="document.getElementById('modal-ag').showModal()"><div class="stat-title">{SVG_ICON_AG} A-G Kills {SVG_ICON_HINT}</div><div class="stat-value hl-white" id="stat-ag">{camp_ag_kills}</div></div>
                    <div class="stat-box"><div class="stat-title">{SVG_ICON_KIA} KIA</div><div class="stat-value hl-white" id="stat-kia">{camp_kia}</div></div>
                    <div class="stat-box"><div class="stat-title">{SVG_ICON_MIA} MIA</div><div class="stat-value hl-white" id="stat-mia">{camp_mia}</div></div>
                </div>

                {pilot_hours_html}

                <h2>MISSION LOGS</h2>
                {final_missions_html}
            </div>

            <div id="tab-pilots" class="tab-content">
                <h2>OVERALL PILOT COMBAT RECORDS</h2>
                {pilot_summary_html}
            </div>

        </div>
        {modals_html}
        <script>
            function removeMission(event, missionId, aa, ag, kia, mia) {{
                event.preventDefault(); 
                if(confirm('Are you sure you want to scrub this flight from the tactical report?')) {{
                    document.getElementById(missionId).remove();
                    
                    const updateStat = (id, subtractVal) => {{
                        let el = document.getElementById(id);
                        if(el) el.innerText = Math.max(0, parseInt(el.innerText) - subtractVal);
                    }};
                    
                    updateStat('stat-missions', 1);
                    updateStat('stat-aa', aa);
                    updateStat('stat-ag', ag);
                    updateStat('stat-kia', kia);
                    updateStat('stat-mia', mia);
                }}
            }}

            function closeTacticalModal(id) {{
                const modal = document.getElementById(id);
                modal.classList.add('closing');
                setTimeout(() => {{
                    modal.close();
                    modal.classList.remove('closing');
                }}, 240);
            }}
            function switchTab(tabId) {{
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.querySelector('[onclick="switchTab(\\''+tabId+'\\')"]').classList.add('active');
                document.getElementById(tabId).classList.add('active');
            }}
        </script>
    </body>
    </html>"""

        output_path = os.path.join(mission_folder, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        return True, f"Report successfully generated at:\n{output_path}"

    # ==========================================
    # GRAPHICAL USER INTERFACE (GUI) WITH RADAR
    # ==========================================
    print("[TACTICAL INFO] Starting standard Tkinter GUI (Responsive / Centered)...")

    class RadarScanner(tk.Canvas):
        def __init__(self, parent, size=60, color="#3ba5ff", bg="#111318"):
            super().__init__(parent, width=size, height=size, bg=bg, highlightthickness=0)
            self.size = size
            self.color = color
            self.center = size / 2
            self.radius = size / 2 - 2
            self.angle = 0
            self.scanning = False
            self.draw_static()
            
            self.beam = self.create_arc(2, 2, size-2, size-2, start=0, extent=45, fill=color, stipple='gray25', outline="")
            self.line = self.create_line(self.center, self.center, self.center, 2, fill=color, width=2)
            
            self.itemconfigure(self.beam, state='hidden')
            self.itemconfigure(self.line, state='hidden')

        def draw_static(self):
            self.create_oval(2, 2, self.size-2, self.size-2, outline="#2d323b", width=1)
            self.create_oval(self.center/2 + 1, self.center/2 + 1, self.size - self.center/2 - 1, self.size - self.center/2 - 1, outline="#2d323b", width=1)
            self.create_line(self.center, 0, self.center, self.size, fill="#2d323b", width=1)
            self.create_line(0, self.center, self.size, self.center, fill="#2d323b", width=1)

        def start(self):
            self.scanning = True
            self.itemconfigure(self.beam, state='normal')
            self.itemconfigure(self.line, state='normal')
            self.animate()

        def stop(self):
            self.scanning = False
            self.itemconfigure(self.beam, state='hidden')
            self.itemconfigure(self.line, state='hidden')

        def animate(self):
            if not self.scanning: return
            self.angle = (self.angle + 8) % 360 
            self.itemconfigure(self.beam, start=self.angle)
            rad = math.radians(self.angle + 45) 
            x = self.center + self.radius * math.cos(rad)
            y = self.center - self.radius * math.sin(rad)
            self.coords(self.line, self.center, self.center, x, y)
            self.after(30, self.animate)

    class BMSReportApp:
        def __init__(self, root):
            self.root = root
            self.root.title("BMS Tactical Report Builder")
            self.root.geometry("500x750") 
            self.root.minsize(450, 680) 
            
            self.BG_MAIN = "#0d1117"     
            self.BG_PANEL = "#12151c"    
            self.BORDER_DARK = "#333333" 
            self.ACCENT_CYAN = "#83a5c2" 
            self.TEXT_WHITE = "#c9d1d9"  
            self.TEXT_GRAY = "#888888"   
            
            self.root.configure(bg=self.BG_MAIN) 
            
            self.MONO_FONT = ("Consolas", 10) 
            self.MONO_FONT_BOLD = ("Consolas", 11, "bold") 

            self.folder_path = tk.StringVar()
            self.date_filter_start = tk.StringVar() 
            self.date_filter_end = tk.StringVar()   
            self.theater_var = tk.StringVar(value="Auto-Detect")
            self.campaign_var = tk.StringVar(value="Auto-Detect")
            self.network_var = tk.StringVar(value="All Missions")

            self.theaters_data = {
                "Auto-Detect": ["Auto-Detect"],
                "Korea Theater of Operations (KTO)": ["Auto-Detect", "Tiger Spirit", "Rolling Fire", "Iron Fortress", "Bear Trap", "Modern Fire", "Tactical Engagement"],
                "Balkans Theater of Operations (BTO)": ["Auto-Detect", "Balance of Power", "Under Siege", "Powderkeg", "Deny Flight Two", "Serbian Annex", "Joint Guard", "Tactical Engagement"],
                "Israel Theater of Operations (ITO)": ["Auto-Detect", "Serpent Sting", "Solid Truss", "Standing Wave", "Peace for Galilee", "Old School", "Red Line", "Tactical Engagement"],
                "Hellenic Theater of Operations (HTO)": ["Auto-Detect", "Tactical Engagement"]
            }

            self.main_container = tk.Frame(root, bg=self.BG_MAIN)
            self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

            header_frame = tk.Frame(self.main_container, bg=self.BG_MAIN)
            header_frame.pack(pady=(0, 15), anchor="center")

            try:
                logo_file = get_resource_path("launcher_logo.png")
                if os.path.exists(logo_file):
                    self.logo_img = tk.PhotoImage(file=logo_file).subsample(2, 2) 
                    tk.Label(header_frame, image=self.logo_img, bg=self.BG_MAIN).pack(side="top", pady=(0, 10))
                else:
                    print(f"[UI] Could not locate logo at: {logo_file}")
            except Exception as e:
                print(f"[UI] Error loading logo: {e}") 

            tk.Label(header_frame, text="AAR COMMAND CENTER", font=("Consolas", 16, "bold"), bg=self.BG_MAIN, fg=self.TEXT_WHITE).pack(side="top")

            def create_panel(parent, title_text=None):
                container = tk.Frame(parent, bg=self.BG_MAIN)
                container.pack(fill="x", pady=6)
                tk.Frame(container, bg=self.ACCENT_CYAN, height=2).pack(fill="x")
                panel_body = tk.Frame(container, bg=self.BG_PANEL, highlightbackground=self.BORDER_DARK, highlightthickness=1)
                panel_body.pack(fill="x")
                if title_text:
                    tk.Label(panel_body, text=title_text, font=self.MONO_FONT_BOLD, bg=self.BG_PANEL, fg=self.ACCENT_CYAN).pack(pady=(10, 5), anchor="center")
                return panel_body

            p1 = create_panel(self.main_container, "1. Select Debrief Folder")
            self.btn_browse = tk.Button(p1, text="BROWSE FOLDER", command=self.select_folder, font=self.MONO_FONT_BOLD, bg="#232733", fg=self.TEXT_WHITE, activebackground=self.BORDER_DARK, activeforeground=self.TEXT_WHITE, bd=1, relief="solid")
            self.btn_browse.pack(pady=(5, 5), anchor="center", ipadx=10, ipady=2)
            self.entry_path = tk.Label(p1, textvariable=self.folder_path, font=("Consolas", 8), bg=self.BG_PANEL, fg="#83a5c2", bd=0, justify="center")
            self.entry_path.pack(fill="x", padx=15, pady=(0, 10))

            p2 = create_panel(self.main_container, "2. Mission Filters")
            f_dates = tk.Frame(p2, bg=self.BG_PANEL)
            f_dates.pack(pady=5, anchor="center")
            tk.Label(f_dates, text="Dates:", font=self.MONO_FONT, bg=self.BG_PANEL, fg=self.TEXT_WHITE).pack(side="left", padx=5)
            self.entry_date_start = tk.Entry(f_dates, textvariable=self.date_filter_start, font=self.MONO_FONT, bg=self.BORDER_DARK, fg=self.TEXT_WHITE, insertbackground="white", bd=1, relief="solid", highlightthickness=0, width=11, justify="center")
            self.entry_date_start.pack(side="left", padx=5, ipady=4)
            tk.Label(f_dates, text="-", font=self.MONO_FONT, bg=self.BG_PANEL, fg=self.TEXT_WHITE).pack(side="left")
            self.entry_date_end = tk.Entry(f_dates, textvariable=self.date_filter_end, font=self.MONO_FONT, bg=self.BORDER_DARK, fg=self.TEXT_WHITE, insertbackground="white", bd=1, relief="solid", highlightthickness=0, width=11, justify="center")
            self.entry_date_end.pack(side="left", padx=5, ipady=4)

            f_net = tk.Frame(p2, bg=self.BG_PANEL)
            f_net.pack(pady=(5, 10), anchor="center")
            tk.Label(f_net, text="Network:", font=self.MONO_FONT, bg=self.BG_PANEL, fg=self.TEXT_WHITE).pack(side="left", padx=5)
            style = ttk.Style()
            style.theme_use('clam')
            style.configure("TCombobox", fieldbackground=self.BORDER_DARK, background=self.BG_MAIN, foreground=self.TEXT_WHITE, font=self.MONO_FONT, borderwidth=1, bordercolor=self.BORDER_DARK, arrowcolor=self.TEXT_WHITE)
            self.combo_net = ttk.Combobox(f_net, textvariable=self.network_var, values=["All Missions", "Multiplayer (Networked)", "Single Player (Local)"], font=self.MONO_FONT, width=24)
            self.combo_net.pack(side="left", padx=5)

            p3 = create_panel(self.main_container, "3. Campaign Metadata")
            f_th = tk.Frame(p3, bg=self.BG_PANEL)
            f_th.pack(pady=5, anchor="center")
            tk.Label(f_th, text="Theater:", font=self.MONO_FONT, width=10, anchor="e", bg=self.BG_PANEL, fg=self.TEXT_WHITE).pack(side="left")
            self.combo_theater = ttk.Combobox(f_th, textvariable=self.theater_var, values=list(self.theaters_data.keys()), font=self.MONO_FONT, width=28)
            self.combo_theater.bind("<<ComboboxSelected>>", self.update_campaigns)
            self.combo_theater.pack(side="left", padx=5)

            f_ca = tk.Frame(p3, bg=self.BG_PANEL)
            f_ca.pack(pady=(5, 10), anchor="center")
            tk.Label(f_ca, text="Campaign:", font=self.MONO_FONT, width=10, anchor="e", bg=self.BG_PANEL, fg=self.TEXT_WHITE).pack(side="left")
            self.combo_campaign = ttk.Combobox(f_ca, textvariable=self.campaign_var, values=self.theaters_data["Auto-Detect"], font=self.MONO_FONT, width=28)
            self.combo_campaign.pack(side="left", padx=5)

            action_frame = tk.Frame(self.main_container, bg=self.BG_MAIN)
            action_frame.pack(pady=(10, 5), fill="x")

            self.btn_generate = tk.Button(action_frame, text="GENERATE TACTICAL REPORT", command=self.generate, font=self.MONO_FONT_BOLD, bg=self.ACCENT_CYAN, fg=self.BG_MAIN, activebackground="#5cb6ff", activeforeground=self.BG_MAIN, bd=0, relief="flat", state=tk.DISABLED)
            self.btn_generate.pack(pady=(0, 10), anchor="center", ipadx=20, ipady=8)
            
            self.radar = RadarScanner(action_frame, size=35, color=self.ACCENT_CYAN, bg=self.BG_MAIN)
            self.radar.pack(anchor="center")

            console_panel = create_panel(self.main_container)
            console_panel.pack(fill="both", expand=True) 
            
            self.console_textbox = tk.Text(console_panel, font=("Consolas", 8), bg=self.BG_PANEL, fg=self.TEXT_WHITE, state=tk.DISABLED, wrap="word", bd=0, highlightthickness=0, height=5)
            self.console_textbox.pack(fill="both", expand=True, padx=10, pady=10)

            self.message_queue = queue.Queue()
            self.root.bind("<<UpdateConsole>>", self.poll_console_wrapper)
            self.root.bind("<<ProcessingFinished>>", self.on_processing_finished)
            self.final_result = None 

        def select_folder(self):
            folder_selected = filedialog.askdirectory(title="Select BMS Debrief Folder")
            if folder_selected:
                self.folder_path.set(folder_selected)
                self.btn_generate.configure(state=tk.NORMAL)

        def update_campaigns(self, event=None):
            selected_theater = self.combo_theater.get()
            campaigns = self.theaters_data.get(selected_theater, ["Auto-Detect", "Tactical Engagement"])
            self.combo_campaign['values'] = campaigns
            self.campaign_var.set("Auto-Detect")

        def generate(self):
            folder = self.folder_path.get()
            fecha_start = self.date_filter_start.get()
            fecha_end = self.date_filter_end.get()
            theater = self.theater_var.get()
            campaign = self.campaign_var.get()
            network = self.network_var.get()

            if not folder: return
            
            self.btn_generate.configure(state=tk.DISABLED, text="PROCESSING...")
            self.btn_browse.configure(state=tk.DISABLED)
            self.entry_date_start.configure(state=tk.DISABLED)
            self.entry_date_end.configure(state=tk.DISABLED)
            self.combo_theater.configure(state=tk.DISABLED)
            self.combo_campaign.configure(state=tk.DISABLED)
            self.combo_net.configure(state=tk.DISABLED)
            
            self.console_textbox.configure(state=tk.NORMAL)
            self.console_textbox.delete("1.0", tk.END)
            self.console_textbox.configure(state=tk.DISABLED)

            self.radar.start() 

            self.message_queue.put("[INFO] Starting telemetry engine...")
            if fecha_start or fecha_end:
                self.message_queue.put(f"[INFO] Applying date filter: {fecha_start} - {fecha_end}")
            if network != "All Missions":
                self.message_queue.put(f"[INFO] Applying connection filter: {network}")
                
            self.message_queue.put("[INFO] Running Omnivorous Auto-Archiver for master briefings...")
            self.message_queue.put("[INFO] Scanning flight logs...")
            self.message_queue.put("[OK] Extracting dynamic kills (A-A, A-G)...")
            self.message_queue.put("[OK] Analyzing KIA/MIA pilot records...")
            
            processing_thread = threading.Thread(target=self.process_thread_wrapper, args=(folder, fecha_start, fecha_end, theater, campaign, network, self.message_queue, self.final_result_callback))
            processing_thread.start()
            
            self.root.after(10, self.poll_console_wrapper)

        def process_thread_wrapper(self, folder, date_start, date_end, theater, campaign, network, message_queue, result_callback):
            time.sleep(0.5)
            
            try:
                success, message = process_report(
                    mission_folder=folder, 
                    date_start_str=date_start,
                    date_end_str=date_end,
                    user_theater=theater,
                    user_campaign=campaign,
                    user_network=network
                )
                
                final_msg = "[INFO] Finalizing report and tab structure..."
                if success:
                    final_msg += f"\n[OK] Report successfully generated:\n{message}"
                else:
                    final_msg += f"\n[ERROR] Report generation failed:\n{message}"
                
                message_queue.put(final_msg)
                result_callback(success, message, folder)
            except Exception as e:
                message_queue.put(f"[CRITICAL ERROR] {str(e)}")
                result_callback(False, str(e), folder)
            finally:
                self.root.event_generate("<<ProcessingFinished>>")

        def final_result_callback(self, success, message, folder_path):
            self.final_result = (success, message, folder_path)

        def poll_console_wrapper(self, event=None):
            try:
                while True:
                    message = self.message_queue.get_nowait()
                    self.console_textbox.configure(state=tk.NORMAL)
                    self.console_textbox.insert(tk.END, message + "\n")
                    self.console_textbox.see(tk.END) 
                    self.console_textbox.configure(state=tk.DISABLED)
            except queue.Empty:
                self.root.after(100, self.poll_console_wrapper)

        def on_processing_finished(self, event=None):
            self.radar.stop() 
            
            self.btn_generate.configure(state=tk.NORMAL, text="GENERATE TACTICAL REPORT")
            self.btn_browse.configure(state=tk.NORMAL)
            self.entry_date_start.configure(state=tk.NORMAL)
            self.entry_date_end.configure(state=tk.NORMAL)
            self.combo_theater.configure(state=tk.NORMAL)
            self.combo_campaign.configure(state=tk.NORMAL)
            self.combo_net.configure(state=tk.NORMAL)

            if self.final_result:
                success, message, folder = self.final_result
                if success:
                    messagebox.showinfo("MISSION SUCCESS", "Report successfully generated.")
                    try:
                        os.startfile(os.path.join(folder, "Final_Campaign_Report.html"))
                    except Exception as e:
                        pass
                else:
                    messagebox.showerror("MISSION FAILED", message)
                self.final_result = None 

    print("[TACTICAL INFO] Starting Tkinter main loop...")
    root = tk.Tk()
    app = BMSReportApp(root)
    root.mainloop()

except Exception as e:
    import traceback
    print("\n" + "="*60)
    print("!!! CRITICAL STARTUP ERROR DETECTED !!!")
    print("="*60 + "\n")
    traceback.print_exc()
    print("\n" + "="*60)
    input("Press ENTER to close this window and copy the error...")
    sys.exit(1)