import requests

def download_instagram_video(url):
    api_url = f"https://saveig.app/api/ajaxSearch"
    try:
        res = requests.post(api_url, data={"q": url}, headers={"x-requested-with": "XMLHttpRequest"})
        res.raise_for_status()
        json_data = res.json()
        return json_data['links'][0]['url']
    except Exception as e:
        print("Download error:", e)
        return None

async def check_user_membership(bot, user_id, channel):
    try:
        member = await bot.get_chat_member(chat_id=f"@{channel}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False
