from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('Dv/jLTe9Hjfv29yLkOKmE3NsPmGQQhPP6Hj+CfzoN716mEEpOokXfe/n8TE+s3ZImeimsF6Lf4neUNbmXIX65b7oMsHc0YWJte3dOZbLz/GXlpDDKEwjp0vRAc0ueLhf5sYNk3bss7/dLRqCx+v8JQdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('641700cfc7bd588430948046b6c3c9a8')

line_bot_api.push_message('U0b55f1fefdcf18168b0c8c515701a585', TextSendMessage(text='Successfully deployed'))

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
    message = TextSendMessage(text=event.message.text)
    
    if (message == "123") :
        message = '呵呵呵'
    
    line_bot_api.reply_message(event.reply_token,message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
