import requests

TOKEN = "너의 토큰"
CHAT_ID = "너의 chat_id"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)
