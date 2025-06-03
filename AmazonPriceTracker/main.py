import smtplib
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
load_dotenv()
from_address=os.getenv("from_address")
to_address=os.getenv("to_address")
password=os.getenv("password")

live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(live_url, headers=headers)
soup=BeautifulSoup(response.content, "html.parser")
element = float(soup.find(class_="a-offscreen").getText().split("$")[1])
print(element)


title = soup.find(id="productTitle").get_text().strip()
print(title)
BUY_PRICE = 100

if element < BUY_PRICE:
    message = f"{title} is on sale for {element}!"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(from_address, password)
        connection.sendmail(
            from_addr=from_address,
            to_addrs=to_address,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}".encode("utf-8")
        )