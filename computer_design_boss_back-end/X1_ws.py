import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from demo import garbage_classification
from pathlib import Path
from set_up import config
config_data = config()

import websocket  # 使用websocket_client
answer = ""
isFirstcontent = False

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    content =''
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        text = choices['text'][0]
        if ( 'reasoning_content' in text and '' != text['reasoning_content']):
            reasoning_content = text["reasoning_content"]
            print(reasoning_content, end="")
            global isFirstcontent
            isFirstcontent = True

        if('content' in text and '' != text['content']):
            content = text["content"]
            if(True == isFirstcontent):
                print("\n*******************以上为思维链内容，模型回复内容如下********************\n")
            print(content, end="")
            isFirstcontent = False
        global answer
        answer += content
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": config_data.set_LLM_temperature,
                "max_tokens": config_data.set_LLM_max_tokens       # 请根据不同模型支持范围，适当调整该值的大小
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, Spark_url,domain, question):
    # print("星火:")
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})



text = []


# 管理对话历史，按序编为列表
def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

# 获取对话中的所有角色的content长度
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

# 判断长度是否超长，当前限制8K tokens
def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def main_answer(appid, api_key, api_secret, Spark_url, domain, Input):
    global text
    text = []
    global answer
    answer = ""
    question = checklen(getText("user", Input))
    print("星火:", end="")
    main(appid, api_key, api_secret, Spark_url, domain, question)
    talk = getText("assistant", answer)
    return talk

class think_speaker:
    def __init__(self):
        self.appid = "2e81dc67"  # 填写控制台中获取的 APPID 信息
        self.api_secret = "NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3"  # 填写控制台中获取的 APISecret 信息
        self.api_key = "fd79a4d97543e35b2881a64b81b8f124"  # 填写控制台中获取的 APIKey 信息
        # self.domain = "spark-x"  # 控制请求的模型版本
        self.domain = "generalv3"  # 控制请求的模型版本

        # 服务地址
        self.Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # 查看接口文档  https://www.xfyun.cn/doc/spark/X1ws.html
        # self.img_path = r'uploads\img.png'
        self.img_path = r'uploads/images/img.png'

    def think_speak(self, Input, flig):
        # print(111111)
        if flig:
            # print(222222)
            g_c_answer = garbage_classification(self.img_path)
            # print(g_c_answer)
            return g_c_answer
        else:
            talk = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, Input)
            # print(talk)
            return talk



# if __name__ == '__main__':
#     # 以下密钥信息从服务管控页面获取：https://console.xfyun.cn/services/bmx1
#     appid = "9e54e001"  # 填写控制台中获取的 APPID 信息
#     api_secret = "MWZlZmE4MzE4YTMxNWUxMDg1ZDI2MDBi"  # 填写控制台中获取的 APISecret 信息
#     api_key = "55edcb29ab95c53aad65b95343544821"  # 填写控制台中获取的 APIKey 信息
#     domain = "spark-x"       #控制请求的模型版本
#     # 服务地址
#     Spark_url = "wss://spark-api.xf-yun.com/v1/x1"  #查看接口文档  https://www.xfyun.cn/doc/spark/X1ws.html
#     img_path = r'img.png'
#
#     while (1):
#         Input = input("\n" + "我:")
#         if '垃圾分类' in Input:
#             g_c_answer = garbage_classification(Path(img_path))
#             print(g_c_answer)
#             Input = Input + g_c_answer
#             main_answer(appid, api_key, api_secret, Spark_url, domain, Input)
#         else:
#             main_answer(appid, api_key, api_secret, Spark_url, domain, Input)