"""
Autopilot Pro Configuration File
=================================
Customize ports, timeouts, and other settings here.
"""

# Server Configuration
SERVER_CONFIG = {
    "LTV_HTV": {
        "name": "LTV/HTV Detection",
        "port": 7860,
        "icon": "🚙",
        "script": "LTV_HTV_Model/LTV_HTV_Model.py",
        "enabled": True
    },
    "Pedestrian": {
        "name": "Pedestrian Detection",
        "port": 7861,
        "icon": "🚶",
        "script": "Pedestrian_Model/Pedestrian_Model.py",
        "enabled": True
    },
    "TrafficLight": {
        "name": "Traffic Light Detection",
        "port": 7862,
        "icon": "🚦",
        "script": "Traffic_Light_Model/TRAFFIC_LIGHT_MODEL.py",
        "enabled": True
    },
    "TrafficSign": {
        "name": "Traffic Sign Detection",
        "port": 7869,
        "icon": "🚸",
        "script": "TRAFFIC_SIGN_MODEL/TRAFFIC_SIGN_MODEL.py",
        "enabled": True
    },
    "AutopilotPro": {
        "name": "Autopilot Pro (Combined)",
        "port": 7868,
        "icon": "🤖",
        "script": "AUTOPILOT PRO/Autopilotpro.py",
        "enabled": True
    }
}

# Launcher Settings
LAUNCHER_SETTINGS = {
    "server_startup_timeout": 120,      # seconds to wait for each server
    "health_check_interval": 1,         # seconds between health checks
    "auto_open_browser": True,          # automatically open UI in browser
    "show_server_logs": False,          # show detailed server output
    "graceful_shutdown_timeout": 5      # seconds to wait before force kill
}

# UI Settings
UI_PATH = "UI/home.html"                # path to main UI file

# Performance Settings
PERFORMANCE = {
    "static_confidence_threshold": 0.4,  # for uploaded images
    "live_confidence_threshold": 0.7     # for camera feed
}

