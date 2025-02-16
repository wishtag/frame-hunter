import os
from PIL import ImageGrab, Image
import pyautogui
import imagehash
import time
import pydirectinput
import numpy as np
from datetime import datetime, date
from pytz import timezone
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def read_json(file):
    f = open (file, "r")
    data = json.loads(f.read())
    f.close()
    return data

def write_json(file, object):
    f = open (file, "w")
    json.dump(object, f)
    f.close()

json_time = read_json("resets.json")["total_seconds"]
isShiny = False

color = [255,198,206]
#color2 = [107,165,165]
#delayUp = 0.2
#delayLow = 0.6

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
    #bush = ImageGrab.grab(bbox=(1727,279,1791,343))
    #bush.save(f"img/bush{resets["resets"]}.png")
    #bush.close()
    pyautogui.hotkey('shift', 'f1')
    pyautogui.hotkey('ctrl', 'p')
    pydirectinput.press('x')
    pydirectinput.keyDown('tab')
    time.sleep(0.8)
    pydirectinput.keyUp('tab')

    screenshot = ImageGrab.grab(bbox=(1644,445,1652,458))
    pixels = screenshot.load()
    screenshot.close()

    r, g, b = pixels[1, 1]
    if r != color[0] or g != color[1] or b != color[2]:
        isShiny = True
        print("Is Shiny\nSave State Created")
        screenshot = ImageGrab.grab(bbox=(961,247,1919,885))
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

        webhook = DiscordWebhook(url="", username="Sparkles")
        with open("img/screenshot.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="screenshot.png")
        embed = DiscordEmbed(title=f"Shiny Mew Found", description=f"{resets['resets']} encounters over the span of {time_formatted} ({resets["total_seconds"]})", color="FCDE3A")
        embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
        embed.set_image(url="attachment://screenshot.png")
        embed.set_footer(text="Emerald")
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

        print(f"Not Shiny, {resets["resets"]} encounters {time_formatted} ({resets["total_seconds"]} seconds)")
        write_json("resets.json", resets)


"""
while isShiny == False:
    time.sleep(.5)
    for i in range(7):
        pydirectinput.press('down')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(2):
        pydirectinput.press('left')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(3):
        pydirectinput.press('down')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(7):
        pydirectinput.press('left')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(5):
        pydirectinput.press('down')
        time.sleep(np.random.uniform(delayLow, delayUp))

    time.sleep(1.5)
    pydirectinput.press('up')
    pydirectinput.press('up')
    time.sleep(3)
    for i in range(3):
        pydirectinput.press('up')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(5):
        pydirectinput.press('right')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(10):
        pydirectinput.press('up')
        time.sleep(np.random.uniform(delayLow, delayUp))
    for i in range(4):
        pydirectinput.press('right')
        time.sleep(np.random.uniform(delayLow, delayUp))
    pydirectinput.press('down')
    time.sleep(0.5)
    pydirectinput.press('x')
    time.sleep(8)

    screenshot = ImageGrab.grab(bbox=(1644,445,1652,458))
    pixels = screenshot.load()
    screenshot.close()

    r, g, b = pixels[1, 1]
    if r != color[0] or g != color[1] or b != color[2]:
        screenshot2 = ImageGrab.grab(bbox=(1680,780,1684,784))
        pixels2 = screenshot2.load()
        screenshot2.close()

        r2, g2, b2 = pixels2[1, 1]
        if r2 == color2[0] and g2 == color2[1] and b2 == color2[2]:
            isShiny = True
            print("Is Shiny\nSave State Created")
            screenshot = ImageGrab.grab(bbox=(961,247,1919,885))
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

            webhook = DiscordWebhook(url=, username="Sparkles")
            with open("img/screenshot.png", "rb") as f:
                webhook.add_file(file=f.read(), filename="screenshot.png")
            embed = DiscordEmbed(title=f"Shiny Mew Found", description=f"{resets['resets']} encounters over the span of {time_formatted} ({resets["total_seconds"]})", color="FCDE3A")
            embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
            embed.set_image(url="attachment://screenshot.png")
            embed.set_footer(text="Emerald")
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
        else:
            print("Got off track, reloading to save state")
            pyautogui.press('f1')
            #print("Got off track, soft reseting...")
            #pyautogui.hotkey('ctrl', 'r')
            #time.sleep(3.5)
            #pydirectinput.press('x')
            #time.sleep(1)
            #pydirectinput.press('x')
            #time.sleep(0.5)
            #pydirectinput.press('x')
            #time.sleep(1)
            #pydirectinput.press('x')
            #time.sleep(2)
            #pydirectinput.press('x')
            #time.sleep(2)
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

        print(f"Not Shiny, {resets["resets"]} encounters {time_formatted} ({resets["total_seconds"]} seconds)")
        write_json("resets.json", resets)
        
        pydirectinput.press('x')
        time.sleep(3)
        pydirectinput.press('down')
        pydirectinput.press('right')
        pydirectinput.press('x')
        time.sleep(1)
        pydirectinput.press('x')
        time.sleep(4)
        pydirectinput.press('x')

        pyautogui.hotkey('shift', 'f1')
"""