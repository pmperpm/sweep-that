import pygame
import tkinter as tk
import subprocess
import sys
from sweepthat_config import Config
import sweepthat_game
import sweepthat_cardpoem
import sweepthat_stats

class Menu:
    def __init__(self) -> None:
        pygame.font.init()
        self.__menu_bg = pygame.image.load("backgrounds/menubg.png")
        self.__play_msg = "PLAY"
        self.__cardpoem_msg = "CARD & POEM"
        self.__stats_msg = "STATS"
        self.__quit_msg = "QUIT"
        self.__small_font = pygame.font.Font(Config.FONT_PATH, 30)
        self.__selected_option = 0
        self.__running = True
        self.__SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.__SONG_END)
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.mixer.music.load("asset/clicked sound.wav")
        pygame.display.set_caption("SWEEP THAT Game")


    def draw(self):
        self.screen.blit(self.__menu_bg, (0, 0))

        msg_play = self.__small_font.render(self.__play_msg, True, Config.COLORS["BLACK"])
        msg_play_rect = msg_play.get_rect(center=(Config.WIDTH // 2 + 177, Config.HEIGHT // 2 - 190))
        self.screen.blit(msg_play, msg_play_rect)

        msg_cardpoem = self.__small_font.render(self.__cardpoem_msg, True, Config.COLORS["BLACK"]) 
        msg_cardpoem_rect = msg_cardpoem.get_rect(center=(Config.WIDTH // 2 + 177, Config.HEIGHT // 2 - 55))
        self.screen.blit(msg_cardpoem, msg_cardpoem_rect)

        msg_stats = self.__small_font.render(self.__stats_msg, True, Config.COLORS["BLACK"])
        msg_stats_rect = msg_stats.get_rect(center=(Config.WIDTH // 2 + 177, Config.HEIGHT // 2 + 85))
        self.screen.blit(msg_stats, msg_stats_rect)

        msg_quit = self.__small_font.render(self.__quit_msg, True, Config.COLORS["BLACK"])
        msg_quit_rect = msg_quit.get_rect(center=(Config.WIDTH // 2 + 177, Config.HEIGHT // 2 + 220))
        self.screen.blit(msg_quit, msg_quit_rect)

        pygame.display.flip()
        return msg_play_rect, msg_cardpoem_rect, msg_quit_rect, msg_stats_rect
    
    def handle_stats(self):
        try:
            subprocess.Popen([sys.executable, "sweepthat_stats.py"])
            sweepthat_stats.App
        except Exception as e:
            print(f"Error loading stats: {e}")


    def event(self, msg_play_rect, msg_cardpoem_rect, msg_quit_rect, msg_stats_rect):
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
                        sweepthat_cardpoem.CNP(self.screen).run()
                    elif msg_stats_rect.collidepoint(event.pos):
                        pygame.mixer.music.play()
                        self.handle_stats()
                    elif msg_quit_rect.collidepoint(event.pos):
                        pygame.mixer.music.play()
                        pygame.quit()
                        quit()

    def run(self):
        while self.__running:
            msg_play_rect, msg_cardpoem_rect, msg_quit_rect, msg_stats_rect = self.draw()
            self.event(msg_play_rect, msg_cardpoem_rect, msg_quit_rect, msg_stats_rect)
