# ---------------------------- Lastest Version of Event Plotting With the Normalized Amplitude ----------------------------------------
def plot_event(trace, event, t_event, t_bef, d_bef, xf, yf, FI,RMS, s,
               save=True):  # event is the data for one event, t_event is the time,  t_bef is the time before the event to get the whole picture, d_bef data before the event,thr_on the threshold for sta lta t0n, t0ff, thr_off
    import matplotlib.pyplot as plt  # yf is the normalized yabs resulted from rrft
    label1 = trace.stats.starttime.isoformat()  #
    label2 = trace.id
    width1 = 15
    height1 = 9
    fig, axs = plt.subplots(2, 1, figsize=(width1, height1), gridspec_kw={'height_ratios': [4, 2]})
    axs[0].plot(xf, yf, 'k')
    axs[0].set_xlabel('Frequency [Hz]')
    axs[0].set_ylabel('Normalized Amplitude')
    axs[1].plot(t_bef, d_bef, 'k')
    axs[1].plot(t_event, event, 'b', label='Event')
    i, j = axs[1].get_ylim()
    try:
        axs[1].vlines(t_event[0], i, j, color='r', lw=2,
                      label="Event start", linestyles='dashed')
        axs[1].vlines(t_event[-1], i, j, color='b', lw=2,
                      label="Event end", linestyles='dashed')
    except IndexError:
        pass
    axs[1].set_xlabel('Time [seconds * sample rate]')
    axs[1].set_ylabel('Amplitude')
    fig.suptitle("Station ID:%s\n" % label2 + "\nDate:%s" % label1)
    textstr = '\n'.join((
        r'$\mathrm{FI}=%.2f$' % (FI,),
        r'$\mathrm{Ton}=%.2f$' % (t_event[0],),
        r'$\mathrm{Toff}=%.2f$' % (t_event[-1],),
        r'$\mathrm{RMS}=%.2f$' % (RMS,)))
    axs[0].text(0.9, 0.95, textstr, transform=axs[0].transAxes, fontsize=10, verticalalignment='top')
    if save:
        #plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/Event_{}.pdf'.format([s]))
        plt.show()

import os
os.chdir('C:/Users/HP/Desktop/Geology of Ecuador/BB4')
from scipy.fft import rfft, rfftfreq,fft
from obspy.signal.invsim import cosine_taper
from Thesis_3_4 import t_on_off, sta_lta, plot_STA_LTA
from obspy import read
import numpy as np

file = 'Copia de 8E.BB4.HHZ.20140811.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
st1 = st.copy()
st.filter('lowpass', freq=10, zerophase=True)
st.filter('highpass', freq=1, zerophase=True)# These filters are applied to get the STA ratio
tr = st[0]
data1 = np.array(tr.data)
npts = tr.stats.npts
sr = tr.stats.sampling_rate
time = np.arange(npts, dtype=np.float32) / sr
nsta = int(1 * sr)
nlta = int(7 * sr)
sta = sta_lta(data1, nsta, nlta)  # STA/LTA ratio
tOn = 3.1
tOff = 0.4
triggers = t_on_off(sta, tOn, tOff)
t_on = triggers[:, 0]
t_off = triggers[:, 1]
tr = st1[0]
data = np.array(tr.data)
npts = tr.stats.npts
sr = tr.stats.sampling_rate
time = np.arange(npts, dtype=np.float32) / sr
window = 500  # window of 5 seconds
FI = []
events_data = []
events_time = []
t_bef, d_bef = [], []
xf_all, yf_all = [], []
staevent = []
RMS = []
max_freq = []
cf = []
for s in range(0,len(t_on), 1):
    rms_amplitude = np.sqrt(np.mean(data[t_on[s]:t_off[s]] ** 2))
    RMS.append(rms_amplitude)
    edata = data[t_on[s]:t_off[s]]
    # Compute the FFT
    demean = edata - np.mean(edata)
    fft_signal = rfft(demean)
    freqs = rfftfreq(len(demean)) * sr  # Real Frequency --> Real numbers
    # Normalize the spectral amplitude
    xf1 = freqs
    yf1 = np.abs(fft_signal)
    area1 = np.trapz(yf1, xf1)
    y_nor1 = yf1 / area1
    xf_all.append(xf1)
    yf_all.append(y_nor1)
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
    ti = t_on[s]
    tf = t_off[s]
    events_data.append(data1[ti:tf])
    events_time.append(time[ti:tf])
    d_bef.append(data1[ti - 10000:tf + 10000])
    t_bef.append(time[ti - 10000:tf + 10000])
print(len(t_on))
r = len(events_data)
for pl in range (0,r,1):
    plot_event(tr, events_data[pl], events_time[pl], t_bef[pl], d_bef[pl], xf_all[pl], yf_all[pl], FI[pl], RMS[pl], pl, save=True)














# # ---------------------------- Lastest Version of Event Plotting With the Normalized Amplitude ----------------------------------------
# def plot_event(trace, event, t_event, t_bef, d_bef, xf, yf, FI,RMS, s,
#                save=True):  # event is the data for one event, t_event is the time,  t_bef is the time before the event to get the whole picture, d_bef data before the event,thr_on the threshold for sta lta t0n, t0ff, thr_off
#     import matplotlib.pyplot as plt  # yf is the normalized yabs resulted from rrft
#     label1 = trace.stats.starttime.isoformat()  #
#     label2 = trace.id
#     width1 = 15
#     height1 = 9
#     fig, axs = plt.subplots(2, 1, figsize=(width1, height1), gridspec_kw={'height_ratios': [4, 2]})
#     axs[0].plot(xf, yf, 'k')
#     axs[0].set_xlabel('Frequency [Hz]')
#     axs[0].set_ylabel('Normalized Amplitude')
#     axs[1].plot(t_bef, d_bef, 'k')
#     axs[1].plot(t_event, event, 'b', label='Event')
#     i, j = axs[1].get_ylim()
#     try:
#         axs[1].vlines(t_event[0], i, j, color='r', lw=2,
#                       label="Event start", linestyles='dashed')
#         axs[1].vlines(t_event[-1], i, j, color='b', lw=2,
#                       label="Event end", linestyles='dashed')
#     except IndexError:
#         pass
#     axs[1].set_xlabel('Time [seconds * sample rate]')
#     axs[1].set_ylabel('Amplitude')
#     fig.suptitle("Station ID:%s\n" % label2 + "\nDate:%s" % label1)
#     textstr = '\n'.join((
#         r'$\mathrm{FI}=%.2f$' % (FI,),
#         r'$\mathrm{Ton}=%.2f$' % (t_event[0],),
#         r'$\mathrm{Toff}=%.2f$' % (t_event[-1],),
#         r'$\mathrm{RMS}=%.2f$' % (RMS,)))
#     axs[0].text(1.01, 0.95, textstr, transform=axs[0].transAxes, fontsize=10, verticalalignment='top')
#     if save:
#         #plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/Event_{}.pdf'.format([s]))
#         plt.show()
#
# import os
# os.chdir('C:/Users/HP/Desktop/Geology of Ecuador/BB4')
# from scipy.fft import rfft, rfftfreq
# from obspy.signal.invsim import cosine_taper
# from Thesis_3_4 import t_on_off, sta_lta, plot_STA_LTA
# from obspy import read
# import numpy as np
#
# file = 'Copia de 8E.BB4.HHZ.20150301.mseed'
# st = read(file)
# st.detrend(type='demean')
# st.detrend(type='linear')
# st.taper(type="cosine", max_percentage=0.05)
# st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
# st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
# st1 = st.copy()
# st.filter('lowpass', freq=10, zerophase=True)  # These filters are applied to get the STA ratio
# st.filter('highpass', freq=0.2, zerophase=True)
# tr = st[0]
# data1 = np.array(tr.data)
# npts = tr.stats.npts
# sr = tr.stats.sampling_rate
# time = np.arange(npts, dtype=np.float32) / sr
# nsta = int(1 * sr)
# nlta = int(7 * sr)
# sta = sta_lta(data1, nsta, nlta)  # STA/LTA ratio
# tOn = 3
# tOff = 0.2
# triggers = t_on_off(sta, tOn, tOff)
# t_on = triggers[:, 0]
# t_off = triggers[:, 1]
# tr = st1[0]
# data = np.array(tr.data)
# npts = tr.stats.npts
# sr = tr.stats.sampling_rate
# time = np.arange(npts, dtype=np.float32) / sr
# window = 500  # window of 5 seconds
# FI = []
# events_data = []
# events_time = []
# t_bef, d_bef = [], []
# xf_all, yf_all = [], []
# staevent = []
# RMS = []
# center_freq = []
# peak_freq = []
# for s in range(0,len(t_on), 1):
#     rms_amplitude = np.sqrt(np.mean(data[t_on[s]:t_off[s]] ** 2))
#     RMS.append(rms_amplitude)
#     # -----------Peak Frequency-----------
#     edata = data[t_on[s]:t_off[s]]
#     yf = rfft(edata)
#     xf = rfftfreq(len(edata)) * sr  # Real Frequency --> Real numbers
#     yfabs = np.abs(yf)
#     p1 = 0.1  # 10%
#     tap1 = cosine_taper(len(yfabs), p1)  # Taper for the frequency domain
#     tap1_freq = yfabs * tap1
#     pf_index = np.argmax(tap1_freq)
#     peak_freq.append(xf[pf_index])
#     # ----------Center Frequency----------
#     e = np.array(yfabs)
#     tem = []
#     for i in range(0, len(yfabs), 1):
#         c = np.abs(sum(e[i + 1:len(e)]) - sum(e[0:i]))
#         tem.append(c)
#     temp = np.array(tem)
#     cf_index = np.argmin(temp)
#     center_freq.append(xf[cf_index])
#     # ----------Frequency Index-----------
#     Alower = e[int(min(xf, key=lambda x: abs(x - 0))):int(min(xf, key=lambda x: abs(x - 3))) + 1]
#     Aupper = e[int(min(xf, key=lambda x: abs(x - 7))):int(min(xf, key=lambda x: abs(x - 10))) + 1]
#     Fi = np.log10(np.mean(Aupper) / np.mean(Alower))
#     FI.append(Fi)
#     ti = t_on[s]
#     tf = t_off[s]
#     events_data.append(data1[ti:tf])
#     events_time.append(time[ti:tf])
#     d_bef.append(data1[ti - 5000:tf + 5000])
#     t_bef.append(time[ti - 5000:tf + 5000])
#
# r = len(events_data)
# for pl in range (1,r,1):
#     plot_event(tr, events_data[pl], events_time[pl], t_bef[pl], d_bef[pl], xf_all[pl], yf_all[pl], FI[pl], RMS[pl], pl, save=True)
#

#=====================================================================================================

#
#
# # ---------------------------- Lastest Version of Event Plotting With the Normalized Amplitude ----------------------------------------
# def plot_event(trace, event, t_event, t_bef, d_bef, xf, yf, FI,RMS, s,
#                save=True):  # event is the data for one event, t_event is the time,  t_bef is the time before the event to get the whole picture, d_bef data before the event,thr_on the threshold for sta lta t0n, t0ff, thr_off
#     import matplotlib.pyplot as plt  # yf is the normalized yabs resulted from rrft
#     label1 = trace.stats.starttime.isoformat()  #
#     label2 = trace.id
#     width1 = 15
#     height1 = 9
#     fig, axs = plt.subplots(2, 1, figsize=(width1, height1), gridspec_kw={'height_ratios': [4, 2]})
#     axs[0].plot(xf, yf, 'k')
#     axs[0].set_xlabel('Frequency [Hz]')
#     axs[0].set_ylabel('Normalized Amplitude')
#     axs[1].plot(t_bef, d_bef, 'k')
#     axs[1].plot(t_event, event, 'b', label='Event')
#     i, j = axs[1].get_ylim()
#     try:
#         axs[1].vlines(t_event[0], i, j, color='r', lw=2,
#                       label="Event start", linestyles='dashed')
#         axs[1].vlines(t_event[-1], i, j, color='b', lw=2,
#                       label="Event end", linestyles='dashed')
#     except IndexError:
#         pass
#     axs[1].set_xlabel('Time [seconds * sample rate]')
#     axs[1].set_ylabel('Amplitude')
#     fig.suptitle("Station ID:%s\n" % label2 + "\nDate:%s" % label1)
#     textstr = '\n'.join((
#         r'$\mathrm{FI}=%.2f$' % (FI,),
#         r'$\mathrm{Ton}=%.2f$' % (t_event[0],),
#         r'$\mathrm{Toff}=%.2f$' % (t_event[-1],),
#         r'$\mathrm{RMS}=%.2f$' % (RMS,)))
#     axs[0].text(1.01, 0.95, textstr, transform=axs[0].transAxes, fontsize=10, verticalalignment='top')
#     if save:
#         plt.savefig('C:/Users/HP/Desktop/Thesis Project/FIGURES/Event_{}.pdf'.format([s]))
#
# import os
# os.chdir('C:/Users/HP/Desktop/Geology of Ecuador/BB4')
# from scipy.fft import rfft, rfftfreq
# from obspy.signal.invsim import cosine_taper
# from Thesis_3_4 import t_on_off, sta_lta, plot_STA_LTA
# from obspy import read
# import numpy as np
#
# file = 'Copia de 8E.BB4.HHZ.20150301.mseed'
# st = read(file)
# st.detrend(type='demean')
# st.detrend(type='linear')
# st.taper(type="cosine", max_percentage=0.05)
# st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
# st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
# st1 = st.copy()
# st.filter('lowpass', freq=10, zerophase=True)  # These filters are applied to get the STA ratio
# st.filter('highpass', freq=0.2, zerophase=True)
# tr = st[0]
# data1 = np.array(tr.data)
# npts = tr.stats.npts
# sr = tr.stats.sampling_rate
# time = np.arange(npts, dtype=np.float32) / sr
# nsta = int(1 * sr)
# nlta = int(7 * sr)
# sta = sta_lta(data1, nsta, nlta)  # STA/LTA ratio
# tOn = 3
# tOff = 0.2
# triggers = t_on_off(sta, tOn, tOff)
# t_on = triggers[:, 0]
# t_off = triggers[:, 1]
# tr = st1[0]
# data = np.array(tr.data)
# npts = tr.stats.npts
# sr = tr.stats.sampling_rate
# time = np.arange(npts, dtype=np.float32) / sr
# window = 500  # window of 5 seconds
# FI = []
# events_data = []
# events_time = []
# t_bef, d_bef = [], []
# xf_all, yf_all = [], []
# staevent = []
# RMS = []
# for s in range(10,20, 1):
#     rms_amplitude = np.sqrt(np.mean(data[t_on[s]:t_off[s]] ** 2))
#     RMS.append(rms_amplitude)
#     # ---------- Frequency Domain -------------
#     ti = t_on[s]
#     tf = t_off[s]
#     N = int((tf - ti))  # Number of data points
#     p1 = 0.1  # 10%
#     tap = cosine_taper(N, p1)  # Taper for the time domain
#     demean = data[ti:tf] - np.mean(data[ti:tf])
#     tap_data = demean * tap
#     yf = rfft(tap_data)
#     xf = rfftfreq(len(tap_data)) * sr  # Real Frequency --> Real numbers
#     yfabs = np.abs(yf)
#     e = np.array(yfabs)
#     xf1 = xf
#     yf1 = yfabs
#     area1 = np.trapz(yf1, xf1)
#     y_nor1 = yf1 / area1
#     xf_all.append(xf1)
#     yf_all.append(y_nor1)
#     # ----------Frequency Index-----------
#     Alower = e[int(min(xf, key=lambda x: abs(x - 0))):int(min(xf, key=lambda x: abs(x - 3))) + 1]
#     Aupper = e[int(min(xf, key=lambda x: abs(x - 7))):int(min(xf, key=lambda x: abs(x - 10))) + 1]
#     Fi = np.log10(np.mean(Aupper) / np.mean(Alower))
#     FI.append(Fi)
#     events_data.append(data1[ti:tf])
#     events_time.append(time[ti:tf])
#     d_bef.append(data1[ti - 5000:tf + 5000])
#     t_bef.append(time[ti - 5000:tf + 5000])
#
# r = len(events_data)
# for pl in range (1,r,1):
#     plot_event(tr, events_data[pl], events_time[pl], t_bef[pl], d_bef[pl], xf_all[pl], yf_all[pl], FI[pl], RMS[pl], pl,save = True )


import os
os.chdir('C:/Users/HP/Desktop/Geology of Ecuador/Classification')
from scipy.fft import rfft, rfftfreq
from obspy import read
import numpy as np
import matplotlib.pyplot as plt

HF = []
file = '8E.BB3.HHZ.20140811.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
for elem in data[6920978:6921897]:
    HF.append(elem)
for elem in data[7244214:7245293]:
    HF.append(elem)
for elem in data[6771021:6773621]:
    HF.append(elem)
file = '8E.BB4.HHZ.20150307.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
for elem in data[6067586:6068398]:
    HF.append(elem)
for elem in data[7914503:7918238]:
    HF.append(elem)

HYB = []
file = '8E.BB4.HHZ.20150426.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
for elem in data[7356334:7357083]:
    HYB.append(elem)
for elem in data[5050209:5056271]:
    HYB.append(elem)
for elem in data[2805372:2816293]:
    HYB.append(elem)

file = '8E.BB4.HHZ.20150309.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
for elem in data[6178726:6181958]:
    HYB.append(elem)
for elem in data[6186483:6187489]:
    HYB.append(elem)

LF = []
file = '8E.BB4.HHZ.20150427.mseed'
st = read(file)
st.detrend(type='demean')
st.detrend(type='linear')
st.taper(type="cosine", max_percentage=0.05)
st.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
st.filter('highpass', freq=1 / 60 / 60, zerophase=True)
tr = st[0]
data = np.array(tr.data)
for elem in data[5422433:5423798]:
    LF.append(elem)
for elem in data[3311375:3312674]:
    LF.append(elem)
for elem in data[1636508:1637551]:
    LF.append(elem)
for elem in data[4804382:4805413]:
    LF.append(elem)
for elem in data[5016615:5017546]:
    LF.append(elem)


demean = HF - np.mean(HF)
fft_signal = rfft(demean)
freqs = rfftfreq(len(demean)) * sr  # Real Frequency --> Real numbers
xfHF = freqs
yfHF = np.abs(fft_signal)
areaHF = np.trapz(yfHF, xfHF)
y_norHF = yfHF / areaHF

demean = LF - np.mean(LF)
fft_signal = rfft(demean)
freqs = rfftfreq(len(demean)) * sr  # Real Frequency --> Real numbers
xfLF = freqs
yfLF = np.abs(fft_signal)
areaLF = np.trapz(yfLF, xfLF)
y_norLF = yfLF / areaLF

demean = HYB - np.mean(HYB)
fft_signal = rfft(demean)
freqs = rfftfreq(len(demean)) * sr  # Real Frequency --> Real numbers
xfHYB = freqs
yfHYB = np.abs(fft_signal)
areaHYB = np.trapz(yfHYB, xfHYB)
y_norHYB = yfHYB / areaHYB

plt.plot(xfHYB, y_norHYB, label='Hybrid', lw = 0.3, color ='k')
plt.plot(xfLF, y_norLF, label='Low Frequency', lw = 0.3, color ='r')
plt.plot(xfHF, y_norHF, label='High Frequency', lw = 0.3, color ='b')
plt.legend()
plt.show()
