from openpibo.speech import Speech
from openpibo.audio import Audio

# 고정멘트(다시 한번만 ~등 추출을 위한 코드)


def tts(msg, filename):
    o_audio=Audio()
    o_speech = Speech()

    url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
    
    tts(f"<speak>\
                  <voice name='WOMAN_DIALOG_BRIGHT'>{msg}<break time='500ms'/></voice>\
                </speak>",filename)
    o_audio.play(filename, out='local', volume=500, background=False)       
    
    
if __name__=="__main__": 
    msg = "다시 한번만 말씀해주시겠어요?"
    tts(msg, "repeat.wav")
