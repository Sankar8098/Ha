import os

from typing import List
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from aiofiles import open
from httpx import AsyncClient
from bot import logging


async def teraBoxDl(url: str) -> List:
    baseurl = f'https://teradownloader.com/download?link={quote(url)}'
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    try:
        browser.get(baseurl)
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.p-5')))
        elements = browser.find_elements(By.CSS_SELECTOR, 'div.p-5 > a')
        filename = browser.find_element(By.CSS_SELECTOR, 'div.p-5 > a > h5').text
        links = [link.get_attribute('href') for link in elements]
        return [links[2], filename]
    except Exception as e:
        logging.LOGGER(str(e))
        print(e)
        print("I give up...")
    finally:
        browser.quit()


async def teraBoxFile(url: str) -> str:
    resp = await teraBoxDl(url)
    try: os.mkdir('downloads')
    except: pass
    try:
        with AsyncClient() as client:
            r = await client.get(resp[0])
            r.raise_for_status()
            async with open(f'{resp[1]}', 'w') as f:
                await f.write(r.content)
                await f.close()
                return os.path.abspath(f.name)
    except Exception as e:
        logging.LOGGER(str(e))
        print(e)
        return str(e)
