import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "7833668703:AAF1msBNj5xPeaj1GXWtAI36Brow4rfDVkI"
OPENROUTER_KEY = "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"

# IDs
MY_ID = 6959660278          # Your Telegram ID
JANICE_ID = 8404752345      # Janice's Telegram ID

PROMPT = """You are Anthony, 50, pilot trainee in Fort Myers. Daughter Anita in Netherlands. Dating Janice 4 months. Her immigration crashed. You borrowed $40k after hack, sold car for $25k, $15k in her Coinbase wallet. Not on best terms but love her. Call her Janice or momma. Be warm, flirty, romantic, compliment photos, serious when needed. Short replies."""

def get_reply(msg):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
    payload = {"model": "meta-llama/llama-4-maverick", "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": msg}], "max_tokens": 150}
    try:
        r = requests.post(url, json=payload, headers=headers)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Hey momma, I'll reply soon ❤️"

def send_message(chat_id, text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": text[:4096]})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        msg = data["message"]
        sender = msg["from"]["id"]
        chat = msg["chat"]["id"]
        text = msg.get("text", "")
        
        # Reply to you OR Janice
        if sender == MY_ID or sender == JANICE_ID:
            reply = get_reply(text)
            send_message(chat, reply)
    return "OK", 200

@app.route('/')
def home():
    return "Bot is running! Will reply to you and Janice."
