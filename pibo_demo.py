from util_pibo import mySpeech

import pandas as pd
from question_parser import question_data

import threading

from openpibo.motion import Motion

import time


class pibo_motion(threading.Thread):
    def __init__(self, debug = False):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.o_motion = Motion()
        self.debug = debug
        
    def test(self, motion_name):
        print(motion_name)
        # motion_name : /home/pi/openpibo-examples/jungmin/breath.json

        ret = self.o_motion.get_motion("test", path=motion_name)
        print(ret)
        while True:
            self.o_motion.set_motion("test", path=motion_name)        
        
class pibo_speech(threading.Thread):
    def __init__(self, debug = False):
        threading.Thread.__init__(self)
        self.daemon = True

        self.o_speech = mySpeech()
        #self.o_motion = Motion()
        self.o_question = question_data("/home/pi/QnA/questions.txt")
        
        self.point = []
        self.debug = debug
        
    def demo(self, num = None):
        def record(reverse=False):
            res = self.o_speech.stt()
            if self.debug == True:
                print(res)
            if "네" in res or "그렇" in res or "맞아" in res or "있어" in res:
                if reverse == False:
                    return 5
                if reverse == True:
                    return 1
            elif "아니" in res or "없" in res or "아닌" in res or "아닙" in res:
                if reverse == False:
                    return 1
                if reverse == True:
                    return 5
            elif "모르" in res or "보통" in res:
                return 3
            else:
                msg = "다시 한 번만 말씀해 주시겠어요?"
                self.o_speech.tts(string=msg)
                #self.o_speech.tts(msg, "repeat1.wav")
                # self.o_speech.o_audio.play('repeat1.wav', out='local', volume=-1000, background=False)
                return record(reverse)
                
        if num == None:
            for d in self.o_question:
                category = d["category"]
                thresh = d["thresh"]
                question = d["question"]
                pos, neg = d["res"]
                
                points = 0

                for q in question:
                    if self.debug == True:
                        print(q)
                    self.o_speech.tts(string=q)
                    points += record()
                    
                    if self.debug == True:
                        print(points)
                    
                if points >= thresh:
                    if self.debug == True:
                        print(pos)
                    self.o_speech.tts(string=pos)
                else:
                    if self.debug == True:
                        print(neg)
                    self.o_speech.tts(string=neg)
                    
                break
        else:
            d = self.o_question[num]
            category = d["category"]
            thresh = d["thresh"]
            question = d["question"]
            pos, neg = d["res"]
            
            points = 0

            for q in question:
                if self.debug == True:
                        print(q)
                self.o_speech.tts(string=q)
                points += record()
                
                if self.debug == True:
                    print(points)
                
            if points >= thresh:
                if self.debug == True:
                    print(pos)
                self.o_speech.tts(string=pos)
            else:
                if self.debug == True:
                    print(neg)
                self.o_speech.tts(string=neg)
      
    

def demo():
    o_p_speech = pibo_speech(True)
    o_p_motion = pibo_motion(True)
    o_p_speech.start()
    o_p_motion.start()
    
    time.sleep(3)
    
    o_p_speech.demo(5)
    # time.sleep(10)
    
    # o_p_speech.demo(2)
    # time.sleep(10)
    
    # o_p_speech.demo(3)
    # time.sleep(10)  
      
    # o_p_speech.demo(4)
    # time.sleep(10)
    
    # o_p_speech.demo(5)
    # time.sleep(10)
    
    # o_p_speech.demo(6)
    # time.sleep(10)
    
    # o_p_speech.demo(6)
    # time.sleep(10)
    
    ### o_p_speech.demo(argument)
    # None argument : all category test
    # argument = 0~7 : 지지표현 ~ 비일관성 까지 카테고리(개별)
    
    import os
    #print(os.getcwd())
    #o_p_motion.test(f"{os.getcwd()}/breath.json")  # 이거 왜 안 돼 ..ㅠㅠ


if __name__ == "__main__":
    demo() 
    import time
    #import keyboard
    #o_p_motion=Motion()
    while True:
        #o_p_motion.set_motion(name="breath1", cycle=1)
        time.sleep(1)
        #if keyboard.read_key() == "q":
            #print("bye")
            #break
