import os
import pygame
from player import MusicPlayer


def get_music_files(folder):
    supported_formats = (".mp3", ".wav", ".ogg")
    files = []

    if not os.path.exists(folder):
        return files

    for file_name in os.listdir(folder):
        if file_name.lower().endswith(supported_formats):
            files.append(os.path.join(folder, file_name))

    files.sort()
    return files


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((700, 400))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    music_folder = os.path.join(os.path.dirname(__file__), "music")
    playlist = get_music_files(music_folder)

    if not playlist:
        print("No music files found in the music folder.")
        pygame.quit()
        return

    player = MusicPlayer(playlist)

    font1 = pygame.font.SysFont("Arial", 30)
    font2 = pygame.font.SysFont("Arial", 22)
    font3 = pygame.font.SysFont("Arial", 18)

    running = True
    while running:
        screen.fill((30, 30, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False

        player.update()

        title = font1.render("Music Player", True, (255, 255, 255))
        screen.blit(title, (250, 20))

        track_text = font2.render("Current Track: " + player.get_current_track_name(), True, (200, 220, 255))
        screen.blit(track_text, (40, 90))

        status_text = font2.render("Status: " + player.status, True, (255, 220, 180))
        screen.blit(status_text, (40, 130))

        position_text = font2.render("Position: " + str(player.get_position_seconds()) + " sec", True, (180, 255, 180))
        screen.blit(position_text, (40, 170))

        pygame.draw.rect(screen, (80, 80, 80), (40, 220, 600, 25))
        progress_width = int(600 * player.get_progress_ratio())
        pygame.draw.rect(screen, (100, 220, 120), (40, 220, progress_width, 25))

        controls = [
            "Keyboard Controls:",
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit"
        ]

        y = 280
        for line in controls:
            text = font3.render(line, True, (230, 230, 230))
            screen.blit(text, (40, y))
            y += 24

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()