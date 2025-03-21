import requests
import datetime
import pytz
import os

today = str(datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'))
[year, month, day] = today.split('-')
print([year, month, day])
if len(month) == 1:
    month = "0" + month
if len(day) == 1:
    day = "0" + day

from qiniu import Auth, put_data, build_batch_delete,BucketManager
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_KEY"]
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = os.environ["BUCKET_NAME"]

# 摸鱼日历
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
}  # 发送头信息
req = requests.get(
    url=f"https://api.vvhan.com/api/moyu", headers=header)
byte1 = req.content
key1= f'DailyChange/calendar/moyu{year}{month + day}.png'
token1 = q.upload_token(bucket_name, key1, 3600)
ret1, info1 = put_data(token1, key1, byte1)
print(info1)