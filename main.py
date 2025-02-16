import os
from PIL import ImageGrab
import pyautogui
import time
import pydirectinput
from datetime import datetime
from pytz import timezone
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def read_json(file):
    with open(os.path.abspath(file), 'r') as f:
        data = json.loads(f.read())
    return data

def write_json(file, object):
    with open(os.path.abspath(file), 'w') as f:
        json.dump(object, f)

settings = read_json("settings.json")
discord = settings["discord"]
bounding_boxes = settings["bounding_boxes"]

json_time = read_json("resets.json")["total_seconds"]
isShiny = False

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

print("Make sure the window is focused on")
time.sleep(3)

try:
    os.remove("img/screenshot.png")
except:
    pass

while isShiny == False:
    resets = read_json("resets.json")

    pyautogui.press('f1')
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.1)
    pyautogui.hotkey('shift', 'f1')
    pyautogui.hotkey('ctrl', 'p')
    pydirectinput.press('x')
    pydirectinput.keyDown('tab')
    while True:
        time.sleep(0.005)
        screenshot = ImageGrab.grab(bbox=settings["screen_size"])
        pixels = screenshot.load()
        screenshot.close()
        print(pixels[bounding_boxes["name_plate"][0], bounding_boxes["name_plate"][1]])
        r, g, b = pixels[bounding_boxes["name_plate"][0], bounding_boxes["name_plate"][1]]
        if r == settings["colors"]["name_plate"][0] and g == settings["colors"]["name_plate"][1] and b == settings["colors"]["name_plate"][2]:
            break
    pydirectinput.keyUp('tab')

    screenshot = ImageGrab.grab(bbox=settings["screen_size"])
    pixels = screenshot.load()
    screenshot.close()

    r, g, b = pixels[bounding_boxes["encounter"][0], bounding_boxes["encounter"][1]]
    if r != settings["colors"]["encounter"][0] or g != settings["colors"]["encounter"][1] or b != settings["colors"]["encounter"][2]:
        isShiny = True
        print("Is Shiny\nSave State Created")
        screenshot = ImageGrab.grab(bbox=bounding_boxes["game_screen"])
        screenshot.save("img/screenshot.png")
        screenshot.close()
        pyautogui.hotkey('shift', 'f9')

        hour = datetime.now(timezone('US/Central')).hour
        minute = datetime.now(timezone('US/Central')).minute
        second = datetime.now(timezone('US/Central')).second
        current_time = (hour*60**2) + (minute*60) + second
        elapsed_time = current_time - start_time
        resets = read_json("resets.json")
        resets["resets"] = resets["resets"] + 1
        resets["total_seconds"] = json_time + elapsed_time
        write_json("resets.json", resets)

        resets = read_json("resets.json")

        seconds = resets["total_seconds"]
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

        webhook = DiscordWebhook(url=discord["url"], username=discord["name"])
        with open("img/screenshot.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="screenshot.png")
        embed = DiscordEmbed(title=f"Shiny {settings['pokemon_name']} Found", description=f"{resets['resets']} encounters over the span of {time_formatted} ({resets['total_seconds']})", color="FCDE3A")
        embed.set_author(name="Shiny Found", icon_url=discord["icon"])
        embed.set_image(url="attachment://screenshot.png")
        embed.set_footer(text=discord["game"])
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()
    else:
        hour = datetime.now(timezone('US/Central')).hour
        minute = datetime.now(timezone('US/Central')).minute
        second = datetime.now(timezone('US/Central')).second
        current_time = (hour*60**2) + (minute*60) + second
        elapsed_time = current_time - start_time
        resets = read_json("resets.json")
        resets["resets"] = resets["resets"] + 1
        resets["total_seconds"] = json_time + elapsed_time

        s = resets["total_seconds"]
        h = str(int(s // 3600)).zfill(2)
        m = str(int((s % 3600) // 60)).zfill(2)
        s = str(int(s % 60)).zfill(2)
        time_formatted = f"{h}:{m}:{s}"

        print(f"Not Shiny, {resets['resets']} encounters {time_formatted} ({resets['total_seconds']} seconds)")
        write_json("resets.json", resets)