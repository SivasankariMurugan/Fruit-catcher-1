import pgzrun
import random

TITLE = "Fruit Catcher"
WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (175, 238, 238)
BUTTON_COLOR = (100, 200, 100)
TEXT_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)

game_active = False
current_level = 0
level1_over = False
level2_over = False

basket = Actor("basket", (WIDTH // 2, HEIGHT - 50))
falling_objects = []
fruits = ["apple", "banana", "strawberry"]
bombs = ["bomb1", "bomb2"]
speed = 2
score = 0
high_score = 0
target_fruit = random.choice(fruits)
time_left = 60

def basket_control():
    if keyboard.left and basket.x > 70:
        basket.x -= 5
    if keyboard.right and basket.x < WIDTH - 70:
        basket.x += 5

def fruit_bomb_generator():
    if random.randint(1, 100) == 1:
        new_fruit = Actor(random.choice(fruits), (random.randint(50, WIDTH - 50), 0))
        collision = False
        for obj in falling_objects:
            if new_fruit.colliderect(obj):
                collision = True
        if not collision:
            falling_objects.append(new_fruit)
    if random.randint(1, 150) == 1:
        new_bomb = Actor(random.choice(bombs), (random.randint(50, WIDTH - 50), 0))
        collision = False
        for obj in falling_objects:
            if new_bomb.colliderect(obj):
                collision = True
        if not collision:
            falling_objects.append(new_bomb)

def collision_detection():
    global score
    for obj in falling_objects:
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

def begin():
    global game_active, score, falling_objects, current_level, speed, time_left
    game_active = True
    score = 0
    falling_objects.clear()
    current_level = 1
    speed = 2
    time_left = 60

def draw():
    screen.fill(BACKGROUND_COLOR)
    if game_active:
        basket.draw()
        for obj in falling_objects:
            obj.draw()
        display_score()
        screen.draw.text(f"Time left: {time_left}", topright=(WIDTH - 10, 10), fontsize=30, color=BLACK)
        if current_level == 1:
            screen.draw.text(f"Catch only {target_fruit}!", topleft=(200, 12), fontsize=30, color=BLACK)
    else:
        if not level1_over:
            screen.draw.filled_rect(Rect((250, 90), (100, 40)), BUTTON_COLOR)
            screen.draw.text("Start", center=(300, 110), fontsize=24, color=TEXT_COLOR)
            screen.draw.text("Fruit Catcher", center=(300, 50), fontsize=40, color=TEXT_COLOR)
            if current_level > 0:
                screen.draw.text(f"Score: {score}", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=40, color=TEXT_COLOR)
                screen.draw.text(f"High Score: {high_score}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=40, color=TEXT_COLOR)
        if level1_over:
            rect = Rect((250, HEIGHT // 2 - 20), (120, 50))
            screen.draw.filled_rect(rect, BUTTON_COLOR)
            screen.draw.text("Begin Level 2", center=rect.center, fontsize=24, color=TEXT_COLOR)
            screen.draw.text(f"Level 1 ended", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=30, color=BLACK)

def on_mouse_down(pos):
    global current_level
    if not game_active:
        start_rect = Rect((250, 90), (100, 40))
        level2_rect = Rect((250, HEIGHT // 2 - 20), (100, 40))
        if start_rect.collidepoint(pos):
            begin()
        elif level1_over and level2_rect.collidepoint(pos):
            current_level = 2
            begin()


def display_score():
    screen.draw.text(f"Score: {score}", topleft=(12, 12), fontsize=30, color=BLACK)
    screen.draw.text(f"Level: {current_level}", topleft=(12, 45), fontsize=30, color=BLACK)

def level_checker():
    global level1_over, level2_over, current_level
    if current_level == 1 and (score >= 30 or time_left == 0):
        level1_over = True
        end_level()
    elif current_level == 2 and (score >= 40 or time_left == 0):
        level2_over = True
        end_level()

def update():
    if not game_active:
        return
    for obj in falling_objects:
        obj.y += speed
    basket_control()
    collision_detection()
    fruit_bomb_generator()
    level_checker()

def end_level():
    global game_active, high_score
    game_active = False
    if score > high_score:
        high_score = score

def update_timer():
    global time_left, game_active
    if time_left > 0:
        time_left -= 1
    else:
        clock.unschedule(update_timer)
        end_level()


clock.schedule_interval(update_timer, 1.0)
pgzrun.go()



