import pygame, random, pygame_gui

pygame.init()


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image


counter = 0
def draw():
    global found_word
    WIN.blit(title_surf, title_rect)

    if counter >= 0 and counter <= 7:
        WIN.blit(frames[counter], (0, 150))
    
    # Calculate the total width of all the letters
    total_width = len(random_word) * FONT.size(" ")[0]
    # Calculate the starting position to center the text horizontally
    start_x = (WIDTH - total_width) // 2
    # Start drawing from this x-coordinate
    x = start_x

    found_word = True
    
    for letter in random_word:
        if letter in guessed_letters:
            img = FONT.render(letter, True, "White")
            WIN.blit(img, (x, HEIGHT/2))
        else:
            img = FONT.render("_", True, "White")  # Display underscores for unguessed letters
            WIN.blit(img, (x, HEIGHT/2))
            found_word = False
        # Move to the next position for the next letter
        x += FONT.size(letter)[0]  # Increase x by the width of the current letter
        
        # Add some space between letters
        x += 10
    
    
def user_guess(letter):
    global counter

    if letter in random_word:
        guessed_letters.append(letter)

    else:
        counter += 1


def restart_game():
    global counter, guessed_letters, random_word

    if counter == 7 or found_word:
        counter = 0
        guessed_letters = []
        random_word = random.choice(list_of_words)


list_of_words = ["apple", "banana", "coconut", "grape", "kiwi", "lemon", "mango", "orange", "pineapple", "raspberry", "strawberry", "watermelon"]
guessed_letters = []
random_word = random.choice(list_of_words)

WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()
UI_REFRESH_RATE = clock.tick(60)/1000
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))

FONT = pygame.font.Font("assets/font.ttf", 30)
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect= pygame.Rect((350, 250), (60, 50)), manager= MANAGER, object_id= "#main_text_entry")

title_surf = pygame.image.load("assets/title.png").convert_alpha()
title_rect = title_surf.get_rect(topleft= (200, 0))

sprite_sheet_image = pygame.image.load('assets/spritesheet.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

frames = []
for i in range(8):
    frames.append(sprite_sheet.get_image(i, 32, 32, 5, "BLACK"))

running = True
while running:
    clock.tick(60)
    WIN.fill("black")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
            user_guess(event.text)

        MANAGER.process_events(event)

         
    draw()
    MANAGER.update(UI_REFRESH_RATE)
    MANAGER.draw_ui(WIN)
    restart_game()
    pygame.display.update()

pygame.quit()
