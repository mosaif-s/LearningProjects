from audioop import error

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
from dotenv import load_dotenv

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://tinder.com")

wait = WebDriverWait(driver, 10)

# Step 1: Reject cookies (if present)
try:
    reject_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o874957067"]/div/div[2]/div/div/div[1]/div[2]/button')))
    reject_button.click()
except:
    print("No cookies panel")

# Step 2: Click "Log in"
sign_in_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in")))
sign_in_button.click()

# Step 3: Click "Log in with Facebook"
facebook_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Log in with Facebook']")))
facebook_btn.click()

# Step 4: Switch to Facebook popup
time.sleep(3)
main_window = driver.current_window_handle
popup_window = [w for w in driver.window_handles if w != main_window][0]
driver.switch_to.window(popup_window)

# Step 5: Enter Facebook credentials
email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
email_input.send_keys(ACCOUNT_EMAIL)

password_input = driver.find_element(By.ID, "pass")
password_input.send_keys(ACCOUNT_PASSWORD)
password_input.send_keys(Keys.ENTER)

# Step 6: Click "Continue as Matthew" if prompted
try:
    continue_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Continue as Matthew']"))
    )
    continue_btn.click()
except:
    print("No 'Continue as Matthew' prompt")

# Step 7: Return to Tinder window
time.sleep(3)
driver.switch_to.window(main_window)

# Step 8: Handle Tinder permission prompts
try:
    allow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Allow']")))
    allow_btn.click()
except:
    print("No location prompt")

try:
    allow_btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="o-853424009"]/div/div/div/div/div[3]/button[2]')))
    allow_btn2.click()
except:
    print("No notifications prompt")

print("✅ Logged in and ready to swipe.")
for n in range(100):

    #Add a 1 second delay between likes.
    time.sleep(1)

    try:
        print("called")
        like_button = driver.find_elements(By.CSS_SELECTOR, 'button[type="button"]')[-1]
        like_button.click()

    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click()

        except NoSuchElementException:
            time.sleep(3)

driver.quit()

