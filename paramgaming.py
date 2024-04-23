import asyncio
import os
import random

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

PROXY_FOLDER = os.path.join('extension', 'proxy')
PROXY_HOST = "119.42.38.143"
PROXY_PORT = "6325"
PROXY_USER = "tonggiang"
PROXY_PASS = "Zxcv123123"

MAIL_DOMAIN = '@maildrop.cc'
# PARAM_REF_LINK = 'https://paramgaming.com/?referCode=2DB4064178#/signup'
PARAM_REF_LINK = 'https://paramgaming.com/?referCode=B50AF67760#/signup'
PARAM_PWD = '123456789!@'


def create_proxy_extension():
    manifest_json = """
    {
      "version": "1.0.0",
      "manifest_version": 3,
      "name": "Chrome Proxy",
      "permissions": [
        "proxy",
        "tabs",
        "storage",
        "webRequest",
        "webRequestAuthProvider"
      ],
      "host_permissions": [
        "<all_urls>"
      ],
      "background": {
        "service_worker": "background.js"
      },
      "minimum_chrome_version": "22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    with open(f"{PROXY_FOLDER}/manifest.json", "w") as f:
        f.write(manifest_json)
    with open(f"{PROXY_FOLDER}/background.js", "w") as f:
        f.write(background_js)


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"


class ParamGaming:
    async def batching_signup(self, concurrency, from_number, to_number):
        # TODO: add farmers
        # farmer_list = ['z-meme', 'z-pepe', 'z-bobo', 'z-momo']
        farmer_list = ['poopoo', 'booboo', 'moomoo', 'zoozoo', 'ziizii', 'piipii', 'tiitii']
        farm_numbers = [i for i in range(from_number, to_number)]
        chunked_numbers = [farm_numbers[i:i + concurrency] for i in range(0, len(farm_numbers), concurrency)]
        for chunk in chunked_numbers:
            try:
                tasks = [self.signup_param(f'{random.choice(farmer_list)}{i}', is_confirm=True, retry_time=0) for i in chunk]
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                print(e.message)
                pass

    async def signup_param(self, username, is_confirm=True, retry_time=0):
        print(f"Start {'confirm' if is_confirm else 'login'} to account {username}\n")
        mail = f'{username}{MAIL_DOMAIN}'
        mail_url = f'https://maildrop.cc/inbox/?mailbox={username}'
        print(f'Mail url: {mail_url}\n')
        options = uc.ChromeOptions()
        # create_proxy_extension()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={user_agent}")
        # options.headless = False
        # options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        # options.add_argument(f"--load-extension={PROXY_FOLDER}")
        options.add_argument("--window-size=1280,960")
        driver = uc.Chrome(options=options, headless=True)
        try:
            driver.get('https://nowsecure.nl')
            await asyncio.sleep(3)
            # driver.maximize_window()
            driver.get(PARAM_REF_LINK)
            await asyncio.sleep(3)
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
            await asyncio.sleep(5)
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
            confirm_url = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/center/div[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/a[1]")
                )
            ).get_attribute('href')
            driver.get(confirm_url)
            await asyncio.sleep(5)
            # WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            #     (By.XPATH, "//h3[contains(., 'successfully')]"))
            # )
            print(f'{datetime.now()} Successfully confirmed {username}')
        except Exception as e:
            print(e.message)
        finally:
            # await asyncio.sleep(10)
            print('Closing driver\n')
            driver.quit()
