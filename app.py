from flask import Flask, request, abort

from bs4 import BeautifulSoup as bs
import requests

import re

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

search_board = ''

search_page = 0

delete_reply = TextSendMessage(text = '請輸入要從選單移除的看板\n[ Ex ]: NBA , Gossiping , Stock ...')

join_reply = TextSendMessage(text = '請輸入要加到選單的看板\n[ Ex ]: NBA , Gossiping , Stock ...')

please_return_reply = TextSendMessage(text = '若要輸入其他指令，請先輸入「算了」放棄當前工作')

discard_reply = TextSendMessage(text = '回到主選單')

headers = {
    "user_agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
        
url_dict = {'C_Chat':'https://www.ptt.cc/bbs/C_Chat/index.html'}

user_columns = [
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/PpLDWf8.png?2',
                        title='C_Chat',
                        text='C_Chat',
                        actions=[
                                MessageAction
                                (
                                    label='功能表',
                                    text= 'C_Chat 功能表'
                                ),
                            URIAction(
                                label='跳到該看板',
                                uri='https://www.ptt.cc/bbs/C_Chat/index.html'
                            ),
                                        MessageAction
                                        (
                                            label='返回主選單',
                                            text= '算了'
                                        )
                        ]
                    )
                ]
        
state = 0
range = 10

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
    
    text = event.message.text
    
    if event.source.user_id == "U0b55f1fefdcf18168b0c8c515701a585":
        print(event.message.text, state,event.timestamp)

    if (state == 0):
        if (text == '列表' and user_columns != []):
            state = 1
            template  = CarouselTemplate(columns=user_columns)
            carousel_template_message = TemplateSendMessage(alt_text='最愛選單',template = template);
            line_bot_api.reply_message(event.reply_token, carousel_template_message)  
        elif (text == '列表' and user_columns == []):
            reply = TextSendMessage(text = '目前列表中沒有項目哦，輸入「加入」來增加一個看板吧')
            line_bot_api.reply_message(event.reply_token,reply)
        elif (text == '加入'):
            state = 2
            line_bot_api.reply_message(event.reply_token,join_reply)
        elif (text == '刪除'):
            state = 3
            line_bot_api.reply_message(event.reply_token,delete_reply)
        elif (text == '指令'):
            reply = TextSendMessage(text = '1. 列表:列出選單看板項目\n2. 加入:加入喜歡看板到「選單」中\n3. 刪除:將「選單」中的看板刪除\n4. 算了:停止目前的工作並返回主選單')
            line_bot_api.reply_message(event.reply_token,reply)
        elif (text =='印'):
            reply = TextSendMessage(text = str(url_dict))
            line_bot_api.reply_message(event.reply_token,reply)
        else:
            reply = TextSendMessage(text = '沒有這個指令，要查詢可以輸入「指令」哦!')
            line_bot_api.reply_message(event.reply_token,reply)
    elif (state == 1):
        Carousel_reply_handle(event)
    elif (state == 2):
        add(event)
    elif(state == 3):
        delete(event)
    elif(state == 4):
        menuhandler(event)
    elif(state == 5):
        searchhandler(event)
    elif(state == 6):
        range_new_handler(event) 
    elif (state == 7):
        range_hot_handler(event)

    
    return

def add(event):
    global state
    global user_columns
    text = event.message.text
    url = 'https://www.ptt.cc/bbs/hotboards.html'

    if (state == 2):
        if (text == '算了'):
            state = 0
            line_bot_api.reply_message(event.reply_token,discard_reply)
        elif (text == '列表' or text == '加入' or text == '刪除' or text == '指令'):
            line_bot_api.reply_message(event.reply_token,please_return_reply)
        else :
            res = requests.get(url,headers = headers,cookies={'over18':'1'})
            soup = bs(res.text,"html.parser")
            data = soup.select("div.b-ent")
            for ele in data :
                board_name = ele.select("div.board-name")[0].text
                if (text == board_name):
                    board_url = 'https://www.ptt.cc' + ele.select("a.board")[0]["href"]
                    url_dict[board_name] = board_url
                    to_add = CarouselColumn(
                                        thumbnail_image_url='https://i.imgur.com/PpLDWf8.png?2',
                                        title=text,
                                        text=ele.select("div.board-title")[0].text,
                                        actions=
                                        [
                                            MessageAction
                                            (
                                                label='功能表',
                                                text= text + ' ' + '功能表'
                                            ),
                                            URIAction
                                            (
                                                label='跳到該看板',
                                                uri= board_url
                                            ),
                                            MessageAction
                                            (
                                                label='返回主選單',
                                                text= '算了'
                                            )
                                        ]
                                        )
                    user_columns.append(to_add)
                    state = 0
                    join_success = TextSendMessage(text = '成功加入 ' + text + ' 至選單中')
                    line_bot_api.reply_message(event.reply_token,join_success)
                    return
            
            join_fail = TextSendMessage(text = '沒有這個看板ㄛ，請再輸入一次')
            line_bot_api.reply_message(event.reply_token,join_fail)
    return
            
def delete(event):
    global state
    text = event.message.text
    if (state == 3):
        if (text == '算了'):
            state = 0
            line_bot_api.reply_message(event.reply_token,discard_reply)
        elif (text == '列表' or text == '加入' or text == '刪除' or text == '指令'):
            line_bot_api.reply_message(event.reply_token,please_return_reply)
        else :
            for board in user_columns:
                if (board.title == text):
                    state = 0
                    user_columns.remove(board)
                    del_success_reply = TextSendMessage('成功從選單中移除 ' + text)
                    line_bot_api.reply_message(event.reply_token,del_success_reply)
                    return
            
            del_fail_reply = TextSendMessage('選單中沒有這個看板ㄛ，請重新輸入 ' + text)
            line_bot_api.reply_message(event.reply_token,del_fail_reply)
    return

def Carousel_reply_handle(event):
    global state
    text = event.message.text
    textlist = text.split()
    if (state == 1):
        if (text == '算了'):
            state = 0
            line_bot_api.reply_message(event.reply_token,discard_reply)
        elif (text == '列表' or text == '加入' or text == '刪除' or text == '指令'):
            line_bot_api.reply_message(event.reply_token,please_return_reply)
        elif (textlist[1] == '功能表'):
            buttons_template_message = TemplateSendMessage(
                    alt_text='功能表',
                    template=ButtonsTemplate(
                        title='功能表',
                        text=textlist[0] + '版功能表',
                        actions=[
                            MessageAction(
                                label='熱門文章',
                                text= textlist[0] + ' ' +'版熱門文章，請輸入搜尋頁數:'
                            ),
                            MessageAction(
                                label='最新內容',
                                text= textlist[0] + ' ' +'版最新內容，請輸入搜尋筆數:'
                            ),
                            MessageAction(
                                label='搜尋關鍵字',
                                text= textlist[0] + ' ' +'版搜尋關鍵字'
                            ),
                            MessageAction(
                                label='返回選單',
                                text= '算了'
                            ),
                        ]
                    )
                )
            state = 4
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
    return
        
def searchhandler(event):
    global state
    global search_page
    global search_board
    text = event.message.text
    
    if (state == 5):
        if (text == '算了'):
            state = 0
            line_bot_api.reply_message(event.reply_token,discard_reply)
        else :
            search_list = ''
            count = 1
            for i in range (0,30,1):
                uurl = 'https://www.ptt.cc/bbs/' + search_board + '/index' + str(search_page-i) + '.html'
                res = requests.get(uurl,headers = headers,cookies={'over18':'1'})
                soup = bs(res.text,"html.parser")
                datanum = soup.select("div.r-ent")
                for ele in datanum:
                    num_recv = ele.select("div.nrec")[0].text
                    title = ele.select("div.title")[0].text.strip()
                    if title.__contains__(text):
                        search_list += ( str(count) + '. <'+ num_recv + '> ' + ele.select("div.title")[0].text.strip() + '\nhttps://www.ptt.cc' + ele.select("div.title a")[0]["href"] + '\n\n')
                        count +=1
            if (search_list != ''): 
                search_reply = TextSendMessage(text = search_list)
                line_bot_api.reply_message(event.reply_token,search_reply)
                return
            else :
                reply = TextSendMessage(text = '在 ' + search_board +' 版上找不到含有「 '+text+' 」的文章，請輸入另外的關鍵字' )
                line_bot_api.reply_message(event.reply_token,reply)
                return
    return

  
def menuhandler(event):
    global state
    global search_page
    global search_board
    text = event.message.text
    textlist = text.split()
    
    if (state == 4):
        if (url_dict.get(textlist[0])!=None):

            url = url_dict[textlist[0]]
            res = requests.get(url,headers = headers)
            soup = bs(res.text,"html.parser")
            datanum = soup.select("div.r-ent")
            data = soup.select("div.action-bar")

            for ele in data :
                d = ele.select("div.btn-group.btn-group-paging")
                for k in d:
                    f = k.select("a.btn.wide")[1]["href"]
                    ret = int(re.findall(r"\d+",f)[0])

            if (textlist[1] == '版熱門文章，請輸入搜尋頁數:'):
                state = 7
                search_board = textlist[0]
                search_page = ret
                return
            
            elif (textlist[1] == '版最新內容，請輸入搜尋筆數:'):
                state = 6
                search_board = textlist[0]
                search_page = ret
                return
            
            elif (textlist[1] == '版搜尋關鍵字'):
                state = 5
                search_board = textlist[0]
                search_page = ret
                return
                
        elif(textlist[0] == '算了'):
            state = 0
            line_bot_api.reply_message(event.reply_token,discard_reply)
            return
        else:
            line_bot_api.reply_message(event.reply_token,please_return_reply)
            return
    return

def range_hot_handler(event):
    global state
    global search_page
    global search_board
    global range
    text = event.message.text

    if (state == 7 ):
        try: 
            ran = int(text)
            print(ran)
            if (ran >= 0 and ran<100):
                hot_list = ''
                count = 1
                i = 0
                while i < ran:
                    uurl = 'https://www.ptt.cc/bbs/' + search_board + '/index' + str(search_page-i) + '.html'
                    res1 = requests.get(uurl,headers = headers,cookies={'over18':'1'})
                    soup1 = bs(res1.text,"html.parser")
                    datanum = soup1.select("div.r-ent")
                    for ele in datanum:
                        num_recv = ele.select("div.nrec")[0].text
                        if (num_recv != '' and num_recv[0] != 'X' and (num_recv == '爆' or int(num_recv) > 40) and len(hot_list)< 4900):
                            hot_list += ( str(count) + '. <'+ num_recv + '> ' + ele.select("div.title")[0].text.strip() + '\nhttps://www.ptt.cc' + ele.select("div.title a")[0]["href"] + '\n\n')
                            count +=1
                    i+=1
                
                hot_reply = TextSendMessage(text = hot_list)
                line_bot_api.reply_message(event.reply_token,hot_reply)
                return
            else:
                hot_reply = TextSendMessage(text = '請輸入有效的數字 : 1-99')
                line_bot_api.reply_message(event.reply_token,hot_reply)
                return
            return
        except ValueError:
            if (text == '算了'):
                state = 0
                line_bot_api.reply_message(event.reply_token,discard_reply)
                return
            else:
                hot_reply = TextSendMessage(text = '請輸入數字')
                line_bot_api.reply_message(event.reply_token,hot_reply)
                return
        
def range_new_handler(event):
    global state
    global search_page
    global search_board
    global range
    text = event.message.text
    if (state == 6): 
        try:
            number = int(text)
            if (number <= 50 and number > 0):
                new_list = ''
                count = 1
                i = 0
                while i<number:
                    uurl = 'https://www.ptt.cc/bbs/' + search_board + '/index' + str(search_page-i) + '.html'
                    res1 = requests.get(uurl,headers = headers,cookies={'over18':'1'})
                    soup1 = bs(res1.text,"html.parser")
                    datanum = soup1.select("div.r-ent")
                    for ele in datanum:
                        num_recv = ele.select("div.nrec")[0].text
                        if count <= number :
                            new_list += ( str(count) + '. <'+ num_recv + '> ' + ele.select("div.title")[0].text.strip() + '\nhttps://www.ptt.cc' + ele.select("div.title a")[0]["href"] + '\n\n')
                            count +=1
                    i+=1
                new_reply = TextSendMessage(text = new_list)
                line_bot_api.reply_message(event.reply_token,new_reply)
                return  
            else:
                hot_reply = TextSendMessage(text = '請輸入有效的數字 : 1-50')
                line_bot_api.reply_message(event.reply_token,hot_reply)
        except ValueError:
            if (text == '算了'):
                state = 0
                line_bot_api.reply_message(event.reply_token,discard_reply)
            else:
                hot_reply = TextSendMessage(text = '請輸入數字')
                line_bot_api.reply_message(event.reply_token,hot_reply)
            return
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
