import time
import cv2
import numpy as np
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import pyautogui
import pyperclip


class ImageFinder:
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def find_image_occurrences(self, screenshot, cropped_image):
        # Convert images to grayscale
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        cropped_image_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # Find the width and height of the cropped image
        w, h = cropped_image_gray.shape[::-1]

        # Perform template matching to find occurrences of the cropped image in the screenshot
        res = cv2.matchTemplate(screenshot_gray, cropped_image_gray, cv2.TM_CCOEFF_NORMED)

        # Set a threshold for matching
        loc = np.where(res >= self.threshold)

        occurrences = []
        for pt in zip(*loc[::-1]):
            # Add (x, y, width, height) for rectangle
            occurrences.append((pt[0], pt[1], w, h))

        return occurrences


class AutomationBot:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def click_and_type(self, x, y):
        # Move the mouse to the position and click
        self.mouse.position = (x, y)
        self.mouse.click(Button.left)
        time.sleep(0.5)
        # Type and press Ctrl+Enter
        self.keyboard.type('https://x.com/shitstorm73w/status/1808066702179291387')
        time.sleep(0.5)

        self.keyboard.press(Key.ctrl_l)
        time.sleep(0.2)
        self.keyboard.press(Key.enter)
        time.sleep(0.2)
        self.keyboard.release(Key.ctrl_l)
        time.sleep(0.5)

    def page_down(self):
        self.keyboard.press(Key.page_down)
        self.keyboard.release(Key.page_down)

    def copy_url(self):
        self.keyboard.press(Key.ctrl_l)
        self.keyboard.press('l')  # Focus the address bar
        self.keyboard.release(Key.ctrl_l)
        self.keyboard.release('l')
        time.sleep(0.5)
        self.keyboard.press(Key.ctrl_l)
        self.keyboard.press('c')  # Copy the URL
        self.keyboard.release(Key.ctrl_l)
        self.keyboard.release('c')
        time.sleep(0.5)

        # Retrieve the copied URL
        url = pyperclip.paste()
        return url

    def navigate_back(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.alt_l)


class Main:
    def __init__(self):
        self.image_finder = ImageFinder()
        self.bot = AutomationBot()

    def run(self):
        while True:
            time.sleep(3)

            # Take a screenshot of the current screen
            screenshot = pyautogui.screenshot()

            # Load the cropped image
            cropped_image = cv2.imread('img.png')

            # Find occurrences
            occurrences = self.image_finder.find_image_occurrences(screenshot, cropped_image)

            # Print the coordinates
            print("Occurrences:")
            for (x, y, w, h) in occurrences:
                mid_x = x + w // 2
                mid_y = y + h // 2
                print(f"Midpoint: ({mid_x}, {mid_y})")

            # Perform automation tasks
            for (x, y, w, h) in occurrences:
                self.bot.click_and_type(x + w // 2, y + h // 2)
                time.sleep(1.5)
                
            # Scroll down the page
            self.bot.page_down()
            time.sleep(2)  # Wait before the next iteration

            # Copy the URL from the address bar
            url = self.bot.copy_url()

            # Check if the URL contains "search?q"
            if "search?q" not in url:
                self.bot.navigate_back()



if __name__ == "__main__":
    main = Main()
    main.run()
