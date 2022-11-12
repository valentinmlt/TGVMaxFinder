import time

from TgvFinder import tools, settings
from TgvFinder.travel import Travel

print(f"{'-' * 43} STARTING {'-' * 43}")

# Configuration and generation of Travel class

sleeping_time = settings.SLEEPING_TIME


origine = 'PARIS (intramuros)'
destination = 'BORDEAUX ST JEAN'
days_go = ['2022-11-13', '2022-11-14', '2022-11-15', '2022-11-16', '2022-11-17', '2022-11-18', '2022-11-19', '2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25', '2022-11-26', '2022-11-27', '2022-11-28', '2022-11-29', '2022-11-30']
days_back = ['2022-11-13', '2022-11-14', '2022-11-15', '2022-11-16', '2022-11-17', '2022-11-18', '2022-11-19', '2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23', '2022-11-24', '2022-11-25', '2022-11-26', '2022-11-27', '2022-11-28', '2022-11-29', '2022-11-30',]


travels_list = [Travel(origine, destination, days_go),
                Travel(destination, origine, days_back),]


# Initialisation of the travel class, not sending notification for the new data to no overload notification

for travel in travels_list:
    travel.verify(notify=False)
    time.sleep(1)


tools.notify('Initialisation complete', 'STARTING')

# End of initialisation

# Starting the watching processus

time.sleep(sleeping_time)

while True:
    for travel in travels_list:

        travel.verify(notify=True)
        time.sleep(1)

    print(f"{'-' * 43} SLEEPING ({sleeping_time}) : {time.strftime('%d %b %Y %H:%M:%S', time.localtime())} {'-' * 43}")
    time.sleep(sleeping_time)





















