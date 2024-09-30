import requests
from PIL import Image
import pytesseract
from io import BytesIO
from bs4 import BeautifulSoup

URL = 'https://iocletenders.nic.in/nicgep/app?page=FrontEndTendersByLocation&service=page'

session = requests.Session()
response = session.get(URL)

soup = BeautifulSoup(response.content, 'html.parser')
captcha_image_url = soup.find('img', {'id': 'captchaImage'})['src']
captcha_image_url = 'https://iocletenders.nic.in' + captcha_image_url

captcha_image_response = session.get(captcha_image_url)

captcha_image = Image.open(BytesIO(captcha_image_response.content))
captcha_text = pytesseract.image_to_string(captcha_image)

print("CAPTCHA Text:", captcha_text)

payload = {
    'captcha_input_name': captcha_text,
}

response = session.post(URL, data=payload)

print(response.content)
