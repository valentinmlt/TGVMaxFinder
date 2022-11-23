import calendar
import datetime

import requests
import re


from . import settings


def compare_list_of_dict(list1: list, list2: list):
    """
    Compare 2 lists.
    Return a tuple containing :
        a list of items added between list1 and list2
        a list of items deleted between list1 and list2

    :param list1:
    :param list2:
    :return: tuple(new_item_list, deleted_item_list)
    """
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    new_items_list = []
    deleted_items = []

    for item1 in list1:
        if item1 not in list2:
            deleted_items.append(item1)

    for item2 in list2:
        if item2 not in list1:
            new_items_list.append(item2)

    return new_items_list, deleted_items


def verify_stations(origine, destination):
    """
    Verify if the given names will be recognized by SNCF API.
    Return True if all is correct and False otherwise.
    Display the valid names available if not.

    :param origine:
    :param destination:
    :return: Boolean
    """

    stations_list = getStations()

    stations_name_are_correct = origine in stations_list and destination in stations_list

    if not stations_name_are_correct:
        print('Recognized stations names :')
        print(stations_list)

    return stations_name_are_correct


def getStations():
    """
    :return: a list of all stations found on the API
    """

    stations_name_url = "https://data.sncf.com/api/records/1.0/search/?rows=0&facet=origine&dataset=tgvmax"
    stations_json = requests.get(stations_name_url).json()
    facet = stations_json['facet_groups'][0]

    assert facet['name'] == 'origine', 'Facet is not origin, raising an error'

    stations_list = [value['name'] for value in facet['facets']]

    return stations_list


def makeSimpleQuery(origine, destination):
    """
    Make a simple query url to interogate the API.

    :param origine:
    :param destination:
    :return: str query url
    """
    url = """https://data.sncf.com/api/v2/catalog/datasets/tgvmax/exports/json"""
    return f"""{url}?where=od_happy_card = 'OUI' and origine = '{origine}' and destination = '{destination}'"""


def verifyDateFormat(days_list: list):
    """
    Verify the compatibility of list a date with the API
    Format = YYYY-MM-DD

    :param days_list:
    :return: Boolean
    """
    assert isinstance(days_list, list), 'days_list must be a list'

    for date in days_list:
        assert isinstance(date, str), 'All dates must be a string'

        if not (len(date) == 10 and re.match('20\d\d-[0-1]\d-[0-3]\d', date)):
            return False

    return True


def verifyHourFormat(hours_list: list, timeformat: str):
    """
    Verify the compatibility of list a date with the API
    Format = "%H:%M"

    :param hour:
    :return: Boolean
    """
    assert isinstance(hours_list, list), 'days_list must be a list'
    for hour in hours_list:
        try:
            datetime.datetime.strptime(hour, timeformat)
        except ValueError as e:
            print('ValueError Raised:', e)
            return False
    return True


def notify(text: str, title: str):
    """
    Use alertzy API to inform the user from news

    :param text:
    :param title:
    :return: None
    """
    if notify:
        alertzy_id = settings.ALERTZY_ID

        data = {
            'accountKey': alertzy_id,
            'title': title,
            'message': text,
        }

        response = requests.post('https://alertzy.app/send', data=data)
        print(f'Notification sended : {response.content}')


def all_day_from_month(MM: int, YYYY: int, ):
    """
    Give all the date of a month in the right format YYYY-MM-DD
    :param MM:
    :param YYYY:
    :return: list
    """
    assert isinstance(MM, int), 'MM must be an int'
    assert isinstance(YYYY, int), 'YYYY must be an int'
    assert 0 < MM <= 12, 'MM Must be between 1 and 12'

    num_days = calendar.monthrange(YYYY, MM)[1]
    return [f"{YYYY}-{str(MM).zfill(2)}-{str(DD).zfill(2)}" for DD in range(1, num_days + 1)]




