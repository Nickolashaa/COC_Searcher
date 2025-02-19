from PIL import Image
import pyaudio
import wave
import time
import os
import sys
from paddleocr import PaddleOCR


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ScreenReader:
    def __init__(self):
        os.system("cd platform-tools && adb connect 127.0.0.1:5555")
        self.ocr = PaddleOCR(lang='en', show_log=False)

    def read(self, name):
        result = self.ocr.ocr(resource_path(name), cls=False)
        if result[-1] is None:
            return 0
        num = result[-1][-1][-1][0]
        num = int(''.join([c for c in num if c.isdigit()]))
        return num

    def screen(self, region: tuple, coords: list, names: list):
        os.system(
            "cd platform-tools && adb -s 127.0.0.1:5555 shell screencap -p /sdcard/screen.png")
        os.system(
            "cd platform-tools && adb -s 127.0.0.1:5555 pull /sdcard/screen.png")
        img = Image.open(resource_path('platform-tools\\screen.png'))
        img = img.crop(region)
        for i in range(3):
            crop_box = (
                coords[i][0],
                coords[i][1],
                coords[i][0] + coords[i][2],
                coords[i][1] + coords[i][3]
            )
            cropped_img = img.crop(crop_box)
            cropped_img.save(resource_path(names[i]))

    def play_sound(self):
        wf = wave.open(resource_path("app\\sfx\\sound.wav"), "rb")
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

    def next(self):
        os.system(
            "cd platform-tools && adb -s 127.0.0.1:5555 shell input tap 1500 675")
        time.sleep(1.5)

    def reload(self):
        os.system("cd platform-tools && adb kill-server")
        os.system("cd platform-tools && adb start-server")
        os.system("cd platform-tools && adb connect 127.0.0.1:5555")


def parsing(gold, elixir, dark_elixir, main_self):
    print('Начинаю парсинг')
    while not main_self.stop_event.is_set():
        main_self.reader.screen(
            region=(80, 120, 230, 255),
            coords=[(0, 0, 150, 40), (0, 45, 150, 40), (0, 90, 150, 40)],
            names=[resource_path('app\\parse_pic\\gold.png'),
                   resource_path('app\\parse_pic\\elixir.png'),
                   resource_path('app\\parse_pic\\dark_elixir.png')]
        )
        print(1)
        current_gold = main_self.reader.read('app\\parse_pic\\gold.png')
        current_elixir = main_self.reader.read('app\\parse_pic\\elixir.png')
        current_dark_elixir = main_self.reader.read('app\\parse_pic\\dark_elixir.png')

        print(2)
        if not current_gold or not current_elixir or not current_dark_elixir:
            time.sleep(2.5)
            continue

        if not (current_gold >= gold and current_elixir >= elixir and current_dark_elixir >= dark_elixir):
            main_self.reader.next()
        else:
            main_self.reader.reload()
            main_self.reader.play_sound()
            main_self.btn.setText('Старт')
            main_self.activated = False
            main_self.stop_event.set()
            main_self.thread = None
            break
