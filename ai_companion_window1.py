
# ai_companion_window1.py

import pygame

def create_input_window():
    pygame.init()
    screen_width = 400
    screen_height = 150
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Input Window")
    
    input_font = pygame.font.Font(None, 32)
    input_text = ""
    city_text = ""
    input_active = True
    city_entered = False

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not city_entered:
                        city_entered = True
                    else:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if not city_entered:
                        input_text = input_text[:-1]
                    else:
                        city_text = city_text[:-1]
                else:
                    if not city_entered:
                        input_text += event.unicode
                    else:
                        city_text += event.unicode

        screen.fill((255, 255, 255))  # Clear the screen
        pygame.draw.rect(screen, (0, 0, 0), (50, 10, 300, 50), 2)  # Draw input box for input
        pygame.draw.rect(screen, (0, 0, 0), (50, 70, 300, 50), 2)  # Draw input box for city input

        text_surface = input_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 15))  # Display input text
        
        
        text_surface = input_font.render(city_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 75))  # Display city text

        pygame.display.update()

    with open("input.txt", "w") as file:
        file.write(input_text)
    with open("city.txt", "w") as file:
        file.write(city_text)

    return (input_text, city_text)

def main():
    while True:
        input_text = create_input_window()
        city_text = create_input_window()

if __name__ == "__main__":
    main()
