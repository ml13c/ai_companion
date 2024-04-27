# ai_companion_window2.py
from datetime import datetime
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
    
def read_city_text():
    if os.path.exists("city.txt"):
        with open("city.txt", "r") as file:
            city_text = file.read().strip()
        # Clear the city input file after reading
        open("city.txt", "w").close()
        return city_text
    else:
        return None

def read_startup_text():
    if os.path.exists("startup.txt"):
        with open("startup.txt", "r") as file:
            startup_text = file.read().strip()
        open("startup.txt", "w").close()
        return startup_text
    else: return None

def get_weather_data(city_text):
    user_api = os.environ['current_weather_data']
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + city_text + "&appid=" + user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    
    try:
        # Extract weather information
        temp_city = (1.8 * (api_data['main']['temp'] - 273.15) + 32)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

        # Format weather information as a string
        weather_info = f"{city_text.upper()}  || {date_time}\n"
        weather_info += "{:.2f} F\n".format(temp_city)
        weather_info += f"{weather_desc}\n"
        weather_info += f"Humidity  : {hmdt}%\n"
        weather_info += f"Wind Speed : {wind_spd} kmph"
        

        return weather_info
    except KeyError as e:
        print(f"Error occurred while fetching weather data: {e}")
        return "Failed to fetch weather data for " + city_text

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
    weather_box_width = 370
    weather_box_height = 150
    weather_box_x = 50
    weather_box_y = 50

    weather_font = pygame.font.Font('freesansbold.ttf', 20)  # Font for weather information

    running = True
    clock = pygame.time.Clock()

    previous_input_text = None  # Store the previous input text
    previous_city_text = None   #Store previous city text

    screen.fill((0, 0, 0))  # Fill the screen with black initially
    screen.blit(default_image, (screen_width // 2 - default_image.get_width() // 2, screen_height // 2 - default_image.get_height() // 2))
    pygame.display.flip()  # Update the display with the default image
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        input_text = read_input_text()
        city_text = read_city_text()


        if input_text != previous_input_text or city_text != previous_city_text:  # Check if the input text has changed
            if input_text:
                if input_text.lower() == "hello":
                    image_url = "https://th.bing.com/th/id/OIP.UWqdBnAIc0qReLdc3pdoVgHadA?rs=1&pid=ImgDetMain"
                    weather_info = None  # Clear weather info if user input is "hello"
                elif input_text.lower() == "weather":
                    if city_text:#if city_text is read or entered
                        if city_text =="dallas" or "london" or "paris":#idk why any city goes through but it works how i want-(fix--in [city,city,city])
                            print("went through if city is dallas", city_text)
                            image_url = "https://th.bing.com/th/id/OIP.h76oAZ679LlVOdwM59y00AHaGN?w=206&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"
                            # Example weather information
                            weather_info = get_weather_data(city_text)
                            print(weather_info)
                        else:
                            print("city other than dallas entered:", city_text)
                    else:
                        print("blank-run through location")
                        
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
                    weather_lines = weather_info.split('\n')
                    for i, line in enumerate(weather_lines):
                        text_surface = weather_font.render(line, True, (0, 0, 0))  # Render text with black color
                        text_rect = text_surface.get_rect()
                        text_rect.topleft = (weather_box_x + 10, weather_box_y + 10 + (i * 25))  # Adjust position and spacing
                        screen.blit(text_surface, text_rect)

                pygame.display.flip()
                previous_input_text = input_text  # Update the previous input text
                previous_city_text = city_text

        clock.tick(30)

    pygame.quit()

def main():
    default_image_url = "https://i.ytimg.com/vi/-Dx4yVlxmBU/maxresdefault.jpg"
    display_image_window(default_image_url)

if __name__ == "__main__":
    main()
