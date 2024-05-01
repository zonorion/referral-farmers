import asyncio
import os
import random

import undetected_chromedriver as uc
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

MAIL_DOMAIN = '@congnt24.baby'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
REF = 'https://link.uprock.com/i/3f7f4748'


class Uprock:
    async def signup_uprock(self, username):
        print(f"Start register account {username}\n")
        mail = f'{username}{MAIL_DOMAIN}'
        # mail_url = f'https://maildrop.cc/inbox/?mailbox={username}'
        # print(f'Mail url: {mail_url}\n')
        options = uc.ChromeOptions()
        # create_proxy_extension()
        # options.add_argument('--auto-open-devtools-for-tabs')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        # options.add_argument(f"--load-extension={PROXY_FOLDER}")
        options.add_argument("--window-size=1280,960")
        driver = uc.Chrome(options=options, headless=False)
        try:
            driver.get(REF)
            await asyncio.sleep(5)
            driver.find_element(by=By.ID, value='react-aria-:R2tjff5lta:').click()
            driver.find_element(by=By.ID, value='react-aria-:R2tjff5lta:').send_keys(mail)
            await asyncio.sleep(0.5)
            driver.find_element(by=By.XPATH, value="/html/body/main/div/div/main/div/div/div/form/div/div[3]/button").click()
            await asyncio.sleep(0.5)
            driver.execute_script(f"window.open('https://yopmail.com/');")
            driver.switch_to.window(driver.window_handles[-1])
            await asyncio.sleep(3)
            driver.find_element(by=By.ID, value='login').click()
            driver.find_element(by=By.ID, value='login').send_keys('congnt24')
            await asyncio.sleep(0.5)
            driver.find_element(by=By.XPATH, value='//*[@id="refreshbut"]/button').click()
            await asyncio.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="refresh"]'))
            ).click()
            await asyncio.sleep(5)
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(iframes[2])
            confirm_url = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="mail"]/div/table[2]/tbody/tr/td/p[3]/span/a')
                )
            ).get_attribute('href')
            driver.find_element(by=By.XPATH, value="/html/body/header/div[2]/button[2]").click()
            await asyncio.sleep(1)
            print(confirm_url)
            driver.get('https://nowsecure.nl')
            await asyncio.sleep(3)
            driver.get(confirm_url)
            # driver.switch_to.window(driver.window_handles[-1])
            await asyncio.sleep(5)
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[@title='Widget containing a Cloudflare security challenge']")))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))).click()
            await asyncio.sleep(100000)

            # for window_handle in driver.window_handles:
            #     print(window_handle)
            # driver.switch_to.window(driver.window_handles[-1])
        except Exception as e:
            print('Oops! Something went wrong: ', e)
        finally:
            await asyncio.sleep(60)
            driver.close()
