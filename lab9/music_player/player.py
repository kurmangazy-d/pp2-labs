import os
import pygame


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current_index = 0
        self.status = "Stopped"
        self.is_playing = False
        self.track_length = 1

    def load_current_track(self):
        current_track = self.playlist[self.current_index]
        pygame.mixer.music.load(current_track)

        try:
            sound = pygame.mixer.Sound(current_track)
            self.track_length = max(1, int(sound.get_length()))
        except:
            self.track_length = 1

    def play(self):
        self.load_current_track()
        pygame.mixer.music.play()
        self.status = "Playing"
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.status = "Stopped"
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_index])

    def get_position_seconds(self):
        position_ms = pygame.mixer.music.get_pos()
        if position_ms < 0:
            return 0
        return position_ms // 1000

    def get_progress_ratio(self):
        if self.track_length <= 0:
            return 0
        return min(1.0, self.get_position_seconds() / self.track_length)

    def update(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_track()