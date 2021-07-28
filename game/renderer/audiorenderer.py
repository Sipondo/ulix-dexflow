import pyglet

pyglet.options["audio"] = ("openal", "pulse", "directsound", "silent")
from pyglet.media import Player, StaticSource, load
from pathlib import Path

# TODO prebuffered audio


emap = {
    "select": "SE/GUI sel cursor.ogg",
    "confirm": "SE/GUI sel decision.ogg",
    "cancel": "SE/GUI sel cancel.ogg",
    "menuopen": "SE/GUI menu open.ogg",
    "menuclose": "SE/GUI menu close.ogg",
    "spotted": "SE/Exclaim.wav",
    "receive": "SE/Pkmn move learnt.ogg",
    "buy": "SE/Mart buy item.ogg",
}

SOUND_EFFECT_CHANNELS = 8
VOLUME = 0.0
VOLUME_MUSIC = 0.7


class AudioRenderer:
    def __init__(self, gui):
        self.game = gui
        self.silent = False

        self.bgm_player = pyglet.media.Player()
        self.current_music = ""
        self.se_players = [pyglet.media.Player() for _ in range(SOUND_EFFECT_CHANNELS)]
        self.se_id = 0

        self.cache_se = {}

    def on_tick(self, time, frame_time):
        pyglet.clock.tick()

    def preload_effect(self, name):
        # Deprecated
        return None

    def play_preload(self, eff):
        # Deprecated
        return

    def play_effect(self, name):
        if name in emap:
            name = emap[name]
        if self.silent:
            return
        try:
            # name = "ME/Battle victory.ogg"
            self.se_player.loop = False
            self.se_player.volume = 0.4 * VOLUME
            # sound = pyglet.media.load(str(self.p_audio / name), streaming=True)
            if name not in self.cache_se:
                self.cache_se[name] = self.game.m_res.get_sound(name)
            sound = self.cache_se[name]
            self.se_player.queue(sound)
            if self.se_player.playing:
                self.se_player.next_source()
            self.se_player.play()
            self.se_id = (self.se_id + 1) % len(self.se_players)
        except Exception as e:
            print("Music exception:", e)

    def effect(self, name):
        self.play_effect(name)

    def cache_effect(self, name):
        if self.silent:
            return
        try:
            if name not in self.cache_se:
                self.cache_se[name] = self.game.m_res.get_sound(name)
        except Exception as e:
            print("Music exception:", e)

    def play_music(self, name):
        if self.silent:
            return
        if self.current_music != name:
            # name = "ME/Battle victory.ogg"
            # self.bgm_player.loop = True
            # self.bgm_player.eos_action = "loop"
            self.bgm_player.volume = 0.4 * VOLUME * VOLUME_MUSIC
            # music = pyglet.media.load(str(self.p_audio / name), streaming=True)
            music = self.game.m_res.get_sound(name)
            if music is not None:
                self.bgm_player.queue(music)
                # self.bgm_player.queue(music)
                if self.bgm_player.playing:
                    self.bgm_player.next_source()
                self.bgm_player.play()
                self.current_music = name
            else:
                print("MUSIC NOT FOUND: ", name)

    @property
    def se_player(self):
        return self.se_players[self.se_id]
