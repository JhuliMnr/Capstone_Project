# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 19:20:18 2023

@author: JhuliiMnr
"""

# This code is meant to recognize an actual event, compares the arrival times
# and group them according a threshold (1.5 seconds), the idea is to separate
# events.
def modes(lst):
    freq_dict = {}
    for elem in lst:
        if elem in freq_dict:
            freq_dict[elem] += 1
        else:
            freq_dict[elem] = 1
    max_freq = max(freq_dict.values())
    if max_freq > 2:
        modes = [k for k, v in freq_dict.items() if v == max_freq]
    else:
        modes = None
    freq = max(freq_dict.values())
    return modes, freq

def group_events(sublists, threshold_time, lengroup):
    sorted_events = sorted(sublists, key=lambda x: x[0])
    event_groups = []
    current_group = [sorted_events[0]]
    threshold = sorted_events[0][0] + threshold_time
    for sublist in sorted_events[1:]:
        if (sublist[0] < threshold and
                sublist[1] not in [x[1] for x in current_group] and
                sublist[2] == current_group[0][2]):
            current_group.append(sublist)
        else:
            event_groups.append(current_group)
            current_group = [sublist]
            threshold = sublist[0] + threshold_time
    filtered_groups = []
    for group in event_groups:
        if len(group) >= lengroup:
            filtered_groups.append(group)
    return filtered_groups

#========================================================================
from timeit import default_timer as timer
from datetime import timedelta
start = timer()
import pandas as pd
file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/All_stations_all_events.csv'
# This file was previously ordered first using the date, then the arrival time and finally the stations.
df = pd.read_csv(file)
df.fillna(0, inplace=True)
#df = pd.read_csv('All_Events.csv', sep = ';', thousands='.', decimal=',') #this csv contains the info of 4 stations just for August 1st 2014
date = df.Date.dropna().values  # station.time_date this will be separated later
T_arr = df.Arrival_Time.dropna().values  # Time in seconds don't forget¡
T_off = df.Trigger_off.dropna().values
type = df.Type.dropna().values
station = df.Station.dropna().values       # Station of the events
gap = df.Gap.dropna().values
FI = df.Frequency_Index.dropna().values
pamp  = df.Phase_Amplitude.dropna().values
length = df.Length.dropna().values
maxamp = df.Maximum_Amplitude.dropna().values
maxfreq = df.Maximum_Frequency.dropna().values
cenfreq = df.Center_Frequency.dropna().values
rms = df.RMS_Amplitude.dropna().values
#==============================================================================
events = []
for e in range(0, len(station)):
    events.append([T_arr[e], station[e], date[e], type[e],FI[e], maxamp[e], pamp[e], rms[e], maxfreq[e], cenfreq[e], length[e], gap[e],T_off[e]])
#==============================================================================
final = group_events(events, 1.5, 3) # group_events(list of events, the time threshold, minimum number of events per group)
import numpy as np
Event_type = []
event_type=[]
for i in range(0, len(final)):
    ty = []
    Fi = []
    for j in range(0, len(final[i])):
        ty.append(final[i][j][3])
        Fi.append(final[i][j][4])
    mode_fi, freqs = modes(ty)
    if mode_fi == None  or len(mode_fi)>1:
        mean_fi = np.mean(Fi)
        if mean_fi >= -0.768550:
            event_type.append('HF')
            t = 0
            while t < len(final[i]):
                Event_type.append('HF')
                t += 1
        if mean_fi <= -0.911470 and mean_fi >= -2.196439:
            event_type.append('LF')
            t = 0
            while t < len(final[i]):
                Event_type.append('LF')
                t += 1
        if mean_fi < -0.768550 and mean_fi > -0.911470:
            event_type.append('HYB')
            t = 0
            while t < len(final[i]):
                Event_type.append('HYB')
                t += 1
        if mean_fi < -2.196439:
            event_type.append('EXP')
            t = 0
            while t < len(final[i]):
                Event_type.append('EXP')
                t += 1
    else:
        if mode_fi[0] == 'HF':
            event_type.append('HF')
            t = 0
            while t < len(final[i]):
                Event_type.append('HF')
                t += 1
        if mode_fi[0] == 'LF':
            event_type.append('LF')
            t = 0
            while t < len(final[i]):
                Event_type.append('LF')
                t += 1
        if mode_fi[0] == 'HYB':
            event_type.append('HYB')
            t = 0
            while t < len(final[i]):
                Event_type.append('HYB')
                t += 1
        if mode_fi[0] == 'EXP':
            event_type.append('EXP')
            t = 0
            while t < len(final[i]):
                Event_type.append('EXP')
                t += 1


# dfeve = pd.DataFrame(zip(*[final]), columns=['Events'])
# dftype = pd.DataFrame(zip(*[event_type]), columns=['Event_Type'])
# df = pd.concat([dfeve, dftype], axis=1)
# df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/Final_Events_allstations_1.5s.csv')
vt_event = []
vt_type = []
for t in range(len(event_type)):
    if event_type[t] == 'HF':
        vt_event.append(final[t])
        vt_type.append(event_type[t])
dfevevt = pd.DataFrame(zip(*[vt_event]), columns=['Events'])
dftypevt = pd.DataFrame(zip(*[vt_type]), columns=['Event_Type'])
df = pd.concat([dfevevt, dftypevt], axis=1)
df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/Final_vt_Events_allstations_1.5s.csv')


# def group_sublists(sublists):
#     # Sort the sublists by tarr
#     sorted_sublists = sorted(sublists, key=lambda x: x[0])
#
#     # Initialize the groups list
#     groups = []
#
#     # Initialize the current group with the first sublist
#     current_group = [sorted_sublists[0]]
#
#     # Initialize the threshold
#     threshold = sorted_sublists[0][0] + 2.6
#
#     # Loop through the remaining sublists
#     for sublist in sorted_sublists[1:]:
#         # Check if the current sublist belongs in the current group
#         if (sublist[0] < threshold and
#                 sublist[1] not in [x[1] for x in current_group] and
#                 sublist[2] == current_group[0][2]):
#             current_group.append(sublist)
#         # If the current sublist doesn't belong in the current group, start a new group
#         else:
#             # Check if the current group has different station values and at least 3 sublists
#             if (len(set([x[1] for x in current_group])) == len(current_group)
#                     and len(current_group) >= 3):
#                 groups.append(current_group)
#             current_group = [sublist]
#             threshold = sublist[0] + 2.6
#
#     # Add the last current group to the list of groups
#     if (len(set([x[1] for x in current_group])) == len(current_group)
#             and len(current_group) >= 3):
#         groups.append(current_group)
#
#     return groups
# fin = group_sublists(events)

fevents = final
Tarr = []
time = []
stationf = []
fi = []
v1 = []
v2 = []
v4 = []
v5 = []
v6 = []
v7 = []
v8 = []
v9 = []
for i in range(0, len(fevents)):
    for j in range(0, len(fevents[i])): #events.append([T_arr[e], station[e], date[e], ,FI[e], maxamp[e], pamp[e], rms[e], maxfreq[e], cenfreq[e], length[e], gap[e],T_off[e]])
        Tarr.append(fevents[i][j][0])
        stationf.append(fevents[i][j][1])
        time.append(fevents[i][j][2])
        fi.append(fevents[i][j][4])
        v1.append(fevents[i][j][5]) #maxamp
        v2.append(fevents[i][j][6]) #pamp
        v4.append(fevents[i][j][7]) #RMS
        v5.append(fevents[i][j][8]) #Max freq
        v6.append(fevents[i][j][9]) #center_freq
        v7.append(fevents[i][j][10]) #Length
        v8.append(fevents[i][j][11]) #gap
        v9.append(fevents[i][j][12]) #triggeroff

dftarr = pd.DataFrame(zip(*[Tarr]), columns=['Arrival_Time'])
dfstn = pd.DataFrame(zip(*[stationf]), columns=['Station'])
dfdate = pd.DataFrame(zip(*[time]), columns=['Date'])
df9 = pd.DataFrame(zip(*[fi]), columns=['Frequency_Index'])
df1 = pd.DataFrame(zip(*[v1]), columns=['Maximum_Amplitude'])
df2 = pd.DataFrame(zip(*[v2]), columns=['Phase_Amplitude'])
df4 = pd.DataFrame(zip(*[v4]), columns=['RMS_Amplitude'])
df5 = pd.DataFrame(zip(*[v5]), columns=['Maximum_Frequency'])
df6 = pd.DataFrame(zip(*[v6]), columns=['Center_Frequency'])
df7 = pd.DataFrame(zip(*[v7]), columns=['Length'])
df8 = pd.DataFrame(zip(*[v8]), columns=['Gap'])
dftof = pd.DataFrame(zip(*[v9]), columns=['Trigger_off'])
dfet = pd.DataFrame(zip(*[Event_type]), columns=['Event_Type'])
df = pd.concat([dftarr,dfstn, dfdate,dfet,df9,df1, df2, df4, df5, df6, df7, df8,dftof], axis=1)
df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/Events_allstations_1.5s.csv')

df = pd.concat([dftarr,dfstn,dfet], axis=1)
df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/VT_events/HFEvents_allstations_1.5s_ToFindVguess.csv')

end = timer()
print(timedelta(seconds=end-start))


#==================================================================
# Bar plot for recognized events
#==================================================================
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import datetime as dt
# import os
# os.chdir("C:/Users/HP/Desktop")
# #====================================================
# file = 'C:/Users/HP/Desktop/Merged_alldata_allstations.csv'
# # This file was previously ordered first using the date, then the arrival time and finally the stations.
# df = pd.read_csv(file)
# df.fillna(0, inplace=True)
# #df = pd.read_csv('All_Events.csv', sep = ';', thousands='.', decimal=',') #this csv contains the info of 4 stations just for August 1st 2014
# type = df.Type.dropna().values
# # create a list of repetitive strings
# string_list = type
# # create a dictionary to count the frequency of each string
# string_count = {}
# for string in string_list:
#     if string in string_count:
#         string_count[string] += 1
#     else:
#         string_count[string] = 1
# # set the colors for the bars
# colors = ['black','red', 'blue', 'green' ]
# # plot the histogram with different colors
# plt.bar(string_count.keys(), string_count.values(), color=colors[:len(string_count)])
# # add labels and title
# plt.xlabel('Type of Event')
# plt.ylabel('Number of Events')
# plt.title('Histogram of Event Type Frequency')
# # display the plot
# plt.show()

# #======================================================================
# #  This codes creates a BAS event recognition
# #======================================================================
# import pandas as pd
# import numpy as np
# import ast
# file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/All_Events.csv'
# df = pd.read_csv(file)
# #df = pd.read_csv('All_Events.csv', sep = ';', thousands='.', decimal=',') #this csv contains the info of 4 stations just for August 1st 2014
# date = df.Station_Date.dropna().values  # station.time_date this will be separated later
# T_arr = df.Arrival_Time.dropna().values  # Time in seconds don't forget¡
# T_off = df.Trigger_off.dropna().values
# station = []        # Station of the events
# time_date = []       # Contains the dates of the events year-month-day
# for i in range(len(date)):
#     station.append(date[i][0:3])
#     time_date.append(date[i][4:])
# date_time = pd.to_datetime(time_date)  # This is for the plot only
# gap = df.Interevent_time.dropna().values
# FI = df.Frequency_Index.dropna().values
# pamp  = df.Peak_to_Peak_Amplitude.dropna().values
# length = df.Duration.dropna().values
# maxamp = df.Peak_Amplitude.dropna().values
# maxfreq = df.Peak_Frequency.dropna().values
# cenfreq = df.Center_Frequency.dropna().values
# rmaamp = df.RMS_Amplitude.dropna().values
# rmsamp = np.array([ast.literal_eval(i) for i in rmaamp])
# RMS= list()
# for g in range(0, len(rmsamp)):
#     RMS.append(rmsamp[g][0])
# cf_mf = []
# pa_rms = []
# for k in range(0, len(station)):
#     if station[k] == 'BAS': # calculate the CF/PF
#         cf_mf.append(cenfreq[k]/maxfreq[k])
#         pa_rms.append(pamp[k]/RMS[k])
# Events = []
# for t in range(0,len(cf_mf)):
#     if RMS[t] > 100 and FI[t] < 1 and cf_mf[t] < 20 and pa_rms[t] < 17:
#         Events.append([T_arr[t], station[t],time_date[t], FI[t],maxamp[t], pamp[t], RMS[t], maxfreq[t], cenfreq[t], length[t], gap[t],
#          T_off[t], cf_mf[t], pa_rms[t]])
#
# Event_type = []
# for i in range(0, len(Events)):
#     mean_fi = Events[i][3]
#     if mean_fi >= -0.4:
#         Event_type.append('HF')
#     if mean_fi <= -1.3 and mean_fi >= -1.8:
#         Event_type.append('LF')
#     if mean_fi < -0.4 and mean_fi > -1.3:
#         Event_type.append('HYB')
#     if mean_fi < -1.8:
#         Event_type.append('EXP')
# fevents = Events
# Tarr = []
# time = []
# station = []
# fi = []
# v1 = []
# v2 = []
# v4 = []
# v5 = []
# v6 = []
# v7 = []
# v8 = []
# v9 = []
# v10= []
# v11= []
# for i in range(0, len(fevents)):
#     Tarr.append(fevents[i][0])
#     station.append(fevents[i][1])
#     time.append(fevents[i][2])
#     fi.append(fevents[i][3])
#     v1.append(fevents[i][4])
#     v2.append(fevents[i][5])
#     v4.append(fevents[i][6])
#     v5.append(fevents[i][7])
#     v6.append(fevents[i][8])
#     v7.append(fevents[i][9])
#     v8.append(fevents[i][10])
#     v9.append(fevents[i][11])
#     v10.append(fevents[i][12])
#     v11.append(fevents[i][13])
# dftarr = pd.DataFrame(zip(*[Tarr]), columns=['Arrival_Time'])
# dfstn = pd.DataFrame(zip(*[station]), columns=['Station'])
# dfdate = pd.DataFrame(zip(*[time]), columns=['Date'])
# df9 = pd.DataFrame(zip(*[fi]), columns=['Frequency_Index'])
# df1 = pd.DataFrame(zip(*[v1]), columns=['Maximum_Amplitude'])
# df2 = pd.DataFrame(zip(*[v2]), columns=['Phase_Amplitude'])
# df4 = pd.DataFrame(zip(*[v4]), columns=['RMS_Amplitude'])
# df5 = pd.DataFrame(zip(*[v5]), columns=['Maximum_Frequency'])
# df6 = pd.DataFrame(zip(*[v6]), columns=['Center_Frequency'])
# df7 = pd.DataFrame(zip(*[v7]), columns=['Length'])
# df8 = pd.DataFrame(zip(*[v8]), columns=['Gap'])
# dftof = pd.DataFrame(zip(*[v9]), columns=['Trigger_off'])
# dfcfmf = pd.DataFrame(zip(*[v10]), columns=['CF_MF'])
# dfparms = pd.DataFrame(zip(*[v11]), columns=['PA_RMS'])
# dfet = pd.DataFrame(zip(*[Event_type]), columns=['Event_Type'])
# df = pd.concat([dftarr,dfstn, dfdate,df9, dfet,df1, df2, df4, df5, df6, df7, df8,dftof,dfcfmf,dfparms], axis=1)
# df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_newversion/Merged/Final_Events_eventrecognition.csv')