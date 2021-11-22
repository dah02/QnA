import os, sys
import time

from threading import Thread

import openpibo
from openpibo.speech import Speech
from openpibo.audio import Audio

import requests
import json

import argparse

def mic(dst, timeout=5):
    if os.path.isfile(dst):
        os.remove(dst)
    cmd = f"arecord -D default -c2 -r 16000 -f S32_LE -d {timeout} -t wav -q -vv -V streo stream.raw;sox stream.raw -c 1 -b 16 {dst};rm stream.raw"
    os.system(cmd)
    audio_obj.play(filename=dst, out='local', volume=-2000)
    time.sleep(5)
    audio_obj.stop()
    
def kakao_stt(dst):
    kakao_account = "c4010fd08c325ded03991081577c935c"
    url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
    #headers = {'Content-Type':'application/octet-stliream', 'Authorization':'KakaoAK' + kakao_account}
    headers = {
      'Content-Type': 'application/octet-stliream',
      'Authorization': 'KakaoAK ' + kakao_account
    }
    with open(dst, 'rb') as f:
        data = f.read()
    res = requests.post(url, headers=headers, data=data)
    try:
      result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    except Exception as ex:
      result_json_string = res.text[res.text.index('{"type":"errorCalled"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    return result['value']
    
        
def stt(num):
    filename = f"stream{num}.wav"
    mic(filename)
    result = kakao_stt(filename)
    print(result)
    
def read_txt(filename):
    f=open(filename, 'r')
    output = []
    for num, line in enumerate(f.readlines()):
        line = line.rstrip('\n')
        if not len(line) == 0:
            output.append(line)
    return output
    
def kakao_tts(num, line):
    filename = f"tts{num}.mp3"
    speech_obj.tts(f"<speak>\
              <voice name='MAN_READ_CALM'>{line}<break time='500ms'/></voice>\
            </speak>",filename)
    audio_obj.play(filename, out='local', volume=-1500, background=False)
    
if __name__ == "__main__":
    #arg = argparse.ArgumentParser()
    questions = read_txt('questions.txt')
    audio_obj = Audio()
    speech_obj = Speech()
    for num, line in enumerate(questions):
        print(f"{num}, {line}")
        kakao_tts(num, line)
        #stt(num)
