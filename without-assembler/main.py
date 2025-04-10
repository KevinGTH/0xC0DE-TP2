from server_interface import GiniAPIClient
from gui import GUI
if __name__ == '__main__':
    API_URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"
    api_client = GiniAPIClient(API_URL)
    ui = GUI(api_client)
    ui.run()