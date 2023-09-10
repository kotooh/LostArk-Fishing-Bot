import time
import random
import cv2
import keyboard
import numpy as np
import pydirectinput
import datetime

from PIL import ImageGrab

fishX, fishY = 1111, 263

fishing = cv2.imread('image.png', 0)
templateWidth, templateHeight = fishing.shape[::-1]

print("Fishing will be started in 5 seconds!")
pydirectinput.click(x=fishX, y=fishY, button="right")
time.sleep(5)
print("Started!")

def main():
    cast = True
    successCount = 1
    lastCastTimestamp = None

    while True:
        currentTime = datetime.datetime.now()

        # repair
        if successCount % 10 == 0:
            sleep(5000, 5000)
            togglePetWindow()

            pydirectinput.click(x=1245, y=700, button="left")
            sleep(1000, 1000)
            pydirectinput.click(x=730, y=800, button="left")
            sleep(1000, 1000)
            pydirectinput.click(x=915, y=630, button="left")
            sleep(1000, 1000)
            pydirectinput.press("esc")
            sleep(1000, 1000)

            togglePetWindow()
            successCount += 1
            
            pydirectinput.click(x=fishX, y=fishY, button="right")
            sleep(2000, 2000)

        if cast or currentTime >= lastCastTimestamp + datetime.timedelta(seconds = 30):
            print("Casting out lure")
            keyboard.press_and_release('e')
            cast = False
            
            lastCastTimestamp = currentTime
            continue

        imagePixels = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        pixelsNumpy = np.array(imagePixels)

        grayscaleImage = cv2.cvtColor(pixelsNumpy, cv2.COLOR_BGR2GRAY)
        templateMatch = cv2.matchTemplate(
            grayscaleImage, fishing, cv2.TM_CCOEFF_NORMED)
        matchLocations = np.where(templateMatch >= 0.8)

        for point in zip(*matchLocations[::-1]):
            if point != None:
                print("Detected catch! Reeling in lure")
                keyboard.press_and_release('e')
                cast = True
                time.sleep(random.uniform(6, 7.5))

                successCount += 1
                break

        time.sleep(0.500)

def sleep(min, max):
    sleepTime = random.randint(min, max) / 1000.0
    if sleepTime < 0:
        return
    time.sleep(sleepTime)

def togglePetWindow():
    pydirectinput.keyDown('alt')
    sleep(10, 30)
    pydirectinput.press('p')
    sleep(10, 30)
    pydirectinput.keyUp('alt')
    sleep(10, 30)

    sleep(400, 500)

main()