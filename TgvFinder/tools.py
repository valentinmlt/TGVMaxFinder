import requests
import re



def verifyStations(origine, destination):
    """
    Raise an error if origine or destination aren't redcognized by SNCF Api.

    :param origine:
    :param destination:
    :return: None
    """
    stations_list = getStations()

    return_value = origine in stations_list and destination in stations_list

    if not return_value:
        print('something wrong')
        print('for help : ')
        print(stations_list)

    return return_value


def getStations():
    """
    :return: a list of all stations found on the API
    """

    verify_url = "https://data.sncf.com/api/records/1.0/search/?rows=0&facet=origine&dataset=tgvmax"

    stations_json = requests.get(verify_url).json()

    facet = stations_json['facet_groups'][0]

    assert facet['name'] == 'origine', 'Facet is not origin, raising an error'

    stations_list = [value['name'] for value in facet['facets']]

    return stations_list


def makeSimpleQuery(origine, destination):
    url = """https://data.sncf.com/api/v2/catalog/datasets/tgvmax/exports/json"""
    return f"""{url}?where=od_happy_card = 'OUI' and origine = '{origine}' and destination = '{destination}'"""


def verifyDateFormat(days_list: list):
    assert isinstance(days_list, list), 'days_list must be a list'

    for date in days_list:
        assert isinstance(date, str), 'All date must be a string'
        if len(date) == 10 and re.match('[0-9]+-[0-9]+-[0-9]', date):
            pass
        else:
            return False
    return True


def notify(text: str, title: str, group='default'):
    data = {
        'accountKey': (None, 'sip5rod6npqzfq5'),
        'title': (None, title),
        'message': (None, text),
        'group': (None, group),
        'buttons': (None, '[{"text":"Google", "link":"http://google.com","color":"success"}]'),
    }

    response = requests.post('https://alertzy.app/send', data=data)
    print('notification sended')
    print(response.content)
