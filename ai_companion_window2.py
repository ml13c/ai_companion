# ai_companion_window2.py

import pygame
import requests
from io import BytesIO
import os

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print("Failed to download image:", response.status_code)
        return None

def read_input_text():
    if os.path.exists("input.txt"):
        with open("input.txt", "r") as file:
            input_text = file.read().strip()
        # Clear the input file after reading
        open("input.txt", "w").close()
        return input_text
    else:
        return None


def display_image_window(default_image_url, weather_info=None):
    pygame.init()
    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Image Display")
    
    default_image_data = download_image(default_image_url)
    if default_image_data:
        default_image = pygame.image.load(default_image_data).convert_alpha()
    else:
        print("Failed to load default image.")
        pygame.quit()
        return

    # Define the dimensions and position of the weather info box
    weather_box_width = 300
    weather_box_height = 100
    weather_box_x = 50
    weather_box_y = 50

    weather_font = pygame.font.Font(None, 24)  # Font for weather information

    running = True
    clock = pygame.time.Clock()

    previous_input_text = None  # Store the previous input text

    screen.fill((0, 0, 0))  # Fill the screen with black initially
    screen.blit(default_image, (screen_width // 2 - default_image.get_width() // 2, screen_height // 2 - default_image.get_height() // 2))
    pygame.display.flip()  # Update the display with the default image

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        input_text = read_input_text()

        if input_text != previous_input_text:  # Check if the input text has changed
            if input_text:
                if input_text.lower() == "hello":
                    image_url = "https://th.bing.com/th/id/OIP.UWqdBnAIc0qReLdc3pdoVgHadA?rs=1&pid=ImgDetMain"
                    weather_info = None  # Clear weather info if user input is "hello"
                elif input_text.lower() == "weather":
                    image_url = "https://th.bing.com/th/id/OIP.APU3wubdujwCOog0fPieEgHaJ4?rs=1&pid=ImgDetMain"
                    # Example weather information
                    weather_info = "Weather: Sunny, 25°C"
                else:
                    print("Im sorry I dont quite understand.")
                    previous_input_text = input_text  # Update the previous input text
                    continue

                image_data = download_image(image_url)
                if image_data:
                    image = pygame.image.load(image_data).convert_alpha()
                    screen.fill((0, 0, 0))
                    screen.blit(image, (screen_width // 2 - image.get_width() // 2, screen_height // 2 - image.get_height() // 2))
                
                # Draw weather info box
                
                if weather_info:
                    # Display weather information inside the box
                    pygame.draw.rect(screen, (255, 255, 255), (weather_box_x, weather_box_y, weather_box_width, weather_box_height))
                    text_surface = weather_font.render(weather_info, True, (0, 0, 0))
                    screen.blit(text_surface, (weather_box_x + 10, weather_box_y + 10))  # Adjust position as needed

                pygame.display.flip()
                previous_input_text = input_text  # Update the previous input text

        clock.tick(30)

    pygame.quit()

def main():
    default_image_url = "https://i.ytimg.com/vi/-Dx4yVlxmBU/maxresdefault.jpg"
    display_image_window(default_image_url)

if __name__ == "__main__":
    main()
