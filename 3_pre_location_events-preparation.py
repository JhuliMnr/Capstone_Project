import numpy as np
from timeit import default_timer as timer
from datetime import timedelta
start = timer()
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
station_locs = np.array([[629798.2,7412258.9],[630006.7,7413884.8],[627994.1,7417545.5],[626036.7,7414616.9],[626724.1,7416094.8],[632215.5,7413976]])
x_min, x_max = 620000, 640000
y_min, y_max = 7405000, 7425000
res = 5
x_vals = np.arange(x_min, x_max + res, res)
y_vals = np.arange(y_min, y_max + res, res)
xx, yy = np.meshgrid(x_vals, y_vals)
grid_coords = np.c_[xx.ravel(), yy.ravel()]
distances = cdist(grid_coords, station_locs)
distances = distances.reshape(xx.shape + (station_locs.shape[0],))
mins = [] # coordinates for the minimum of the standard deviation
vguess = 4.46 * 1000
#===============================================================
import pandas as pd
import ast
file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/All_HF_toLocation_1.5s.csv'
# This file was previously ordered first using the date, then the arrival time and finally the stations.
df = pd.read_csv(file)
df.fillna(0, inplace=True)
events = df.Event_Location.dropna().values
Events = np.array([ast.literal_eval(i) for i in events])
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
for k in range(len(station)):
    if station[k] == station_combination[5]: #['BB1', 'BB3', 'BB4'],
        tarr = [np.nan, tarr_list[k][0], np.nan, tarr_list[k][1], tarr_list[k][2],  np.nan]
        tarr_ind = [1, 3, 4]  # tarr_ind = [0,1,2,3,4,5]
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
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k )
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # #plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(*[k,tarr_list[k][0],vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[3]: #['BB2', 'BB3', 'BB4', 'BB5'],
        tarr = [np.nan, np.nan, tarr_list[k][0], tarr_list[k][1], tarr_list[k][2], tarr_list[k][3] ]
        tarr_ind = [2, 3, 4, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[2]: #['BB1', 'BB3', 'BB4', 'BB5'],
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
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[0]: #['BB2', 'BB3', 'BB4'],
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
        print([xx[min_std_x, min_std_y],yy[min_std_x, min_std_y]])
        # Plot the standard deviation grid as a color mesh plot
        import matplotlib.pyplot as pltt
        # pltt.figure(figsize=(8, 6))
        # pltt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # pltt.colorbar()
        # pltt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # pltt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # pltt.title("Standard Deviation for HF event:%s\n" % k)
        # pltt.xlabel('X')
        # pltt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # pltt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
        # pltt.show()
    elif station[k] == station_combination[1]: #['BB3', 'BB4', 'BB5'],
        tarr = [np.nan,np.nan,np.nan,tarr_list[k][0], tarr_list[k][1], tarr_list[k][2]]
        tarr_ind = [ 3, 4, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        print([xx[min_std_x, min_std_y], yy[min_std_x, min_std_y]])
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[4]: #['BB2', 'BB4', 'BB5'],
        tarr = [np.nan,np.nan,tarr_list[k][0],np.nan, tarr_list[k][1], tarr_list[k][2]]
        tarr_ind = [2, 4, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        #    *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[6]: #['BB1', 'BB4', 'BB5'],
        tarr = [np.nan,tarr_list[k][0],np.nan,np.nan, tarr_list[k][1], tarr_list[k][2]]
        tarr_ind = [1, 4, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        # # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    elif station[k] == station_combination[7]: #['BB2', 'BB3', 'BB5'],
        tarr = [np.nan,np.nan,tarr_list[k][0],tarr_list[k][1],np.nan,tarr_list[k][2]]
        tarr_ind = [2, 3, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))
    else: #['BB1', 'BB3', 'BB5']
        tarr = [np.nan,tarr_list[k][0],np.nan, tarr_list[k][1], np.nan, tarr_list[k][2]]
        tarr_ind = [1, 3, 5]  # tarr_ind = [0,1,2,3,4,5]
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
        # Plot the standard deviation grid as a color mesh plot
        # plt.figure(figsize=(8, 6))
        # plt.pcolormesh(xx, yy, stds, cmap='PuBu_r')
        # plt.colorbar()
        # plt.plot(station_locs[:, 0], station_locs[:, 1], 'ko', markersize=8)
        # plt.plot(xx[min_std_x, min_std_y], yy[min_std_x, min_std_y], 'wx', markersize=12, markeredgewidth=2)
        # plt.title("Standard Deviation for HF event:%s\n" % k)
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.svg'.format(
        # #     *[k, tarr_list[k][0], vguess]))
        # plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/HF_events_location/HF{}-{}-{}.png'.format(
        #     *[k, tarr_list[k][0], vguess]))

df = pd.DataFrame(zip(*[mins]), columns=['Event_Location'])
df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/HF_Location_5m_1.5s_versionlast.csv')

end = timer()
print(timedelta(seconds=end - start))
