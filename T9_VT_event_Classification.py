#========================== version 28/04/2023 =====================================
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 19:20:18 2023

@author: JhuliMnr
"""
#update: newversion
# This code is BASED ON events_recognition but meant to obtain one list of events
# I want to compare the FI of the same event to classify the whole event between
# HF, LF, HYB, and EXP so thus I will not separte/split one event
#===================================================================================
from timeit import default_timer as timer
from datetime import timedelta
start = timer()
import pandas as pd
import numpy as np
import ast
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
    freq = freq_dict.values()
    return modes, freq
file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_AlldatawoBAS.csv'
df = pd.read_csv(file)
#df = pd.read_csv('All_Events.csv', sep = ';', thousands='.', decimal=',') #this csv contains the info of 4 stations just for August 1st 2014
date = df.Date.dropna().values  # station.time_date this will be separated later
T_arr = df.Arrival_Time.dropna().values  # Time in seconds don't forget¡
T_off = df.Trigger_off.dropna().values
station = []        # Station of the events
time_date = []       # Contains the dates of the events year-month-day
for i in range(len(date)):
    station.append(date[i][0:3])
    time_date.append(date[i][4:])
date_time = pd.to_datetime(time_date)  # This is for the plot only
gap = df.Interevent_time.dropna().values
FI = df.Frequency_Index.dropna().values
pamp  = df.Peak_to_Peak_Amplitude.dropna().values
length = df.Duration.dropna().values
maxamp = df.Peak_Amplitude.dropna().values
maxfreq = df.Peak_Frequency.dropna().values
cenfreq = df.Center_Frequency.dropna().values
rmaamp = df.RMS_Amplitude.dropna().values
rmsamp = np.array([ast.literal_eval(i) for i in rmaamp])
RMS= list()
for g in range(0, len(rmsamp)):
    RMS.append(rmsamp[g][0])

#==============================================================================
events = []
for e in range(0, len(station)):
    events.append([T_arr[e],station[e],time_date[e], FI[e], maxamp[e], pamp[e], RMS[e], maxfreq[e], cenfreq[e],length[e], gap[e], T_off[e]])
#==============================================================================
# We have all the metrics and values for each station now we order it according to its Tarr
# lets order by its Tarr
Ordered_events = sorted(events, key=lambda x: x[0])
i = 0
j = 1
grouped = []  # here will be saved all the events with a similar t_arr in a 2.6 threshold
# once I order it, if Tarr (i) + 2.5seconds is bigger than the next value of Tarr (j)
# I use this part to delete the events that don't repeat since the first Tarr and the
# following events during the 2.5 second window are considered part of the same event,
# values that are off will be ignored and the actual events will be saved in 'events'.
while i < len(Ordered_events)-2:
    if Ordered_events[i][0] + 2.6 >= Ordered_events[j][0]:
        if i+1==j:
            grouped.append(Ordered_events[i])
        grouped.append(Ordered_events[j])
        j += 1
    else:
        i = j
        j = i + 1
# Now I create a nested list where each sublist contains a single event (events1)
l = grouped
i=0
threshold= l[i][0]
s, last = [[l[i]]], None
for x in range(1,len(l)):
    if last is None or l[x][0] <= threshold+2.6:
        s[-1].append(l[x])
        threshold = l[i][0]
    else:
        threshold = l[x][0]
        i = x
        s.append([l[x]])
    last = l[x][0]
events1 = []
# When I have the nested list, I can test if the event is an actual event since
# the sublist can contain just one element, so for now I will use a threshold of 3
# which means that the sublist will be considered an event only if it was recorded in 3 stations
for g in range(0,len(s),1):
    if len(s[g])>=3:
        events1.append(s[g])
# In the previous steps I only consider the Tarr but it can create an error since the data are from
# various days so the Tarr can be repeated, the sublist may contain events from different dates so
# I use this part to avoid that
date_events = [] # this list will contain the final events
cont = 0 # this will count the outliers
outliers = [] # the outlaiers are events that have more than one valid mode
out = [] # outliers info like modes, frequencies of modes and the index of the event in events1
for i in range(0, len(events1)):
    temp = []
    for j in range(0,len(events1[i])):
        temp.append(events1[i][j][2])
    mod, freq = modes(temp)
    event1 = [] # in case there was more than one events this will keep the first recognized mode and event
    event2 = [] # this will contain the second event of second valied mode
    if mod is not None: # by the definition of modes function if the date frequency is one or two, the modes() will be None
        for k in range(0,len(events1[i])):
            if mod[0] == events1[i][k][2]:
                event1.append(events1[i][k])
        if len(mod) > 1:
            cont += 1
            out.append([mod, freq, i])
            outliers.append(events1[i])
            for m in range(1, len(mod)):
                for g in range(0,len(events1[i])):
                    if mod[m] == events1[i][g][2]:
                        event2.append(events1[i][g])
    if len(event1) > 2:
        date_events.append(event1)
    if len(event2) > 2:
        date_events.append(event2)
Event_type = []
for i in range(0, len(date_events)):
    Fi = []
    for j in range(0, len(date_events[i])):
        Fi.append(date_events[i][j][3])
    mean_fi = np.mean(Fi)
    if mean_fi >= -0.4:
        t = 0
        while t < len(date_events[i]):
            Event_type.append('HF')
            t += 1
    if mean_fi <= -1.3 and mean_fi >= -1.8:
        t = 0
        while t < len(date_events[i]):
            Event_type.append('LF')
            t += 1
    if mean_fi < -0.4 and mean_fi > -1.3:
        t = 0
        while t < len(date_events[i]):
            Event_type.append('HYB')
            t += 1
    if mean_fi < -1.8:
        t = 0
        while t < len(date_events[i]):
            Event_type.append('EXP')
            t += 1
# #========================== version 31/08/2023 =====================================
# # -*- coding: utf-8 -*-
# """
# Created on Wed Mar 29 19:20:18 2023
#
# @author: Estudiantes
# """
#
# # This code is BASED ON events_recognition but meant to obtain one list of events
# # I want to compare the FI of the same event to classify the whole event between
# # HF, LF, HYB, and EXP so thus I will not separte/split one event
# #===================================================================================
# from timeit import default_timer as timer
# from datetime import timedelta
# start = timer()
# import pandas as pd
# import numpy as np
# import ast
# def modes(lst):
#     freq_dict = {}
#     for elem in lst:
#         if elem in freq_dict:
#             freq_dict[elem] += 1
#         else:
#             freq_dict[elem] = 1
#     max_freq = max(freq_dict.values())
#     if max_freq > 2:
#         modes = [k for k, v in freq_dict.items() if v == max_freq]
#     else:
#         modes = None
#     freq = freq_dict.values()
#     return modes, freq
# file = 'C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_AlldatawoBAS.csv'
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
#
# #==============================================================================
# events = []
# for e in range(0, len(station)):
#     events.append([T_arr[e],station[e],time_date[e], FI[e], maxamp[e], pamp[e], RMS[e], maxfreq[e], cenfreq[e],length[e], gap[e], T_off[e]])
# #==============================================================================
# # We have all the metrics and values for each station now we order it according to its Tarr
# # lets order by its Tarr
# Ordered_events = sorted(events, key=lambda x: x[0])
# i = 0
# j = 1
# grouped = []  # here will be saved all the events with a similar t_arr in a 2.6 threshold
# # once I order it, if Tarr (i) + 2.5seconds is bigger than the next value of Tarr (j)
# # I use this part to delete the events that don't repeat since the first Tarr and the
# # following events during the 2.5 second window are considered part of the same event,
# # values that are off will be ignored and the actual events will be saved in 'events'.
# while i < len(Ordered_events)-2:
#     if Ordered_events[i][0] + 2.6 >= Ordered_events[j][0]:
#         if i+1==j:
#             grouped.append(Ordered_events[i])
#         grouped.append(Ordered_events[j])
#         j += 1
#     else:
#         i = j
#         j = i + 1
# # Now I create a nested list where each sublist contains a single event (events1)
# l = grouped
# i=0
# threshold= l[i][0]
# s, last = [[l[i]]], None
# for x in range(1,len(l)):
#     if last is None or l[x][0] <= threshold+2.6:
#         s[-1].append(l[x])
#         threshold = l[i][0]
#     else:
#         threshold = l[x][0]
#         i = x
#         s.append([l[x]])
#     last = l[x][0]
# events1 = []
# # When I have the nested list, I can test if the event is an actual event since
# # the sublist can contain just one element, so for now I will use a threshold of 3
# # which means that the sublist will be considered an event only if it was recorded in 3 stations
# for g in range(0,len(s),1):
#     if len(s[g])>=3:
#         events1.append(s[g])
# # In the previous steps I only consider the Tarr but it can create an error since the data are from
# # various days so the Tarr can be repeated, the sublist may contain events from different dates so
# # I use this part to avoid that
# date_events = [] # this list will contain the final events
# cont = 0 # this will count the outliers
# outliers = [] # the outlaiers are events that have more than one valid mode
# out = [] # outliers info like modes, frequencies of modes and the index of the event in events1
# for i in range(0, len(events1)):
#     temp = []
#     for j in range(0,len(events1[i])):
#         temp.append(events1[i][j][2])
#     mod, freq = modes(temp)
#     event1 = [] # in case there was more than one events this will keep the first recognized mode and event
#     event2 = [] # this will contain the second event of second valied mode
#     if mod is not None: # by the definition of modes function if the date frequency is one or two, the modes() will be None
#         for k in range(0,len(events1[i])):
#             if mod[0] == events1[i][k][2]:
#                 event1.append(events1[i][k])
#         if len(mod) > 1:
#             cont += 1
#             out.append([mod, freq, i])
#             outliers.append(events1[i])
#             for m in range(1, len(mod)):
#                 for g in range(0,len(events1[i])):
#                     if mod[m] == events1[i][g][2]:
#                         event2.append(events1[i][g])
#     if len(event1) > 2:
#         date_events.append(event1)
#     if len(event2) > 2:
#         date_events.append(event2)
# Event_type = []
# for i in range(0, len(date_events)):
#     Fi = []
#     for j in range(0, len(date_events[i])):
#         Fi.append(date_events[i][j][3])
#     mean_fi = np.mean(Fi)
#     if mean_fi >= -0.4:
#         t = 0
#         while t < len(date_events[i]):
#             Event_type.append('HF')
#             t += 1
#     if mean_fi <= -1.3 and mean_fi >= -1.8:
#         t = 0
#         while t < len(date_events[i]):
#             Event_type.append('LF')
#             t += 1
#     if mean_fi < -0.4 and mean_fi > -1.3:
#         t = 0
#         while t < len(date_events[i]):
#             Event_type.append('HYB')
#             t += 1
#     if mean_fi < -1.8:
#         t = 0
#         while t < len(date_events[i]):
#             Event_type.append('EXP')
#             t += 1























#========================== version 31/08/2022 =====================================
import pandas as pd
import os
os.chdir("C:/Users/HP/Desktop/Geology of Ecuador/Prueba Agosto")
year = '2014' #%(2014 2015)
#===================================================
Stations = ['BAS', 'BB1', 'BB2','BB3', 'BB4','BB5']
tarr_st = []
startmonth = 8
endmonth = 8
totalevents = []
for month in range(startmonth,endmonth+1):
    m = str(month)
    for i in Stations:
        try:
            file = '{}.{}-{}-VT_Events.csv'.format(*[i, year, m.zfill(2)])
            var = pd.read_csv(file)
            Tarr = var.Arrival_Time.dropna().values
            time = var.Time.dropna().values
            date = var.Station_Date.dropna().values
            FI = var.Frequency_Index.dropna().values  # Frequency Index
            v1 = var.Duration.dropna().values
            v2 = var.Interevent_time.dropna().values
            v4 = var.Peak_Amplitude.dropna().values
            v5 = var.Peak_to_Peak_Amplitude.dropna().values
            v6 = var.RMS_Amplitude.dropna().values
            v7 = var.Peak_Frequency.dropna().values
            v8 = var.Center_Frequency.dropna().values
            v9 = var.Trigger_off.dropna().values
            for k in range(0, len(Tarr)):
                tarr_st.append([Tarr[k], time[k],date[k],FI[k],v1[k],v2[k],v4[k],v5[k],v6[k],v7[k],v8[k],v9[k]])  #With this we put the name of the station to every Tarr
            # print(Tarr)
        except FileNotFoundError:
            pass
# lets order by its Tarr
tarr_f = sorted(tarr_st, key=lambda x: x[0])
i = 0
j = 1
events = []
while i < len(tarr_f)-1:
    if tarr_f[i][0] + 2.6 >= tarr_f[j][0]:
        if i+1==j:
            events.append(tarr_f[i])
        events.append(tarr_f[j])
        j += 1
    else:
        i = j
        j = i + 1

l = events
i=0
threshold= l[i][0]
s, last = [[l[i]]], None
for x in range(1,len(l)-1):
    if last is None or l[x][0] <= threshold+2.6:
        s[-1].append(l[x])
        threshold = l[i][0]
    else:
        threshold = l[x][0]
        i = x
        s.append([l[x]])
    last = l[x][0]
events1 = []
for g in range(0,len(s),1):
    if len(s[g])>=3:
        events1.append(s[g])
fevents = []
nfevents = []
for h in range(0,len(events1)):
    if events1[h][0][2][4:] == events1[h][1][2][4:] == events1[h][2][2][4:]:
        fevents.append(events1[h])
    else:
        nfevents.append(events1[h])
print(fevents)
Tarr = []
time = []
station = []
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
    try:
        for j in range(0, 4):
            Tarr.append(fevents[i][j][0])
            time.append(fevents[i][j][1])
            station.append(fevents[i][j][2])
            fi.append(fevents[i][j][3])
            v1.append(fevents[i][j][4])
            v2.append(fevents[i][j][5])
            v4.append(fevents[i][j][6])
            v5.append(fevents[i][j][7])
            v6.append(fevents[i][j][8])
            v7.append(fevents[i][j][9])
            v8.append(fevents[i][j][10])
            v9.append(fevents[i][j][11])
    except IndexError:
        pass
TAR = [fevents[tr][0][0] for tr in range(0, len(fevents), 1)] # List of the first Tarr of a single event
dfTAR = pd.DataFrame(zip(*[Tarr]), columns=['TARR'])
dftarr = pd.DataFrame(zip(*[Tarr]), columns=['Arrival_Time'])
dfdate = pd.DataFrame(zip(*[time]), columns=['Time'])
dfstn = pd.DataFrame(zip(*[station]), columns=['Station_Date'])
df9 = pd.DataFrame(zip(*[fi]), columns=['Frequency_Index'])
df1 = pd.DataFrame(zip(*[v1]), columns=['Duration'])
df2 = pd.DataFrame(zip(*[v2]), columns=['Interevent_time'])
df4 = pd.DataFrame(zip(*[v4]), columns=['Peak_Amplitude'])
df5 = pd.DataFrame(zip(*[v5]), columns=['Peak_to_Peak_Amplitude'])
df6 = pd.DataFrame(zip(*[v6]), columns=['RMS_Amplitude'])
df7 = pd.DataFrame(zip(*[v7]), columns=['Peak_Frequency'])
df8 = pd.DataFrame(zip(*[v8]), columns=['Center_Frequency'])
dftof = pd.DataFrame(zip(*[v9]), columns=['Trigger_off'])
df = pd.concat([dftarr,dfdate,dfstn,df9, df1, df2, df4, df5, df6, df7, df8,dftof,dfTAR], axis=1)
df.to_csv('2014-08-VT_RealEvents.csv')






#=================================================================================

# #===============================================================
# import pandas as pd
# import os
# os.chdir("C:/Users/HP/Desktop/Geology of Ecuador/Prueba Agosto")
# year = '2014' #%(2014 2015)
# #===================================================
# Stations = ['BAS', 'BB1', 'BB2','BB3', 'BB4','BB5']
# tarr_st = []
# startmonth = 8
# endmonth = 8
# totalevents = []
# for month in range(startmonth,endmonth+1):
#     m = str(month)
#     for i in Stations:
#         try:
#             file = '{}.{}-{}-VT_Events.csv'.format(*[i, year, m.zfill(2)])
#             var = pd.read_csv(file)
#             Tarr = var.Arrival_Time.dropna().values
#             time = var.Time.dropna().values
#             date = var.Station_Date.dropna().values
#             for k in range(0, len(Tarr)):
#                 tarr_st.append([Tarr[k], time[k],date[k]])  #With this we put the name of the station to every Tarr
#             # print(Tarr)
#         except FileNotFoundError:
#             pass
#     # lets order by its Tarr
#     tarr_f = sorted(tarr_st, key=lambda x: x[0])
#     i = 0
#     j = 1
#     events = []
#     while i < len(tarr_f)-1:
#         if tarr_f[i][0] + 2.5 >= tarr_f[j][0] and tarr_f[i][2] == tarr_f[j][2]:
#             if i+1==j:
#                 events.append(tarr_f[i])
#             events.append(tarr_f[j])
#             j += 1
#         else:
#             i = j
#             j = i + 1
#
#     l = events
#     i=0
#     threshold= l[i][0]
#     s, last = [[l[i]]], None
#     for x in range(1,len(l)):
#         if last is None or l[x][0] <= threshold+2.5:
#             s[-1].append(l[x])
#             threshold = l[i][0]
#         else:
#             threshold = l[x][0]
#             i = x
#             s.append([l[x]])
#         last = l[x][0]
#     print(l)
#     events1 = []
#     for g in range(0,len(s),1):
#         if len(s[g])>=3:
#             events1.append(s[g])
#     # def extract(list):
#     #     return [elem[0] for elem in list]
#     # extract(events1[0])
#     # print(extract(events1[0]))






# #===============================================================
# import pandas as pd
# import os
# os.chdir("C:/Users/HP/Desktop/Geology of Ecuador/Prueba Agosto")
# year = '2014' #%(2014 2015)
# #===================================================
# Stations = ['BAS', 'BB1', 'BB2','BB3', 'BB4','BB5']
# tarr_st = []
# startmonth = 8
# endmonth = 8
# totalevents = []
# for month in range(startmonth,endmonth+1):
#     m = str(month)
#     for i in Stations:
#         try:
#             file = '{}.{}-{}-VT_Events.csv'.format(*[i, year, m.zfill(2)])
#             var = pd.read_csv(file)
#             Tarr = var.Arrival_Time.dropna().values
#             for k in range(0, len(Tarr)):
#                 tarr_st.append([Tarr[k], i])  #With this we put the name of the station to every Tarr
#             # print(Tarr)
#         except FileNotFoundError:
#             pass
#     # lets order by its Tarr
#     tarr_f = sorted(tarr_st, key=lambda x: x[0])
#     i = 0
#     j = 1
#     events = []
#     while i < len(tarr_f)-1:
#         if tarr_f[i][0] + 2.5 >= tarr_f[j][0]:
#             if i+1==j:
#                 events.append(tarr_f[i])
#             events.append(tarr_f[j])
#             j += 1
#         else:
#             i = j
#             j = i + 1
#
#     l = events
#     i=0
#     threshold= l[i][0]
#     s, last = [[l[i]]], None
#     for x in range(1,len(l)):
#         if last is None or l[x][0] <= threshold+2.5:
#             s[-1].append(l[x])
#             threshold = l[i][0]
#         else:
#             threshold = l[x][0]
#             i = x
#             s.append([l[x]])
#         last = l[x][0]
#
#     events1 = []



#============================================================
#===============================================================
# import pandas as pd
# import os
# os.chdir("C:/Users/HP/Desktop/Geology of Ecuador/Prueba Agosto")
# year = '2014' #%(2014 2015)
# #===================================================
# Stations = ['BAS', 'BB1', 'BB2','BB3', 'BB4','BB5']
# tarr_st = []
# startmonth = 8
# endmonth = 8
# totalevents = []
# for month in range(startmonth,endmonth+1):
#     m = str(month)
#     for i in Stations:
#         try:
#             file = '{}.{}-{}-VT_Events.csv'.format(*[i, year, m.zfill(2)])
#             var = pd.read_csv(file)
#             Tarr = var.Arrival_Time.dropna().values
#             for k in range(0, len(Tarr)):
#                 tarr_st.append([Tarr[k], i])  #With this we put the name of the station to every Tarr
#             # print(Tarr)
#         except FileNotFoundError:
#             pass
#     # lets order by its Tarr
#     tarr_f = sorted(tarr_st, key=lambda x: x[0])
#     events = []
#     # ==>>>>>>> Until here everything works :3
#     for i in range(0, len(tarr_f)-1,1):
#         if tarr_f[i][0] + 2.5 >= tarr_f[i+1][0]:
#             events.append(tarr_f[i])
#
#     i = 0
#     j = 1
#     events = []
#     while i < len(tarr_f)-1:
#         if tarr_f[i][0] + 2.5 >= tarr_f[j][0]:
#             if i+1==j:
#                 events.append(tarr_f[i])
#             events.append(tarr_f[j])
#             j += 1
#         else:
#             i = j + 1
#             j = i + 1
#
#     print(events)
#
#     l = events
#     i=0
#     threshold= l[i][0]
#     s, last = [[l[i]]], None
#     for x in range(1,len(l)):
#         if last is None or l[x][0] <= threshold+2.5:
#             s[-1].append(l[x])
#             threshold = l[i][0]
#         else:
#             threshold = l[x][0]
#             i = x
#             s.append([l[x]])
#         last = l[x][0]
#
#     events1 = []
#     for g in range(0,len(s),1):
#         if len(s[g])>=3:
#             events1.append(s[g])
#     totalevents.append(events1)