import pgzrun
from pygame.transform import scale
import random


WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (207, 159, 255) 
BUTTON_COLOR = (100, 200, 100) 
TEXT_COLOR = (0, 0, 0) 
game_active = False  # Game state to determine if the game should run


basket = Actor("basket", (WIDTH // 2, HEIGHT - 50))
falling_objects = []
fruits = ["apple", "banana", "strawberry"]
bombs = ["bomb1", "bomb2"]
speed = 2
score = 0



def draw():
    if game_active:
        screen.fill(BACKGROUND_COLOR)
        basket.draw()       
        for obj in falling_objects:
            obj.draw()
    else: 
        screen.fill(BACKGROUND_COLOR)
        screen.draw.filled_rect(Rect((250, 90), (100, 40)), BUTTON_COLOR)
        screen.draw.text("Start", center=(300, 110), fontsize=24, color=TEXT_COLOR)
        screen.draw.text("Fruit Catcher", center=(300, 50), fontsize=40, color=TEXT_COLOR)

def update():
    global game_active, speed, score

    print("SCORE:", score)

    if not game_active:
        return

    # Move the basket
    if keyboard.left and basket.x > 70:
        basket.x -= 5
    if keyboard.right and basket.x < WIDTH - 70:
        basket.x += 5

     # Update falling objects
    for obj in falling_objects:
        obj.y += speed

        # Check if object is caught by basket
        if obj.y >= basket.top and obj.colliderect(basket):
            print("SCORE:", score)
            if obj.image in fruits:
                score += 10
            elif obj.image in bombs:
                score -= 5
            falling_objects.remove(obj)

        elif obj.y > HEIGHT:
            falling_objects.remove(obj)

       # Spawn new objects
    if random.randint(1, 80) == 1:
        if random.randint(1,4)>1:
            new_object = Actor(random.choice(fruits), (random.randint(50, WIDTH - 50), 0))
            if not any(new_object.colliderect(obj) for obj in falling_objects):
                falling_objects.append(new_object)
        else:
            new_object = Actor(random.choice(bombs), (random.randint(50, WIDTH - 50), 0))
            if not any(new_object.colliderect(obj) for obj in falling_objects):
                falling_objects.append(new_object)
    

def on_mouse_down(pos):
    global game_active
    # Check if the start button is clicked
    if not game_active and Rect((250, 90), (100, 40)).collidepoint(pos):
        game_active = True

pgzrun.go()