# ai_companion_window1.py

import pygame

def create_input_window():
    pygame.init()
    screen_width = 400
    screen_height = 100
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Input Window")
    
    input_font = pygame.font.Font(None, 32)
    input_text = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill((255, 255, 255))  # Clear the screen
        pygame.draw.rect(screen, (0, 0, 0), (50, 25, 300, 50), 2)  # Draw input box

        text_surface = input_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (55, 30))  # Display input text

        pygame.display.update()

    with open("input.txt", "w") as file:
        file.write(input_text)

    return input_text

def main():
    while True:
        input_text = create_input_window()

if __name__ == "__main__":
    main()
