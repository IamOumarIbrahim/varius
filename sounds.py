# Silent SoundManager. Audio elements can be customized here later.

class SoundManager:
    def __init__(self):
        self.sfx_volume = 0.0
        self.music_volume = 0.0

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume

    def set_music_volume(self, volume):
        self.music_volume = volume

    def play(self, name):
        # Silent dummy action
        pass

    def start_music(self):
        # Silent dummy action
        pass

    def stop_music(self):
        # Silent dummy action
        pass
