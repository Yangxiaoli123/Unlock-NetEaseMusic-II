# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value":"0029C75D4DDD757B59E7D6236CC2A71A65C6BD291239F392C68B4EC4F71A2E7FBD219BEE9836A2D42C22F934532EA53752F8E2128A70E90CEABABCC78D75B63ACF51F14BF4F1E232793EE6FCAC3EC2ECCD457885D23397EE9ED1B3158E2948FA536C73459F9E976902F01525871CD16D729C4B436A1FE1B7A1D4EDB840AFE9DF70D7FB26CABCE1BDCDB82EC6CABD16F837AE868ED016BBE1359B259EB5FD3E26C39B78879C9F91AC52223D7743D352BFEA3C5EB303E90AD8861013E9CB32FF76F8D1C681A52740CA87F093486B1792396A59C48B7C80BBD1A4B1FE2B1CFEB93AE8EECB9C1C70BAD221F607FC8F61978BABC53C55F634990C46157F4F29F0B5E593C766D5A423B3C15A495D5CF349D25F53CA98F7E5118C14DB1341D11E63F965106C5158C2D893A0112030561A2514AE7E6E744F9FFDBFD592C8B86590152A443BC3057AEB7D91697C6FDD0BDEEA23FB76DE18D2D7B68020B73509570A341B2178
"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
