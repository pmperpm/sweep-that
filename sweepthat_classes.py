import pygame, random, os, csv
from pathlib import Path
from sweepthat_config import *
import sweepthat_game

class Piece:
    def __init__(self, image_path, x, y, paired_index):
        # Image
        self.__image = pygame.image.load(os.path.join(Config.card_image_folder,image_path))#Load Image

        self.__original_image = self.__image
        self.__rect = self.__image.get_rect(topleft=(x, y))
        self.__font = pygame.font.Font(None, 16)
        self.__visible = True
        self.__paired_index = paired_index

        self.__image = self._scale_image(self.__original_image, Config.CARD_WIDTH, Config.CARD_HEIGHT)
        
        self.__original_image = self.__original_image
        self.__rect = self.__image.get_rect(topleft=(x, y))
        self.__font = pygame.font.Font(None, 16)
        self.__visible = True
        self.__paired_index = paired_index

    @property
    def rect(self):
        return self.__rect
    
    @property
    def visible(self):
        return self.__visible
    
    @property
    def paired_index(self):
        return self.__paired_index
    
    @visible.setter
    def visible(self, value):
        self.__visible = value

    def _scale_to_fill(self, image, target_width, target_height):
        """Scale image to fill target dimensions, cropping if necessary"""
        # Get original dimensions
        original_width, original_height = image.get_size()
        
        # Calculate scaling factors
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        # Use the larger ratio to ensure the image fills the space
        scale_ratio = max(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        
        # Scale the image
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        
        # Calculate cropping area (centered)
        crop_x = (new_width - target_width) // 2
        crop_y = (new_height - target_height) // 2
        
        # Create a subsurface that fits exactly in our card dimensions
        final_image = scaled_image.subsurface(
            pygame.Rect(crop_x, crop_y, target_width, target_height))
        
        return final_image

    def draw(self, screen):
        if self.__visible:
            screen.blit(self.__image, self.__rect) # draw img
            pygame.draw.rect(screen, Config.COLORS["DARK_GREEN"], self.__rect, 2)

class Board:
    _instance = None
    paired_initialized = False
    shared_paired = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Board, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.__card_data = []
            self.__cards = []
            self.__bg = random.choice(THAI_BG)
            self.__board_rect = pygame.Rect(
                int(Config.BORDER_SIZE),
                int(Config.BORDER_SIZE),
                int(Config.WIDTH - 2 * Config.BORDER_SIZE),
                int(Config.HEIGHT - 2 * Config.BORDER_SIZE),
            )
            self.__paired = Board.shared_paired
            self.create_board()
            self.__initialized = True

    @property
    def cards(self):
        return self.__cards
    
    @property
    def paired(self):
        return self.__paired
    
    @property
    def card_data(self):
        return self.__card_data

    # def initialize_pairs(self):
    #     num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
    #     Board.shared_paired = list(range(num_pairs))
    #     random.shuffle(Board.shared_paired)
    #     Board.paired_initialized = True
    #     print(f"Initialized shared paired: {Board.shared_paired}")

    def backgrounds(self):
        self.__bg = random.choice(THAI_BG)

    def create_board(self):
        # Pair card and sound
        num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
        self.__paired = list(range(num_pairs))
        random.shuffle(self.__paired)
        print(f'self paired{self.__paired}')

        card_images = [IMAGE_FILES[i] for i in self.__paired] # create card

        # Calculate positions
        left__x = 50
        left__y = 50

        # TOP LEFT
        # first row
        x, y = 50,50
        for i in range(4):
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], 'TOP LEFT'])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(4,7): # 5-7
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "TOP LEFT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(7,9): # 8-9
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "MIDDLE LEFT"])
                x += Config.CARD_WIDTH + 5

        # BOTTOM LEFT
        # first row
        x, y = left__x, Config.HEIGHT - left__y - Config.CARD_HEIGHT
        for i in range(9,13): # 10-13
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "BOTTOM LEFT"])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(13,15): # 14-15
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "BOTTOM LEFT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(15,18): # 16 - 18
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "MIDDLE LEFT"])
                x += Config.CARD_WIDTH + 5

        right_x = 310
        right_y = 50

        # TOP RIGHT
        # First row
        x, y = Config.WIDTH - right_x - Config.CARD_WIDTH, right_y
        for i in range(18,22): # 18 - 21
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "TOP RIGHT"])
                x += Config.CARD_WIDTH + 5
        # Second row
        x = 593
        y += Config.CARD_HEIGHT + 5
        for i in range(22,25): # 22 - 25
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "TOP RIGHT"])
                x += Config.CARD_WIDTH + 5
        # Third row
        x = 683
        y += Config.CARD_HEIGHT + 5 # 5 is card space
        for i in range(25,27): # 26-27
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "MIDDLE RIGHT"])
                x += Config.CARD_WIDTH + 5

        # BOTTOM RIGHT
        x, y = 505, Config.HEIGHT - right_y - Config.CARD_HEIGHT
        for i in range(27,31): # 28-31
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "BOTTOM RIGHT"])
                x += Config.CARD_WIDTH + 5
        # second row
        x = 683
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(31,33): # 32-33
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "BOTTOM RIGHT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = 593
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(33, 36): # 34-36
            if i < len(card_images):
                self.__cards.append(Piece(card_images[i], x, y, self.__paired[i]))
                self.__card_data.append([i, card_images[i], x, y, self.__paired[i], "MIDDLE RIGHT"])
                x += Config.CARD_WIDTH + 5

        # print(f'card_data{self.card_data}')

    def draw(self, screen):
        screen.blit(self.__bg, (0, 0))
        for card in self.__cards:
            card.draw(screen)

    def get_card_images_info(self):
        """Returns a list of dictionaries containing card info: {index, image_name, position}"""
        card_info = []
        for i, card in enumerate(self.__cards):
            if card.visible:  # Only include visible cards
                # Extract the image filename from the path
                image_name = os.path.basename(self.__card_data[i][1])
                card_info.append({
                    'index': i,
                    'image_name': image_name,
                    'position': self.__card_data[i][5] 
                })
        return card_info


class Sound:
    played_sounds_global = set()  #track all played sounds across instances

    def __init__(self, paired):
        self.__paired = paired
        self.__correct_index = None
        self.__all_sounds_played = False

    def play_sound(self):
        if self.__all_sounds_played:
            print("All sounds have been played already")
            self.__correct_index = None
            return False

        # Get available indices that haven't been played
        available_indices = [
            i for i in range(len(self.__paired)) 
            if self.__paired[i] not in Sound.played_sounds_global
        ]

        if not available_indices:
            print("All sounds have been played")
            self.__all_sounds_played = True
            self.__correct_index = None
            return False

        # Select a random unplayed sound
        self.__correct_index = random.choice(available_indices)
        Sound.played_sounds_global.add(self.__paired[self.__correct_index])  # Mark as played globally

        sound_path = os.path.join(
            Config.sound_folder,
            SOUND_FILES[self.__paired[self.__correct_index]]
        )
        print(f"Playing sound at index: {self.__correct_index} (Paired index: {self.__paired[self.__correct_index]})")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        return True  
    
    @property
    def correct_index(self):
        return self.__correct_index
    
    @correct_index.setter
    def correct_index(self, value):
        self.__correct_index = value
    
class User:
    def __init__(self) -> None:
        self.__user_score = 0

    def draw_status(self, screen, status):
        if status == "WIN":
            bg = pygame.image.load("asset/WIN.png")
        elif status == "LOSE":
            bg = pygame.image.load("asset/LOSE.png")
        
        # if the background image is loaded
        if bg:
            screen.blit(bg, (0, 0))

    @property
    def score(self):
        return self.__user_score
    
    @score.setter
    def score(self, value):
        self.__user_score = value

class Rahu:
    def __init__(self):
        self.images = Config.RAHU
        self.current_rahu = None
        self.game_level = None 

    def set_level(self, level): 
        """ get game level""" 
        self.game_level = level

    def get_current_rahu(self):
        if self.is_active():
            return self.images
        return None
    
    def spawn(self):
        """ return the rahu """
        if not self.current_rahu and self.images:
            selected = random.choice(self.images)
            self.current_rahu = {
                "surface": selected["surface"],
                "pos": selected["pos"],
                "position": (0, 0)
            }
            return True
        return False

    def get_rahu_pos(self):
        """ Get rahu position """
        if self.current_rahu:
            return self.current_rahu["pos"]
        return None
    
    def clear(self):
        """ remove rahu """
        self.current_rahu = None

    def draw(self, screen):
        if self.current_rahu and self.game_level == "HARD":
            screen.blit(
                self.current_rahu['surface'],
                self.current_rahu['position']
            )
    
    def is_active(self):
        """ check if rahu is active """
        return self.current_rahu is not None and self.game_level == "HARD"
    

class PieceManager:
    def __init__(self, board=None):
        # Use an existing board if provided; otherwise, create a new one
        self.__board = board if board else Board()
        self.__sound = Sound(self.__board.paired)

    def play_next_sound(self):
        self.__sound.play_sound() # Play next unplayed sound

    def reset_board(self):
        # reuse the same shared paired list
        self.__board = Board()

    def draw(self, screen):
        if self.__visible:
            screen.blit(self.__image, self.__rect)

    def reset_board(self):
        # new board with newly shuffled cards
        self.__board = Board()

    def draw_pieces(self, screen):
        self.__board.draw(screen)

    def get_selected_piece(self, pos):
        for i, card in enumerate(self.__board.cards):
            if card.rect.collidepoint(pos):
                return i if card.visible else None
        return None

    @property
    def board(self):
        return self.__board
    
    @board.setter
    def board(self, value):
        self.board = value

    @property
    def sound(self):
        return self.__sound
    
    @sound.setter
    def sound(self, value):
        self.sound = value
