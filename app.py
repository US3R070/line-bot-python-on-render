from flask import Flask, request, abort
import json
import re

state = 0

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

user_columns = []

template  = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
                        title='Python基礎教學',
                        text='萬丈高樓平地起',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=270'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='Line Bot聊天機器人',
                        text='台灣最廣泛使用的通訊軟體',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Line Bot申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2532'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                        title='Telegram Bot聊天機器人',
                        text='唯有真正的方便，能帶來意想不到的價值',
                        actions=[
                            MessageAction(
                                label='教學內容',
                                text='Telegrame申請與串接'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://marketingliveincode.com/?page_id=2648'
                            )
                        ]
                    )
                ]
            )


def add_and_del(target):
    if (target == '加入'):
        
        CarouselColumn()
    elif(target == '刪除'):
        A = 2;
    return

def Carousel_template():
    A = 3;

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
    global state
    message = TextSendMessage(text=event.message.text)
    
    if(event.message.text == '選單'):
        Carousel_template()
    elif (event.message.text == '加入' or event.message.text == '刪除'):
        add_and_del(event.message.text)
    elif (event.message.text == '指令'):
        reply = TextSendMessage(text = '1. 選單 : 找出\n')
    else:
        reply = TextSendMessage(text = '沒有這個指令，若要查詢可以輸入「指令」')
        line_bot_api.reply_message(event.reply_token,reply)
    
def state_manager():
    


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
