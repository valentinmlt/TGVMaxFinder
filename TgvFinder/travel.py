import requests

from TgvFinder import tools


class Travel:

    def __init__(self, origine: str, destination: str, days: list):
        assert isinstance(origine, str);'origine must be a string'
        assert isinstance(destination, str);'destination must be a string'
        assert isinstance(days, list);'go_days must be a list'

        self.origine = origine
        self.destination = destination
        self.days = days

        assert tools.verifyStations(origine, destination), 'Verify station names'
        assert tools.verifyDateFormat(days), "Verify date format"

        self.url_query = tools.makeSimpleQuery(origine, destination)
        self.already_processed_train = []

    def verify(self, notify=False):

        r = requests.get(self.url_query)
        if r.status_code == 200:
            data = r.json()
            print(self.url_query)
            print(f'{self.origine} --> {self.destination} : received {len(data)} trains')

            self.verify_if_still_available(data, notify=notify)

            for train in data:
                if not self.isKnown(train):

                    self.already_processed_train.append(train)
                    print(f"{train['origine']} --> {train['destination']} : {train['date']}|{train['heure_depart']} NOW AVAILABLE ({len(self.already_processed_train)})")

                    if notify:

                        text = f"{train['origine']} --> {train['destination']} : {train['date']}|{train['heure_depart']} NOW AVAILABLE"
                        tools.notify(text, 'NEW')

    def verify_if_still_available(self, data_list, notify=False):
        a = self.already_processed_train.copy()
        for train in data_list:
            if self.isKnown(train):
                a.remove(train)

        for train in a:
            self.already_processed_train.remove(train)
            print(f"{train['origine']} --> {train['destination']} : {train['date']}{train['heure_depart']} No longer Available ({len(self.already_processed_train)})")
            print('Train no longer available removing ')
            if notify:
                text = f"{train['origine']} --> {train['destination']} : {train['date']}{train['heure_depart']} No longer Available"
                tools.notify(text, 'END')

    def isKnown(self, train):
        for know_train in self.already_processed_train:
            if train == know_train:
                return True
        return False








