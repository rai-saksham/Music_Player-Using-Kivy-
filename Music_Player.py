from kivy.clock import Clock
# from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty
# StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
from kivy.app import App
import pydub
import pygame
import os
import time
from mutagen.mp3 import MP3
# from pydub import AudioSegment


pydub.AudioSegment.converter = r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
pygame.mixer.init()


class Player(BoxLayout):
    Songs = []
    stopped = True
    current_time = NumericProperty()
    global song
    global identity
    global num

    def scan_button(self):
        global b
        global x
        global song
        song = ''
        dir_path = os.path.dirname(os.path.realpath("C:/Users/USER/Music/"))
        try:
            if x > 1:
                pass
        except NameError:
            x = 1

        """for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.mp3'):
                    name = root + '/' + str(file)
                    self.Songs.append(name)

        for i in self.Songs:
            res = i[i.index('/') + 1:]
            song_name = str(x) + "." + res[:-4]
            b = ToggleButton(text=song_name, group="songlist", size_hint=(1, None),
                             height=dp(30), on_press=self.play)
            self.ids[i] = b
            x += 1
            self.ids.song_list.add_widget(b)"""

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.mp3'):
                    name = root + '/' + str(file)
                    self.Songs.append(name)

                    song_name = str(x) + "." + file[:-4]
                    b = ToggleButton(text=song_name, group="songlist", size_hint=(1, None),
                                     height=dp(30), on_press=self.play)
                    self.ids[name] = b
                    x += 1
                    self.ids.song_list.add_widget(b)

    def stop(self):
        global song
        if self.stopped:
            return
        elif self.Songs[0] == '':
            return
        elif song == '':
            return
        pygame.mixer.music.stop()
        self.ids[str(song)].state = 'normal'
        self.stopped = True
        self.reset()

    def play_song(self):
        global song
        global num
        if song == '':
            if self.Songs[0] == '':
                return
            else:
                song = self.Songs[0]
                num = 1
                self.ids[str(song)].state = 'down'
        pygame.mixer.music.load(song)
        self.ids[str(song)].state = 'down'
        pygame.mixer.music.play(loops=0)
        self.stopped = False

        song_mut = MP3(song)
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        self.ids.total_time.text = converted_song_length
        self.ids.progress_bar.max = song_length
        self.ids.progress_barEvent = Clock.schedule_interval(self.updateprogressbar, 1)
        self.settimeEvent = Clock.schedule_interval(self.settime, 1)
        self.slideEvent = Clock.schedule_interval(self.slide, 1)

    def play(self, instance):
        # print(str(instance.text), str(instance.state))
        global song
        global num
        num1 = instance.text.partition('.')
        num = int(num1[0])
        playing_song = self.Songs[num - 1]
        song = str(playing_song)
        # if instance.state == "down" and self.ids.progress_bar.value > 0:
        #     self.slide(song)
        if not self.stopped:
            self.stop()
        if instance.state == "down":
            self.play_song()
        elif instance.state == "normal":
            self.stop()
            return

    def updateprogressbar(self, value):
        if self.ids.progress_bar.value < self.ids.progress_bar.max:
            self.ids.progress_bar.value += 1

    def settime(self, t):
        current_time = time.strftime('%M:%S', time.gmtime(self.ids.progress_bar.value))
        self.ids.current_time.text = current_time

    def reset(self):
        self.ids.progress_barEvent.cancel()
        self.settimeEvent.cancel()
        self.slideEvent.cancel()
        self.ids.progress_bar.value = 0
        self.ids.current_time.text = "00:00"
        self.ids.total_time.text = "00:00"

    def slide(self, s):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=self.ids.progress_bar.value)
        self.stopped = False

    def previous_button(self):
        global song
        global num
        if song == '':
            return
        elif num <= 1:
            self.ids[str(song)].state = 'normal'
            num = len(self.Songs)
        else:
            self.ids[str(song)].state = 'normal'
            num -= 1
        playing_song = self.Songs[num - 1]
        song = str(playing_song)
        self.stop()
        self.play_song()

    def next_button(self):
        global song
        global num
        if song == '':
            return
        elif num >= len(self.Songs)-1:
            self.ids[str(song)].state = 'normal'
            num =1
        else:
            self.ids[str(song)].state = 'normal'
            num += 1
        playing_song = self.Songs[num - 1]
        song = str(playing_song)
        self.stop()
        self.play_song()

    def volume(self, widget):
        value = self.ids.vol.value
        pygame.mixer.music.set_volume(value)
        self.ids.current_vol.text = str(int(value))

    def separate(self):
        global song
        self.stop()


class Music_PlayerApp(App):
    pass


Music_PlayerApp().run()
