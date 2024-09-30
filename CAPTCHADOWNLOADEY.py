from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import cv2
from PIL import Image
import pytesseract
import numpy as np

webdriver_path = 'path_to_webdriver'
page_url = 'https://iocletenders.nic.in/nicgep/app?page=FrontEndTendersByLocation&service=page'

browser = webdriver.Chrome(executable_path=webdriver_path)
browser.get(page_url)

time.sleep(5)

captcha_element = browser.find_element(By.XPATH, '//*[@id="imgCaptcha"]')
captcha_image_url = captcha_element.get_attribute('src')
print(f"CAPTCHA image URL: {captcha_image_url}")

image_response = requests.get(captcha_image_url)
captcha_image_file = 'captcha_image.png'

with open(captcha_image_file, 'wb') as image_file:
    image_file.write(image_response.content)

print(f"Downloaded CAPTCHA image saved as: {captcha_image_file}")

browser.quit()

captcha_image = cv2.imread(captcha_image_file)
output_folder = 'saved_captchas'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

raw_captcha_path = os.path.join(output_folder, 'raw_captcha.png')
cv2.imwrite(raw_captcha_path, captcha_image)
print(f"Raw CAPTCHA saved at: {raw_captcha_path}")

gray_captcha = cv2.cvtColor(captcha_image, cv2.COLOR_BGR2GRAY)
_, thresholded_captcha = cv2.threshold(gray_captcha, 150, 255, cv2.THRESH_BINARY_INV)

morph_kernel = np.ones((1, 1), np.uint8)
captcha_processed = cv2.dilate(thresholded_captcha, morph_kernel, iterations=1)
captcha_processed = cv2.erode(captcha_processed, morph_kernel, iterations=1)

processed_captcha_path = os.path.join(output_folder, 'processed_captcha.png')
cv2.imwrite(processed_captcha_path, captcha_processed)
print(f"Processed CAPTCHA saved at: {processed_captcha_path}")

captcha_image_pil = Image.fromarray(captcha_processed)
extracted_text = pytesseract.image_to_string(captcha_image_pil)
print("Extracted CAPTCHA text:", extracted_text)
