import pgzrun
from pygame.transform import scale


WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (207, 159, 255) 
BUTTON_COLOR = (100, 200, 100) 
TEXT_COLOR = (0, 0, 0) 
game_active = False  # Game state to determine if the game should run


basket = Actor("basket", (WIDTH // 2, HEIGHT - 50))

def draw():
    if game_active:
        screen.fill(BACKGROUND_COLOR)
        basket.draw()       
    else: 
        screen.fill(BACKGROUND_COLOR)
        screen.draw.filled_rect(Rect((250, 90), (100, 40)), BUTTON_COLOR)
        screen.draw.text("Start", center=(300, 110), fontsize=24, color=TEXT_COLOR)
        screen.draw.text("Fruit Catcher", center=(300, 50), fontsize=40, color=TEXT_COLOR)

def update():
    global game_active

    if not game_active:
        return

    # Move the basket
    if keyboard.left and basket.x > 70:
        basket.x -= 5
    if keyboard.right and basket.x < WIDTH - 70:
        basket.x += 5

def on_mouse_down(pos):
    global game_active
    # Check if the start button is clicked
    if not game_active and Rect((250, 90), (100, 40)).collidepoint(pos):
        game_active = True
        print("Start button clicked! Game is now active.")


pgzrun.go()