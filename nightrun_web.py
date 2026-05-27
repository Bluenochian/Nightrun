#!/usr/bin/env python3
"""
NIGHTRUN 3.0 - Web Dashboard Server
Flask + SocketIO real-time dashboard for Stable Diffusion Forge image generation

Usage:
    python nightrun_web.py

Auto-installs dependencies, detects Forge, opens browser to http://localhost:5000
"""

import os
import sys
import json
import subprocess
import threading
import time
import base64
import webbrowser
import requests
import re
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from queue import Queue, Empty

# ========================
# CONFIGURATION
# ========================

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
FORGE_API = "http://127.0.0.1:7860"
FLASK_PORT = 5000
BROWSER_DELAY = 1.0

# Auto-install dependencies
def ensure_dependencies():
    """Install Flask and SocketIO if missing"""
    required = ['flask', 'flask-socketio', 'requests', 'python-socketio', 'python-engineio']
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

ensure_dependencies()

# ========================
# FLASK APP SETUP
# ========================

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))
app.config['SECRET_KEY'] = 'nightrun-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ========================
# STATE
# ========================

state = {
    'current_prompt_map': {},
    'current_theme': 'default',
    'is_running': False,
    'log_queue': Queue(),
    'forge_running': False,
}

config = {}

# ========================
# THEME DETECTION
# ========================

THEME_KEYWORDS = {
    'cyber': ['cyber', 'neon', 'digital', 'tech'],
    'matrix': ['matrix', 'code', 'falling'],
    'dragon': ['dragon', 'scales', 'wings'],
    'fire': ['fire', 'flame', 'burn', 'hot'],
    'snow': ['snow', 'ice', 'frost', 'cold', 'winter'],
    'steam': ['steam', 'clockwork', 'gears', 'mechanical'],
    'love': ['love', 'romance', 'heart', 'rose'],
    'ocean': ['ocean', 'water', 'sea', 'underwater'],
    'ghost': ['ghost', 'haunted', 'spirit', 'ethereal'],
    'cosmic': ['cosmic', 'space', 'star', 'nebula', 'galaxy'],
    'forest': ['forest', 'tree', 'nature', 'wood', 'fairy', 'woodland'],
    'potion': ['potion', 'alchemy', 'magic', 'arcane'],
    'surveillance': ['surveillance', 'camera', 'dystopia', 'spy'],
    'nuclear': ['nuclear', 'fallout', 'radiation', 'atomic'],
    'vampire': ['vampire', 'blood', 'gothic', 'dark'],
    'mystery': ['mystery', 'detective', 'noir', 'shadow'],
    'medieval': ['medieval', 'castle', 'knight', 'sword', 'ancient'],
    'samurai': ['samurai', 'ninja', 'japan', 'sakura', 'katana'],
    'wasteland': ['wasteland', 'desert', 'apocalypse', 'ruin'],
    'demon': ['demon', 'hell', 'evil', 'dark', 'inferno'],
    'hologram': ['hologram', 'android', 'ai', 'robot'],
    'magic': ['magic', 'wizard', 'arcane', 'spell'],
    'default': []
}

def detect_theme(prompt_text):
    """Detect theme from prompt keywords"""
    if not prompt_text:
        return 'default'
    
    text = prompt_text.lower()
    scores = {}
    
    for theme, keywords in THEME_KEYWORDS.items():
        score = sum(text.count(kw) for kw in keywords)
        if score > 0:
            scores[theme] = score
    
    if not scores:
        return 'default'
    
    return max(scores, key=scores.get)

# ========================
# FORGE API INTERACTION
# ========================

def check_forge():
    """Check if Forge is running"""
    try:
        r = requests.get(f"{FORGE_API}/sdapi/v1/progress?skip_current_image=true", timeout=2)
        state['forge_running'] = r.status_code == 200
        return state['forge_running']
    except:
        state['forge_running'] = False
        return False

def poll_forge_progress():
    """Poll Forge API for progress updates"""
    while state['is_running']:
        try:
            r = requests.get(f"{FORGE_API}/sdapi/v1/progress?skip_current_image=false", timeout=3)
            data = r.json()
            
            if data.get('current_image'):
                img_data = data['current_image']
                if img_data.startswith('data:'):
                    img_data = img_data.split(',')[1]
                
                progress = int((data.get('progress', 0) or 0) * 100)
                socketio.emit('preview_image', {
                    'b64': img_data,
                    'progress': progress,
                    'step': data.get('state', {}).get('sampling_step', 0),
                    'total': data.get('state', {}).get('sampling_steps', 0),
                })
        except:
            pass
        
        time.sleep(0.8)

def poll_and_emit_logs():
    """Emit logs from queue to connected clients"""
    while state['is_running']:
        try:
            line_info = state['log_queue'].get(timeout=0.5)
            text, color = line_info
            socketio.emit('log_line', {'text': text, 'color': color})
        except Empty:
            continue
        except:
            break

# ========================
# ROUTES
# ========================

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Return current config"""
    global config
    if not config:
        config_path = SCRIPT_DIR / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
        else:
            config = {'count': 10}
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def save_config():
    """Save config to config.local.json"""
    global config
    data = request.get_json()
    config.update(data)
    
    config_local_path = SCRIPT_DIR / "config.local.json"
    with open(config_local_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return jsonify({'status': 'ok'})

@app.route('/api/forge', methods=['GET'])
def forge_status():
    """Check Forge status"""
    running = check_forge()
    return jsonify({'running': running})

@app.route('/api/launch', methods=['POST'])
def launch():
    """Launch image generation"""
    data = request.get_json()
    mode = data.get('mode', 'full')
    count = data.get('count', 10)
    
    # Start generation in background
    thread = threading.Thread(
        target=run_generation,
        args=(mode, count),
        daemon=True
    )
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/stop', methods=['POST'])
def stop_generation():
    """Stop generation"""
    state['is_running'] = False
    
    # Create stop signal file
    stop_file = SCRIPT_DIR / "STOP_AFTER_CURRENT_IMAGE.txt"
    stop_file.write_text(datetime.now().isoformat())
    
    return jsonify({'status': 'stopped'})

@app.route('/api/skip', methods=['POST'])
def skip_image():
    """Skip current image"""
    try:
        requests.post(f"{FORGE_API}/sdapi/v1/interrupt", timeout=5)
    except:
        pass
    
    return jsonify({'status': 'skipped'})

# ========================
# GENERATION MOCK
# ========================

def run_generation(mode, count):
    """Mock generation loop (replace with actual nightrun.py integration)"""
    state['is_running'] = True
    
    for i in range(1, count + 1):
        if not state['is_running']:
            break
        
        # Simulate prompt parsing
        prompts = [
            "1girl, solo, cyber, neon, digital", 
            "dragon, fire, scales, wings",
            "snow, winter, ice, cold",
            "ghost, haunted, ethereal, spirit",
            "ocean, water, sea, underwater",
        ]
        
        prompt = prompts[i % len(prompts)]
        
        # Emit log lines
        emit_log(f"[{i:04d}] Starting generation {i}/{count}", 'cyan')
        emit_log(f"[{i:04d}] Generating with prompt: {prompt}", 'bright-cyan')
        
        # Simulate prompt map
        prompt_map = {
            'concept': prompt.split(',')[0],
            'style': 'illustration',
            'lighting': 'soft glow',
        }
        
        state['current_prompt_map'] = prompt_map
        theme = detect_theme(prompt)
        state['current_theme'] = theme
        
        socketio.emit('prompt_map', {
            'map': prompt_map,
            'full_prompt': prompt,
            'theme_id': theme,
        })
        
        # Simulate progress
        for step in range(1, 31):
            if not state['is_running']:
                break
            progress = int((step / 30) * 100)
            socketio.emit('progress', {
                'value': progress,
                'eta': f"00:{30-step}",
                'phase': f"Generating step {step}/30"
            })
            time.sleep(0.1)
        
        emit_log(f"[{i:04d}] Generation complete", 'green')
        
        if mode == 'upscale':
            emit_log(f"[{i:04d}] Upscaling...", 'yellow')
            for step in range(1, 16):
                if not state['is_running']:
                    break
                progress = 50 + int((step / 15) * 50)
                socketio.emit('progress', {
                    'value': progress,
                    'eta': f"00:{15-step}",
                    'phase': f"Upscaling step {step}/15"
                })
                time.sleep(0.1)
            emit_log(f"[{i:04d}] Upscale complete", 'green')
    
    emit_log("Generation batch complete!", 'green')
    state['is_running'] = False

def emit_log(text, color='white'):
    """Queue a log message"""
    state['log_queue'].put((text, color))

# ========================
# SOCKETIO EVENTS
# ========================

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    emit('log_line', {'text': 'Connected to dashboard', 'color': 'cyan'})

@socketio.on('launch')
def handle_launch(data):
    """Launch generation"""
    emit_log(f"Launch requested: mode={data.get('mode')}, count={data.get('count')}", 'green')
    thread = threading.Thread(
        target=run_generation,
        args=(data.get('mode', 'full'), data.get('count', 10)),
        daemon=True
    )
    thread.start()

@socketio.on('stop')
def handle_stop():
    """Stop generation"""
    state['is_running'] = False
    emit_log("Stop signal sent", 'red')

@socketio.on('skip')
def handle_skip():
    """Skip current image"""
    emit_log("Skip signal sent", 'yellow')

# ========================
# MAIN
# ========================

def open_browser():
    """Open browser after server starts"""
    time.sleep(BROWSER_DELAY)
    webbrowser.open(f'http://localhost:{FLASK_PORT}')

if __name__ == '__main__':
    print(f"◈ NIGHTRUN 3.0 - Starting dashboard server...")
    print(f"  Flask: http://localhost:{FLASK_PORT}")
    
    # Check Forge
    if check_forge():
        print(f"  ✓ Forge API detected at {FORGE_API}")
    else:
        print(f"  ⚠ Forge API not responding (will retry on demand)")
    
    # Start browser opener thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start server
    try:
        socketio.run(app, host='0.0.0.0', port=FLASK_PORT, debug=False)
    except KeyboardInterrupt:
        print("\n◈ Nightrun shutting down...")
        sys.exit(0)
