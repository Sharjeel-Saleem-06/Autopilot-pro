#!/usr/bin/env python3
"""
Autopilot Pro - Unified Launcher
=================================
This script automatically launches all Gradio model servers and makes the UI accessible.
Just run this ONE file and everything will start automatically!

Usage: python launch_all.py
"""

import os
import sys
import time
import subprocess
import threading
import signal
import webbrowser
from pathlib import Path
import requests
from typing import List, Dict, Optional

# Color codes for better terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.GREEN):
    """Print colored messages to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_header():
    """Print the application header"""
    header = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🚗  AUTOPILOT PRO LAUNCHER  🚗              ║
    ║                                                           ║
    ║         Multi-Model AI Detection System v1.0             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print_colored(header, Colors.CYAN + Colors.BOLD)

class GradioServerManager:
    """Manages multiple Gradio server instances"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.processes: List[subprocess.Popen] = []
        self.servers: List[Dict] = []
        self.setup_servers()
        
    def setup_servers(self):
        """Define all Gradio servers to launch"""
        self.servers = [
            {
                "name": "LTV/HTV Detection",
                "script": self.base_dir / "LTV_HTV_Model" / "LTV_HTV_Model.py",
                "port": 7860,
                "icon": "🚙",
                "process": None
            },
            {
                "name": "Pedestrian Detection",
                "script": self.base_dir / "Pedestrian_Model" / "Pedestrian_Model.py",
                "port": 7861,
                "icon": "🚶",
                "process": None
            },
            {
                "name": "Traffic Light Detection",
                "script": self.base_dir / "Traffic_Light_Model" / "TRAFFIC_LIGHT_MODEL.py",
                "port": 7862,
                "icon": "🚦",
                "process": None
            },
            {
                "name": "Traffic Sign Detection",
                "script": self.base_dir / "TRAFFIC_SIGN_MODEL" / "TRAFFIC_SIGN_MODEL.py",
                "port": 7869,
                "icon": "🚸",
                "process": None
            },
            {
                "name": "Autopilot Pro (Combined)",
                "script": self.base_dir / "AUTOPILOT PRO" / "Autopilotpro.py",
                "port": 7868,
                "icon": "🤖",
                "process": None
            }
        ]
    
    def check_port_available(self, port: int) -> bool:
        """Check if a port is available or already has a server running"""
        try:
            response = requests.get(f"http://127.0.0.1:{port}", timeout=2)
            return True  # Server already running on this port
        except requests.exceptions.RequestException:
            return False  # Port is free or server not responding
    
    def wait_for_server(self, port: int, timeout: int = 60) -> bool:
        """Wait for a server to become available on specified port"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://127.0.0.1:{port}", timeout=2)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        return False
    
    def launch_server_process(self, server: Dict) -> bool:
        """Launch a single Gradio server process (non-blocking)"""
        script_path = server["script"]
        
        # Check if script exists
        if not script_path.exists():
            print_colored(f"  ❌ Script not found: {script_path}", Colors.RED)
            return False
        
        # Check if server is already running
        if self.check_port_available(server["port"]):
            print_colored(f"  ✓ Already running on port {server['port']}", Colors.GREEN)
            server["status"] = "running"
            return True
        
        try:
            # Launch the server process (non-blocking)
            # Don't redirect output so we can see errors in real-time
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                cwd=script_path.parent
            )
            
            server["process"] = process
            server["status"] = "starting"
            self.processes.append(process)
            
            # Quick check if process died immediately
            time.sleep(0.5)
            if process.poll() is not None:
                print_colored(f"  ❌ {server['name']} process died immediately (exit code: {process.returncode})", Colors.RED)
                return False
            
            return True
                
        except Exception as e:
            print_colored(f"  ❌ Error launching {server['name']}: {e}", Colors.RED)
            server["status"] = "failed"
            return False
    
    def launch_all_servers(self):
        """Launch all Gradio servers in parallel for faster startup"""
        print_colored("\n📡 Starting Gradio Servers in Parallel...\n", Colors.CYAN + Colors.BOLD)
        
        # Phase 1: Start all processes simultaneously
        print_colored("⚡ Phase 1: Starting all processes...", Colors.BLUE + Colors.BOLD)
        for idx, server in enumerate(self.servers, 1):
            print_colored(f"  [{idx}/{len(self.servers)}] 🚀 Launching {server['icon']} {server['name']}...", Colors.YELLOW)
            self.launch_server_process(server)
        
        print()
        print_colored("⏳ Phase 2: Waiting for servers to be ready...", Colors.BLUE + Colors.BOLD)
        print_colored("   (Models are loading into memory - usually takes 30-60 seconds)\n", Colors.YELLOW)
        
        # Phase 2: Wait for all servers to become ready (parallel health checks)
        start_time = time.time()
        max_wait = 120  # Maximum 2 minutes
        check_interval = 2  # Check every 2 seconds
        
        servers_ready = {server["port"]: False for server in self.servers}
        last_ready_count = 0
        
        while time.time() - start_time < max_wait:
            all_ready = True
            elapsed = int(time.time() - start_time)
            ready_count = 0
            
            for server in self.servers:
                port = server["port"]
                
                # Skip if already confirmed ready
                if servers_ready[port]:
                    ready_count += 1
                    continue
                
                # Check if server is responding
                if self.check_port_available(port):
                    servers_ready[port] = True
                    ready_count += 1
                    print_colored(f"  ✅ {server['icon']} {server['name']} is ready! (Port: {port}) [{elapsed}s]", Colors.GREEN)
                else:
                    all_ready = False
            
            # Show progress if no new servers became ready
            if ready_count == last_ready_count and not all_ready:
                progress = "⚡" * ready_count + "⏳" * (len(self.servers) - ready_count)
                print_colored(f"  [{elapsed}s] {progress} ({ready_count}/{len(self.servers)} ready)", Colors.YELLOW)
            
            last_ready_count = ready_count
            
            # Exit early if all servers are ready
            if all_ready:
                break
            
            # Wait before next check
            time.sleep(check_interval)
        
        # Count results
        successful = sum(1 for ready in servers_ready.values() if ready)
        failed = len(self.servers) - successful
        
        # Print summary
        print()
        print_colored("═" * 60, Colors.CYAN)
        total_time = int(time.time() - start_time)
        print_colored(f"\n✅ Successfully launched: {successful}/{len(self.servers)} servers in {total_time}s", Colors.GREEN + Colors.BOLD)
        if failed > 0:
            print_colored(f"❌ Failed or timed out: {failed}/{len(self.servers)} servers", Colors.RED)
            print_colored(f"   (They may still be loading - check status in a moment)", Colors.YELLOW)
        print_colored("\n" + "═" * 60 + "\n", Colors.CYAN)
        
        return successful, failed
    
    def print_server_info(self):
        """Print information about all running servers"""
        print_colored("🌐 Server Information:", Colors.CYAN + Colors.BOLD)
        print_colored("─" * 60, Colors.CYAN)
        for server in self.servers:
            if self.check_port_available(server["port"]):
                url = f"http://127.0.0.1:{server['port']}"
                print_colored(f"  {server['icon']} {server['name']:<30} {url}", Colors.GREEN)
        print_colored("─" * 60 + "\n", Colors.CYAN)
    
    def open_ui(self):
        """Open the HTML UI in default browser"""
        ui_path = self.base_dir / "UI" / "home.html"
        if ui_path.exists():
            print_colored("🌐 Opening Autopilot Pro UI in browser...", Colors.CYAN)
            webbrowser.open(f"file://{ui_path}")
            print_colored(f"✓ UI opened: {ui_path}\n", Colors.GREEN)
        else:
            print_colored(f"⚠️  UI file not found: {ui_path}", Colors.YELLOW)
    
    def shutdown_all_servers(self):
        """Gracefully shutdown all running servers"""
        print_colored("\n\n🛑 Shutting down all servers...", Colors.YELLOW + Colors.BOLD)
        
        for process in self.processes:
            if process and process.poll() is None:  # Process is still running
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print_colored("  ✓ Server stopped gracefully", Colors.GREEN)
                except subprocess.TimeoutExpired:
                    process.kill()
                    print_colored("  ⚠️  Server force killed", Colors.YELLOW)
                except Exception as e:
                    print_colored(f"  ❌ Error stopping server: {e}", Colors.RED)
        
        print_colored("\n✅ All servers stopped. Goodbye! 👋\n", Colors.GREEN + Colors.BOLD)

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print_colored("\n\n⚠️  Interrupt received...", Colors.YELLOW)
    if hasattr(signal_handler, 'manager'):
        signal_handler.manager.shutdown_all_servers()
    sys.exit(0)

def print_instructions():
    """Print usage instructions"""
    instructions = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                   📖 INSTRUCTIONS                         ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║  ✓ All Gradio servers are now running!                   ║
    ║  ✓ The UI should open automatically in your browser      ║
    ║                                                           ║
    ║  💡 Usage:                                                ║
    ║     • Click any model button in the left sidebar         ║
    ║     • Upload images or use live camera detection         ║
    ║     • View performance metrics in the tabs               ║
    ║                                                           ║
    ║  🛑 To stop all servers:                                  ║
    ║     • Press Ctrl+C in this terminal                      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print_colored(instructions, Colors.CYAN)

def check_dependencies():
    """Check and install required dependencies"""
    print_colored("\n🔍 Checking dependencies...\n", Colors.CYAN + Colors.BOLD)
    
    required_modules = {
        'gradio': 'Gradio (Web Interface)',
        'ultralytics': 'Ultralytics YOLO',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'requests': 'Requests'
    }
    
    missing = []
    
    for module, name in required_modules.items():
        try:
            __import__(module)
            print_colored(f"  ✅ {name}", Colors.GREEN)
        except ImportError:
            print_colored(f"  ❌ {name} - NOT INSTALLED", Colors.RED)
            missing.append(module)
    
    if missing:
        print_colored(f"\n⚠️  Missing {len(missing)} required dependencies!", Colors.YELLOW + Colors.BOLD)
        print_colored("\n📥 Installing missing dependencies...", Colors.BLUE + Colors.BOLD)
        print_colored("   (This may take a few minutes)\n", Colors.YELLOW)
        
        try:
            # Install requirements
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt", 
                "--quiet", "--disable-pip-version-check"
            ])
            print_colored("\n✅ All dependencies installed successfully!\n", Colors.GREEN + Colors.BOLD)
            return True
        except subprocess.CalledProcessError as e:
            print_colored(f"\n❌ Failed to install dependencies: {e}", Colors.RED)
            print_colored("\nPlease run manually: pip install -r requirements.txt", Colors.YELLOW)
            return False
    else:
        print_colored("\n✅ All dependencies are installed!\n", Colors.GREEN)
        return True

def main():
    """Main launcher function"""
    # Print header
    print_header()
    
    # Check and install dependencies
    if not check_dependencies():
        print_colored("❌ Cannot proceed without required dependencies.", Colors.RED)
        sys.exit(1)
    
    # Create server manager
    manager = GradioServerManager()
    
    # Set up signal handler for graceful shutdown
    signal_handler.manager = manager
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Launch all servers
    successful, failed = manager.launch_all_servers()
    
    if successful == 0:
        print_colored("❌ No servers could be started. Please check the error messages above.", Colors.RED)
        sys.exit(1)
    
    # Print server information
    manager.print_server_info()
    
    # Open UI in browser
    manager.open_ui()
    
    # Print instructions
    print_instructions()
    
    # Keep the script running
    print_colored("⏳ Press Ctrl+C to stop all servers and exit...\n", Colors.YELLOW)
    
    try:
        # Monitor processes and keep script alive
        while True:
            time.sleep(5)
            # Check if any critical process died
            alive_count = sum(1 for p in manager.processes if p and p.poll() is None)
            if alive_count < len(manager.processes):
                print_colored(f"⚠️  Warning: Some servers may have stopped ({alive_count}/{len(manager.processes)} running)", Colors.YELLOW)
    except KeyboardInterrupt:
        pass
    finally:
        manager.shutdown_all_servers()

if __name__ == "__main__":
    main()

