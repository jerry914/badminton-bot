from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import sys
import json
sys.path.append("gateway")
import chatGPT_handler
# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


chatGPT_toggle = False
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global chatGPT_toggle
    if ("小雀" in event.message.text):
        chatGPT_toggle = not chatGPT_toggle
        message = TextSendMessage(text="Assistant is now " + ("ON" if chatGPT_toggle else "OFF"))
        line_bot_api.reply_message(event.reply_token, message)
    if (chatGPT_toggle and "小雀" not in event.message.text):
        response = chatGPT_handler.run_conversation(event.message.text+" userID"+event.source.user_id)
        message = TextSendMessage(text=response)
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)