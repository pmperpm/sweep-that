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
        self.last_click_time = pygame.time.get_ticks()  # Initialize with current time
        self.piece_manager.play_next_sound()

        # self.piece_manager.sound.play_sound()  # Play a sound when the game starts



        if self.message_end_time != 0 and pygame.time.get_ticks() > self.message_end_time:
            self.game_message = ''
            self.game_message_small = ''
            self.message_end_time = 0
            if self.user.user_score == 18 or self.oppo.oppo_score == 18:
                self.game_end()
            else:
                self.continue_game()
                
    # def start_game(self):
        

    def run(self):

        while self.running:
            # Background color
            # self.screen.fill(Config.COLORS["LIGHT_BROWN"])
            self.board.draw(self.screen)

            # Display game message
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

            # Check for inactivity (outside event loop)
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
                    # Optionally display a message or perform other actions
                    self.game_message_small = "game will start again in ..."
                    self.message_end_time = pygame.time.get_ticks() + 2000 # Display message
                    self.oppo_acted = True
                    if self.user.user_score == 18 or self.oppo.oppo_score == 18:
                        GameEnd(self).run()
                        self.running = False
                        break
                    else:
                        self.continue_game()
                    pygame.mixer.music.stop()
                    self.last_click_time = pygame.time.get_ticks()  # Reset to prevent looping

            # Handle events
            for event in pygame.event.get():
                self.total_time = pygame.time.get_ticks()
                # print(self.total_time)
                if event.type == pygame.QUIT:
                    self.running = False


                    ################ CARD GAME ##############
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player_selected_card = self.piece_manager.get_selected_piece(event.pos)
                    # self.player_selected_card = self.piece_manager.get_selected_piece(event.pos)

                    if self.player_selected_card is not None:
                        self.last_click_time = pygame.time.get_ticks()

                        # Get the *actual* card object, important for correct comparison
                        clicked_card = self.piece_manager.board.cards[self.player_selected_card]

                        # Compare the *card object* with the target card
                        if self.player_selected_card == self.piece_manager.sound.correct_index:
                            print(f'Correct! Clicked index: {self.player_selected_card}, Correct index: {self.piece_manager.sound.correct_index}')
                            self.user.user_score += 1
                            # Set the card and sound
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

                            # Reset selected card
                            self.player_selected_card = None
                        else:  # Incorrect card
                            print(f'Incorrect! Clicked index: {self.player_selected_card}, Correct index: {self.piece_manager.sound.correct_index}')
                            self.game_message = 'INCORRECT !'
                            self.game_message_small = 'game will start again in ...'
                            self.message_end_time = pygame.time.get_ticks() + 2000
                            pygame.mixer.music.stop()


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart when 'R' is pressed
                        self.restart_game()

            pygame.display.flip()

        pygame.quit()

    def continue_game(self):
        self.player_selected_card = None
        
        # Don't create a new Sound instance - reuse the existing one
        # This preserves the played_sounds tracking
        if not self.piece_manager.sound.all_sounds_played:
            self.piece_manager.play_next_sound()

    def draw_asset(self, img, duration=5000):
        self.status = img
        self.status_start_time = pygame.time.get_ticks()
