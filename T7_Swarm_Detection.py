# ====================================================
import pandas as pd
import numpy as np
import os
os.chdir("C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_newversion")
#=====================================================

network = '8E'
channel = 'HHZ'
stations = ['BAS','BB1','BB2','BB3','BB5'] #'BB1','BB2','BB3',,'BB5'
fday = 1  # start day
eday = 31  # end day
fmonth = 1  # start month
emonth = 12  # end month
year = ['2014','2015'] #,'2015'
swarm = []
rates = []
dates = []
# ======================================================================
for y in year:
    year = str(y)
    for s in stations:
        station = str(s)
        for k in range(fmonth, emonth + 1, 1):
            month = str(k)
            for a in range(fday, eday + 1, 1):
                day = str(a)
                try:
                    file = '{}.{}.{}.{}{}{}_newversion_1-10Hz.csv'.format(
                        *[network, station, channel, year, month.zfill(2), day.zfill(2)])
                    df = pd.read_csv(file)
                    d3 = df.Event_Rate.dropna().values
                    swarm.append([d3[np.argmax(d3)],'{}-{}-{}'.format(*[year,month.zfill(2),day.zfill(2)]) ]) #'2022-01-01'
                    rates.append(d3[np.argmax(d3)])
                    dates.append('{}-{}-{}'.format(*[year,month.zfill(2),day.zfill(2)]))
                    #print([d3[np.argmax(d3)],'{}/{}/{}'.format(*[year, month.zfill(2),day.zfill(2)]) ])
                except FileNotFoundError:
                    pass

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
dates = [mdates.datestr2num(date) for date in dates]
fig, ax = plt.subplots()
ax.plot_date(dates, rates)
ax.set_xlabel('Date')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.savefig('swarm_detection_plot.png')
plt.show()


