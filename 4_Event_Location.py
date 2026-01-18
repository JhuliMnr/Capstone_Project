import numpy as np
from timeit import default_timer as timer
from datetime import timedelta
start = timer()
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
station_locs = np.array([[629798.2,7412258.9],[630006.7,7413884.8],[627994.1,7417545.5],[626036.7,7414616.9],[626724.1,7416094.8],[632215.5,7413976]])
x_min, x_max = 624000, 635000
y_min, y_max = 7405000, 7425000
res = 10
x_vals = np.arange(x_min, x_max + res, res)
y_vals = np.arange(y_min, y_max + res, res)
xx, yy = np.meshgrid(x_vals, y_vals)
grid_coords = np.c_[xx.ravel(), yy.ravel()]
distances = cdist(grid_coords, station_locs)
distances = distances.reshape(xx.shape + (station_locs.shape[0],))
mins = [] # coordinates for the minimum of the standard deviation

#===============================================================
import pandas as pd
import ast
file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/All_HF_toLocation.csv'
# This file was previously ordered first using the date, then the arrival time and finally the stations.
df = pd.read_csv(file)
df.fillna(0, inplace=True)
events = df.Events.dropna().values
Events = np.array([ast.literal_eval(i) for i in events])
Events = Events[:11]
sorting = []
station = []
tarr_list = []
for e in range(len(Events)):
    Events[e].sort(key=lambda x: x[1])
    sorting.append(Events[e])
    tarr = []
    stations = []
    for t in range(len(Events[e])):
        stations.append(Events[e][t][1])
        tarr.append(Events[e][t][0])
    station.append(stations)
    tarr_list.append(tarr)
station_combination = []
from collections import Counter
sublist_counts = Counter(tuple(sublist) for sublist in station)
for sublist, count in sublist_counts.items():
    if count > 1:
        station_combination.append(list(sublist))
Vguess = np.arange(3000, 4000, 100) # The vguess should be in Km/s but due to the calculations it has to be converted to m/s
list_vguess = []
for vguess in Vguess:
    speed = []
    for k in range(len(station)):
        if station[k] == station_combination[0]: #['BB1', 'BB3', 'BB4', 'BB5'],
            tarr = [np.nan,tarr_list[k][0],np.nan, tarr_list[k][1], tarr_list[k][2], tarr_list[k][3]]
            tarr_ind = [1, 3, 4, 5]  # tarr_ind = [0,1,2,3,4,5]
            results = []
            for i in tarr_ind:
                distances_to_station = distances[:, :, i]
                result = tarr[i] - (distances_to_station / vguess)
                results.append(result)
            stds = np.std(results, axis=0)
            min_std = np.min(stds)
            min_std_loc = np.argmin(stds)
            min_std_x, min_std_y = np.unravel_index(min_std_loc, stds.shape)
            mins.append([xx[min_std_x, min_std_y],yy[min_std_x, min_std_y]])
            print([xx[min_std_x, min_std_y],yy[min_std_x, min_std_y]])
            speed.append([vguess, np.min(stds)])
            # Plot the standard deviation grid as a color mesh plot
            # plt.figure(figsize=(8, 6))
            # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
            # plt.colorbar()
            # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
            # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
            # plt.title("Standard Deviation for HF event:%s\n" % k)
            # plt.xlabel('X')
            # plt.ylabel('Y')
            # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
            #     *[k, tarr_list[k][0], vguess]))
            plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
                *[k, tarr_list[k][0], vguess]))
        else:
            tarr = [np.nan,np.nan,tarr_list[k][0],tarr_list[k][1], tarr_list[k][2], np.nan]
            tarr_ind = [2, 3, 4]  # tarr_ind = [0,1,2,3,4,5]
            results = []
            for i in tarr_ind:
                distances_to_station = distances[:, :, i]
                result = tarr[i] - (distances_to_station / vguess)
                results.append(result)
            stds = np.std(results, axis=0)
            min_std = np.min(stds)
            min_std_loc = np.argmin(stds)
            min_std_x, min_std_y = np.unravel_index(min_std_loc, stds.shape)
            mins.append([xx[min_std_x, min_std_y],yy[min_std_x, min_std_y]])
            # print([xx[min_std_x, min_std_y],yy[min_std_x, min_std_y]])
            # speed.append([vguess, np.min(stds)])
            # # Plot the standard deviation grid as a color mesh plot
            # plt.figure(figsize=(8, 6))
            # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
            # plt.colorbar()
            # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
            # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
            # plt.title("Standard Deviation for HF event:%s\n" % k)
            # plt.xlabel('X')
            # plt.ylabel('Y')
            # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
            #     *[k, tarr_list[k][0], vguess]))
            # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
            #     *[k, tarr_list[k][0], vguess]))
    list_vguess.append(speed)
dfmins = pd.DataFrame(zip(*[mins]), columns=['Event_Location'])
dfvguess = pd.DataFrame(zip(*[list_vguess]), columns=['Vguess'])
df = pd.concat([dfmins,dfvguess], axis=1)
df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_newversion/HF_Event_Location_vguess.csv')

end = timer()
print(timedelta(seconds=end - start))
