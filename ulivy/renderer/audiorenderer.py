emap = {
    "select": "se/gui_sel_cursor.ogg",
    "confirm": "se/gui_sel_decision.ogg",
    "cancel": "se/gui_sel_cancel.ogg",
    "menuopen": "se/gui_menu_open.ogg",
    "menuclose": "se/gui_menu_close.ogg",
    "spotted": "se/exclaim.wav",
    "receive": "se/pkmn_move_learnt.ogg",
    "buy": "se/mart_buy_item.ogg",
}

SOUND_EFFECT_CHANNELS = 8
VOLUME = 0.05
VOLUME_MUSIC = 0.07


from kivy.utils import platform

if platform == "android":
    from kivy.core.audio import SoundLoader

    from kivy.core.audio.audio_android import SoundAndroidPlayer as SoundFX
    from kivy.core.audio.audio_android import SoundAndroidPlayer as SoundMusic
else:
    vibrator = None
    from kivy.core.audio.audio_sdl2 import SoundSDL2 as SoundFX
    from kivy.core.audio.audio_sdl2 import MusicSDL2 as SoundMusic


class AudioRenderer:
    def __init__(self, gui):
        self.game = gui
        self.silent = False

        self.current_music = ""

        self.se_id = 0

        self.cache_se = {}

        self.music = None
        self.music_name = ""

        self.emap = {}
        for k, v in emap.items():
            sound_file = self.game.m_res.get_sound(v)
            if sound_file:
                if platform == "android":
                    self.emap[k] = SoundLoader.load(sound_file)
                else:
                    emap[k] = sound_file
                    self.emap[k] = SoundFX(source=sound_file)
                    self.emap[k].load()

    def on_tick(self, time, frame_time):
        return
        pyglet.clock.tick()

    def preload_effect(self, name):
        # Deprecated
        return None

    def play_preload(self, eff):
        # Deprecated
        return

    def get_effect_preload(self, name):
        if not name:
            return
        # if name in self.emap:
        #     sound = self.emap[name]
        # else:
        sound = None
        sound_file = self.game.m_res.get_sound(name)

        if sound_file:
            if platform == "android":
                sound = SoundLoader.load(sound_file)
            else:
                sound = SoundFX(source=sound_file)  # SoundLoader.load(sound_file)
                sound.load()

        if sound:
            # sound.loop = False
            return sound
        else:
            print("SOUND NOT FOUND: ", name)
            return None

    def play_effect(self, name):
        if not name:
            return
        sound = None

        if name in self.emap:
            sound = self.emap[name]
        else:
            if name in emap:
                sound_file = emap[name]
            else:
                sound_file = self.game.m_res.get_sound(name)

            if sound_file:
                if platform == "android":
                    sound = SoundLoader.load(sound_file)
                else:
                    sound = SoundFX(source=sound_file)  # SoundLoader.load(sound_file)
                    sound.load()

        if sound:
            # sound.loop = False
            sound.play()
        else:
            print("SOUND NOT FOUND: ", name)

    def effect(self, name):
        self.play_effect(name)

    def cache_effect(self, name):
        return
        if self.silent:
            return
        try:
            if name not in self.cache_se:
                self.cache_se[name] = self.game.m_res.get_sound(name)
        except Exception as e:
            print("Music exception:", e)

    def play_music(self, name, loop=True):
        if self.music_name == name:
            return
        self.music_name = name

        if self.music is not None:
            print("stopping")
            self.music.stop()
            print("stopped")

        self.music = None
        sound_file = self.game.m_res.get_sound(name)

        if sound_file:
            if platform == "fandroid":
                self.music = SoundLoader.load(sound_file)
            else:
                self.music = SoundMusic(source=sound_file)
                self.music.load()

        if self.music:
            self.music.loop = loop
            self.music.play()
        else:
            self.music = None
            print("MUSIC NOT FOUND: ", name)

    # @property
    # def se_player(self):
    #     return self.se_players[self.se_id]
