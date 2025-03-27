import pygame, random, os, csv

from pygame.sprite import *
from sweepthat_config import *

class Piece:
    def __init__(self, image_path, x, y, paired_index):
        # Image
        self.image = pygame.image.load(os.path.join(Config.card_image_folder,image_path))#Load Image
        self.image = pygame.transform.scale(self.image, (Config.CARD_WIDTH, Config.CARD_HEIGHT))

        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.font = pygame.font.Font(None, 16)
        self.visible = True
        self.paired_index = paired_index


    def draw(self, screen):
        if self.visible:
            # pygame.draw.rect(screen, Config.COLORS["WHITE"], self.rect)
            screen.blit(self.image, self.rect) # draw img
            pygame.draw.rect(screen, Config.COLORS["DARK_GREEN"], self.rect, 2)


class Board:
    paired_initialized = False
    shared_paired = []

    def __init__(self):
        self.card_data = []
        self.cards = []
        self.bg = random.choice(THAI_BG)
        self.board_rect = pygame.Rect(
            int(Config.BORDER_SIZE),
            int(Config.BORDER_SIZE),
            int(Config.WIDTH - 2 * Config.BORDER_SIZE),
            int(Config.HEIGHT - 2 * Config.BORDER_SIZE),
        )
        if not Board.paired_initialized:
            self.initialize_pairs()
        self.paired = Board.shared_paired
        self.create_board()

    def initialize_pairs(self):
        num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
        Board.shared_paired = list(range(num_pairs))
        random.shuffle(Board.shared_paired)
        Board.paired_initialized = True
        print(f"Initialized shared paired: {Board.shared_paired}")

    def backgrounds(self):
        self.bg = random.choice(THAI_BG)

    # def pairs(self):
    #     num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
    #     pairs = list(range(num_pairs))
    #     random.shuffle(pairs)
    #     return pairs

    def create_board(self):
        # Pair card and sound
        num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
        self.paired = list(range(num_pairs))
        random.shuffle(self.paired)
        print(f'self paired{self.paired}')

        card_images = [IMAGE_FILES[i] for i in self.paired] # create card

        # Calculate positions
        left__x = 50
        left__y = 50

        # TOP LEFT
        # first row
        x, y = 50,50
        for i in range(4):
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(4,7): # 5-7
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(7,9): # 8-9
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5

        # BOTTOM LEFT
        # first row
        x, y = left__x, Config.HEIGHT - left__y - Config.CARD_HEIGHT
        for i in range(9,13): # 10-13
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(13,15): # 14-15
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(15,18): # 16 - 18
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5

        right_x = 310
        right_y = 50

        # TOP RIGHT
        # First row
        x, y = Config.WIDTH - right_x - Config.CARD_WIDTH, right_y
        for i in range(18,22): # 18 - 21
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # Second row
        x = 593
        y += Config.CARD_HEIGHT + 5
        for i in range(22,25): # 22 - 25
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # Third row
        x = 683
        y += Config.CARD_HEIGHT + 5 # 5 is card space
        for i in range(25,27): # 26-27
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5

        # BOTTOM RIGHT
        x, y = 505, Config.HEIGHT - right_y - Config.CARD_HEIGHT
        for i in range(27,31): # 28-31
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # second row
        x = 683
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(31,33): # 32-33
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5
        # third row
        x = 593
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(33, 36): # 34-36
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([card_images[i],x,y])
                x += Config.CARD_WIDTH + 5

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        for card in self.cards:
            card.draw(screen)
        # Draw all cards on top of the background

    # def draw_card(self,screen):
    #     for card in self.cards:
    #         card.draw(screen)

class Sound:
    def __init__(self, paired):
        self.paired = paired
        self.correct_index = None
        self.play_sound()

    def play_sound(self):
        if not self.paired:
            return

        self.correct_index = random.randint(0, len(self.paired)-1)
        sound_path = os.path.join(
            Config.sound_folder,
            SOUND_FILES[self.paired[self.correct_index]]
        )
        print(f'sound correct index : {self.correct_index}')
        # print('SOUND')
        # print(f'sound file pair correct idx : {SOUND_FILES[self.paired[self.correct_index]]}')
        # print(f'paired : {self.paired}')
        # print(f'correct idx : {self.correct_index}')
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()


class Asset:
    def __init__(self) -> None:
        self.start_time = 0
        self.total_time = 0
        self.is_counting = False
        # Add font initialization if not already present
        self.medium_font = pygame.font.Font(None, 36)  # Example size

    def draw_countdown(self, screen, minutes):
        """Handles minute-based countdown visualization"""
        # Initialize timer on first call
        if not self.is_counting and minutes > 0:
            self.total_time = minutes * 60 * 1000  # Convert minutes to milliseconds
            self.start_time = pygame.time.get_ticks()
            self.is_counting = True

        # Calculate remaining time
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = max(0, self.total_time - elapsed_time)

        # Format time display (MM:SS.CS)
        minutes_remaining = remaining_time // 60000
        seconds_remaining = (remaining_time // 1000) % 60
        time_text = f"{minutes_remaining:02d}:{seconds_remaining:02d}"

        # Draw text
        time_surface = self.medium_font.render(time_text, True, Config.COLORS["BLACK"])
        text_rect = time_surface.get_rect(center=(Config.WIDTH//2, Config.HEIGHT//2-50))
        screen.blit(time_surface, text_rect)

        # Draw progress bar
        if self.total_time > 0:
            progress_width = (elapsed_time / self.total_time) * 200
            pygame.draw.rect(screen, Config.COLORS["BLACK"], 
                           (Config.WIDTH//2-100, Config.HEIGHT//2+20, progress_width, 20))

        # Handle completion
        if remaining_time <= 0 and self.is_counting:
            self.is_counting = False
            return True
        return False

        # start_time = pygame.time.get_ticks()
        # while self.is_draw:
        #     self.screen.blit(img, (0,0))
        #     time = pygame.time.get_ticks() - start_time
        #     if time > duration:
        #         self.is_draw = False

        
        # """Display an asset for a set duration"""
        # self.status = img
        # self.status_start_time = pygame.time.get_ticks()
        # self.status_duration = duration

        # # Force redraw immediately to show the asset
        # # self.screen.fill((255, 255, 255))  # Optional: Set a background color
        # self.board.draw(self.screen)
        # self.piece_manager.draw_pieces(self.screen)
        # self.screen.blit(self.status.asset_image, self.status.rect)
        # pygame.display.flip()

        # Pause the game to show the image before continuing
        # pygame.time.delay(duration)

    # def draw_asset(self, img, duration):
    #     self.status = img
    #     self.status_start_time = pygame.time.get_ticks()

class User:
    def __init__(self) -> None:
        self.user_score = 0
        self.user_ui =  pygame.image.load("images/10 STATUS.svg")

    def draw(self, screen):
        # Draw the user interface
        screen.blit(self.user_ui, (0, 0))

class Opponent:
    def __init__(self) -> None:
        self.oppo_score = 0
        self.oppo_ui =  pygame.image.load("images/10 STATUS.svg")

    def draw(self, screen):
        # Draw the opponent interface
        screen.blit(self.opponent_ui, (0, 0))

class PieceManager:
    def __init__(self, board=None):
        # Use an existing board if provided; otherwise, create a new one
        self.board = board if board else Board()
        self.sound = Sound(self.board.paired)

    def reset_board(self):
        # Resetting should reuse the same shared paired list
        self.board = Board()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def reset_board(self):
        # Create a new board with newly shuffled cards
        self.board = Board()

    def draw_pieces(self, screen):
        self.board.draw(screen)

    def get_selected_piece(self, pos):
        for i, card in enumerate(self.board.cards):
            if card.rect.collidepoint(pos):
                return i  # Return the index of the clicked card
        return None


