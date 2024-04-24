import time
import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from telegram_service import TelegramBot

load_dotenv()

chrome_options = Options()
chrome_options.add_argument("--headless")


def crawl_data(chain):
    with Chrome(options=chrome_options) as browser:
        url = ''.join([os.getenv("APE_BONDS_URL"), str(chain)])
        browser.get(url)
        time.sleep(5)
        html = browser.page_source

    try:
        soup = BeautifulSoup(html, "html.parser")
        tokens = soup.find_all("div", {"class": "css-19aks3c"})
        chain_name = soup.find("span", {"class": "css-w7gdm9"}).text
        result = f"-------------{chain_name} CHAIN------------"

        for idx, token in enumerate(tokens):
            # name_token = token.find("div", {"class": "css-dlmr47"}).text
            # img = token.find("img").get('src')
            # type_token = token.find("div", {"class": "css-1e8v7uh"}).text
            symbol = token.find("span", {"class": "css-11u4bai"}).text
            discount_percent = token.find("span", {"class": "css-1hsh4tf"})

            if discount_percent:
                result = '\n'.join([result, f'{symbol}: {discount_percent.text}'])

        return result
    except Exception as e:
        print(e)


def do_process():
    chains = eval(os.getenv("CHAINS"))
    message = ''

    for chain in chains:
        message = '\n\n'.join([message, crawl_data(chain)])

    TelegramBot().send_message(message)

#
# if __name__ == '__main__':
#     do_process()
