import requests
from telegram import Bot
import os

# تنظیمات
TELEGRAM_TOKEN = "6520725138:AAF9YpmlJ0ypzFyZwaNr0hf_60xh9RW_kFc"
CHANNEL_ID = "@TVCminer"
GITHUB_REPO = 'https://api.github.com/repos/mmjavadgh/v2rayPy/contents/links.txt'
GITHUB_TOKEN = "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"

def get_links_from_channel():
    bot = Bot(token=TELEGRAM_TOKEN)
    messages = bot.get_chat_history(chat_id=CHANNEL_ID, limit=10)  # تعداد پیام‌ها را تغییر دهید اگر نیاز دارید

    links = []
    for message in messages:
        if message.entities:
            for entity in message.entities:
                if entity.type == 'url':
                    links.append(message.text[entity.offset:entity.offset+entity.length])

    return links

def update_github_file(links):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    current_content = requests.get(GITHUB_REPO, headers=headers).json()
    current_sha = current_content['sha']
    
    new_content = f"{'\n'.join(links)}\n"
    
    data = {
        'message': 'Update links.txt',
        'content': new_content,
        'sha': current_sha,
    }

    response = requests.put(GITHUB_REPO, headers=headers, json=data)
    print(response.json())

if __name__ == "__main__":
    links = get_links_from_channel()
    update_github_file(links)
