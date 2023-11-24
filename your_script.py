import requests

# تنظیمات
CHANNEL_USERNAME = "TVCminer"
GITHUB_REPO = 'https://api.github.com/repos/mmjavadgh/v2rayPy/contents/links.txt'
GITHUB_TOKEN = "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"

def get_text_from_channel():
    try:
        # استفاده از تلگرام وب برای دریافت محتوای کانال
        url = f'https://t.me/{CHANNEL_USERNAME}'
        response = requests.get(url)
        
        if response.status_code == 200:
            # گرفتن متن کامل از محتوای دریافتی
            text = response.text
            return text
        else:
            print(f"Error: Unable to fetch content from the channel. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_github_file(text):
    if text is None:
        return
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    # دریافت محتوای فایل از گیت‌هاب
    current_content = requests.get(GITHUB_REPO, headers=headers).json()

    if 'content' not in current_content:
        print("Error: Couldn't retrieve file content from GitHub.")
        return

    current_sha = current_content['sha']

    # ایجاد محتوای جدید با متن دریافتی
    new_content = text

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
    text = get_text_from_channel()
    update_github_file(text)
