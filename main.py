import requests
import datetime
import pytz
import os

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0"
}  # 发送头信息
today = str(datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'))
[year, month, day] = today.split('-')
print([year, month, day])
if len(month) == 1:
    month = "0" + month
if len(day) == 1:
    day = "0" + day
req = requests.get(
    url=f"http://img.owspace.com/Public/uploads/Download/{year}/{month + day}.jpg", headers=header)
byte = req.content

# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client
# import sys
# import os
# import logging
#
# # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#
# secret_id = os.environ["COS_SECRET_ID"]
# secret_key = os.environ["COS_SECRET_KEY"]
# bucket_name = os.environ["COS_BUCKET_NAME"]
# region = 'ap-beijing'
# token = None
# scheme = 'https'
#
# config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# client = CosS3Client(config)
# response = client.put_object(
#     Bucket=bucket_name,  # Bucket 由 BucketName-APPID 组成
#     Body=byte,
#     Key="DailyChange/cos_calendar.jpg",
#     StorageClass='STANDARD',
#     ContentType='image/jpeg'
# )
from qiniu import Auth, put_data, build_batch_delete,BucketManager
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = os.environ["ACCESS_KEY"]
secret_key = os.environ["SECRET_KEY"]
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = os.environ["BUCKET_NAME"]
#上传后保存的文件名
key = f'DailyChange/calendar/ows{year}{month + day}.jpg'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

ret, info = put_data(token, key, byte)
print(info)
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
# bucket = BucketManager(q)
# ops = build_batch_delete(bucket_name, ["DailyChange/calendar/屏幕截图(3).png"])
# ret, info = bucket.batch(ops)
# print(info)