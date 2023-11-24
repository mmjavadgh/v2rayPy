import re
from telegram import Bot
import requests
from bs4 import BeautifulSoup

# تنظیمات
TELEGRAM_TOKEN = "6520725138:AAF9YpmlJ0ypzFyZwaNr0hf_60xh9RW_kFc"
CHANNEL_ID = "@TVCminer"
GITHUB_REPO = 'https://api.github.com/repos/mmjavadgh/v2rayPy/contents/links.txt'
GITHUB_TOKEN = "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"
CHANNEL_URL = 'https://t.me/TVCminer'

# الگوی شناسایی لینک‌های v2ray
v2ray_link_pattern = re.compile(r'vmess://[a-zA-Z0-9+/=_-]+')

def get_v2ray_links_from_text(text):
    # یافتن تمام لینک‌های v2ray در یک متن
    links = v2ray_link_pattern.findall(text)
    return links

def get_links_from_channel():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        
        # استفاده از get_chat برای دریافت اطلاعات کانال
        chat = bot.get_chat(CHANNEL_ID)
        
        # استفاده از get_messages برای دریافت پیام‌ها
        messages = bot.get_messages(chat_id=CHANNEL_ID, limit=10)  # تعداد پیام‌ها را تغییر دهید اگر نیاز دارید

        links = []
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == 'url':
                        # افزودن لینک‌های v2ray به لیست لینک‌ها
                        v2ray_links = get_v2ray_links_from_text(message.text[entity.offset:entity.offset + entity.length])
                        links.extend(v2ray_links)

        return links
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def update_github_file(links):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    # دریافت محتوای فایل از گیت‌هاب
    current_content = requests.get(GITHUB_REPO, headers=headers).json()

    if 'content' not in current_content:
        print("Error: Couldn't retrieve file content from GitHub.")
        return

    current_sha = current_content['sha']

    # ایجاد محتوای جدید با لینک‌های v2ray
    new_content = f"{'\n'.join(links)}\n"

    data = {
        'message': 'Update links.txt',
        'content': new_content,
        'sha': current_sha,
    }

    # ارسال درخواست به گیت‌هاب برای به‌روزرسانی فایل
    response = requests.put(GITHUB_REPO, headers=headers, json=data)

    if response.status_code == 200:
        print("File updated successfully on GitHub.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    links = get_links_from_channel()
    update_github_file(links)
