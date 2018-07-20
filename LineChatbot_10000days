# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import math
import datetime
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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





# CHECK_POINT、SOME_TEXT、BIRTH_LISTはglobal変数として扱う(関数内外問わず値が変化するもの)


CHECK_POINT = 0
# CHECK_POINTの質問→誤答or正答の質問を変える
SOME_TEXT = ["4桁じゃないと計算できないよ～","２桁じゃないと計算できないよ～","数字を入力してね！","え？月はそんなにありません～","え？日はそんなにありません～","間違えすぎだよ、馬鹿！"]
#要所要所でだすTEXT
BIRTH_LIST=[]
#正しい入力を格納するリスト


# CHECK_POINTが5の時、年の決定を意味する
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    global CHECK_POINT
    global BIRTH_LIST
    global SOME_TEXT

    if event.message.text == "こんにちは":
        return_text = "こんにちはって何？"

    elif event.message.text == "1万日":
        CHECK_POINT = 1
        return_text = "生まれた西暦を教えてください！"

    elif CHECK_POINT == 1:
        try:
             input_year = int (event.message.text)
             data_size = int (math.log10(input_year) + 1)
             if data_size != 4:
                 CHECK_POINT = 1
                 return_text = SOME_TEXT[0]#4桁じゃないとダメー
             else:
                 BIRTH_LIST.append(input_year)
                 #年を入力しています。
                 CHECK_POINT = 5
                 return_text = "生まれた月はいつですか？"
        except ValueError:
            CHECK_POINT = 1
            return_text = SOME_TEXT[2] #数字を入力してね。

    # 月を入力してもらうぞーー
    elif CHECK_POINT == 5 or CHECK_POINT == 6:
        try:
             input_month = int (event.message.text)
             data_size = int (math.log10(input_month) + 1)
             if data_size > 2:
                 CHECK_POINT = 6
                 return_text = SOME_TEXT[1] + "\n 1～12月の間でお願いします"#２桁じゃないと計算できないよ～
             elif input_month < 1 or input_month > 12:
                CHECK_POINT = 6
                return_text = SOME_TEXT[3] + "\n 1～12月の間でお願いします"
             else:
                BIRTH_LIST.append(input_month)
                #月を入力、追加しています。
                CHECK_POINT = 10
                return_text = "生まれた日を入力してね！"

        except ValueError:
            CHECK_POINT = 6
            return_text = SOME_TEXT[2] + "\n もし「3月」とかって入力してたら月の「数字だけ」を入力してね！"#数字を入力してね。

    # 日にちを入力してもらうぞーー
    elif CHECK_POINT == 10 or CHECK_POINT == 11:
        try:
             input_day = int (event.message.text)
             data_size = int (math.log10(input_day) + 1)
             if data_size > 2:
                 CHECK_POINT = 11
                 return_text = SOME_TEXT[1] + "\n その数字は読み込めないよ"#２桁じゃないと計算できないよ～
             elif input_day < 1 or input_day > 31:
                CHECK_POINT = 11
                return_text = SOME_TEXT[4] + "\n その数字は読み込めないよ～"
             else:
                BIRTH_LIST.append(input_day)
                #日を入力、追加しています。
                CHECK_POINT = 15
                year = int(BIRTH_LIST[0])
                month = int(BIRTH_LIST[1])
                day = int(BIRTH_LIST[2])
                try:
                    BIRTH_DAY = datetime.date(year,month,day)
                    one_day = datetime.timedelta(days = 1)
                    days_10000 = BIRTH_DAY + one_day * 10000
                    return_text = datetime.datetime.strftime(days_10000, "%Y-%m-%d")
                    #あとは相手の名前を取得とかして、面白くする。
                    BIRTH_LIST = []
                    CHECK_POINT = 0
                    #10000日記念日用に取得したデータを初期化する。

                except ValueError:
                    CHECK_POINT = 11
                    del BIRTH_LIST[2]
                    # さっきリストに加えた日付(input_day)を消します
                    return_text = str(month) + "月は" + str(day) + "日は存在しないよ…　\n 日付を入力しなおしてね！"

        except ValueError:
            CHECK_POINT = 11
            return_text = SOME_TEXT[2] + "\n もし「11日」とかって入力してたら日にちの「数字だけ」を入力してね！"#数字を入力してね。
            # return_text = "生まれた月はいつですか？"

    else:
        return_text = "うるさい、ばか"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_text)
    )


    # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(text=event.message.text)
    # )




if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
