import pygame
from sweepthat_config import Config
import sweepthat_game
import sweepthat_cardpoem

class Menu:
    def __init__(self) -> None:
        pygame.font.init()
        self.menu_bg = pygame.image.load("backgrounds/menu.gif")
        self.play_msg = "PLAY"
        self.cardpoem_msg = "CARD & POEM"
        self.quit_msg = "QUIT"
        self.small_font = pygame.font.Font(Config.FONT_PATH, 30)
        self.selected_option = 0
        self.running = True
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.mixer.music.load("asset/clicked sound.wav")
        pygame.display.set_caption("SWEEP THAT Game")


    def draw(self):
        self.screen.blit(self.menu_bg, (0, 0))

        msg_play = self.small_font.render(self.play_msg, True, Config.COLORS["BLACK"])
        msg_play_rect = msg_play.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 58))
        self.screen.blit(msg_play, msg_play_rect)

        msg_cardpoem = self.small_font.render(self.cardpoem_msg, True, Config.COLORS["BLACK"]) 
        msg_cardpoem_rect = msg_cardpoem.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 160))
        self.screen.blit(msg_cardpoem, msg_cardpoem_rect)

        msg_quit = self.small_font.render(self.quit_msg, True, Config.COLORS["BLACK"])
        msg_quit_rect = msg_quit.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 260))
        self.screen.blit(msg_quit, msg_quit_rect)

        pygame.display.flip()
        return msg_play_rect, msg_cardpoem_rect, msg_quit_rect


    def event(self, msg_play_rect, msg_cardpoem_rect, msg_quit_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if msg_play_rect.collidepoint(event.pos):
                        pygame.mixer.music.play()
                        sweepthat_game.Game().run()
                    elif msg_cardpoem_rect.collidepoint(event.pos):
                        pygame.mixer.music.play()
                        sweepthat_cardpoem.CNP().run()
                    elif msg_quit_rect.collidepoint(event.pos):
                        pygame.mixer.music.play()
                        pygame.quit()
                        quit()

    def run(self):
        while self.running:
            msg_play_rect, msg_cardpoem_rect, msg_quit_rect = self.draw()
            self.event(msg_play_rect, msg_cardpoem_rect, msg_quit_rect)
