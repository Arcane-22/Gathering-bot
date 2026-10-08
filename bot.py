import numpy as np
import mss
import pyautogui
import keyboard
import time

from config import PANIC_KEY, START_DELAY
from detection import find_tree, wander_click_point
from chat import read_chat, chop_succeeded, inventory_full, is_chopping

running = True

def stop_bot():
    global running
    running = False
    print("\n[PANIC] Stopping.")

keyboard.add_hotkey(PANIC_KEY, stop_bot)


def wait_for_result(sct, max_seconds=15):
    started_chopping = False
    last_line = read_chat(sct)

    for _ in range(max_seconds):
        time.sleep(1)
        current_line = read_chat(sct)

        if current_line == last_line:
            continue

        last_line = current_line

        if inventory_full(current_line):
            return "full"
        if chop_succeeded(current_line):
            return "success"
        if not started_chopping and is_chopping(current_line):
            print("Started chopping, waiting for completion...")
            started_chopping = True

    return "timeout"


print(f"Starting in {START_DELAY} seconds. Press {PANIC_KEY.upper()} anytime to stop.")
time.sleep(START_DELAY)

with mss.MSS() as sct:
    monitor = sct.monitors[1]

    while running:
        frame = np.array(sct.grab(monitor))
        frame_bgr = frame[:, :, :3]

        tree = find_tree(frame_bgr)

        if tree is None:
            wx, wy = wander_click_point(frame_bgr.shape[1], frame_bgr.shape[0])
            print(f"No tree found, wandering to ({wx}, {wy})")
            pyautogui.click(wx, wy)
            time.sleep(3)
            continue

        print(f"Clicking tree at {tree}")
        pyautogui.click(tree)

        result = wait_for_result(sct)

        if result == "full":
            print("Inventory full! Stopping.")
            running = False
        elif result == "success":
            print("Chop succeeded!")
        else:
            print("No success detected, trying next tree.")

print("Stopped.")