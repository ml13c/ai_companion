import pygame
import spritessheet
import threading
import time

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Cortanabit-animationframes.png').convert_alpha()
sprite_sheet = spritessheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)

# Make a list storing each frame for animations
animation_list = []
# Define the number of frames for each action
animation_frames = {
    'idle': 11,
    'weather': 15,
    'cross': 11,
    'crossstill': 3,  # Assuming crossstill is from frame 39 to 45
    'uncross': 9,
    'dismiss': 15,
    'still': 3
}

actions = ['idle', 'weather', 'cross', 'crossstill', 'uncross', 'dismiss', 'still']
step_counter = 0

# Load frames for each action
for action in actions:
    temp_img_list = []
    for _ in range(animation_frames[action]):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 500, 500, 1.4))
        step_counter += 1
    animation_list.append(temp_img_list)

action_map = {'idle': 0, 'weather': 1, 'cross': 2, 'crossstill': 3, 'uncross': 4, 'dismiss': 5, 'still': 6}
action = 6
last_update = pygame.time.get_ticks()
animation_cooldown = 150
frame = 0
animation_active = False


def listen_for_input():
    global action, next_action, animation_active
    while True:
        user_input = input()
        if user_input in action_map:
            if action == action_map['crossstill'] and action_map[user_input] != action_map['uncross']:
                next_action = action_map[user_input]
                action = action_map['uncross']
            else:
                action = action_map[user_input]
                animation_active = True  # Mark the animation as active

# Start the input listener in a separate thread
input_thread = threading.Thread(target=listen_for_input, daemon=True)
input_thread.start()

run = True
while run:
    # Update background
    screen.fill(BG)
    
    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0
            if action == action_map['cross']:
                action = action_map['crossstill']  # Transition to crossstill after cross completes
            elif action == action_map['crossstill']:
                frame = 0  # Loop back to the start of crossstill
            elif action == action_map['uncross'] and next_action is not None:
                action = next_action
                next_action = None
                animation_active = True  # Mark the animation as active
            elif animation_active:
                action = 6  # Reset action to still after completing the animation
                animation_active = False  # Mark the animation as inactive
    
    # Show frame image
    screen.blit(animation_list[action][frame], (0, 0))
        
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
