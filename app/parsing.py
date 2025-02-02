from mss import mss
import easyocr
import pyautogui
from PIL import Image
import pyaudio
import wave
import time


class ScreenReader:
    def __init__(self):
        self.reader = easyocr.Reader(['ru'])
    
    def read(self, name):
        result = self.reader.readtext(name, allowlist='0123456789 ')
        for (bbox, text, procent) in result:
            if text is None:
                return '0'
            return str(text)
        
    def screen(self, region: dict, coords: list, names: list):
        time.sleep(3)
        with mss() as sct:
            screenshot = sct.grab(region)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            img.save("app/parse_pic/screenshot.png")

            for i in range(3):
                crop_box = (
                    coords[i][0],
                    coords[i][1],
                    coords[i][0] + coords[i][2],
                    coords[i][1] + coords[i][3]
                )
                cropped_img = img.crop(crop_box)
                cropped_img.save(names[i])
                
    def play_sound(self):
        wf = wave.open("app/sfx/sound.wav", "rb")
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()


def parsing(gold, elixir, dark_elixir, main_self):
    reader = ScreenReader()
    while not main_self.stop_event.is_set():
        reader.screen(
            region={
                "top": 150,
                "left": 95,
                "width": 200,
                "height": 160},
            coords=[
                (0, 0, 170, 40),
                (0, 55, 170, 40),
                (0, 110, 170, 40)],
            names=['app/parse_pic/gold.png',
                   'app/parse_pic/elixir.png',
                   'app/parse_pic/dark_elixir.png']
        )
        current_gold = int(reader.read('app/parse_pic/gold.png').replace(' ', ''))
        current_elixir = int(reader.read('app/parse_pic/elixir.png').replace(' ', ''))
        current_dark_elixir = int(reader.read('app/parse_pic/dark_elixir.png').replace(' ', ''))
        print(current_gold, current_elixir, current_dark_elixir)
        if current_gold >= gold and current_elixir >= elixir and current_dark_elixir >= dark_elixir:
            reader.play_sound()
            main_self.btn.setText('Старт')
            main_self.activated = False
            main_self.stop_event.set()
        else:
            pyautogui.press('B')
