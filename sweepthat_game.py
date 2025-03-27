# sweepthat.py
import pygame
from sweepthat_config import Config
from sweepthat_classes import *
from sweepthat_menu import *

class Game(Menu):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.font.init()
        # self.asset = Asset()
        self.total_time = 0
        self.message_end_time = 0
        self.user_score = 0
        self.oppo_score = 0
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


        self.piece_manager = PieceManager(self.board)
        self.player_selected_card = None
        self.running = True
        self.game_message, self.game_message_small,self.game_message_medium = "","", ""
        self.time_message1, self.time_message2, self.time_message3, self.time_message4 = "","","",""
        self.last_click_time = pygame.time.get_ticks()  # Initialize with current time
        self.piece_manager.sound.play_sound()

        # self.piece_manager.sound.play_sound()  # Play a sound when the game starts

        # msg_text_medium = self.font.render(self.game_message_medium, True, Config.COLORS["BLACK"])
        # msg_rect_medium = msg_text_medium.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        # self.screen.blit(msg_text_medium, msg_rect_medium)

        # msg_time1 = self.font.render(self.game_message_medium, True, Config.COLORS["BLACK"])
        # msg_rect_medium = msg_text_medium.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        # self.screen.blit(msg_text_medium, msg_rect_medium)

        # msg_time2 = self.font.render(self.game_message_medium, True, Config.COLORS["BLACK"])
        # msg_rect_medium = msg_text_medium.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        # self.screen.blit(msg_text_medium, msg_rect_medium)

        # msg_time3 = self.font.render(self.game_message_medium, True, Config.COLORS["BLACK"])
        # msg_rect_medium = msg_text_medium.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        # self.screen.blit(msg_text_medium, msg_rect_medium)

        # msg_time3 = self.font.render(self.game_message_medium, True, Config.COLORS["BLACK"])
        # msg_rect_medium = msg_text_medium.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        # self.screen.blit(msg_text_medium, msg_rect_medium)

        if self.message_end_time != 0 and pygame.time.get_ticks() > self.message_end_time:
            self.game_message = ''
            self.game_message_small = ''
            self.message_end_time = 0
            if self.user_score == 18 or self.oppo_score == 18:
                self.game_end()
            else:
                self.continue_game()

    # def display_text(self, size, width, height, message):
    #     self.font = pygame.font.Font(Config.FONT_PATH, size)
    #     msg_text = self.font.render(message, True, Config.COLORS["BLACK"])
    #     msg_rect = msg_text.get_rect(center=(width, height))
    #     self.screen.blit(msg_text, msg_rect)

    
    def run(self):
        while self.running:
            # Background color
            # self.screen.fill(Config.COLORS["LIGHT_BROWN"])
            self.board.draw(self.screen)
            # self.board.draw_card(self.screen)


            # ################# MEMORIZING PART ##################


            # main_text = Text(50, Config.WIDTH // 2, Config.HEIGHT // 2, "Select time you want to use to\nmemorize the card position.")
            # _3min = Text(30, Config.WIDTH // 2 - 50, Config.HEIGHT // 2 + 40, "3 min")
            # _5min = Text(30, Config.WIDTH // 2 - 25, Config.HEIGHT // 2 + 40, "5 min")
            # _7min = Text(30, Config.WIDTH // 2 + 25, Config.HEIGHT // 2 + 40, "7 min")
            # _skip = Text(30, Config.WIDTH // 2 + 50, Config.HEIGHT // 2 + 40, "SKIP")

            # ### COUNTDOWN ####
            # if self.is_counting:
            #     elapsed_time = pygame.time.get_ticks() - self.start_time
            #     remaining_time = max(0, self.total_time - elapsed_time)
                
            #     # Format display string
            #     minutes = remaining_time // 60000
            #     seconds = (remaining_time // 1000) % 60
            #     time_text = f"{minutes:02d}:{seconds:02d}"
                
            #     # Draw countdown text
            #     time_surface = self.medium_font.render(time_text, True, Config.COLORS["BLACK"])
            #     text_rect = time_surface.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 - 100))
            #     self.screen.blit(time_surface, text_rect)

            # # for event in pygame.event.get()L
            # # ################################# self.board.draw_card(self.screen)

            # Display game message
            msg_text = self.font.render(self.game_message, True, Config.COLORS["BLACK"])
            msg_rect = msg_text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 20))
            self.screen.blit(msg_text, msg_rect)

            msg_text_small = self.small_font.render(self.game_message_small, True, Config.COLORS["BLACK"])
            msg_rect_small = msg_text_small.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 + 80))
            self.screen.blit(msg_text_small, msg_rect_small)

            ############## GAME PART #############
            if self.message_end_time != 0 and pygame.time.get_ticks() > self.message_end_time:
                self.game_message = ''
                self.game_message_small = ''
                self.message_end_time = 0
                if self.user_score == 18 or self.oppo_score == 18:
                    self.game_end()
                else:
                    self.continue_game()

            # Check for inactivity (outside event loop)
            if self.player_selected_card is None:
                if pygame.time.get_ticks() - self.last_click_time > 20000:
                    self.oppo_score += 1
                    print(f'Opponent correct!  Oppo score: {self.oppo_score}')
                    # Set the card and sound
                    # clicked_card.visible = False
                    self.piece_manager.board.cards[self.piece_manager.sound.correct_index].visible = False
                    self.piece_manager.sound.correct_index = None
                    # Optionally display a message or perform other actions
                    self.game_message = "Opponent CORRECT !"
                    self.game_message_small = "game will start again in ..."
                    self.message_end_time = pygame.time.get_ticks() + 2000 # Display message
                    self.oppo_acted = True
                    if self.user_score == 18 or self.oppo_score == 18:
                        self.game_end()
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

                            # Set the card and sound
                            clicked_card.visible = False
                            self.piece_manager.sound.correct_index = None
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
                            self.user_score += 1
                            print(f'user score : {self.user_score}')

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
        # count down
        # countdown_images = ["images/THREE.png", "images/TWO.png", "images/ONE.png"]
        # for img in countdown_images:
        #     self.draw_asset(Asset(img))  # Duration for each image
        #     pygame.display.flip()
        #     pygame.time.delay(1000)

        self.player_selected_card = None
        # self.piece_manager.reset_board()
        # Reinitialize sound with new paired indices
        self.piece_manager.sound = Sound(self.piece_manager.board.paired)
        self.piece_manager.sound.play_sound()

    ####### adjust more ##########
    def game_end(self):
        if self.user_score == 18:
            self.game_message = 'YOU WIN !'
            self.game_message_small = 'great job ! Do you want to play again ?'
            # self.game_message_smaller = '> press R to restart the game'
            # self.game_message_smaller_2 = '> press m to go to the menu'
            # self.message_end_time = pygame.time.get_ticks() + 2000
        elif self.oppo_score == 18:
            self.game_message = 'YOU LOSE !'
            self.game_message_small = 'better luck next time ! Do you want to play again ?'
            # self.message_end_time = pygame.time.get_ticks() + 2000
        # restart game or not?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart when 'R' is pressed
                    self.restart_game()

    def draw_asset(self, img, duration=5000):
        self.status = img
        self.status_start_time = pygame.time.get_ticks()

    def restart_game(self):
        # Reset game state
        self.user_score = 0
        self.oppo_score = 0
        self.oppo_acted = False
        self.player_selected_card = None
        self.game_message, self.game_message_small = '', ''

        # Recreate the board and sound
        self.piece_manager = PieceManager()
        self.piece_manager.sound.play_sound()
        self.board.backgrounds()

