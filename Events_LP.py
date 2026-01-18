from obspy import read
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from obspy.signal.invsim import cosine_taper
import os
os.chdir("C:/Users/HP/Desktop/Geology of Ecuador")
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
sr = 100
i = 230000
j = 250000
fs = 100
even1 = data[i:j]
time1 = t[i:j]
N = int(len(even1))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even1 - np.mean(even1)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf1 = xf
yf1 = yfabs
st = read('8E.BB2.HHZ.20141203.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 8225000
j = 8230000
fs = 100
even2 = data[i:j]
time2 = t[i:j]
N = int(len(even2))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even2 - np.mean(even2)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf2 = xf
yf2 = yfabs
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even3 = data[i:j]
time3 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even3 - np.mean(even3)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf3 = xf
yf3 = yfabs
#===============================================================
st = read('8E.BB4.HHZ.20150118.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even4 = data[i:j]
time4 = t[i:j]
N = int(len(even4))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even4 - np.mean(even4)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf4 = xf
yf4 = yfabs
#===============================================================
st = read('8E.BB5.HHZ.20140629.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even5 = data[i:j]
time5 = t[i:j]
N = int(len(even5))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even5 - np.mean(even5)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf5 = xf
yf5 = yfabs
#===============================================================
st = read('8E.BB5.HHZ.20140630.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even6 = data[i:j]
time6 = t[i:j]
N = int(len(even6))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even6 - np.mean(even6)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf6 = xf
yf6 = yfabs
#=========================================================
area6 = np.trapz(yf6, xf6) #VLP
y_nor6 = yf6 / area6
area5 = np.trapz(yf5, xf5) #HYB
y_nor5 = yf5 / area5
area4 = np.trapz(yf4, xf4) #HF
y_nor4 = yf4 / area4
area3 = np.trapz(yf3, xf3)
y_nor3 = yf3 / area3
area2 = np.trapz(yf2, xf2)
y_nor2 = yf2 / area2
area1 = np.trapz(yf1, xf1)
y_nor1 = yf1 / area1
plt.plot(xf3, y_nor3, label='Hybrid', lw = 0.3)
plt.plot(xf2, y_nor2, label='Low Frequency', lw = 0.3)
plt.plot(xf1, y_nor1, label='High Frequency', lw = 0.3)
plt.plot(xf4, y_nor4, label='High Frequency', lw = 0.3)
plt.plot(xf5, y_nor5, label='Hybrid', lw = 0.3)
plt.plot(xf6, y_nor6, label='Very Low Frequency', lw = 0.3)
plt.legend()
plt.show()

















































































# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:32:48 2023

@author: Estudiantes
"""

#=======================================================================
from obspy import read
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('C:/Users/HP/Desktop/Geology of Ecuador')
#=======================================================================
network = '8E'
channel = 'HHZ'
stations = ['BAS','BB1','BB2','BB3','BB4','BB5']
fday = 12        #start day
eday = 12       #end day
fmonth = 4     #start month
emonth = 4     #end month
year = '2014'
#======================================================================

for k in range(fmonth,emonth+1,1):
    month = str(k)
    for a in range(fday,eday+1,1):
        day = str(a)
        datst = []
        for s in stations:
            station = str(s)
            try:
                file = '{}.{}.{}.{}{}{}.mseed'.format(*[network, station, channel, year, month.zfill(2), day.zfill(2)])
                st = read(file)
                st.detrend(type='demean')
                st.detrend(type='linear')
                st.taper(type="cosine", max_percentage=0.05)
                st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
                st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
                tr = st[0]
                data = np.array(tr.data)
                df = tr.stats.sampling_rate
                npts = tr.stats.npts
                t = np.arange(npts, dtype=np.float32) / df
                datst.append([data,t, tr.id])
            except FileNotFoundError:
                pass 
from scipy import signal
from scipy.signal import butter, filtfilt

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y                
             
i = 0
step = 360000
low = 0.2
high = 2.1
for j in range(0, len(datst[i][0]), 360000):
    fig, axs = plt.subplots(4, 1, figsize=(14, 9), sharex= True)
    for i in range(0, len(datst)):
        xi = datst[i][0][j:j+step]
        ti = datst[i][1][j:j+step]
        yi = butter_bandpass_filter(xi, low, high, 100)
        axs[i].plot(ti,yi, color = 'k')
        label = datst[i][2][3:6]
        axs[i].set_ylabel("Station:%s\n" % label)
        
        # fig, axs = plt.subplots(4, 1, figsize=(14, 9), sharex= True)
        # xi = datst[0][0][7575000:7725000]
        # x2 = datst[1][0][7575000:7725000]
        # x3 = datst[2][0][7575000:7725000]
        # x4 = datst[3][0][7575000:7725000]
        # fs = 100
        # y = butter_bandpass_filter(xi,1,5,fs)
        # y2 = butter_bandpass_filter(x2,1,5,fs)
        # y3 = butter_bandpass_filter(x3,1,5,fs)
        # y4 = butter_bandpass_filter(x4,1,5,fs)
        # t = datst[0][1][7575000:7725000]
        # axs[0].plot(t,y)
        # axs[1].plot(t,y2)
        # axs[2].plot(t,y3)
        # axs[3].plot(t,y4)
   
        fig, axs = plt.subplots(4, 1, figsize=(14, 9), sharex= True)
        i = 0
        j = 8000000
        xi = datst[0][0][i:j]
        x2 = datst[1][0][i:j]
        x3 = datst[2][0][i:j]
        x4 = datst[3][0][i:j]
        fs = 100
        low = 0.2
        high = 10
        y = butter_bandpass_filter(xi,low,high,fs)
        y2 = butter_bandpass_filter(x2,low,high,fs)
        y3 = butter_bandpass_filter(x3,low,high,fs)
        y4 = butter_bandpass_filter(x4,low,high,fs)
        t = datst[0][1][i:j]
        axs[0].plot(t,y, color='k')
        axs[1].plot(t,y2, color='k')
        axs[2].plot(t,y3, color='k')
        axs[3].plot(t,y4, color='k')    
                
                
                
  # i = 8340000
  # j = 8360000              
                
#  8E.BB3..HHZ | 2014-08-11
#========== Hybrid Event ==================
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))                
i = 1730000
j = 1760000
fs = 100   
even = data[i:j]
time = t[i:j]
yi = butter_bandpass_filter(even, 1, 10, fs, order=5)
plt.plot(time,yi, color = 'k')
plt.show()
frequencies, times, spectrogram = signal.spectrogram(yi, fs)
plt.pcolormesh(times, frequencies[:50], spectrogram[:50], cmap='terrain')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
#=============================================
# 8E.BB2..HHZ | 2014-12-03
#========== LP Event ==================      
st = read('8E.BB2.HHZ.20141203.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))               
i = 8225000
j = 8230000
fs = 100
even = data[i:j]
time = t[i:j]
yi = butter_bandpass_filter(even, 1, 10, fs, order=5)
plt.plot(time,yi, color = 'k')
plt.show()
frequencies, times, spectrogram = signal.spectrogram(yi, fs)
plt.pcolormesh(times, frequencies[:50], spectrogram[:50], cmap='terrain')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show() 
#==============================================
#  8E.BB3..HHZ | 2014-08-11
#============= VT Event =======================
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))                
i = 230000
j = 250000
fs = 100   
even = data[i:j]
time = t[i:j]
yi = butter_bandpass_filter(even, 1, 10, fs, order=5)
plt.plot(time,yi, color = 'k')
plt.show()
frequencies, times, spectrogram = signal.spectrogram(yi, fs)
plt.pcolormesh(times, frequencies[:50], spectrogram[:50], cmap='terrain')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()             
 
#==================================================
#  Normalized events for the FI spectral band
#==================================================
from obspy import read
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from obspy.signal.invsim import cosine_taper
import os
os.chdir("C:/Users/Estudiantes/Documents/Jhuliana Monar/Processed_data/Downsampled_data")
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data)) 
sr = 100               
i = 230000
j = 250000
fs = 100   
even1 = data[i:j]
time1 = t[i:j]
N = int(len(even1))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even1 - np.mean(even1)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf1 = xf
yf1 = yfabs
st = read('8E.BB2.HHZ.20141203.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))                
i = 8225000
j = 8230000
fs = 100   
even2 = data[i:j]
time2 = t[i:j]
N = int(len(even2))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even2 - np.mean(even2)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf2 = xf
yf2 = yfabs
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))                
i = 1730000
j = 1760000
fs = 100   
even3 = data[i:j]
time3 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even3 - np.mean(even3)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf3 = xf
yf3 = yfabs
area3 = np.trapz(yf3, xf3)
y_nor3 = yf3 / area3
area2 = np.trapz(yf2, xf2)
y_nor2 = yf2 / area2
area1 = np.trapz(yf1, xf1)
y_nor1 = yf1 / area1
plt.plot(xf3, y_nor3, label='Hybrid', lw = 0.3)
plt.plot(xf2, y_nor2, label='Low Frequency', lw = 0.3)
plt.plot(xf1, y_nor1, label='High Frequency', lw = 0.3)
plt.legend()
plt.show()

fig, axs = plt.subplots(4, 1, figsize=(14, 9), sharex= True)
y = butter_bandpass_filter(xi,low,high,fs)
y2 = butter_bandpass_filter(x2,low,high,fs)
y3 = butter_bandpass_filter(x3,low,high,fs)
y4 = butter_bandpass_filter(x4,low,high,fs)
t = datst[0][1][i:j]
axs[0].plot(t,y, color='k')
axs[1].plot(t,y2, color='k')
axs[2].plot(t,y3, color='k')
axs[3].plot(t,y4, color='k')  

#==================================================
# FOR SPECTROGRAM -- AND AMPLITUDE vs TIME
#==================================================
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))                
i = 1730000
j = 1760000
fs = 100   
even = data[i:j]
time = t[i:j]
yi = butter_bandpass_filter(even, 1, 10, fs, order=5)
#plt.plot(time,yi, color = 'k')
#plt.show()
frequencies, times, spectrogram = signal.spectrogram(yi, fs)
fig, axs = plt.subplots(2, 1, figsize=(12, 5))
axs[0].plot(time,yi, color='k')
axs[0].set_ylabel('Amplitude')
axs[0].set_xlabel('Time [s]')
axs[1].pcolormesh(times, frequencies[:50], spectrogram[:50], cmap='terrain')
fig.tight_layout(h_pad=2)

#==================================================
#  Normalized events for the FI spectral band
#   for six events
#==================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from obspy.signal.invsim import cosine_taper
import os
os.chdir("C:/Users/Estudiantes/Documents/Jhuliana Monar/Processed_data/Downsampled_data")
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
sr = 100
i = 230000
j = 250000
fs = 100
even1 = data[i:j]
time1 = t[i:j]
N = int(len(even1))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even1 - np.mean(even1)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf1 = xf
yf1 = yfabs
st = read('8E.BB2.HHZ.20141203.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 8225000
j = 8230000
fs = 100
even2 = data[i:j]
time2 = t[i:j]
N = int(len(even2))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even2 - np.mean(even2)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf2 = xf
yf2 = yfabs
st = read('8E.BB3.HHZ.20140811.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even3 = data[i:j]
time3 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even3 - np.mean(even3)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf3 = xf
yf3 = yfabs
st = read('8E.BB4.HHZ.20150118.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1745000
j = 17550000
fs = 100
even4 = data[i:j]
time4 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even4 - np.mean(even4)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf4 = xf
yf4 = yfabs
st = read('8E.BB5.HHZ.20140629.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 5860000
j = 5861000
fs = 100
even5 = data[i:j]
time5 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even5 - np.mean(even5)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf5 = xf
yf5 = yfabs
st = read('8E.BB5.HHZ.20140630.mseed')
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
t = np.arange(0,len(data))
i = 1730000
j = 1760000
fs = 100
even6 = data[i:j]
time6 = t[i:j]
N = int(len(even3))  # Number of data points
p1 = 0.1  # 10%
tap = cosine_taper(N, p1)  # Taper for the time domain
demean = even6 - np.mean(even6)
tap_data = demean * tap
yf = rfft(tap_data)
xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
pf_index = np.argmax(np.abs(yf))
yfabs = np.abs(yf)
xf6 = xf
yf6 = yfabs
area6 = np.trapz(yf6, xf6) #VLP
y_nor6 = yf6 / area6
area5 = np.trapz(yf5, xf5) #HYB
y_nor5 = yf5 / area5
area4 = np.trapz(yf4, xf4) #HF
y_nor4 = yf4 / area4
area3 = np.trapz(yf3, xf3)
y_nor3 = yf3 / area3
area2 = np.trapz(yf2, xf2)
y_nor2 = yf2 / area2
area1 = np.trapz(yf1, xf1)
y_nor1 = yf1 / area1
plt.plot(xf3, y_nor3, label='Hybrid', lw = 0.3)
plt.plot(xf2, y_nor2, label='Low Frequency', lw = 0.3)
plt.plot(xf1, y_nor1, label='High Frequency', lw = 0.3)
plt.plot(xf4, y_nor4, label='High Frequency', lw = 0.3)
plt.plot(xf5, y_nor5, label='Hybrid', lw = 0.3)
plt.plot(xf6, y_nor6, label='Very Low Frequency', lw = 0.3)
plt.legend()
plt.show()