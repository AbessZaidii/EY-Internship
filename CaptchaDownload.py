from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import cv2
from PIL import Image
import pytesseract
import numpy as np

driver_path = 'path_to_your_webdriver'

url = 'https://iocletenders.nic.in/nicgep/app?page=FrontEndTendersByLocation&service=page'

driver = webdriver.Chrome(executable_path=driver_path)

driver.get(url)

time.sleep(5)

captcha_image = driver.find_element(By.XPATH, '//*[@id="imgCaptcha"]')

captcha_url = captcha_image.get_attribute('src')
print(f"CAPTCHA URL: {captcha_url}")

response = requests.get(captcha_url)
captcha_image_path = 'downloaded_captcha.png'

with open(captcha_image_path, 'wb') as f:
    f.write(response.content)

print(f"CAPTCHA image downloaded and saved at: {captcha_image_path}")

driver.quit()

image = cv2.imread(captcha_image_path)

save_folder = 'captcha_images'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

original_captcha_path = os.path.join(save_folder, 'original_captcha.png')
cv2.imwrite(original_captcha_path, image)
print(f"Original CAPTCHA image saved at: {original_captcha_path}")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((1, 1), np.uint8)
processed_image = cv2.dilate(thresh_image, kernel, iterations=1)
processed_image = cv2.erode(processed_image, kernel, iterations=1)

processed_captcha_path = os.path.join(save_folder, 'processed_captcha.png')
cv2.imwrite(processed_captcha_path, processed_image)
print(f"Processed CAPTCHA image saved at: {processed_captcha_path}")

pil_image = Image.fromarray(processed_image)

captcha_text = pytesseract.image_to_string(pil_image)

print("Extracted Text:", captcha_text)
