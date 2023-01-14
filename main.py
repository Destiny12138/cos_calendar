import requests
import datetime

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
}  # 发送头信息
today = str(datetime.date.today())
[year, month, day] = today.split('-')
if len(month) == 1:
    month = "0" + month
if len(day) == 1:
    day == "0" + day
req = requests.get(
    url=f"http://img.owspace.com/Public/uploads/Download/{year}/{month + day}.jpg", headers=header)
byte = req.content
# print(byte)

# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = os.environ["COS_SECRET_ID"]
secret_key = os.environ["COS_SECRET_KEY"]
bucket_name = os.environ["COS_BUCKET_NAME"]
region = 'ap-beijing'
token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)
response = client.put_object(
    Bucket=bucket_name,  # Bucket 由 BucketName-APPID 组成
    Body=byte,
    Key="cos_calendar.jpg",
    StorageClass='STANDARD',
    ContentType='text/html; charset=utf-8'
)
if response["ETag"] is not None:
    try:
        url = 'https://sc.ftqq.com/SCT89587TadBaqqoSlrs5X1cNBnTUOghV.send'
        requests.post(url, data={'text': "成功"})
    except Exception as e:
        print("错误")