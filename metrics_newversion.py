from scipy.fft import rfft, rfftfreq
from timeit import default_timer as timer
from datetime import timedelta
start = timer()
from Thesis_3_4 import sta_lta, t_on_off
from obspy import read
import numpy as np
import pandas as pd

import os
#==============================================================================
os.chdir("C:/Users/HP/Desktop/Geology of Ecuador/wholedata")
# ============================================================================
N_events = []
network = '8E'
channel = 'HHZ'
stations = ['BAS'] #'BB1','BB2','BB3',,'BB5'
fday = 1  # start day
eday = 31  # end day
fmonth = 1  # start month
emonth = 1  # end month
year = ['2014'] #,'2015'
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
                    file = '{}.{}.{}.{}{}{}.mseed'.format(
                        *[network, station, channel, year, month.zfill(2), day.zfill(2)])
                    st = read(file)
                    st.detrend(type='demean')
                    st.detrend(type='linear')
                    st.taper(type="cosine", max_percentage=0.05)
                    st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
                    st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
                    st1 = st.copy()
                    st.filter('lowpass', freq=10, zerophase=True)  # These filters are applied to get the STA ratio
                    st.filter('highpass', freq=1, zerophase=True)
                    tr = st[0]
                    print(file)
                    data1 = np.array(tr.data)
                    npts = tr.stats.npts
                    sr = tr.stats.sampling_rate
                    time = np.arange(npts, dtype=np.float32) / sr
                    nsta = int(1 * sr)
                    nlta = int(7 * sr)
                    sta = sta_lta(data1, nsta, nlta)  # STA/LTA ratio
                    tOn = 3.1 # The threshold where the event start
                    tOff = 0.4 # The threshold where the event ends
                    triggers = t_on_off(sta, tOn, tOff)
                    t_on = triggers[:, 0]
                    t_off = triggers[:, 1]
                    tr = st1[0]
                    data = np.array(tr.data)
                    npts = tr.stats.npts
                    sr = tr.stats.sampling_rate
                    time = np.arange(npts, dtype=np.float32) / sr
                    max_freq = []
                    cf = []
                    FI = []
                    RMS = []
                    max_amp = []
                    p_amp = []
                    length = np.divide((t_off - t_on), sr)
                    gap = [(t_on[i+1] - t_off[i])/sr for i in range(len(t_on)-1)]
                    c = [[]]  # those are the start of an event separated by hour
                    p = 360000
                    while p <= len(data) - 360000:
                        for i in t_on:
                            if i > p - 360000 and i <= p:
                                c[-1].append(i)
                        c.append([])
                        p += 360000
                    event_rate = [len(e) for e in c]  # number of events each hour
                    for s in range(0,len(t_on), 1):
                        # Calculate the RMS amplitude
                        rms_amplitude = np.sqrt(np.mean(data[t_on[s]:t_off[s]] ** 2))
                        RMS.append(rms_amplitude)
                        edata = data[t_on[s]:t_off[s]]
                        # Calculate the maximum amplitude
                        demean = edata - np.mean(edata)
                        pa = max(abs(demean))
                        max_amp.append(pa)
                        # Calculate the phase-amplitude
                        pamp = max(edata) - min(edata)
                        p_amp.append(pamp)
                        # Compute the FFT
                        fft_signal = rfft(demean)
                        freqs = rfftfreq(len(demean)) * sr  # Real Frequency --> Real numbers
                        # Calculate the peak frequency
                        peak_freq = freqs[np.argmax(np.abs(fft_signal))]
                        max_freq.append(peak_freq)
                        # Calculate the center frequency and frequency index
                        freq_sum = np.cumsum(np.abs(fft_signal))
                        center_freq = freqs[np.argmin(np.abs(freq_sum - freq_sum[-1] / 2))]
                        cf.append(center_freq)
                        upper_amp = np.mean(np.abs(fft_signal[freqs > center_freq]))
                        lower_amp = np.mean(np.abs(fft_signal[freqs < center_freq]))
                        freq_index = np.log10(upper_amp / lower_amp)
                        FI.append(freq_index)
                    dfton = pd.DataFrame(list(zip(*[t_on])), columns=['Trigger_on'])
                    dftof = pd.DataFrame(list(zip(*[t_off])), columns=['Trigger_off'])
                    df1 = pd.DataFrame(list(zip(*[length])), columns=['Length'])
                    df2 = pd.DataFrame(list(zip(*[gap])), columns=['Gap'])
                    df3 = pd.DataFrame(list(zip(*[event_rate])), columns=['Event_Rate'])
                    df4 = pd.DataFrame(list(zip(*[max_amp])), columns=['Maximum_Amplitude'])
                    df5 = pd.DataFrame(list(zip(*[p_amp])), columns=['Phase_Amplitude'])
                    df6 = pd.DataFrame(list(zip(*[RMS])), columns=['RMS_Amplitude'])
                    df7 = pd.DataFrame(list(zip(*[max_freq])), columns=['Maximum_Frequency'])
                    df8 = pd.DataFrame(list(zip(*[cf])), columns=['Center_Frequency'])
                    df9 = pd.DataFrame(list(zip(*[FI])), columns=['Frequency_Index'])
                    df = pd.concat([dfton, dftof, df1, df2, df3, df4, df5, df6, df7, df8, df9], axis=1)
                    df.to_csv('C:/Users/HP/Desktop/Thesis Project/RESULTS/Metrics_newversion/{}.{}.{}.{}{}{}_newversion_1-10Hz.csv'.format(
                        *[network, station, channel, year, month.zfill(2), day.zfill(2)]))
                except FileNotFoundError:
                    pass
end = timer()
print(timedelta(seconds=end - start))
