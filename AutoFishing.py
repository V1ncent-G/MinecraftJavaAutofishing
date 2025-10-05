# Vincent Guo - 10/5/2025

# Update plans:
    # CRITICAL - recasts a second time after retrieving for some reason. Problem caused by sample rate being high and seeing bobber splash after it has already retrieved
    # Handle full inventory
    # Handle broken rods
    # Allow full screen

# Notes, please read:
    # Run following command in terminal (open terminal with ctrl+~) to install:
        # pip install easyocr rich pyautogui numpy
    
    # Turn on minecraft subtitles. Music & sound > closed caption > ON
    # Program keyboard interrupt with ctrl+C or kill terminal
    # Works best if minecraft is on split screen. Program is ~25% of the left and minecraft is ~75% of the right 
    # Start the AutoFishing.py program on vsc or cmd. Tab into minecraft and afk fish

import cv2
import easyocr
import pyautogui
import numpy as np
import time
from rich import print
import os

os.system("cls")
print("[bold deep_sky_blue1]Starting Auto-Fisher - " + time.asctime())

# ------------- SETTINGS -------------
KEYWORDS = ["splashes"]  # loose match for MC subtitles
CLICK_POS = (3000, 1200)  # where your bobber/right-click should land (verify!)
RIGHT_CLICK_DELAY = 0.5
LOOP_SLEEP = 0.2
# ------------------------------------

# Choose a safer region default (right/bottom area) — tweak as needed
W, H = pyautogui.size()
screenRegion = (int(W*0.7), int(H*0.6), int(W*0.28), int(H*0.35))

catchCount = 0
reader = easyocr.Reader(["en"], gpu=False)

# One-time debug frame: confirm subtitles are inside the OCR region
dbg = pyautogui.screenshot(region=screenRegion)
dbg.save("debug_grab.png")
print("[yellow]Saved debug_grab.png. Open it to ensure subtitles are visible in the region.")

try:
    while True:
        phraseFound = False

        screenCapture = pyautogui.screenshot(region=screenRegion)
        ocrImage = cv2.cvtColor(np.array(screenCapture), cv2.COLOR_RGB2BGR)
        results = reader.readtext(ocrImage)  # list of (bbox, text, conf)

        # Log what OCR sees (first few entries)
        if results:
            seen = [r[1] for r in results[:5]]
            print(f"[grey50]OCR saw: {seen}        ", end="\r")

        for _, text, conf in results:
            t = text.lower()
            if any(k in t for k in KEYWORDS):
                phraseFound = True
                catchCount += 1
                print(f"\n[grey89]Attempting catch number: [grey58]{catchCount}  (matched: '{text}', conf={conf:.2f})")
                pyautogui.moveTo(*CLICK_POS)
                pyautogui.click(button="right")
                break

        if phraseFound:
            time.sleep(RIGHT_CLICK_DELAY)
            pyautogui.click(button="right")

        time.sleep(LOOP_SLEEP)

except KeyboardInterrupt:
    print("\n[green]Stopped by user.")
