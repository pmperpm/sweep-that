import pygame, os
from sweepthat_config import Config
import sweepthat_menu

class CNP:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.__menu = sweepthat_menu.Menu()
        self.__card_width = 141
        self.__card_height = 172
        self.__cards_per_page = 15
        self.__rows = 3
        self.__cols = 5
        self.__current_page = 0
        self.__total_pages = (len(Config.card_prac_files) + self.__cards_per_page - 1) // self.__cards_per_page
        self.__currently_playing = None  # Track playing sound
        
        # Load background
        self.bg = pygame.image.load("asset/cnp_bg2.png")
        self.bg = pygame.transform.scale(self.bg, (Config.WIDTH, Config.HEIGHT))
        
        # Load card images
        self.__card_images = []
        for image_file in Config.card_prac_files:
            image_path = os.path.join(Config.card_prac_folder, image_file)
            img = pygame.image.load(image_path)
            img = pygame.transform.scale(img, (self.__card_width, self.__card_height))
            self.__card_images.append(img)
        
        # Load sounds
        self.__sounds = []
        for sound_file in Config.sound_files:
            sound_path = os.path.join(Config.sound_folder, sound_file)
            sound = pygame.mixer.Sound(sound_path)
            self.__sounds.append(sound)
        
        # buttons
        button_width, button_height = 120, 40
        self.__next_button = pygame.Rect(
            Config.WIDTH - 150, 
            Config.HEIGHT - 50, 
            button_width, 
            button_height
        )
        self.__back_button = pygame.Rect(
            30,
            Config.HEIGHT - 50,
            button_width,
            button_height
        )
        self.menu_button = pygame.Rect(
            Config.WIDTH // 2 - button_width // 2,
            Config.HEIGHT - 50,
            button_width,
            button_height
        )
        
        # card positions
        self.__card_positions = []
        start_x = (Config.WIDTH - (self.__cols * (self.__card_width + 10))) // 2
        start_y = 100
        
        for row in range(self.__rows):
            for col in range(self.__cols):
                x = start_x + col * (self.__card_width + 10)
                y = start_y + row * (self.__card_height + 10)
                self.__card_positions.append((x, y))
    
    def stop_current_sound(self):
        if self.__currently_playing:
            self.__currently_playing.stop()
            self.__currently_playing = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Stop playing sound
                self.stop_current_sound()
                
                if self.__next_button.collidepoint(event.pos) and self.__current_page < self.__total_pages - 1:
                    self.__current_page += 1
                    return
                
                if self.__back_button.collidepoint(event.pos) and self.__current_page > 0:
                    self.__current_page -= 1
                    return
                
                if self.menu_button.collidepoint(event.pos):
                    return "menu"
                
                # if a card was clicked
                for i in range(self.__current_page * self.__cards_per_page, 
                             min((self.__current_page + 1) * self.__cards_per_page, len(self.__card_images))):
                    card_index = i - (self.__current_page * self.__cards_per_page)
                    if card_index >= len(self.__card_positions):
                        continue
                    
                    x, y = self.__card_positions[card_index]
                    card_rect = pygame.Rect(x, y, self.__card_width, self.__card_height)
                    if card_rect.collidepoint(event.pos):
                        if i < len(self.__sounds):
                            self.stop_current_sound() # stop previous sound
                            self.__sounds[i].play()
                            self.__currently_playing = self.__sounds[i]
        
        elif event.type == pygame.QUIT:
            self.stop_current_sound()
            return "quit"
        
        return None
    
    def draw(self):
        # background
        self.screen.blit(self.bg, (0, 0))
        
        # current page of cards
        start_index = self.__current_page * self.__cards_per_page
        end_index = min(start_index + self.__cards_per_page, len(self.__card_images))
        
        for i in range(start_index, end_index):
            card_index = i - start_index
            if card_index >= len(self.__card_positions):
                continue
                
            x, y = self.__card_positions[card_index]
            self.screen.blit(self.__card_images[i], (x, y))
        
        font = pygame.font.Font(Config.FONT_PATH, 24)
        
        # Back button
        if self.__current_page > 0:
            pygame.draw.rect(self.screen, Config.COLORS["WHITE"], self.__back_button)
            text = font.render("Back", True, Config.COLORS["DARK_BLUE"])
            text_rect = text.get_rect(center=self.__back_button.center)
            self.screen.blit(text, text_rect)
        
        # Next button
        if self.__current_page < self.__total_pages - 1:
            pygame.draw.rect(self.screen, Config.COLORS["WHITE"], self.__next_button)
            text = font.render("Next", True, Config.COLORS["DARK_BLUE"])
            text_rect = text.get_rect(center=self.__next_button.center)
            self.screen.blit(text, text_rect)
        
        pygame.draw.rect(self.screen, Config.COLORS["WHITE"], self.menu_button)
        text = font.render("Menu", True, Config.COLORS["DARK_BLUE"])
        text_rect = text.get_rect(center=self.menu_button.center)
        self.screen.blit(text, text_rect)
            
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_current_sound()
                    return "quit"
                
                result = self.handle_event(event)
                if result == "menu":
                    self.stop_current_sound()
                    self.__menu.run()
            
            self.screen.fill((255, 255, 255))
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "quit"
