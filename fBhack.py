import requests
from telegram import Bot

# 🔵 Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7256577569:AAHyOFgwSk6hmV1vfhIgW8wub74IW3MTQf4"
TELEGRAM_CHAT_ID = "6524755764"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 🔵 Facebook API Details
ACCESS_TOKEN = "7%3AeOs1nQspTbPX9A%3A2%3A1742110211%3A-1%3A-1"
FB_USER_ID = "61558789512339"  # "me" means your own account


# 🔍 Function to Get 'People You May Know'
def get_people_you_may_know():
    url = f"https://graph.facebook.com/v18.0/{FB_USER_ID}/friends?access_token={ACCESS_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for user in data.get("data", []):
            name = user.get("name")
            user_id = user.get("id")
            profile_link = f"https://www.facebook.com/{user_id}"

            # 🟢 Send to Telegram
            message = f"👤 {name}\n🔗 Profile: {profile_link}"
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    else:
        print("❌ Failed to fetch data:", response.text)


# 🚀 Run Function
get_people_you_may_know()
