import time
import cv2
import numpy as np
import pyautogui

def find_image_occurrences(screenshot, cropped_image):
    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    cropped_image_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Find the width and height of the cropped image
    w, h = cropped_image_gray.shape[::-1]

    # Perform template matching to find occurrences of the cropped image in the screenshot
    res = cv2.matchTemplate(screenshot_gray, cropped_image_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold for matching
    threshold = 0.8
    loc = np.where(res >= threshold)

    midpoints = []
    for pt in zip(*loc[::-1]):
        # Calculate the midpoint of the detected occurrence
        mid_x = pt[0] + w // 2
        mid_y = pt[1] + h // 2
        midpoints.append((pt[0], pt[1], w, h))  # Add (x, y, width, height) for rectangle

    return midpoints

def draw_rectangles(screenshot, occurrences):
    for (x, y, w, h) in occurrences:
        # Draw a rectangle around the occurrences
        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return screenshot

time.sleep(3)

# Take a screenshot of the current screen
screenshot = pyautogui.screenshot()
screenshot = np.array(screenshot)
screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

# Load the cropped image
cropped_image = cv2.imread('img.png')

# Find occurrences
occurrences = find_image_occurrences(screenshot, cropped_image)

# Draw rectangles around occurrences
screenshot_with_rectangles = draw_rectangles(screenshot, occurrences)

# Print the coordinates and display/save the image
print("Occurrences with rectangles:")
for (x, y, w, h) in occurrences:
    mid_x = x + w // 2
    mid_y = y + h // 2
    print(f"Midpoint: ({mid_x}, {mid_y})")

# Save or display the result
cv2.imwrite('screenshot_with_rectangles.png', screenshot_with_rectangles)
cv2.imshow('Detected Occurrences', screenshot_with_rectangles)
cv2.waitKey(0)
cv2.destroyAllWindows()


# use the pymouse
# While(True):
    # find the occurences of the comment button
    # for each occurence click --> type --> Ctrl+Enter
    # Click pg down


# make a beautiful code with object oriented programming






















