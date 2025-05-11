import pygame
from sweepthat_config import Config
from sweepthat_classes import *
from sweepthat_menu import *
from game_end import GameEnd
from datetime import datetime
from sweepthat_db import *

class Game(Menu):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.font.init()
        # self.asset = Asset()

        # attribute to store in database
        self.__start_datetime = "" 
        self.__react_time = 0
        self.__start_react_time = 0
        self.__card_pos = "N/A"
        self.__cor_pos = "N/A"
        self.__pos_rahu = "N/A"

        self.__message_end_time = 0
        self.__user = User()
        self.__rahu = Rahu()
        self.__db = DB()
        self.__oppo_score = 0
        self.__oppo_acted = False
        self.__count_time = 0
        self.__start_time = 0
        self.__MUSIC_END = pygame.USEREVENT + 1
        self.__board = Board()
        self.__is_counting = False
        pygame.mixer.music.set_endevent(self.__MUSIC_END)

        self.__font = pygame.font.Font(Config.FONT_PATH, 70)
        self.__small_font = pygame.font.Font(Config.FONT_PATH, 30)
        self.__medium_font = pygame.font.Font(Config.FONT_PATH, 50)

        # pygame.display.set_caption("SWEEP THAT Game")
        self.__piece_manager = PieceManager(self.board)
        self.__player_selected_card = None
        self.__running = True
        self.__game_message, self.__oppo_score_msg = "", ""
        self.__user_score_msg = ""
        self.__last_click_time = pygame.time.get_ticks()

        # select level var
        self.__selecting_level = True  # level selection
        self.__level_options = [
            # {"text": "EASY", "speed": 25000, "rect": None},  #
            {"text": "NORMAL", "speed": 20000, "rect": None},  #
            {"text": "HARD", "speed": 10000, "rect": None}  # 
        ]
        self.__inactivity_threshold = 20000  # 

        # Memorization var
        self.__mem_time = 0 # memorize time to count
        self.__mem_start_t = 0
        self.__in_mem_phase = False
        self.__mem_complete = False
        self.__confirm = False
        self.__selecting_mem_time = True  # New state for time selection
        self.__time_options = [
            {"text": "3 minutes", "time": 3 * 60 * 1000, "rect": None},
            {"text": "5 minutes", "time": 5 * 60 * 1000, "rect": None},
            {"text": "SKIP", "time": 0, "rect": None}
        ]

    @property
    def user(self):
        return self.__user
    
    @property
    def rahu(self):
        return self.__rahu
    
    @property
    def board(self):
        return self.__board
    
    @property
    def piece_manager(self):
        return self.__piece_manager
    
    @property
    def mem_complete(self):
        return self.__mem_complete
    
    @mem_complete.setter
    def mem_complete(self, value):
        self.__mem_complete = value

    @property
    def oppo_score(self):
        return self.__oppo_score

    def draw_level_selection(self):
        # get start time
        self.__start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        title_text = self.__medium_font.render("Select level:", True, Config.COLORS["BLACK"])
        self.screen.blit(title_text, (Config.WIDTH//2 - title_text.get_width()//2, Config.HEIGHT//2 - 100))

        # Draw level options
        for i, option in enumerate(self.__level_options):
            text = self.__small_font.render(option["text"], True, Config.COLORS["BLACK"])
            rect = pygame.Rect(Config.WIDTH//2 - 100, Config.HEIGHT//2 + i*60, 200, 50)
            option["rect"] = rect  # Store rect for click detection
            
            # Draw button
            pygame.draw.rect(self.screen, Config.COLORS["WHITE"], rect)
            pygame.draw.rect(self.screen, Config.COLORS["DARK_GREEN"], rect, 2)
            self.screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

    def level_selec_click(self, pos):
        for option in self.__level_options:
            if option["rect"].collidepoint(pos):  # if click is inside a button
                self.__selected_level = option["text"]
                return True 
        return False 
    
    def time_selec_click(self, pos):
        for option in self.__time_options:
            if option["rect"] and option["rect"].collidepoint(pos):
                return True
        return False

    def draw_time_selection(self):
        # select time
        title_text = self.__medium_font.render("Select memorization time:", True, Config.COLORS["BLACK"])
        self.screen.blit(title_text, (Config.WIDTH//2 - title_text.get_width()//2, Config.HEIGHT//2 - 100))

        # Draw time 
        for i, option in enumerate(self.__time_options):
            text = self.__small_font.render(option["text"], True, Config.COLORS["BLACK"])
            rect = pygame.Rect(Config.WIDTH//2 - 100, Config.HEIGHT//2 + i*60, 200, 50)
            option["rect"] = rect 

            # Draw button
            pygame.draw.rect(self.screen, Config.COLORS["WHITE"], rect)
            pygame.draw.rect(self.screen, Config.COLORS["DARK_GREEN"], rect, 2)
            self.screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

    def draw_countdown(self, remain_t):
        min = remain_t // 60000
        sec = (remain_t % 60000) // 1000
        t_text = f"{min:02d}:{sec:02d}"
        count_text = self.__medium_font.render(t_text, True, Config.COLORS["BLACK"])
        prompt_text = self.__small_font.render("Memorize the card positions!", True, Config.COLORS["BLACK"])

        count_bg = pygame.Surface((300, 100), pygame.SRCALPHA)
        count_bg.fill((255, 255, 255, 128))

        self.screen.blit(count_bg, (Config.WIDTH//2 - 150, Config.HEIGHT - 120))
        self.screen.blit(prompt_text, (Config.WIDTH//2 - prompt_text.get_width()//2, Config.HEIGHT - 110))
        self.screen.blit(count_text, (Config.WIDTH//2 - count_text.get_width()//2, Config.HEIGHT - 80))

    def draw_start_prompt(self):
        prompt_text = self.__medium_font.render("Memorization time complete!", True, Config.COLORS["BLACK"])
        inst_text = self.__small_font.render("Press ENTER to start the game", True, Config.COLORS["BLACK"])

        prompt_bg = pygame.Surface((500, 150), pygame.SRCALPHA)
        prompt_bg.fill((255, 255, 255, 180))

        self.screen.blit(prompt_bg, (Config.WIDTH//2 - 250, Config.HEIGHT//2 - 75))
        self.screen.blit(prompt_text, (Config.WIDTH//2 - prompt_text.get_width()//2, Config.HEIGHT//2 - 50))
        self.screen.blit(inst_text, (Config.WIDTH//2 - inst_text.get_width()//2, Config.HEIGHT//2 + 10))

    def run(self):
        while self.__running:
            self.screen.fill(Config.COLORS["LIGHT_BROWN"])
            self.__board.draw(self.screen)

            # Level selection phase
            if self.__selecting_level:
                self.draw_level_selection()
            
            # Time selection phase
            elif self.__selecting_mem_time:
                self.draw_time_selection()

            # Memorization phase
            elif self.__in_mem_phase:
                current_time = pygame.time.get_ticks()
                elapsed = current_time - self.__mem_start_t
                remaining = max(0, self.__mem_time - elapsed)

                self.draw_countdown(remaining)

                if remaining <= 0 and not self.__confirm:
                    self.__in_mem_phase = False
                    self.__confirm = True

            # Waiting for confirm
            elif self.__confirm:
                self.draw_start_prompt()

            # Main game 
            elif self.__mem_complete:
                if hasattr(self, '_Game__selected_level') and self.__selected_level == "HARD":
                    if not self.__rahu.is_active():  # Only spawn if not already active
                        self.__rahu.spawn()

                if self.__game_message:
                    msg_text = self.__font.render(self.__game_message, True, Config.COLORS["BLACK"])
                    msg_rect = msg_text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
                    self.screen.blit(msg_text, msg_rect)

                msg_user_score = self.__small_font.render(str(self.__user_score_msg), True, Config.COLORS["WHITE"])
                msg_rect_user_score = msg_user_score.get_rect(center=(Config.WIDTH // 2 + 50, Config.HEIGHT // 2 + 120))
                self.screen.blit(msg_user_score, msg_rect_user_score)
                self.__user_score_msg = self.__user.score

                msg_oppo_score = self.__small_font.render(str(self.__oppo_score_msg), True, Config.COLORS["WHITE"])
                msg_rect_oppo_score = msg_oppo_score.get_rect(center=(Config.WIDTH // 2 + 50, Config.HEIGHT // 2 - 135))
                self.screen.blit(msg_oppo_score, msg_rect_oppo_score)
                self.__oppo_score_msg = self.__oppo_score

                ############## GAME PART #############
                self.__rahu.set_level(self.__selected_level)
                self.__rahu.draw(self.screen)

                if self.__message_end_time != 0 and pygame.time.get_ticks() > self.__message_end_time:
                    self.__game_message = ''
                    self.__game_message_small = ''
                    self.__message_end_time = 0
                    if self.user.score == 18 or self.__oppo_score == 18:
                        GameEnd(self).run()
                        self.__running = False
                        break
                    else:
                        self.continue_game()

                # Check for inactivity
                if self.__player_selected_card is None:
                    if pygame.time.get_ticks() - self.__last_click_time > 20000:
                        self.__oppo_score += 1
                        self.__oppo_score_msg = self.__oppo_score
                        self.__game_message = "Opponent CORRECT !"
                        ###### DATA PART ######
                
                        # time user use to click the card
                        self.__react_time = 0
                        # rahu position 
                        if self.__selected_level == "HARD": # Hard levek
                            self.__pos_rahu = self.__rahu.get_rahu_pos()
                        else: # Normal level
                            self.__pos_rahu = None
                        # card position
                        clicked_index = self.__player_selected_card  # Already stored when clicking
                        if clicked_index is not None and clicked_index < len(self.__board.card_data):
                            self.__card_pos = self.__board.card_data[clicked_index][5]
                        else:
                            self.__card_pos = None
                                # correct position
                        self.__cor_pos = self.__board.card_data[self.__piece_manager.sound.correct_index][5]
                        # correct index
                        for card in current_cards:
                            if self.__piece_manager.sound.correct_index == card['index']:
                                correct_index_data = card['image_name'].split('.')[0] 
                                correct_pos = card['position']
                        # result
                        result = "OPPO CORRECT"
                        print(f'DATA RESULT\n'
                              f'react_time: {self.__react_time}\n'
                              f'rahu_position: {self.__pos_rahu}\n'
                              f'card pos : {correct_pos}\n'
                              f'correct index : {correct_index_data}\n'
                              f'result: {result}')
                        # ADD DATA #
                        self.__db.add_to_csv(date_start=self.__start_datetime,
                        react_time=self.__react_time,
                        cor_pos=self.__cor_pos,
                        cor_idx=correct_index_data,
                        clicked_pos='N/A', # self.card_pos
                        clicked_idx=0, # self.player_selected_card
                        rahu_pos=self.__pos_rahu,
                        result=result
                        )
                        #######################

                        # Set the card and sound
                        self.__piece_manager.board.cards[self.__piece_manager.sound.correct_index].visible = False
                        # print(f'before : {self.piece_manager.sound.correct_index}')
                        self.__piece_manager.sound.correct_index = None
                        # print(f'after : {self.piece_manager.sound.correct_index}')
                        self.__game_message_small = "game will start again in ..."
                        self.__message_end_time = pygame.time.get_ticks() + 2000
                        self.__oppo_acted = True
                        if self.__user.score == 18 or self.__oppo_score == 18:
                            GameEnd(self).run()
                            self.__running = False
                            break
                        else:
                            self.continue_game()
                        pygame.mixer.music.stop()
                        self.__last_click_time = pygame.time.get_ticks()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    current_cards = self.board.get_card_images_info()
                    for card in current_cards:
                        print(f"Card at index {card['index']}: {card['image_name']} at {card['position']}")

                    if self.__selecting_level and self.level_selec_click(event.pos):
                        for option in self.__level_options:
                            if option["rect"] and option["rect"].collidepoint(event.pos):
                                self.__selected_level = option["text"]
                                self.__inactivity_threshold = option["speed"]  # Only for level selection
                                self.__selecting_level = False
                                self.__selecting_mem_time = True
                                # print(f"Selected level: {self.selected_level}")

                    elif self.__selecting_mem_time and self.time_selec_click(event.pos):
                        for option in self.__time_options:
                            if option["rect"] and option["rect"].collidepoint(event.pos):
                                self.__mem_time = option["time"]  # Store memorization time separately
                                self.__selecting_mem_time = False
                                if self.__mem_time > 0:
                                    self.__in_mem_phase = True
                                    self.__mem_start_t = pygame.time.get_ticks()
                                else:
                                    self.__mem_complete = True
                                    self.__piece_manager.play_next_sound()

                # Start confirm
                elif event.type == pygame.KEYDOWN and self.__confirm:
                    if event.key == pygame.K_RETURN:
                        self.__confirm = False
                        self.__mem_complete = True
                        self.__piece_manager.play_next_sound()
                        self.__last_click_time = pygame.time.get_ticks()

                ################ CARD GAME ##############
                if self.__mem_complete and not self.__confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked_index = self.__piece_manager.get_selected_piece(event.pos)
                        # self.player_selected_card = self.piece_manager.get_selected_piece(event.pos)
                        if clicked_index is not None:
                                self.__player_selected_card = clicked_index
                                clicked_card = self.__piece_manager.board.cards[clicked_index]
                                self.__last_click_time = pygame.time.get_ticks()
                                if clicked_index == self.__piece_manager.sound.correct_index:
                                    self.__user.score += 1
                                    clicked_card.visible = False

                                    ###### DATA PART ######
                                    # time user use to click the card
                                    self.__react_time = pygame.time.get_ticks() - self.__start_react_time
                                    # rahu position 
                                    if self.__selected_level == "HARD": # Hard levek
                                        self.__pos_rahu = self.__rahu.get_rahu_pos()
                                        print(f'rahu position: {self.__pos_rahu}')
                                    else: # Normal level
                                        self.__pos_rahu = None
                                    # clicked position
                                    clicked_index = self.__player_selected_card  # Already stored when clicking
                                    if clicked_index is not None and clicked_index < len(self.__board.card_data):
                                        self.__card_pos = self.__board.card_data[clicked_index][5]
                                    # correct position
                                    self.__cor_pos = self.__board.card_data[self.__piece_manager.sound.correct_index][5]
                                    # result
                                    result = "CORRECT"
                                    #clicked index + correct index
                                    for card in current_cards:
                                        if self.__player_selected_card == card['index']:
                                            clicked_index_data = card['image_name'].split('.')[0]
                                            clicked_pos = card['position']
                                        if self.__piece_manager.sound.correct_index == card['index']:
                                            correct_index_data = card['image_name'].split('.')[0] 
                                            correct_pos = card['position']

                                        # print(f"Card at index {card['index']}: {card['image_name']} at {card['position']}")
                                    print(f'DATA RESULT\n'
                                        f'react_time: {self.__react_time}\n'
                                        f'rahu_position: {self.__pos_rahu}\n'
                                        f'clicked index : {clicked_index_data}'
                                        f'clicked pos : {clicked_pos}\n'
                                        f'correct index : {correct_index_data}\n'
                                        f'cor pos: {correct_pos}'
                                        f'result: {result}')
                                    # ADD DATA #
                                    self.__db.add_to_csv(date_start=self.__start_datetime,
                                    react_time=self.__react_time,
                                    cor_pos=self.__cor_pos,
                                    cor_idx=correct_index_data,
                                    clicked_pos=self.__card_pos,
                                    clicked_idx=int(clicked_index_data),
                                    rahu_pos=self.__pos_rahu,
                                    result=result
                                    )
                                    #######################
                                    # print(f'before : {self.piece_manager.sound.correct_index}')
                                    self.__piece_manager.sound.correct_index = None

                                    self.__game_message = 'Correct !'
                                    self.__game_message_small = 'game will start again in ...'
                                    self.__message_end_time = pygame.time.get_ticks() + 2000
                                    pygame.mixer.music.stop()
                                    # print(f'user score : {self.user.user_score}')
                                    self.__user_score_msg = self.__user.score
                                    self.__player_selected_card = None
                                else: # Incorrect card
                                    print(f'Incorrect! Clicked index: {self.__player_selected_card}, Correct index: {self.__piece_manager.sound.correct_index}')

                                    ###### DATA PART ######
                                    # time user use to click the card
                                    self.__react_time = pygame.time.get_ticks() - self.__start_react_time
                                    # rahu position 
                                    if self.__selected_level == "HARD": # Hard levek
                                        self.__pos_rahu = self.__rahu.get_rahu_pos()
                                        print(f'rahu position: {self.__pos_rahu}')
                                    else: # Normal level
                                        self.__pos_rahu = None
                                    # card position
                                    clicked_index = self.__player_selected_card  # Already stored when clicking
                                    if clicked_index is not None and clicked_index < len(self.__board.card_data):
                                        self.__card_pos = self.__board.card_data[clicked_index][5]
                                    # correct position
                                    self.__cor_pos = self.__board.card_data[self.__piece_manager.sound.correct_index][5]
                                    for card in current_cards:
                                        if self.__player_selected_card == card['index']:
                                            clicked_index_data = card['image_name'].split('.')[0]
                                            clicked_pos = card['position']
                                        if self.__piece_manager.sound.correct_index == card['index']:
                                            correct_index_data = card['image_name'].split('.')[0] 
                                            correct_pos = card['position']

                                    # result
                                    result = "INCORRECT"
                                    print(f'DATA RESULT\n'
                                            f'react_time: {self.__react_time}\n'
                                            f'rahu_position: {self.__pos_rahu}\n'
                                            f'clicked index : {clicked_index_data}'
                                            f'clicked pos : {clicked_pos}\n'
                                            f'correct index : {correct_index_data}\n'
                                            f'cor pos: {correct_pos}'
                                            f'result: {result}')
                                    # ADD DATA #
                                    self.__db.add_to_csv(date_start=self.__start_datetime,
                                    react_time=self.__react_time,
                                    cor_pos=self.__cor_pos,
                                    cor_idx=correct_index_data,
                                    clicked_pos=self.__card_pos,
                                    clicked_idx=clicked_index_data,
                                    rahu_pos=self.__pos_rahu,
                                    result=result
                                    )
                                    #######################
                                            
                                    self.__game_message = 'INCORRECT !'
                                    self.__game_message_small = 'game will start again in ...'
                                    self.__message_end_time = pygame.time.get_ticks() + 2000
                                    pygame.mixer.music.stop()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart_game()

            pygame.display.flip()

        pygame.quit()
        
    def continue_game(self):
        self.__rahu.clear()
        self.__player_selected_card = None  
        
        self.__piece_manager.play_next_sound()
        self.__start_react_time = pygame.time.get_ticks()
