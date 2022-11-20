import time

from TgvFinder import tools, settings
from TgvFinder.travel import Travel

print(f"{'-' * 43} STARTING {'-' * 43}")

# Configuration and generation of Travel class

sleeping_time = settings.SLEEPING_TIME


paris = 'PARIS (intramuros)'
bordeaux = 'BORDEAUX ST JEAN'
le_mans = 'LE MANS'
massy = 'MASSY TGV'
nov_days = tools.all_day_from_month(11, 2022)
dec_days = tools.all_day_from_month(12, 2022)
all_days = nov_days + dec_days


travels_list = [Travel(paris, bordeaux, all_days),
                Travel(bordeaux, paris, all_days),
                Travel(paris, le_mans, all_days),
                Travel(le_mans, paris, all_days),
                Travel(massy, bordeaux, all_days),
                Travel(bordeaux, massy, all_days),
                Travel(massy, le_mans, all_days),
                Travel(le_mans, massy, all_days),
                ]


# Initialisation of the travel class, not sending notification for the new data to no overload notification

for travel in travels_list:
    travel.verify(notify=False)
    time.sleep(1)


tools.notify(f'Initialisation complete ( sleeping time : {sleeping_time})', 'STARTING')

# End of initialisation

# Starting the watching processus

time.sleep(sleeping_time)

while True:
    for travel in travels_list:

        travel.verify(notify=True)
        time.sleep(1)

    print(f"{'-' * 43} SLEEPING ({sleeping_time}) : {time.strftime('%d %b %Y %H:%M:%S', time.localtime())} {'-' * 43}")
    time.sleep(sleeping_time)





















