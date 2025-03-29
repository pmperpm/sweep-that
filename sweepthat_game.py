# sweepthat_game.py
import pygame
from sweepthat_config import Config
from sweepthat_classes import *
from sweepthat_menu import *
from game_end import GameEnd

class Game(Menu):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.font.init()
        # self.asset = Asset()
        self.total_time = 0
        self.message_end_time = 0
        self.user = User()
        self.oppo = Opponent()
        self.oppo_acted = False
        self.count_time = 0
        self.start_time = 0
        self.MUSIC_END = pygame.USEREVENT + 1
        self.board = Board()
        self.is_counting = False
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        self.font = pygame.font.Font(Config.FONT_PATH, 70)
        self.small_font = pygame.font.Font(Config.FONT_PATH, 30)
        self.medium_font = pygame.font.Font(Config.FONT_PATH, 50)

        # self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        # pygame.display.set_caption("SWEEP THAT Game")
        self.piece_manager = PieceManager(self.board)
        self.player_selected_card = None
        self.running = True
        self.game_message, self.oppo_score_msg = "", ""
        self.user_score_msg = ""
        self.last_click_time = pygame.time.get_ticks()

        # Memorization var
        self.mem_time = 0 # memorize time to count
        self.mem_start_t = 0
        self.in_mem_phase = False
        self.mem_complete = False
        self.confirm = False
        self.selecting_mem_time = True  # New state for time selection
        self.time_options = [
            {"text": "3 minutes", "time": 3 * 60 * 1000, "rect": None},
            {"text": "5 minutes", "time": 5 * 60 * 1000, "rect": None},
            {"text": "SKIP", "time": 0, "rect": None}
        ]

    def draw_time_selection(self):
        # select time
        title_text = self.medium_font.render("Select memorization time:", True, Config.COLORS["BLACK"])
        self.screen.blit(title_text, (Config.WIDTH//2 - title_text.get_width()//2, Config.HEIGHT//2 - 100))

        # Draw time 
        for i, option in enumerate(self.time_options):
            text = self.small_font.render(option["text"], True, Config.COLORS["BLACK"])
            rect = pygame.Rect(Config.WIDTH//2 - 100, Config.HEIGHT//2 + i*60, 200, 50)
            option["rect"] = rect  # Store rect for click detection
            
            # Draw button
            pygame.draw.rect(self.screen, Config.COLORS["WHITE"], rect)
            pygame.draw.rect(self.screen, Config.COLORS["DARK_GREEN"], rect, 2)
            self.screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

    def draw_countdown(self, remaining_time):
        min = remaining_time // 60000
        sec = (remaining_time % 60000) // 1000
        t_text = f"{min:02d}:{sec:02d}"
        count_text = self.medium_font.render(t_text, True, Config.COLORS["BLACK"])
        prompt_text = self.small_font.render("Memorize the card positions!", True, Config.COLORS["BLACK"])
        
        count_bg = pygame.Surface((300, 100), pygame.SRCALPHA)
        count_bg.fill((255, 255, 255, 128))
        
        self.screen.blit(count_bg, (Config.WIDTH//2 - 150, Config.HEIGHT - 120))
        self.screen.blit(prompt_text, (Config.WIDTH//2 - prompt_text.get_width()//2, Config.HEIGHT - 110))
        self.screen.blit(count_text, (Config.WIDTH//2 - count_text.get_width()//2, Config.HEIGHT - 80))

    def draw_start_prompt(self):
        prompt_text = self.medium_font.render("Memorization time complete!", True, Config.COLORS["BLACK"])
        inst_text = self.small_font.render("Press ENTER to start the game", True, Config.COLORS["BLACK"])
        
        prompt_bg = pygame.Surface((500, 150), pygame.SRCALPHA)
        prompt_bg.fill((255, 255, 255, 180))
        
        self.screen.blit(prompt_bg, (Config.WIDTH//2 - 250, Config.HEIGHT//2 - 75))
        self.screen.blit(prompt_text, (Config.WIDTH//2 - prompt_text.get_width()//2, Config.HEIGHT//2 - 50))
        self.screen.blit(inst_text, (Config.WIDTH//2 - inst_text.get_width()//2, Config.HEIGHT//2 + 10))

    def run(self):
        while self.running:
            self.screen.fill(Config.COLORS["LIGHT_BROWN"])
            self.board.draw(self.screen)

            # Time selection
            if self.selecting_mem_time:
                self.draw_time_selection()
            
            # Memorization phase
            elif self.in_mem_phase:
                current_time = pygame.time.get_ticks()
                elapsed = current_time - self.mem_start_t
                remaining = max(0, self.mem_time - elapsed)
                
                self.draw_countdown(remaining)
                
                if remaining <= 0 and not self.confirm:
                    self.in_mem_phase = False
                    self.confirm = True
            
            # Waiting for confirm
            elif self.confirm:
                self.draw_start_prompt()
            
            # Main game 
            elif self.mem_complete:
                if self.game_message:
                    msg_text = self.font.render(self.game_message, True, Config.COLORS["BLACK"])
                    msg_rect = msg_text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
                    self.screen.blit(msg_text, msg_rect)

                # msg_text_small = self.small_font.render(self.game_message_small, True, Config.COLORS["BLACK"])
                # msg_rect_small = msg_text_small.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 80))
                # self.screen.blit(msg_text_small, msg_rect_small)

                msg_user_score = self.small_font.render(str(self.user_score_msg), True, Config.COLORS["WHITE"])
                msg_rect_user_score = msg_user_score.get_rect(center=(Config.WIDTH // 2 + 50, Config.HEIGHT // 2 + 120))
                self.screen.blit(msg_user_score, msg_rect_user_score)
                self.user_score_msg = self.user.user_score

                msg_oppo_score = self.small_font.render(str(self.oppo_score_msg), True, Config.COLORS["WHITE"])
                msg_rect_oppo_score = msg_oppo_score.get_rect(center=(Config.WIDTH // 2 + 50, Config.HEIGHT // 2 - 135))
                self.screen.blit(msg_oppo_score, msg_rect_oppo_score)
                self.oppo_score_msg = self.oppo.oppo_score

                ############## GAME PART #############
                if self.message_end_time != 0 and pygame.time.get_ticks() > self.message_end_time:
                    self.game_message = ''
                    self.game_message_small = ''
                    self.message_end_time = 0
                    if self.user.user_score == 18 or self.oppo.oppo_score == 18:
                        GameEnd(self).run()
                        self.running = False
                        break
                    else:
                        self.continue_game()

                # Check for inactivity
                if self.player_selected_card is None:
                    if pygame.time.get_ticks() - self.last_click_time > 20000:
                        self.oppo.oppo_score += 1
                        self.oppo_score_msg = self.oppo.oppo_score
                        self.game_message = "Opponent CORRECT !"
                        print(f'Opponent correct!  Oppo score: {self.oppo.oppo_score}')
                        # Set the card and sound
                        # clicked_card.visible = False
                        self.piece_manager.board.cards[self.piece_manager.sound.correct_index].visible = False
                        print(f'before : {self.piece_manager.sound.correct_index}')
                        self.piece_manager.sound.correct_index = None
                        print(f'after : {self.piece_manager.sound.correct_index}')
                        self.game_message_small = "game will start again in ..."
                        self.message_end_time = pygame.time.get_ticks() + 2000
                        self.oppo_acted = True
                        if self.user.user_score == 18 or self.oppo.oppo_score == 18:
                            GameEnd(self).run()
                            self.running = False
                            break
                        else:
                            self.continue_game()
                        pygame.mixer.music.stop()
                        self.last_click_time = pygame.time.get_ticks()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Time selection
                elif event.type == pygame.MOUSEBUTTONDOWN and self.selecting_mem_time:
                    for option in self.time_options:
                        if option["rect"] and option["rect"].collidepoint(event.pos):
                            self.mem_time = option["time"]
                            self.selecting_mem_time = False
                            if self.mem_time > 0:
                                self.in_mem_phase = True
                                self.mem_start_t = pygame.time.get_ticks()
                            else:
                                self.mem_complete = True
                                self.piece_manager.play_next_sound()
                
                # Start confirm
                elif event.type == pygame.KEYDOWN and self.confirm:
                    if event.key == pygame.K_RETURN:
                        self.confirm = False
                        self.mem_complete = True
                        self.piece_manager.play_next_sound()
                        self.last_click_time = pygame.time.get_ticks()

                ################ CARD GAME ##############
                elif self.mem_complete and not self.confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.player_selected_card = self.piece_manager.get_selected_piece(event.pos)
                        # self.player_selected_card = self.piece_manager.get_selected_piece(event.pos)
                        if self.player_selected_card is not None:
                            self.last_click_time = pygame.time.get_ticks()
                            clicked_card = self.piece_manager.board.cards[self.player_selected_card]

                            if self.player_selected_card == self.piece_manager.sound.correct_index:
                                print(f'Correct! Clicked index: {self.player_selected_card}, Correct index: {self.piece_manager.sound.correct_index}')
                                self.user.user_score += 1
                                clicked_card.visible = False
                                print(f'before : {self.piece_manager.sound.correct_index}')
                                self.piece_manager.sound.correct_index = None
                                print(f'after : {self.piece_manager.sound.correct_index}')
                                print(f'all sound : {Board().shared_paired}')
                                # #remove sound
                                # sound_list = Sound.paired
                                # sound_cor_idx = Sound.correct_index
                                # sound_list.remove(f'{sound_cor_idx}') # not working
                                # print(f'sound list : {sound_list}')
                                # Update message and score
                                self.game_message = 'Correct !'
                                self.game_message_small = 'game will start again in ...'
                                self.message_end_time = pygame.time.get_ticks() + 2000
                                pygame.mixer.music.stop()
                                print(f'user score : {self.user.user_score}')
                                self.user_score_msg = self.user.user_score
                                self.player_selected_card = None
                            else: # Incorrect card
                                print(f'Incorrect! Clicked index: {self.player_selected_card}, Correct index: {self.piece_manager.sound.correct_index}')
                                self.game_message = 'INCORRECT !'
                                self.game_message_small = 'game will start again in ...'
                                self.message_end_time = pygame.time.get_ticks() + 2000
                                pygame.mixer.music.stop()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart_game()

            pygame.display.flip()

        pygame.quit()

    def continue_game(self):
        self.player_selected_card = None
        self.piece_manager.sound = Sound(self.piece_manager.board.paired)
        self.piece_manager.play_next_sound()

    # def draw_asset(self, img, duration=5000):
    #     self.status = img
    #     self.status_start_time = pygame.time.get_ticks()