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
    def __init__(self):
        super().__init__()
        self.o_audio=Audio()
        self.debug = False
        
    def my_mic(self, dst, timeout=5):
        if os.path.isfile(dst):
            os.remove(dst)
        #arecord -l 에서 카드가 잡혀야 함. (snd_rpi_simple_card)
        #cmd = f"arecord -D default -c1 -r 16000 -f S32_LE -d {timeout} -t wav -q -vv -V mono stream.raw;sox stream.raw -c 1 -b 16 {dst};rm stream.raw"
        cmd = f"arecord -D plughw:2 -c1 -r 16000 -f S32_LE -d {timeout} -t wav -q -vv -V mono stream.raw;sox stream.raw -c 1 -b 16 {dst};rm stream.raw"
        #cmd = f"arecord -D dmic_sv -c2 -r 48000 -f S32_LE -d {timeout} -t wav -q -vv -V mono stream.raw;sox stream.raw -c 1 -b 16 {dst};rm stream.raw"
        os.system(cmd)
        
        if self.debug:
            self.o_audio.play(filename=dst, out='local', volume=-1000, background=False)
            time.sleep(5)
            self.o_audio.stop()
    
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
    
        
    def my_stt(self, filename="stream.wav"):
        self.my_mic(filename)
        result = self.kakao_stt(filename)
        return result

    def my_tts(self, line, filename="stream.wav"):
        self.tts(f"<speak>\
                  <voice name='WOMAN_DIALOG_BRIGHT'>{line}<break time='500ms'/></voice>\
                </speak>",filename)
        self.o_audio.play(filename, out='local', volume=500, background=False)       
    
if __name__ == "__main__":

    speech_obj = mySpeech()
    speech_obj.test()
