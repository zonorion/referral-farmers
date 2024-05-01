import asyncio
import random
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from selenium import webdriver

MAIL_DOMAIN = '@maildrop.cc'
# zon.lucifer@gmail.com
# PARAM_REF_LINK = 'https://paramgaming.com/?referCode=2DB4064178#/signup'
# tanhoang.cntt@gmail.com
# PARAM_REF_LINK = 'https://paramgaming.com/?referCode=B50AF67760#/signup'
# tanhm.vn@gmail.com
PARAM_REF_LINK = 'https://paramgaming.com/?referCode=64E821357F#/signup'
# tanhoang.eth@gmail.com
# PARAM_REF_LINK = 'https://paramgaming.com/?referCode=A43CBDFD16#/signup'
PARAM_PWD = '123456789!@'

PROXY_HOST = "119.42.38.143"
PROXY_PORT = "6325"
PROXY_USER = "tonggiang"
PROXY_PASS = "Zxcv123123"


class Param:
    async def batching_signup(self, concurrency, from_number, to_number):
        # TODO: add farmers
        # farmer_list = ['z-meme', 'z-pepe', 'z-bobo', 'z-momo']
        # farmer_list = ['poopoo', 'booboo', 'moomoo', 'zoozoo', 'ziizii', 'piipii', 'tiitii']
        farmer_list = ['zz-poopooz', 'zz-boobooz', 'zz-moomooz', 'zz-zoozooz', 'zz-ziiziiz', 'zz-piipiiz', 'zz-tiitiiz']
        farm_numbers = [i for i in range(from_number, to_number)]
        chunked_numbers = [farm_numbers[i:i + concurrency] for i in range(0, len(farm_numbers), concurrency)]
        for chunk in chunked_numbers:
            try:
                tasks = [self.signup_param(f'{random.choice(farmer_list)}{i}', is_confirm=True, retry_time=0) for i in
                         chunk]
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                print(e.message)
                pass

    async def signup_param(self, username, is_confirm=True, retry_time=0):
        print(f"Start {'confirm' if is_confirm else 'login'} to account {username}\n")
        mail = f'{username}{MAIL_DOMAIN}'
        mail_url = f'https://maildrop.cc/inbox/?mailbox={username}'
        print(f'Mail url: {mail_url}\n')
        driver = Driver(uc=True, headless=True, d_width=1280, d_height=960,
                        proxy=f'{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}')
        try:
            driver.get('https://nowsecure.nl')
            await asyncio.sleep(5)
            driver.get(PARAM_REF_LINK)
            await asyncio.sleep(5)
            driver.find_element(by=By.ID, value='email').click()
            driver.find_element(by=By.ID, value='email').send_keys(mail)
            await asyncio.sleep(0.5)
            driver.find_element(by=By.ID, value='password').click()
            driver.find_element(by=By.ID, value='password').send_keys(PARAM_PWD)
            await asyncio.sleep(0.5)
            driver.find_element(by=By.ID, value='cPassword').click()
            driver.find_element(by=By.ID, value='cPassword').send_keys(PARAM_PWD)
            await asyncio.sleep(0.5)
            driver.find_element(by=By.ID, value='disclaimer').click()
            await asyncio.sleep(0.5)
            driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/div/div[3]/div/form/div[5]/button').click()
            await asyncio.sleep(1)
            driver.get(mail_url)
            await asyncio.sleep(10)
            refresh_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Refresh')]"))
            )
            refresh_btn.click()
            active_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[2]/div/div[3][contains(., 'Activate')]"))
            )
            active_link.click()
            await asyncio.sleep(5)
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(iframes[0])
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/center/div[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/a[1]")
                )
            ).click()
            await asyncio.sleep(5)
            print(f'{datetime.now()} Successfully confirmed {username}')
        except Exception as e:
            print(e)
        finally:
            driver.quit()
