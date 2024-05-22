import threading
import time
import subprocess
import requests
import os
from datetime import datetime
import pygame
import geocoder
import pyttsx3
import speech_recognition as sr
from g4f.client import Client
import nest_asyncio
nest_asyncio.apply()
keyword_detected = False
#listen after cortana
def listen_for_command():
    global keyword_detected
    while keyword_detected:
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source2:
                print("Listening after cortana booted up...")
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2, timeout=10)  # 10 seconds no input = timeout
                # Using Google to recognize audio
                cortana_input = r.recognize_google(audio2).lower()
                print("cortana reads:", cortana_input)
                if engine._inLoop:
                    engine.endLoop()
                if "weather in" in cortana_input:
                    testaction = "weather"
                    city_text = cortana_input.split("weather in", 1)[1].strip()
                    print(f"Fetching weather for {city_text}")
                    #weather based on city
                    weather_info = get_weather_data(city_text)
                    print(weather_info)
                    engine.say(weather_info)
                    engine.runAndWait()
                elif "weather" in cortana_input:
                    testaction = "weather"
                    print("weather data being shown")
                    #weather current location
                    weather_info = get_latlonweather_data()
                    print(weather_info)
                    engine.say(weather_info)
                    engine.runAndWait()
                # Exit condition
                elif "exit" in cortana_input:
                    print("going back to sleep")
                    keyword_detected = False
                    break
                else:
                    # Pass user input to GPT-3.5 for further processing
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": cortana_input}],
                    )
                    # Output GPT-3.5 response
                    print("GPT-3.5 Response:", response.choices[0].message.content)
                    engine.say(response.choices[0].message.content)
                    engine.runAndWait()  # Ensure this is only called once    
                                    
        except sr.WaitTimeoutError:
            print("No input received. Going back to sleep.")
            keyword_detected = False
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
#city weather
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
#location weather
def get_latlonweather_data():
    user_api = os.environ['current_weather_data']
    g = geocoder.ip('me')
    lat, lon = g.latlng
    lat_str = str(lat)
    lon_str = str(lon)
    print(g.latlng)
    print(lat, lon)
    complete_latlon_link ="https://api.openweathermap.org/data/2.5/weather?lat="+lat_str+"&lon="+lon_str+"&appid="+user_api
    latlon_link = requests.get(complete_latlon_link)
    latlon_data = latlon_link.json()
    try:
        #variables for latlon data
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        temp_latlon = (1.8*((latlon_data['main']['temp']) - 273.15)+32)
        tempmin_latlon = (1.8*((latlon_data['main']['temp_min']) - 273.15)+32)
        tempmax_latlon = (1.8*((latlon_data['main']['temp_max']) - 273.15)+32)
        weather_latlon = latlon_data['weather'][0]['description']
        hmdt_latlon = latlon_data['main']['humidity']
        windspd_latlon = latlon_data['wind']['speed']
        latlon_location = latlon_data['name']
        #format
        weather_info = f"{latlon_location.upper()}  || {date_time}\n"
        weather_info += "{:.2f} F\n".format(temp_latlon)
        weather_info += "Max: {:.2f} F\n".format(tempmax_latlon)
        weather_info += "Min: {:.2f} F\n".format(tempmin_latlon)
        weather_info += f"{weather_latlon}\n"
        weather_info += f"Humidity  : {hmdt_latlon}%\n"
        weather_info += f"Wind Speed : {windspd_latlon} kmph"
        
        return weather_info
    except KeyError as e:
        print(f"Error occurred while fetching weather data: {e}")
        return "Failed to fetch weather data for " + latlon_location
# Initialize the recognizer 
r = sr.Recognizer() 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)
client = Client()

def listen_for_keyword():
    global keyword_detected
    while not keyword_detected:
        try:
        #use mic as input
            with sr.Microphone() as source:
                print("Listening")
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                user_input = r.recognize_google(audio).lower()
                print("Heard: ", user_input)#constantly listens for cortana
                
                if "cortana" in user_input:#if cortana is heard it checks if there was a command after so you dont have to repeat it again
                    keyword_detected = True
                    parts = user_input.split("cortana")
                    if len(parts) > 1:
                        after_cortana = parts[1].strip()
                        if "weather in" in after_cortana:
                            city_text = after_cortana.split("weather in", 1)[1].strip()
                            print(f"Fetching weather for {city_text}")
                            #weather based on city
                            weather_info = get_weather_data(city_text)
                            print(weather_info)
                            engine.say(weather_info)
                            engine.runAndWait()
                        elif "weather" in after_cortana:
                            print("weather data being shown")
                            #weather current location
                            weather_info = get_latlonweather_data()
                            print(weather_info)
                            engine.say(weather_info)
                            engine.runAndWait()
                        else:
                        # Pass user input to GPT-3.5 for further processing
                            response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[{"role": "user", "content": after_cortana}],
                            )
                            # Output GPT-3.5 response
                            print("GPT-3.5 Response:", response.choices[0].message.content)
                            engine.say(response.choices[0].message.content)
                            engine.runAndWait()  # Ensure this is only called once 

                    else:
                        after_cortana= ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")


# Start the keyword listener in a separate thread
keyword_thread = threading.Thread(target=listen_for_keyword, daemon=True)
keyword_thread.start()

# Wait for the keyword detection before starting the animation script
while not keyword_detected:
    time.sleep(1)

animation_thread = threading.Thread(target=lambda: subprocess.run(["python", "animation.py"]))
animation_thread.start()
listen_for_command()

# Once the keyword is detected, start the animation script
