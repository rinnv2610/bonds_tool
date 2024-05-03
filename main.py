from selenium.webdriver.chrome.options import Options

from ape_bond import ApeBondService
from config import Config
from telegram_bot import TelegramBot

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")


def generator_url_to_ape_bond(url, chain, smart_contract):
    return ''.join([url, "?", f'bondAddress={smart_contract}', "&", f'chain={chain}'])


def process_message_raw(jsons):
    chains = eval(Config.CHAINS)
    results = [jsons.get(str(chain)) for chain in chains]

    # filter list bonds not yet sold out
    bonds_valid = []
    for result in results:
        bonds = result.get("bonds")
        bonds_valid.extend(
            list(filter(lambda x:
                        not bool(x.get("soldOut")) and
                        not bool(x.get("inactive")) and
                        x.get("priceUsd", 0) > 0 and
                        x.get("discount", 0) > 0, bonds
                        )
                 )
        )

    chains = {
        1: "ETH",
        56: "BNB",
        137: "POLYGON",
    }

    # bonds after sort
    sorted_list = sorted(bonds_valid, key=lambda x: x['discount'], reverse=True)
    message = "*** BONDS DISCOUNT ***"
    for data in sorted_list:
        chain = chains.get(data.get("chainId"))
        url = generator_url_to_ape_bond(url=data.get("link"), chain=data.get("chainId"),
                                        smart_contract=data.get("billAddress"))
        message = '\n\n'.join([message,
                               f'{chain}  {data.get("payoutTokenName")}  {round(data.get("discount"), 2)}%  <a href="{url}">Buy</a>'])

    return message


def do_process():
    print("Start doing process...")

    ape_bond_service = ApeBondService()
    jsons = ape_bond_service.get_bonds()
    message = process_message_raw(jsons)

    # Send message to tele
    TelegramBot().send_message(message)


if __name__ == '__main__':
    do_process()
