from slack_bolt import App
from datetime import datetime
import os
import json
import urllib.request, json
USER = {
    'Id': 'Name'
}

# Initializes your app with your bot token and signing secret
app = App(
    token='...',
    signing_secret='...'
)


@app.message('登校')
def attendance(message, say):
    temp = message['text']
    date = datetime.fromtimestamp(int(message['ts'].split('.')[0]))
    
    say(
        text = f"<@{message['user']}>さん\n検温結果 {temp} でメールを送信しました．\n時刻: {date.hour}:{date.minute}"
    )

@app.message('到着')
def arrival(message, say):
    date = datetime.fromtimestamp(int(message['ts'].split('.')[0]))
    say(
        text = f"<@{message['user']}>さん\n手洗いの報告メールを送信しました．\n時刻: {date.hour}:{date.minute}"
    )

@app.message('帰宅')
def leave(message, say):
    date = datetime.fromtimestamp(int(message['ts'].split('.')[0]))
    say(
        text = f"<@{message['user']}>さん\n帰宅の報告メールを送信しました．\n時刻: {date.hour}:{date.minute}"
    )
    say(
        text = f"本日の換気時刻をメールしました．"
    )


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
