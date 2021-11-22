import os, sys
import time

from threading import Thread

import openpibo
from openpibo.speech import Speech
from openpibo.audio import Audio

import requests
import json

import argparse
import numpy as np


class mySpeech(Speech):
    def __init__(self, question = "questions/"):
        super().__init__()
        self.dir_question = question
        self.main_question = []
        self.level1_question = []
        self.read_txt()
        
    def my_mic(self, dst, timeout=5):
        if os.path.isfile(dst):
            os.remove(dst)
        #arecord -l 에서 카드가 잡혀야 함. (snd_rpi_simple_card)
        cmd = f"arecord -D plughw:2 -c1 -r 16000 -f S32_LE -d {timeout} -t wav -q -vv -V mono stream.raw;sox stream.raw -c 1 -b 16 {dst};rm stream.raw"
        os.system(cmd)
        audio_obj.play(filename=dst, out='local', volume=-2000)
        time.sleep(5)
        audio_obj.stop()
    
    def kakao_stt(self,dst):
        url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
        #headers = {'Content-Type':'application/octet-stliream', 'Authorization':'KakaoAK' + kakao_account}
        headers = {
          'Content-Type': 'application/octet-stliream',
          'Authorization': 'KakaoAK ' + self.kakao_account
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
    
        
    def my_stt(self,num):
        filename = f"stream{num}.wav"
        self.my_mic(filename)
        result = self.kakao_stt(filename)
        return result
    
    def read_txt(self):
        f0=open(f'{self.dir_question}/main.txt', 'r')
        f1=open(f'{self.dir_question}/level1.txt', 'r')
        
        for num, line in enumerate(f0.readlines()):
            line = line.rstrip('\n')
            if not len(line) == 0:
                self.main_question.append(line)
                
        for num, line in enumerate(f1.readlines()):
            line = line.rstrip('\n')
            l1_qustion=[]
            if not len(line) == 0:
                self.l1_question.append(line)
                
    def Q_sel(self, num, ch):
        filename = f"tts{num}{ch}.mp3"
        self.tts(f"<speak>\
                  <voice name='WOMAN_READ_CALM'>{line}<break time='500ms'/></voice>\
                </speak>",filename)
        audio_obj.play(filename, out='local', volume=-1500, background=False)
        
    def my_tts(self, num, line):
        filename = f"tts{num}.mp3"
        self.tts(f"<speak>\
                  <voice name='WOMAN_READ_CALM'>{line}<break time='500ms'/></voice>\
                </speak>",filename)
        audio_obj.play(filename, out='local', volume=-1500, background=False)
        
    def test(self):
        for num, line in enumerate(self.main_question):
            print(f"{num}, {line}")
            self.my_tts(num, line)
            #print(self.my_stt(num))
            
    def consult_demo(self):
        for num, line in enumerate(self.main_question):
            print(f"{num}, {line}")
            self.my_tts(num, line)
            res = self.my_stt(num)
            print(res)
            self.my_tts(num, '네, 그렇군요')
            if "그런 편" in res or "네" in res:
                self.my_tts(num, 'a')
                res = self.my_stt(num)      
            elif "아니오" in res or "않습" in res:
                self.my_tts(num, 'b')
            elif "모르" in res or "보통" in res:
                self.my_tts(num, 'b')  
            else:
                self.my_tts(num, "다시 한번 말씀해 주세요.")
                
            
    
if __name__ == "__main__":
    audio_obj = Audio()
    speech_obj = mySpeech()
    speech_obj.test()
