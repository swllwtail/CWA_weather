import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

msg_list = ['Weather ','weather','weather ','天氣圖','map','Map ']
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

def scratch_CWA ():
    image_url = "https://www.cwa.gov.tw/Data/fcst_img/FI04.png"
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    msg = event.message.text
    if (msg in msg_list):
        message = TextSendMessage(type = 'image',original_content_url="https://www.cwa.gov.tw/Data/fcst_img/FI04.png",preview_image_url="https://www.cwa.gov.tw/Data/fcst_img/FI04.png")
        line_bot_api.reply_message(event.reply_token,message)
    return
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
