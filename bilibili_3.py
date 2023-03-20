import requests
import re
import json
import pprint
import subprocess

Bv = input("请输入连接或bv号：")
headers = {
    'referer':'https://www.bilibili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}
def get_response(url):
    response = requests.get(url = url,headers=headers)
    return response

url = Bv
if Bv[:4] == 'http':
    url = Bv
elif Bv[:2] == 'BV':
    url = f'https://www.bilibili.com/video/{Bv}'
else :
    url = f'http://{Bv}'


response = get_response(url)
title = re.findall('<title data-vue-meta="true">(.*?)',response.text)[0]  # findall返回的为列表，变为字符串加[0]
play_info = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
json_data = json.loads(play_info)


audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
video_url = json_data['data']['dash']['video'][0]['baseUrl']
audio_content = requests.get(url = audio_url,headers=headers).content
video_content = requests.get(url = video_url,headers=headers).content

with open(title +'.mp3',mode = 'wb') as f:
    f.write(audio_content)
with open(title +'.mp4',mode='wb') as f1:
    f1.write(video_content)

COMMAND = f'ffmpeg -i {title}.mp4 -i {title}.mp3 -c:v copy -c:a aac -strict experimental {title}output.mp4'
# COMMAND = f'ffmpeg -i video\\{title}.mp4 -i video\\{title}.mp3 -c copy video\\{title}output.mp4'
subprocess.run(COMMAND,shell=True)










