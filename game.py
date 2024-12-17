import pgzrun
import random
import time

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
level1_score = 0
basket = Actor("basket", (WIDTH // 2, HEIGHT - 50))
falling_objects = []
fruits = ["apple", "banana", "strawberry"]
bombs = ["bomb1", "bomb2"]
speed = 2
score = 0
high_score = 0

time_left = 60
total_time_taken = 0
level1_time = 0
level2_time = 0
target_fruit1=random.choice(fruits)
target_fruit2=random.choice(fruits)
background_image=game_bg

def load_highscore():
    global high_score
    try:
        with open("highscore.txt", "r") as file:
            content = file.read()
            if content:
                high_score = int(content)
            else:
                high_score = 0
    except FileNotFoundError:
        high_score = 0

def save_highscore():
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))


def basket_control():
    if keyboard.left and basket.x > 70:
        basket.x -= 5
    if keyboard.right and basket.x < WIDTH - 70:
        basket.x += 5

def fruit_bomb_generator():
    if random.randint(1, 90) == 1:
        new_fruit = Actor(random.choice(fruits), (random.randint(50, WIDTH - 50), 0))
        collision = False
        for obj in falling_objects:
            if new_fruit.colliderect(obj):
                collision = True
        if not collision:
            falling_objects.append(new_fruit)
    if random.randint(1, 145) == 1:
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
            if current_level==1:
                if obj.image == target_fruit1:
                    score += 10
                elif obj.image in bombs:
                    score -= 5
                elif obj.image in fruits:
                    score += 5                
            elif current_level==2:
                if obj.image == target_fruit2:
                    score += 10
                elif obj.image in bombs:
                    score -= 10
                elif obj.image in fruits:
                    score += 5
            falling_objects.remove(obj)
        elif obj.y > HEIGHT:
            falling_objects.remove(obj)


def begin():
    global game_active, score, falling_objects, current_level, speed, time_left, start_time
    game_active = True
    score = 0
    load_highscore()
    falling_objects.clear()
    start_time = time.time()
    if current_level == 1:
        speed = 2
    elif current_level == 2:
        speed = 3
    time_left = 60
    clock.unschedule(update_timer) 
    clock.schedule_interval(update_timer, 1.0) 

 
def draw():
    screen.blit(background_image, (0, 0))
    if game_active:
        basket.draw()
        for obj in falling_objects:
            obj.draw()
        display_score()
        screen.draw.text(f"Time left: {time_left}", topright=(WIDTH - 10, 10), fontsize=30, color=BLACK)
        if current_level==1:
            screen.draw.text(f"Catch only {target_fruit1}!",topleft=(200, 12),
        fontsize=30,
        color=BLACK
            )
        else:
            screen.draw.text(f"Catch only {target_fruit2}!",topleft=(200, 12),
        fontsize=30,
        color=BLACK
            )
    else:
        if not level1_over or level2_over:
            screen.draw.filled_rect(Rect((250, 90), (100, 40)), BUTTON_COLOR)
            screen.draw.text("Start", center=(300, 110), fontsize=24, color=TEXT_COLOR)
            screen.draw.text("Fruit Catcher", center=(300, 50), fontsize=40, color=TEXT_COLOR)
        elif level1_over and not level2_over:
            rect = Rect((250, HEIGHT // 2 - 20), (120, 50))
            screen.draw.filled_rect(rect, BUTTON_COLOR)
            screen.draw.text("Begin Level 2", center=rect.center, fontsize=26, color=TEXT_COLOR)
            screen.draw.text(f"Level 1 ended", center=(WIDTH // 2 + 10, HEIGHT // 2 - 80), fontsize=26, color=BLACK)
            screen.draw.text(f"Level 1 Score: {score}", center=(WIDTH // 2 + 10, HEIGHT // 2 - 40), fontsize=26, color=TEXT_COLOR)
        elif level2_over:
            screen.draw.text(f"Level 2 Score: {score}", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=40, color=TEXT_COLOR)
            screen.draw.text(f"Total Score: {score + level1_score}", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=40, color=TEXT_COLOR)
            screen.draw.text(f"High Score: {high_score}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=40, color=TEXT_COLOR)
            screen.draw.text(f"Total Time Taken: {total_time_taken} s", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color=TEXT_COLOR)

def on_mouse_down(pos):
    global current_level, level1_over
    if not game_active:
        start_rect = Rect((250, 90), (100, 40))
        level2_rect = Rect((250, HEIGHT // 2 - 20), (100, 40))
        if start_rect.collidepoint(pos):
            current_level = 1
            begin()
        elif level1_over and level2_rect.collidepoint(pos):
            current_level = 2
            begin()

def display_score():
    screen.draw.text(f"Score: {score}", topleft=(12, 12), fontsize=30, color=BLACK)
    screen.draw.text(f"Level: {current_level}", topleft=(12, 45), fontsize=30, color=BLACK)

def level_checker():
    global level1_over, level2_over, current_level, level1_score, level1_time, level2_time
    if current_level == 1 and score >= 100 or time_left==0:
        level1_time = 60 - time_left
        level1_score = score
        level1_over = True
        end_level()
    elif current_level == 2 and score >= 150 or time_left==0:
        level2_time = 60 - time_left
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
    global game_active, high_score, total_time_taken,level2_over
    game_active = False
    if level2_over and (score + level1_score) > high_score:
        high_score = score + level1_score
        save_highscore()
    if current_level == 1:
        total_time_taken = level1_time
    elif current_level == 2:
        total_time_taken = level1_time + level2_time
        level2_over=True

def update_timer():
    global time_left, game_active
    if time_left > 0:
        time_left -= 1
    else:
        clock.unschedule(update_timer)
        end_level()

clock.schedule_interval(update_timer, 1.0)
pgzrun.go()