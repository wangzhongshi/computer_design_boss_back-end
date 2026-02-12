# -*- coding:utf-8 -*-
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import threading
import os
from pydub import AudioSegment
from set_up import config
config_data = config()

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


class WsParam:
    """WebSocket 参数配置类"""

    def __init__(self, appid, api_key, api_secret, text):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.text = text

        # 公共参数
        self.common_args = {"app_id": self.appid}

        # 业务参数：raw 格式输出 PCM
        self.business_args = {
            "aue": "raw",  # 音频编码：raw/pcm
            "auf": "audio/L16;rate=16000",
            "vcn": "x4_yezi",  # 发音人（ ye zi 可能已下线，建议用 xiaoyan）
            "tte": "utf8",
            "speed": 50,  # 语速 0-100
            "volume": 50,  # 音量 0-100
            "pitch": 50  # 音高 0-100
        }

        # 数据参数
        text_base64 = base64.b64encode(self.text.encode('utf-8')).decode('utf-8')
        self.data = {"status": 2, "text": text_base64}

    def create_url(self):
        """生成鉴权 URL"""
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 构建签名原文
        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/tts HTTP/1.1"

        # HMAC-SHA256 签名
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')

        # 构建鉴权头
        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature}"'
        )
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        params = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }

        return f"{url}?{urlencode(params)}"


class XunfeiTTS:
    """讯飞 TTS 客户端"""

    def __init__(self, appid, api_key, api_secret):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.pcm_buffer = bytearray()  # 内存缓冲区，避免频繁写盘
        self.output_file = None
        self.ws_param = None

    def pcm_to_mp3(self, pcm_data, mp3_path, sample_rate=16000):
        """将 PCM 字节数据转换为 MP3"""
        try:
            # 使用 BytesIO 避免临时文件
            from io import BytesIO

            audio = AudioSegment(
                data=pcm_data,
                sample_width=2,  # 16bit
                frame_rate=sample_rate,
                channels=1  # 单声道
            )

            audio.export(mp3_path, format="mp3", bitrate="192k")
            print(f"✓ MP3 已保存: {mp3_path}")
            return True

        except Exception as e:
            print(f"✗ 转换失败: {e}")
            return False

    def synthesize(self, text, output_path='./output.mp3'):
        """
        执行语音合成

        Args:
            text: 要合成的文本
            output_path: 输出 MP3 路径
        """
        self.ws_param = WsParam(self.appid, self.api_key, self.api_secret, text)
        self.output_file = output_path
        self.pcm_buffer = bytearray()

        # 清理旧文件
        temp_pcm = './temp.pcm'
        for f in [temp_pcm, output_path]:
            if os.path.exists(f):
                os.remove(f)

        # 创建 WebSocket 连接
        ws_url = self.ws_param.create_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

        print(f"开始合成: {text[:20]}...")
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        return os.path.exists(output_path)

    def _on_open(self, ws):
        """连接建立时发送数据"""

        def run():
            data = {
                "common": self.ws_param.common_args,
                "business": self.ws_param.business_args,
                "data": self.ws_param.data
            }
            ws.send(json.dumps(data))
            print("→ 已发送文本数据")

        threading.Thread(target=run).start()

    def _on_message(self, ws, message):
        """接收音频数据"""
        try:
            msg = json.loads(message)
            code = msg.get("code")
            sid = msg.get("sid")

            if code != 0:
                print(f"错误 [{code}]: {msg.get('message')}")
                ws.close()
                return

            # 解码音频数据
            audio = base64.b64decode(msg["data"]["audio"])
            status = msg["data"]["status"]

            # 累积到缓冲区
            self.pcm_buffer.extend(audio)

            # 最后一帧：关闭连接并转换
            if status == STATUS_LAST_FRAME:
                print("→ 接收完成，正在转换格式...")
                ws.close()

                # 转换为 MP3
                success = self.pcm_to_mp3(bytes(self.pcm_buffer), self.output_file)
                if not success:
                    # 转换失败时保存原始 PCM
                    with open('./failed.pcm', 'wb') as f:
                        f.write(self.pcm_buffer)
                    print("原始 PCM 已保存到 ./failed.pcm")

        except Exception as e:
            print(f"消息处理错误: {e}")

    def _on_error(self, ws, error):
        """错误处理"""
        print(f"✗ WebSocket 错误: {error}")

    def _on_close(self, ws, close_status_code=None, close_msg=None):
        """连接关闭"""
        print(f"✓ 连接已关闭 (code: {close_status_code})")


def tts_demo(text, output_path = None):
    '''
    一次字数上线：280字
    :param text:
    :return:
    '''
    # 配置你的讯飞开放平台凭证
    APPID = config_data.set_tts_appid
    API_SECRET = config_data.set_tts_api_secret
    API_KEY = config_data.set_tts_api_key

    # 初始化 TTS 客户端
    tts = XunfeiTTS(APPID, API_KEY, API_SECRET)
    if output_path == None:
        output_path = "data/demo.mp3"
    else:
        pass
    success = tts.synthesize(text, output_path)

    if success:
        print(f"合成成功！文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    else:
        print("合成失败")


