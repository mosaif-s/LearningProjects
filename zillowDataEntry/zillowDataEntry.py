import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
l1=[]
l2=[]
l3=[]
class zillowDataEntry:
    def __init__(self):
        return

    def zillowScrape(self):
        global l1,l2,l3
        url = 'https://appbrewery.github.io/Zillow-Clone/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        l1=soup.find_all('address')
        l1=[element.text.strip() for element in l1]
        print(l1)

        l2=soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')  # Note: use class_ not class
        l2=[ele.text[0:6] for ele in l2]
        print(l2)

        class_a='StyledPropertyCardDataArea-anchor'
        l3=soup.find_all('a', class_=class_a)
        l3=[ele['href'] for ele in l3]
        print(l3)

    def formFill(self, address, price, link):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSczZtOaOxUhGeNLQumujXPM96pNkFsrzeHEh1aSaMz5rQUdEA/viewform")

        # address_input = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        # )
        # address_input.send_keys(address)
        # address_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
        # i commented up because i thought prescence doesnt mean it is typable (nor does visibility)
        # race condition- google loading, and you typing

        address_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )
        address_input.send_keys(address)
        print(2)
        price_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_input.send_keys(price)

        link_input = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input.send_keys(link)

        xpath='/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div'
        submit_button = driver.find_element(By.XPATH, value=xpath)
        submit_button.click()
        driver.quit()




zl=zillowDataEntry()
zl.zillowScrape()

for i in range(len(l1)):
    zl.formFill(l1[i],l2[i],l3[i])