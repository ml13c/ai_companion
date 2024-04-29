import pygame

def create_input_window():
    pygame.init()
    screen_width = 400
    screen_height = 250
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Input Window")
    
    input_font = pygame.font.Font(None, 32)
    startup_text = ""
    input_text = ""
    city_text = ""
    startup_active = True
    input_active = False
    city_entered = False

    while startup_active or input_active or city_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if startup_active:
                        startup_active = False
                        input_active = True
                    elif input_active:
                        input_active = False
                        city_entered = True
                    else:
                        city_entered = False
                elif event.key == pygame.K_BACKSPACE:
                    if input_active:
                        input_text = input_text[:-1]
                    elif city_entered:
                        city_text = city_text[:-1]
                    else:
                        startup_active = startup_active[:-1]
                else:
                    if input_active:
                        input_text += event.unicode
                    elif city_entered:
                        city_text += event.unicode
                    else:
                        startup_text += event.unicode

        screen.fill((255, 255, 255))  # Clear the screen
        pygame.draw.rect(screen, (0, 0, 0), (50, 10, 300, 50), 2)  # Draw input box for startup
        pygame.draw.rect(screen, (0, 0, 0), (50, 70, 300, 50), 2)  # Draw input box for input
        pygame.draw.rect(screen, (0, 0, 0), (50, 130, 300, 50), 2)  # Draw input box for city input
        
        text_surface = input_font.render(startup_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 15))  # Display startup text

        text_surface = input_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 75))  # Display input text
        
        text_surface = input_font.render(city_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 135))  # Display city text

        pygame.display.update()

    with open("input.txt", "w") as file:
        file.write(input_text)
    with open("city.txt", "w") as file:
        file.write(city_text)
    with open("startup.txt", "w") as file:
        file.write(startup_text)

    return (input_text, city_text, startup_text)

def main():
    while True:
        startup_text, input_text, city_text = create_input_window()
        
if __name__ == "__main__":
    main()
