import requests
import os

TOKEN = os.getenv("8200520928:AAFguwQb8TjB43QoZ-VxzZBBu1bCvhP5pIE")
CHAT_ID = os.getenv("6871609980")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})
