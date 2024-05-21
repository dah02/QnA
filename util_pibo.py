import os, sys
import time

from threading import Thread

import openpibo
from openpibo.speech import Speech
from openpibo.audio import Audio
from openpibo.oled import Oled

import requests
import json

import argparse
import numpy as np

import os, sys

sys.path.append('/home/pi/Pibo_Package_02/Pibo_Conversation')
from data.text_to_speech import text_to_speech, TextToSpeech
from data.speech_to_text import speech_to_text
import data.behavior.behavior_list as behavior
import google



class mySpeech(Speech):
    
    def __init__(self):
        self.response = ''
        self.anwser = ''
        self.none = "None"
    
    def stt(self):        
        audio.audio_play("/home/pi/trigger.wav", 'local', '-1800', False)
        o.draw_image("/home/pi/Pibo_Package_02/Pibo_Conversation/data/behavior/icon/icon_recognition1.png"); o.show()
            
        try:
            self.response = speech_to_text(timeout=10)
            # self.response = input("input: ")
            
        except google.api_core.exceptions.DeadlineExceeded as e:
            print(e)
            self.response = self.none
        
        # 가끔 발생하는 Google API ERROR --> ignore
        except google.api_core.exceptions.Unknown as e:
            print(e)
            self.response = self.none
        
        except google.api_core.exceptions.InvalidArgument as e:
            print(e)
            self.response = self.none
        
        except ValueError as e:     # timeout 시간 넘으면 그냥 retry call 안 하고 중단시킴 (google/api_core/retry.py)
            print(e)                # Sleep generator stopped yielding sleep values.
            self.response = self.none
                
        # # 나오는 에러 싹 다 무시
        # except Exception as e:
        #     print(e)
        #     self.response = self.none
        
        # print(self.response)
        return self.response


    
    def tts(self, bhv='do_breath1', voice='nsujin', string=''):
        """
        * behavior: TTS 와 함께할 동작 ex. 'do_joy'
        * string: 발화할 TTS 내용
        """
        t = Thread(target=behavior.execute, args=([bhv]))
        t.start()
        
        while True:
            text_to_speech(voice='nsujin', text=string)
            break

o = Oled()
audio = TextToSpeech()
speech_obj = mySpeech()
# sp = speech_obj.speech_to_text()

# if __name__ == "__main__":

#     speech_obj = mySpeech()
#     speech_obj.tts(string="do")
