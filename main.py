import time

import requests

from TgvFinder import tools
from TgvFinder.travel import Travel


#configuration

base_url = """https://data.sncf.com/api/v2/catalog/datasets/tgvmax/exports/json"""


origine = 'PARIS (intramuros)'
destination = 'BORDEAUX ST JEAN'
days_go = ['2022-11-13', '2022-11-14', '2022-11-15', '2022-11-16', '2022-11-17', '2022-11-18', '2022-11-19', '2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25', '2022-11-26', '2022-11-27', '2022-11-28', '2022-11-29', '2022-11-30']
days_back = ['2022-11-13', '2022-11-14', '2022-11-15', '2022-11-16', '2022-11-17', '2022-11-18', '2022-11-19', '2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25', '2022-11-26', '2022-11-27', '2022-11-28', '2022-11-29', '2022-11-30',]


# initialisation

try:

    travels_list = [Travel(origine, destination, days_go), Travel(destination, origine, days_back)]
    for travel in travels_list:
        travel.verify(notify=False)
        time.sleep(1)


    tools.notify('Initialisation complete', 'STARTING')

except Exception as e:
    print(e)
    quit()

# Veille

time.sleep(60)

while True:
    for travel in travels_list:
        try:
            travel.verify(notify=True)
            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(120)
            tools.notify(str(e), 'ERROR')
            quit()

    time.sleep(60)





















