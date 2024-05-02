import requests
from config import Config
import json


class ApeBondService:
    def __init__(self):
        self.ape_bonds_api = Config.APE_BONDS_API

    def get_bonds(self):
        try:
            response = requests.get(self.ape_bonds_api)

            if response.status_code != 200:
                print("Error getting bonds")

            return json.loads(response.text)
        except Exception as e:
            print(e)
