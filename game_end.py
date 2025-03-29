import pygame
import sweepthat_game
from sweepthat_config import Config
import sweepthat_menu

class GameEnd:
    def __init__(self, game_instance) -> None:
        self.game = game_instance # use same instanc
        self.menu = sweepthat_menu.Menu()
        self.user = self.game.user  
        self.oppo = self.game.oppo  
        self.choice_font = pygame.font.Font(Config.FONT_PATH, 25)

    def game_end(self):
        if self.user.user_score == 18: 
            bg = pygame.image.load("asset/WIN.png")
            self.game.screen.blit(bg, (0, 0))
        elif self.oppo.oppo_score == 18: 
            bg = pygame.image.load("asset/LOSE.png")
            self.game.screen.blit(bg, (0, 0))

        # Render text messages
        msg_newgame = self.choice_font.render("New Game", True, Config.COLORS["BLACK"]) 
        msg_newgame_rect = msg_newgame.get_rect(center=(Config.WIDTH // 2 - 275, Config.HEIGHT // 2 + 150))
        self.game.screen.blit(msg_newgame, msg_newgame_rect)
        
        msg_cnp = self.choice_font.render("Card&Poem", True, Config.COLORS["BLACK"]) 
        msg_cnp_rect = msg_cnp.get_rect(center=(Config.WIDTH // 2 - 10, Config.HEIGHT // 2 + 150))
        self.game.screen.blit(msg_cnp, msg_cnp_rect)
        
        msg_menu = self.choice_font.render("Menu", True, Config.COLORS["BLACK"]) 
        msg_menu_rect = msg_menu.get_rect(center=(Config.WIDTH // 2 + 250, Config.HEIGHT // 2 + 150))
        self.game.screen.blit(msg_menu, msg_menu_rect)

        pygame.display.flip()  

        # Handle mouse click events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # start game again
                    if msg_newgame_rect.collidepoint(event.pos):
                        self.game.run()
                    elif msg_cnp_rect.collidepoint(event.pos):
                        pass  # Handle Card & Poem button
                    elif msg_menu_rect.collidepoint(event.pos):
                        self.menu.run()

    def run(self):
        while True:
            self.game_end()