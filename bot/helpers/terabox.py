import os

from typing import List
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from aiofiles import open
from httpx import AsyncClient


async def teraBoxDl(url: str) -> List:
    baseurl = f'https://teradownloader.com/download?link={quote(url)}'
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    try:
        browser.get(baseurl)
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.p-5')))
        elements = browser.find_elements(By.CSS_SELECTOR, 'div.p-5 > a')
        links = [link.get_attribute('href') for link in elements]
        return [links[2], ]
    except Exception as e:
        print(e)
        print("I give up...")
    finally:
        browser.quit()


async def teraBoxFile(url: str) -> str:
    with AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        if r.status_code == 200:
            async with open('', 'w') as f:
                await f.write(r.text)
            return soup.find('a', {'class': 'btn btn-primary btn-lg'}).get('href')
    pass
