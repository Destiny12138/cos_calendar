import datetime
import os

import pytz
import requests
from qiniu import Auth, BucketManager, put_data


date_code = datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y%m%d")
year = date_code[:4]
month = date_code[4:6]
day = date_code[6:8]
print([year, month, day])

access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_KEY"]
q = Auth(access_key, secret_key)
bucket_name = os.environ["BUCKET_NAME"]
bucket = BucketManager(q)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
}  # 发送头信息
image_prefix = "DailyChange/calendar/moyu"
image_extension = ".png"
min_image_bytes = 10 * 1024
upload_token_expires = 3600


def is_real_png(response):
    image_data = response.content
    if response.status_code != 200:
        print(f"摸鱼日历下载失败: HTTP {response.status_code}")
        return False
    if len(image_data) < min_image_bytes:
        print(f"摸鱼日历下载内容过小: {len(image_data)} bytes")
        return False
    if not image_data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("摸鱼日历下载内容不是 PNG 图片")
        return False
    return True


def upload_image(key, image_data):
    token = q.upload_token(bucket_name, key, upload_token_expires)
    ret, info = put_data(token, key, image_data)
    print(info)
    if ret is None or getattr(info, "status_code", None) != 200:
        raise RuntimeError(f"上传摸鱼日历图片到七牛失败: {info}")


def find_latest_image_key(target_key):
    marker = None
    candidates = []
    while True:
        ret, eof, info = bucket.list(bucket_name, image_prefix, marker, 1000, None)
        if ret is None:
            raise RuntimeError(f"列举七牛摸鱼日历历史图片失败: {info}")
        for item in ret.get("items", []):
            key = item.get("key")
            if not key or key == target_key or not key.endswith(image_extension):
                continue
            image_date = key[len(image_prefix):-len(image_extension)]
            if len(image_date) == 8 and image_date.isdigit() and image_date < date_code:
                candidates.append((image_date, key))
        marker = ret.get("marker")
        if eof or not marker:
            break
    if not candidates:
        raise RuntimeError("七牛空间中没有可复制的历史摸鱼日历图片")
    return max(candidates)[1]


def copy_latest_image(target_key):
    source_key = find_latest_image_key(target_key)
    print(f"复制历史摸鱼日历图片: {source_key} -> {target_key}")
    ret, info = bucket.copy(bucket_name, source_key, bucket_name, target_key, force="true")
    print(info)
    if ret is None or getattr(info, "status_code", None) != 200:
        raise RuntimeError(f"复制七牛历史摸鱼日历图片失败: {info}")


key = f"{image_prefix}{date_code}{image_extension}"

try:
    req = requests.get(url="https://api.yviii.com/moyu/moyu.php", headers=header, timeout=20)
except requests.RequestException as exc:
    print(f"摸鱼日历下载异常: {exc}")
    copy_latest_image(key)
else:
    if is_real_png(req):
        upload_image(key, req.content)
    else:
        copy_latest_image(key)
