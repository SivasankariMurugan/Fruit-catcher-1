import pgzrun
import random


WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (207, 159, 255)
BUTTON_COLOR = (100, 200, 100)
TEXT_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
game_active = False
current_level = 0


basket = Actor("basket", (WIDTH // 2, HEIGHT - 50))
falling_objects = []
fruits = ["apple", "banana", "strawberry"]
bombs = ["bomb1", "bomb2"]
speed = 2
score = 0
high_score = 0
target_fruit = "apple"

def begin():
    global game_active, score,  falling_objects, current_level, speed
    game_active = True
    score = 0
 
    falling_objects.clear()
    current_level = 1
    speed = 2

def upcoming_levels():
    global game_active,  falling_objects, current_level, speed
    game_active = True

    falling_objects.clear()
    current_level += 1
    if current_level == 2:
        speed = 3

def draw():
    screen.fill(BACKGROUND_COLOR)
    if game_active:
        basket.draw()
        for obj in falling_objects:
            obj.draw()
        display_score(score)
        
        if current_level == 1:
            screen.draw.text(
                f"Catch only {target_fruit}!",
                topleft=(200, 12),
                fontsize=30,
                color=BLACK
            )
    else:
        screen.draw.filled_rect(Rect((250, 90), (100, 40)), BUTTON_COLOR)
        screen.draw.text("Start", center=(300, 110), fontsize=24, color=TEXT_COLOR)
        screen.draw.text("Fruit Catcher", center=(300, 50), fontsize=40, color=TEXT_COLOR)
        if current_level > 0:
            screen.draw.text(f"Score: {score}", center=(300, 300), fontsize=40, color=TEXT_COLOR)
            screen.draw.text(f"High Score: {high_score}", center=(300, 360), fontsize=40, color=TEXT_COLOR)

def display_score(score):
    screen.draw.text(f"Score: {score}", topleft=(12, 12), fontsize=30, color=BLACK)


def update():
    global game_active, speed, score

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
            if current_level == 1 and obj.image == target_fruit:
                score += 10
            elif obj.image in fruits:
                score += 5
            elif obj.image in bombs:
                score -= 5
            falling_objects.remove(obj)
        elif obj.y > HEIGHT:
            falling_objects.remove(obj)

    # Spawn new objects
    if random.randint(1, 80) == 1:
        if random.randint(1, 4) > 1:
            new_object = Actor(random.choice(fruits), (random.randint(50, WIDTH - 50), 0))
            if not any(new_object.colliderect(obj) for obj in falling_objects):
                falling_objects.append(new_object)
        else:
            new_object = Actor(random.choice(bombs), (random.randint(50, WIDTH - 50), 0))
            if not any(new_object.colliderect(obj) for obj in falling_objects):
                falling_objects.append(new_object)

def end_level():
    global game_active, high_score
    game_active = False
    if score > high_score:
        high_score = score
    if current_level == 1:
        upcoming_levels()
    else:
        display_end_screen()


def on_mouse_down(pos):
    global game_active
    if not game_active and Rect((250, 90), (100, 40)).collidepoint(pos):
        if current_level == 0:
            begin()
        else:
            upcoming_levels()

pgzrun.go()
