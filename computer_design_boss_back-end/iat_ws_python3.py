# -*- coding: utf-8 -*-
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
import logging
from typing import Optional, Callable
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2


@dataclass
class ASRConfig:
    """ASR配置类"""
    language: str = "zh_cn"
    accent: str = "mandarin"
    domain: str = "iat"
    vad_eos: int = 10000
    sample_rate: int = 16000


class XunfeiASR:
    """讯飞语音识别客户端 - 线程安全版本"""

    def __init__(self, appid: str, api_key: str, api_secret: str):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self._result_text = ""  # 累积完整结果
        self._lock = threading.Lock()
        self._ws = None
        self._ws_thread: Optional[threading.Thread] = None
        self._is_finished = threading.Event()
        self._is_running = False

    def _create_url(self) -> str:
        """生成鉴权URL"""
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"

        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')

        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode()).decode()

        params = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        return url + '?' + urlencode(params)

    def _on_message(self, ws, message: str):
        """WebSocket消息回调"""
        try:
            data = json.loads(message)
            code = data.get("code", -1)
            sid = data.get("sid", "unknown")

            if code != 0:
                err_msg = data.get("message", "Unknown error")
                logger.error(f"识别错误: {err_msg} (code: {code}, sid: {sid})")
                self._is_finished.set()
                return

            # 解析识别结果
            result_data = data.get("data", {}).get("result", {})
            if "ws" in result_data:
                text_parts = []
                for item in result_data["ws"]:
                    for w in item.get("cw", []):
                        text_parts.append(w.get("w", ""))

                # 线程安全地累积结果
                if text_parts:
                    with self._lock:
                        self._result_text += "".join(text_parts)

            # 检查是否结束
            if result_data.get("ls", False):
                logger.info("识别完成（最后一句话）")
                self._is_finished.set()

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            self._is_finished.set()
        except Exception as e:
            logger.error(f"消息处理异常: {e}")
            self._is_finished.set()

    def _on_error(self, ws, error):
        """错误回调"""
        logger.error(f"WebSocket错误: {error}")
        self._is_finished.set()

    def _on_close(self, ws, close_status_code, close_msg):
        """关闭回调"""
        logger.info(f"WebSocket连接关闭: {close_status_code} - {close_msg}")
        self._is_finished.set()
        self._is_running = False

    def _send_audio_frames(
            self,
            audio_generator,
            config: ASRConfig,
            on_progress: Optional[Callable[[str], None]] = None
    ):
        """发送音频帧的通用方法"""
        status = STATUS_FIRST_FRAME
        frame_count = 0

        business_args = {
            "domain": config.domain,
            "language": config.language,
            "accent": config.accent,
            "vinfo": 1,
            "vad_eos": config.vad_eos
        }

        try:
            for buf in audio_generator:
                if not buf:
                    status = STATUS_LAST_FRAME

                if status == STATUS_FIRST_FRAME:
                    d = {
                        "common": {"app_id": self.appid},
                        "business": business_args,
                        "data": {
                            "status": 0,
                            "format": f"audio/L16;rate={config.sample_rate}",
                            "audio": base64.b64encode(buf).decode('utf-8'),
                            "encoding": "raw"
                        }
                    }
                    self._ws.send(json.dumps(d))
                    status = STATUS_CONTINUE_FRAME

                elif status == STATUS_CONTINUE_FRAME:
                    d = {
                        "data": {
                            "status": 1,
                            "format": f"audio/L16;rate={config.sample_rate}",
                            "audio": base64.b64encode(buf).decode('utf-8'),
                            "encoding": "raw"
                        }
                    }
                    self._ws.send(json.dumps(d))

                elif status == STATUS_LAST_FRAME:
                    d = {
                        "data": {
                            "status": 2,
                            "format": f"audio/L16;rate={config.sample_rate}",
                            "audio": base64.b64encode(buf).decode('utf-8') if buf else "",
                            "encoding": "raw"
                        }
                    }
                    self._ws.send(json.dumps(d))
                    time.sleep(0.5)  # 给服务器处理时间
                    break

                frame_count += 1
                if frame_count % 25 == 0:  # 每秒约25帧（40ms间隔）
                    # 实时反馈当前识别结果
                    if on_progress:
                        current_text = self.get_current_result()
                        on_progress(current_text)

                time.sleep(0.04)  # 40ms间隔

        except Exception as e:
            logger.error(f"发送音频异常: {e}")
        finally:
            try:
                self._ws.close()
            except:
                pass

    def _file_audio_generator(self, audio_file: str, frame_size: int = 8000):
        """文件音频生成器"""
        try:
            with open(audio_file, "rb") as fp:
                while True:
                    buf = fp.read(frame_size)
                    yield buf
                    if not buf:
                        break
        except FileNotFoundError:
            logger.error(f"音频文件不存在: {audio_file}")
            raise
        except Exception as e:
            logger.error(f"读取音频文件失败: {e}")
            raise

    def recognize(
            self,
            audio_file: str,
            config: Optional[ASRConfig] = None,
            timeout: int = 30,
            on_progress: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        识别音频文件

        Args:
            audio_file: PCM音频文件路径（16kHz, 16bit, 单声道）
            config: ASR配置，默认中文普通话
            timeout: 超时时间（秒）
            on_progress: 进度回调函数，实时返回当前识别文本

        Returns:
            str: 完整识别文本
        """
        if self._is_running:
            raise RuntimeError("已有识别任务进行中")

        config = config or ASRConfig()
        self._reset_state()
        self._is_running = True

        try:
            ws_url = self._create_url()

            self._ws = websocket.WebSocketApp(
                ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=lambda ws: threading.Thread(
                    target=self._send_audio_frames,
                    args=(self._file_audio_generator(audio_file), config, on_progress)
                ).start()
            )

            self._ws_thread = threading.Thread(
                target=self._ws.run_forever,
                kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}}
            )
            self._ws_thread.daemon = True
            self._ws_thread.start()

            # 等待完成或超时
            if not self._is_finished.wait(timeout=timeout):
                raise TimeoutError(f"识别超时（>{timeout}秒）")

            return self.get_current_result()

        finally:
            self._cleanup()

    def recognize_microphone(
            self,
            record_seconds: int = 5,
            config: Optional[ASRConfig] = None,
            on_progress: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        从麦克风实时识别

        Args:
            record_seconds: 录音时长（秒）
            config: ASR配置
            on_progress: 进度回调函数

        Returns:
            str: 识别文本
        """
        try:
            import pyaudio
        except ImportError:
            raise ImportError("请先安装pyaudio: pip install pyaudio")

        if self._is_running:
            raise RuntimeError("已有识别任务进行中")

        config = config or ASRConfig()
        self._reset_state()
        self._is_running = True

        # 录音参数
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        stream = None

        def mic_audio_generator():
            """麦克风音频生成器"""
            nonlocal stream
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )

            logger.info(f"🎤 开始录音（{record_seconds}秒）...")
            start_time = time.time()
            frames = 0

            while time.time() - start_time < record_seconds:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames += 1
                    # 每25帧（约1秒）打印一次提示
                    if frames % 25 == 0:
                        elapsed = int(time.time() - start_time)
                        remaining = record_seconds - elapsed
                        if remaining > 0:
                            logger.info(f"⏱️  剩余时间: {remaining}秒")
                    yield data
                except Exception as e:
                    logger.error(f"录音异常: {e}")
                    break

            logger.info("🛑 录音结束")
            yield b""  # 触发结束帧

        try:
            ws_url = self._create_url()

            self._ws = websocket.WebSocketApp(
                ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=lambda ws: threading.Thread(
                    target=self._send_audio_frames,
                    args=(mic_audio_generator(), config, on_progress)
                ).start()
            )

            self._ws_thread = threading.Thread(
                target=self._ws.run_forever,
                kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}}
            )
            self._ws_thread.daemon = True
            self._ws_thread.start()

            # 等待录音完成+识别完成
            timeout = record_seconds + 10
            if not self._is_finished.wait(timeout=timeout):
                raise TimeoutError("识别超时")

            return self.get_current_result()

        finally:
            # 确保资源释放
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            try:
                p.terminate()
            except:
                pass
            self._cleanup()

    def get_current_result(self) -> str:
        """获取当前识别结果（线程安全）"""
        with self._lock:
            return self._result_text

    def _reset_state(self):
        """重置状态"""
        with self._lock:
            self._result_text = ""
        self._is_finished.clear()

    def _cleanup(self):
        """清理资源"""
        self._is_running = False
        if self._ws:
            try:
                self._ws.close()
            except:
                pass
            self._ws = None


class AudioConverter:
    """音频格式转换工具类"""

    @staticmethod
    def convert_to_pcm(input_file: str, output_file: Optional[str] = None) -> str:
        """
        将音频文件转换为讯飞要求的PCM格式（16kHz, 16bit, 单声道）

        需要安装: pip install pydub
        需要安装ffmpeg并添加到PATH
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            raise ImportError("请先安装pydub: pip install pydub")

        if output_file is None:
            base, _ = os.path.splitext(input_file)
            output_file = f"{base}_16k.pcm"

        try:
            # 加载音频（自动检测格式）
            audio = AudioSegment.from_file(input_file)

            # 转换为16kHz, 单声道, 16bit
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

            # 导出为原始PCM
            audio.export(output_file, format="s16le")  # 有符号16位小端

            logger.info(f"✅ 转换完成: {output_file}")
            logger.info(f"   采样率: 16000Hz, 声道: 1, 位深: 16bit")

            return output_file

        except Exception as e:
            logger.error(f"转换失败: {e}")
            raise


def demo_file_recognition(audio_path=None):
    """演示：文件识别"""
    # 直接在函数中设置密钥（后续优化为其他方式）
    appid = '2e81dc67'
    api_key = 'fd79a4d97543e35b2881a64b81b8f124'
    api_secret = 'NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3'

    asr = XunfeiASR(appid, api_key, api_secret)

    # 支持进度回调
    def on_progress(text: str):
        print(f"\r📝 当前识别: {text}", end="", flush=True)

    # 如果是MP3等格式，先转换
    print(f'audio_path:{audio_path}')
    audio_file = audio_path
    if audio_file.endswith('.pcm'):
        pcm_file = audio_file
    else:
        print(f"🔄 转换音频格式: {audio_file}")
        pcm_file = AudioConverter.convert_to_pcm(audio_file)

    try:
        result = asr.recognize(
            pcm_file,
            config=ASRConfig(language="zh_cn", accent="mandarin"),
            timeout=30,
            on_progress=on_progress
        )
        print(f"\n✅ 最终识别结果: {result}")
        return result
    except Exception as e:
        print(f'错误：{e}')
        logger.error(f"识别失败: {e}")


def demo_microphone_recognition():
    """演示：麦克风实时识别"""
    # 直接在函数中设置密钥（后续优化为其他方式）
    appid = '2e81dc67'
    api_key = 'fd79a4d97543e35b2881a64b81b8f124'
    api_secret = 'NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3'

    asr = XunfeiASR(appid, api_key, api_secret)

    def on_progress(text: str):
        print(f"\r📝 识别中: {text}", end="", flush=True)

    try:
        result = asr.recognize_microphone(
            record_seconds=5,
            on_progress=on_progress
        )
        print(f"\n✅ 识别结果: {result}")
    except Exception as e:
        logger.error(f"识别失败: {e}")


if __name__ == "__main__":

    demo_file_recognition()
