import pygame, random, os, csv
from pathlib import Path
from sweepthat_config import *
import sweepthat_game

class Piece:
    def __init__(self, image_path, x, y, paired_index):
        # Image
        self.image = pygame.image.load(os.path.join(Config.card_image_folder,image_path))#Load Image
        # self.image = pygame.transform.scale(self.image, (Config.CARD_WIDTH, Config.CARD_HEIGHT))

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
        # if not Board.paired_initialized:
        #     self.initialize_pairs()
        self.paired = Board.shared_paired
        self.create_board()

    # def initialize_pairs(self):
    #     num_pairs = min(len(IMAGE_FILES), len(SOUND_FILES))
    #     Board.shared_paired = list(range(num_pairs))
    #     random.shuffle(Board.shared_paired)
    #     Board.paired_initialized = True
    #     print(f"Initialized shared paired: {Board.shared_paired}")

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
                self.card_data.append([i, card_images[i], x, y, self.paired[i], 'TOP LEFT'])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(4,7): # 5-7
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "TOP LEFT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y += Config.CARD_HEIGHT + 5
        for i in range(7,9): # 8-9
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "MIDDLE LEFT"])
                x += Config.CARD_WIDTH + 5

        # BOTTOM LEFT
        # first row
        x, y = left__x, Config.HEIGHT - left__y - Config.CARD_HEIGHT
        for i in range(9,13): # 10-13
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "BOTTOM LEFT"])
                x += Config.CARD_WIDTH + 5
        # second row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(13,15): # 14-15
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "BOTTOM LEFT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = left__x
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(15,18): # 16 - 18
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "MIDDLE LEFT"])
                x += Config.CARD_WIDTH + 5

        right_x = 310
        right_y = 50

        # TOP RIGHT
        # First row
        x, y = Config.WIDTH - right_x - Config.CARD_WIDTH, right_y
        for i in range(18,22): # 18 - 21
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "TOP RIGHT"])
                x += Config.CARD_WIDTH + 5
        # Second row
        x = 593
        y += Config.CARD_HEIGHT + 5
        for i in range(22,25): # 22 - 25
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "TOP RIGHT"])
                x += Config.CARD_WIDTH + 5
        # Third row
        x = 683
        y += Config.CARD_HEIGHT + 5 # 5 is card space
        for i in range(25,27): # 26-27
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "MIDDLE RIGHT"])
                x += Config.CARD_WIDTH + 5

        # BOTTOM RIGHT
        x, y = 505, Config.HEIGHT - right_y - Config.CARD_HEIGHT
        for i in range(27,31): # 28-31
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "BOTTOM RIGHT"])
                x += Config.CARD_WIDTH + 5
        # second row
        x = 683
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(31,33): # 32-33
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "BOTTOM RIGHT"])
                x += Config.CARD_WIDTH + 5
        # third row
        x = 593
        y -= (Config.CARD_HEIGHT + 5)
        for i in range(33, 36): # 34-36
            if i < len(card_images):
                self.cards.append(Piece(card_images[i], x, y, self.paired[i]))
                self.card_data.append([i, card_images[i], x, y, self.paired[i], "MIDDLE RIGHT"])
                x += Config.CARD_WIDTH + 5

        # print(f'card_data{self.card_data}')

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        for card in self.cards:
            card.draw(screen)



class Sound:
    played_sounds_global = set()  # Class-level set to track all played sounds across instances

    def __init__(self, paired):
        self.paired = paired
        self.correct_index = None
        self.all_sounds_played = False

    def play_sound(self):
        if self.all_sounds_played:
            print("All sounds have been played already")
            self.correct_index = None
            return False

        # Get available indices that haven't been played globally
        available_indices = [
            i for i in range(len(self.paired)) 
            if self.paired[i] not in Sound.played_sounds_global
        ]

        if not available_indices:
            print("All sounds have been played")
            self.all_sounds_played = True
            self.correct_index = None
            return False

        # Select a random unplayed sound
        self.correct_index = random.choice(available_indices)
        Sound.played_sounds_global.add(self.paired[self.correct_index])  # Mark as played globally

        sound_path = os.path.join(
            Config.sound_folder,
            SOUND_FILES[self.paired[self.correct_index]]
        )
        print(f"Playing sound at index: {self.correct_index} (Paired index: {self.paired[self.correct_index]})")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        return True          

# class Sound:
#     def __init__(self, paired):
#         self.paired = paired
#         self.correct_index = None
#         self.played_sounds = set()  # Track played sound indices from self.paired
#         self.all_sounds_played = False

#     def play_sound(self):
#         # if all sound have been played
#         if self.all_sounds_played:
#             print("All sounds have been played already")
#             self.correct_index = None
#             return False

#         # indices that doesnt play yet
#         available_indices = [
#             i for i in range(len(self.paired)) 
#             if i not in self.played_sounds
#         ]

#         if not available_indices:
#             print("All sounds have been played")
#             self.all_sounds_played = True
#             self.correct_index = None
#             return False

#         # Select a random unplayed sound
#         self.correct_index = random.choice(available_indices)
#         self.played_sounds.add(self.correct_index)  # Mark as played

#         sound_path = os.path.join(
#             Config.sound_folder,
#             SOUND_FILES[self.paired[self.correct_index]]
#         )
#         print(f"Playing sound at index: {self.correct_index} (Paired index: {self.paired[self.correct_index]})")
#         pygame.mixer.music.load(sound_path)
#         pygame.mixer.music.play()
#         return True

class Asset:
    def __init__(self) -> None:
        self.start_time = 0
        self.total_time = 0
        self.is_counting = False
        # Add font initialization if not already present
        self.medium_font = pygame.font.Font(None, 36)  # Example size

    def draw_countdown(self, screen, minutes):
        """minute countdown """
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
    
class User:
    def __init__(self) -> None:
        self.user_score = 0

    def draw_status(self, screen, status):
        if status == "WIN":
            bg = pygame.image.load("asset/WIN.png")
        elif status == "LOSE":
            bg = pygame.image.load("asset/LOSE.png")
        
        # Check if the background image is loaded successfully
        if bg:
            screen.blit(bg, (0, 0))


class Rahu:
    def __init__(self):
        self.images = Config.RAHU
        self.current_rahu = None
        self.game_level = None 

    def set_level(self, level): 
        """ get game level""" 
        self.game_level = level

    # def calc_prob(self):
    #     return random.random() < 0.4
    
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
    
class Narayana:
    def __init__(self) -> None:
        pass

class PieceManager:
    def __init__(self, board=None):
        # Use an existing board if provided; otherwise, create a new one
        self.board = board if board else Board()
        self.sound = Sound(self.board.paired)

    def play_next_sound(self):
        self.sound.play_sound()  # Play next unplayed sound

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


