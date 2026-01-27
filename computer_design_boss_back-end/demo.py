# -*- coding: utf-8 -*-
"""
面向对象版：讯飞图像识别 + 天行垃圾分类查询
"""
from __future__ import annotations

import base64
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
import http.client
import urllib.parse


# -------------------- 配置中心 --------------------
class Config:
    """所有可配参数集中管理"""
    XF_URL = "http://tupapi.xfyun.cn/v1/currency"
    XF_APPID = "2e81dc67"
    XF_API_KEY = "73a70da390a879f6e3ffead79552270d"

    TIANAPI_HOST = "apis.tianapi.com"
    TIANAPI_KEY = "1068d119011a4752c7fda4a2893da167"

    LABEL_JSON = Path(r"data.json")
    LOCAL_IMG = Path(r"img.png")


# -------------------- 工具函数 --------------------
def calc_xf_header(file_name: str) -> Dict[str, str]:
    """计算讯飞所需的 X-CheckSum 等头部"""
    cur_time = str(int(time.time()))
    param = {"image_name": file_name}
    param_b64 = base64.b64encode(json.dumps(param).encode()).decode()
    sign_str = (Config.XF_API_KEY + cur_time + param_b64).encode()
    checksum = hashlib.md5(sign_str).hexdigest()
    return {
        "X-CurTime": cur_time,
        "X-Param": param_b64,
        "X-Appid": Config.XF_APPID,
        "X-CheckSum": checksum,
    }


# -------------------- Service 层 --------------------
class XunfeiImageService:
    """调用讯飞图像识别接口"""

    @staticmethod
    def recognize(img_path: Path) -> Optional[str]:
        """
        返回识别到的 label_id（str），失败返回 None
        """
        file_name = img_path.name
        headers = calc_xf_header(file_name)
        img_bytes = img_path.read_bytes()

        resp = requests.post(Config.XF_URL, headers=headers, data=img_bytes)
        try:
            result = resp.json()
            label_id = str(
                result.get("data", {}).get("fileList", [{}])[0].get("label")
            )
            return label_id
        except Exception as e:
            print("解析讯飞结果失败：", e)
            return None


class TianapiTrashService:
    """调用天行垃圾分类接口"""

    @staticmethod
    def query_trash_info(name: str) -> Optional[List[Dict]]:
        """
        返回天行接口的 list 字段，失败返回 None
        """
        params = urllib.parse.urlencode({"key": Config.TIANAPI_KEY, "word": name})
        headers = {"Content-type": "application/x-www-form-urlencoded"}

        conn = http.client.HTTPSConnection(Config.TIANAPI_HOST)
        conn.request("POST", "/lajifenlei/index", params, headers)
        response = conn.getresponse().read().decode()
        try:
            data = json.loads(response)
            return data["result"]["list"]
        except Exception as e:
            print("天行接口解析失败：", e)
            return None


# -------------------- 业务 orchestrator --------------------
class TrashClassifier:
    """整个业务流程的调度器"""

    def __init__(self) -> None:
        # 加载本地 id→label 映射
        with Config.LABEL_JSON.open(encoding="utf-8") as f:
            # print(666666)
            records = json.load(f)["工作表1"]
        self.id2label: Dict[str, str] = {str(item["id"]): item["label"] for item in records}

    def run(self, img_path: Optional[Path] = None):
        img_path = img_path or Config.LOCAL_IMG

        # 1. 讯飞识别
        label_id = XunfeiImageService.recognize(img_path)
        label_name = self.id2label.get(label_id, "未知类别")
        print(label_name)
        return_str_1 = f"图像识别结果：{label_name}\n"

        # 2. 天行查询
        info_list = TianapiTrashService.query_trash_info(label_name)
        if not info_list:
            return_str_2 = "未查到分类信息"
            return return_str_2

        # 3. 打印结果
        item = info_list[0]
        return_str_3 = f"分类：{item['explain']}\n处理建议：{item['tip']}\n"
        return_str = return_str_1+return_str_3
        return return_str

def garbage_classification(img_path):
    print(333333)
    classifier = TrashClassifier()
    print(444444)
    return_str = classifier.run(Path(img_path))
    print(555555)
    return return_str

# -------------------- 入口 --------------------
if __name__ == "__main__":
    classifier = TrashClassifier()
    classifier.run(Path('img.png'))

    # ai_response = think_speaker.think_speak(user_message)
    # ai_response_data = json.load(ai_response)
    # ai_response_answer = [item["content"] for item in ai_response_data if item["role"] == "assistant"]
    # print(f"ai_response_answer:{ai_response_answer}")