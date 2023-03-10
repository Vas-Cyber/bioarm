import os #библиотека для озвучки
import pyaudio #библиотека для определения голоса
import serial #библиотека для работы с портами и передачей информации по ним
import time #библиотека для временных задержек
import vosk 
from vosk import Model, KaldiRecognizer #библиотека для распознавания речи
import beepy
from rhvoice_wrapper import TTS #библиотека 
import subprocess
import openai


def asdf():
    recognizer = KaldiRecognizer(model,16000)
    cap = pyaudio.PyAudio()
    stream = cap.open(format=pyaudio.paInt16,
                      channels = 1,
                      rate=16000,
                      input=True,
                      frames_per_buffer=8192
                        )
    beepy.beep(sound="coin")
    stream.start_stream()
    while True:
        data = stream.read(4096)
        if len(data) == 0:
            break
        
        if recognizer.AcceptWaveform(data):
            s = recognizer.Result()[14:]
            return(s[:-3])
            break



def palm(): #функция для передачи команды на плату Arduino uno
    ser = serial.Serial('/dev/rfcomm0', 9600)
    k = 0

    while 1:
        ser.write(b'1\n')
        k += 1
        if k > 1:
            break

def chat():
    openai.api_key = "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"
    model_engine = "text-davinci-003"
    prompt = asdf()
    data = tts.get("Минутку, я думаю", voice="elena", format_="wav")
    subprocess.check_output(['aplay', '-q'], input=data)

    max_tokens = 128

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    
    data = tts.get("Ответ", voice="elena", format_="wav")
    subprocess.check_output(['aplay', '-q'], input=data)

   
    data = tts.get(completion.choices[0].text, voice="elena", format_="wav")
    subprocess.check_output(['aplay', '-q'], input=data)



model = Model(model_name="vosk-model-small-ru-0.22")
recognizer = KaldiRecognizer(model,16000)
language = 'ru'
tts = TTS(threads=1)

while True:
    query = asdf()
    print(query)
    if "привет" in query :
        data = tts.get('Привет! Чем могу быть полезна?', voice="elena", format_='wav')
        subprocess.check_output(['aplay', '-q'], input=data)
        while True:
            query = asdf()
            print(query)
            if "ладонь" in query:
                print("m")
                palm()
            elif "поиск" in query:
                print("query")
                chat()
            elif "пока" in query:
                print("...")
                break
            else:
                continue