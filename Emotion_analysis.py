import urllib.request
import json

API_Key = 'Ci9tHmTxqEeitO26aX1OrNuK'
Secret_Key = '44znpekSpRP1GOlOgxkxbzEfP0XzxOIZ'


def get_access_token():
    """
    获取百度AI平台的Access Token
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_Key + \
           '&client_secret=' + Secret_Key
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    return rdata['access_token']


def sentiment_classify(text):
    """
    获取文本的感情偏向（消极 or 积极 or 中立）
    参数：
    text:str 本文
    0:负向，1:中性，2:正向
    """
    raw = {"text":"内容"}
    raw['text'] = text
    data = json.dumps(raw).encode('utf-8')
    host = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + access_token
    request = urllib.request.Request(url=host, data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    print(rdata)
    if 'error_code' in rdata:  # 出错
        if rdata['error_msg'] == 'input empty':  # 文本只有不能识别的内容
            return 1
        else:
            return sentiment_classify(text)  # 并发数量达到上线
    else:
        return rdata['items'][0]['sentiment']


access_token = get_access_token()
