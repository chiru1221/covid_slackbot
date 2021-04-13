'''
Follow these steps to configure the webhook in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Incoming WebHooks".

  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".

  4. Copy the webhook URL from the setup instructions and use it in the next section.

To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Expand "Encryption configuration" and click the "Enable helpers for encryption in transit" checkbox

  3. Paste <SLACK_CHANNEL> into the slackChannel environment variable

  Note: The Slack channel does not contain private info, so do NOT click encrypt

  4. Paste <SLACK_HOOK_URL> into the kmsEncryptedHookUrl environment variable and click "Encrypt"

  Note: You must exclude the protocol from the URL (e.g. "hooks.slack.com/services/abc123").

  5. Give your function's role permission for the `kms:Decrypt` action using the provided policy template
'''
# references
# https://dev.classmethod.jp/articles/slash-commands-train-delay/
# https://qiita.com/tacos_salad/items/9fe997a34cebc8fcef39

import os
import json

# default pacakge でない場合，別途アップロードが必要
from urllib.parse import unquote
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def lambda_handler(event, context):
    request_param = parse_slash_commands(event['body'])
    # print(json.dumps(request_param))
    
    url = 'gas_url?name={}&command={}&value={}'.format(request_param["user_id"], request_param["command"], request_param["text"])
    req = Request(url, method="GET")
    
    try:
        with urlopen(req, timeout=1) as res:
            body = res.read().decode('utf-8')
    except:
        pass
    # print(body)
    
    if (request_param["command"] == "/ventilate"):
        payload = {
            'response_type': 'in_channel',#'ephemeral',    # コマンドを起動したユーザのみに返答する
            'attachments': [
                {
                    'color': '#2E9AFE',
                    'pretext': 'temp1', #str(context),
                    'text': 'temp1.1' #str(json.dumps(request_param))#str(os.listdir)#body#str(req)
                }
            ]
        }
    else:
        payload = {
            'response_type': 'in_channel',#'ephemeral',    # コマンドを起動したユーザのみに返答する
            'attachments': [
                {
                    'color': '#36a64f',
                    'pretext': "temp2", #str(context),
                    'text': "temp2.1"# +  str(json.dumps(request_param))#str(os.listdir)#body#str(req)
                }
            ]
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps(payload)
    }

def parse_slash_commands(payload) -> dict:
    """Slash commandsのパラメータを解析する

    Args:
        payload: 受信したSlash commandsのパラメータ

    Returns:
        dict: 解析したパラメータとその内容
    """
    params = {}
    params["text"] = ""
    key_value_list = unquote(payload).split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params
