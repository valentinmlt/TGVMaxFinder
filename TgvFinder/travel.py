from datetime import datetime
import time

import requests

from TgvFinder import tools


class Travel:

    def __init__(self, origine: str, destination: str, days: list):
        assert isinstance(origine, str), 'origine must be a string'
        assert isinstance(destination, str), 'destination must be a string'
        assert isinstance(days, list), 'go_days must be a list'

        self.origine = origine
        self.destination = destination
        self.days = days

        assert tools.verify_stations(origine, destination), 'Verify station names'
        assert tools.verifyDateFormat(days), "Verify date format"

        self.url_query = tools.makeSimpleQuery(origine, destination)
        self.previous_data = []

    def verify(self, notify=False):
        """
        Verify if new trains are available by querying the API

        :param notify: If you want to use the notification system
        :return:
        """

        try:
            request = requests.get(self.url_query)

            if request.status_code == 200:
                all_dataset = request.json()

                new_data = self.filter_by_date(all_dataset)
                new_trains, deleted_trains = tools.compare_list_of_dict(self.previous_data, new_data)
                self.previous_data = new_data

                print(f'{self.origine} --> {self.destination} : received {len(new_data)} trains')

                if new_trains and notify:
                    new_notifcation_text = f"{self.origine} --> {self.destination} : {len(new_trains)} nouveau(x) train(s)"
                    tools.notify(new_notifcation_text, 'NEW TRAIN(s)')

                if deleted_trains and notify:
                    del_notifcation_text = f"{self.origine} --> {self.destination} : {len(deleted_trains)} train(s) supprimé(s)"
                    tools.notify(del_notifcation_text, 'DELETED TRAIN(s)')

                for train in new_trains:
                    notifcation_text = f"{train['origine']} --> {train['destination']} : {train['date']}|{train['heure_depart']} NOW AVAILABLE"
                    print(notifcation_text)

                for train in deleted_trains:
                    notifcation_text = f"{train['origine']} --> {train['destination']} : {train['date']}|{train['heure_depart']} No longer Available "
                    print(notifcation_text)

            else:
                print(f"{'-' * 43} {self.origine} --> {self.destination} : NOT 200 ( sleep for 20' ) {request.text} {'-' * 43}")
                time.sleep(1200)

        except Exception as error:

            print(f"{'-'*43} {self.origine} --> {self.destination} : ERROR (sleeping 20' seconds) : {str(error)} {'-'*43}")
            time.sleep(1200)

    def filter_by_date(self, all_dataset: list):
        """
        Method to filter the dataset from API to keep the interesting trains
        :param all_dataset:
        :return: a list of filtered data
        """

        self.delete_past_days()

        return [train for train in all_dataset if train['date'] in self.days]

    def delete_past_days(self):
        assert isinstance(self.days, list), 'days must be a list '

        patern = '%Y-%m-%d'

        self.days = [date for date in self.days if datetime.strptime(date, patern).date() >= datetime.today().date()]











