from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import sys

app=Flask(__name__)

#環境変数の取得
LINE_CHANNEL_ACCESS_TOKEN =os.environ['LINE_CHANNEL_SECRET']
LINE_CHANNEL_SECRET =os.environ['LINE_CHANNEL_ACCESS_TOKEN']
line_bot_api=LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature=request.headers["X-Line-Signature"]

    # get request body as text
    body=request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    output_text = "「" + input_text + "」ってコーヒーがあるの？"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text)
    )

if __name__=="__main__":
    #port=int(os.getenv("PORT",5000))
    port=int(os.getenv("PORT"))
    app.run(host="0.0.0.0",port=port)
