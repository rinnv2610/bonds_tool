import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from telegram_bot import TelegramBot
from config import Config
from concurrent.futures import ThreadPoolExecutor

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")


def detect_smart_contract(href):
    return href.split('/')[-1]


def generator_url_to_ape_bond(current_url, href):
    smart_contract = detect_smart_contract(href)
    return ''.join([current_url, "&", f'bondAddress={smart_contract}'])


def crawl_data(chain):
    print("Start crawling data...")
    with Chrome(options=chrome_options) as browser:
        url = ''.join([Config.APE_BONDS_URL, str(chain)])
        browser.get(url)
        time.sleep(10)
        html = browser.page_source

    try:
        soup = BeautifulSoup(html, "html.parser")
        tokens = soup.find_all("div", {"class": "css-19aks3c"})
        chain_name = soup.find("span", {"class": "css-w7gdm9"}).text

        if chain_name.strip() == "ETHEREUM":
            chain_name = "ETH"

        result = []

        for idx, token in enumerate(tokens):
            # name_token = token.find("div", {"class": "css-dlmr47"}).text
            # img = token.find("img").get('src')
            # type_token = token.find("div", {"class": "css-1e8v7uh"}).text
            href = token.find_all("a", {"class": "css-xadny5"})[2]['href']
            symbol = token.find("span", {"class": "css-11u4bai"}).text
            discount_percent = token.find("span", {"class": "css-1hsh4tf"})
            url_redirect = generator_url_to_ape_bond(current_url=url, href=href)

            if discount_percent:
                discount_percent = str(discount_percent.text).split('%')[0]
                result.append(dict(chain_name=chain_name, symbol=symbol, discount_percent=float(discount_percent), url_redirect=url_redirect))

        return result
    except Exception as e:
        print(e)


def process_message_raw(data):
    sorted_list = sorted(data, key=lambda x: x['discount_percent'], reverse=True)

    message = "*** BONDS DISCOUNT ***"
    for data in sorted_list:
        message = '\n\n'.join([message, f'{data.get("chain_name")}  {data.get("symbol")}  {data.get("discount_percent")}%  <a href="{data.get("url_redirect")}">Buy</a>'])

    return message


def do_process():
    print("Start doing process...")

    chains = eval(Config.CHAINS)
    results = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(crawl_data, chain) for chain in chains]

        # Use result() to retrieve the result of each task
        for future in futures:
            results.extend(future.result())

    message = process_message_raw(results)

    # Send message to tele
    TelegramBot().send_message(message)


if __name__ == '__main__':
    do_process()
