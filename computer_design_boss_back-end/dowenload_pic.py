import os
import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def download_images(num_images=130, folder='user_pic', max_retries=3):
    """
    从 Lorem Picsum 下载指定数量的随机图片并保存到文件夹中。
    包含重试机制和请求头模拟，提高稳定性。

    参数:
        num_images (int): 要下载的图片数量，默认为 35。
        folder (str): 保存图片的文件夹名，默认为 'downloaded_images'。
        max_retries (int): 单张图片的最大重试次数，默认为 3。
    """
    os.makedirs(folder, exist_ok=True)

    # 设置带重试策略的会话
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1,          # 重试间隔：1, 2, 4 秒
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的 HTTP 状态码
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # 模拟浏览器请求头，避免被简单拒绝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 图片基础 URL（每次请求会返回不同图片）
    base_url = "https://picsum.photos/300/200"

    success_count = 0
    for i in range(1, num_images + 1):
        # 添加随机参数避免缓存，并加上时间戳确保唯一性
        url = f"{base_url}?random={i}&t={int(time.time() * 1000)}"

        for attempt in range(1, max_retries + 1):
            try:
                print(f"正在下载第 {i} 张图片 (尝试 {attempt}/{max_retries})...")
                response = session.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                # 从响应头获取图片格式
                content_type = response.headers.get('content-type', '').lower()
                if 'image/jpeg' in content_type:
                    ext = 'jpg'
                elif 'image/png' in content_type:
                    ext = 'png'
                elif 'image/gif' in content_type:
                    ext = 'gif'
                elif 'image/webp' in content_type:
                    ext = 'webp'
                else:
                    ext = 'jpg'
                    print(f"  警告：无法识别图片格式，默认保存为 .{ext}")

                # 构造文件名
                filename = f"user_pic_{i:02d}.{ext}"
                filepath = os.path.join(folder, filename)

                # 保存图片
                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"  成功保存: {filename}")
                success_count += 1
                break  # 成功则跳出重试循环

            except requests.exceptions.RequestException as e:
                print(f"  下载失败 (尝试 {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    print(f"  跳过第 {i} 张图片，已达到最大重试次数。")
                else:
                    # 随机延迟，避免同时重试造成冲突
                    delay = random.uniform(1, 3)
                    time.sleep(delay)

        # 每张图片后稍作停顿，降低请求频率
        time.sleep(random.uniform(0.5, 1.5))

    print(f"\n下载完成！成功保存 {success_count} 张图片到文件夹 '{folder}' 中。")

if __name__ == "__main__":
    download_images()