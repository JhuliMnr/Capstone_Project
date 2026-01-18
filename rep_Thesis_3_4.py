from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from collections import deque
import numpy as np
from obspy.signal.headers import clibsignal


def sta_lta(data, nsta, nlta):
    data = np.ascontiguousarray(data, np.float64)
    ndat = len(data)
    stalta = np.empty(ndat, dtype=np.float64)
    clibsignal.recstalta(data, stalta, ndat, nsta, nlta)
    return stalta

def t_on_off(charfct, thres1, thres2, max_len=9e99, max_len_delete=False):
    ind1 = np.where(charfct > thres1)[0]
    if len(ind1) == 0:
        return []
    ind2 = np.where(charfct > thres2)[0]
    on = deque([ind1[0]])
    of = deque([-1])
    ind2_ = np.empty_like(ind2, dtype=bool)
    ind2_[:-1] = np.diff(ind2) > 1
    ind2_[-1] = True
    of.extend(ind2[ind2_].tolist())
    on.extend(ind1[np.where(np.diff(ind1) > 1)[0] + 1].tolist())
    if max_len_delete:
        of.extend([1e99])
        on.extend([on[-1]])
    else:
        of.extend([ind2[-1]])
    pick = []
    while on[-1] > of[0]:
        while on[0] <= of[0]:
            on.popleft()
        while of[0] < on[0]:
            of.popleft()
        if of[0] - on[0] > max_len:
            if max_len_delete:
                on.popleft()
                continue
            of.appendleft(on[0] + max_len)
        pick.append([on[0], of[0]])
    return np.array(pick, dtype=np.int64)

def plot_STA_LTA(trace, cft, thr_on, thr_off, show=True): #plot_STA_LTA(tr, sta, tOn, tOff)
    import matplotlib.pyplot as plt
    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    label1 = trace.stats.starttime.isoformat()
    label2 = trace.id
    t = np.arange(npts, dtype=np.float32) / df
    width1 = 10
    height1 = 6
    width_height_1 = (width1, height1)
    fig = plt.figure(figsize=width_height_1)
    ax1 = fig.add_subplot(211)
    ax1.plot(t, trace.data, 'k')
    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2.plot(t, cft, 'k')
    ax2.set_xlabel("Time [seconds]")
    on_off = np.array(t_on_off(cft, thr_on, thr_off))
    i, j = ax1.get_ylim()
    ax1.set_ylabel('Amplitude')
    try:
        ax1.vlines(on_off[:, 0] / df, i, j, color='r', lw=2, linestyles='dashed')
        ax1.vlines(on_off[:, 1] / df, i, j, color='b', lw=2, linestyles='dashed')
    except IndexError:
        pass
    ax2.axhline(thr_on, color='red', lw=1, ls='--')
    ax2.axhline(thr_off, color='blue', lw=1, ls='--')
    ax2.set_ylabel('STA/LTA Ratio')
    fig.suptitle("Station ID:%s\n" % label2 + "\nDate:%s" % label1)
    if show:
        plt.savefig('C:/Users/HP/Desktop/Thesis Project/stalta_plot.svg')
        plt.show()
if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
#
from scipy.signal import butter, lfilter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
def plot_event(trace, t_on, t_off, event,t_event,t_bef,data_bef,FI,peakfreq,centerfreq,duration,interevent,peakamp,peak2peak,show=True):
    import matplotlib.pyplot as plt
    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    label1 = trace.stats.starttime.isoformat()
    label2 = trace.id
    t = np.arange(npts, dtype=np.float32) / df
    width1 = 15
    height1 = 6
    width_height_1 = (width1, height1)
    fig = plt.figure(figsize=width_height_1)
    ax1 = fig.add_subplot(311)
    on = t_on/df
    off = t_off/df
    ax1.plot(t, trace.data, 'k', label='Raw data')
    ax1.legend(loc='lower right')
    ax2 = fig.add_subplot(312, sharex=ax1)
    trace.detrend(type='demean')
    trace.detrend(type='linear')
    trace.taper(type="cosine", max_percentage=0.05)
    trace.filter('lowpass', freq=0.4 * 100, zerophase=True)  # anti-alias filter
    trace.filter('highpass', freq=1 / 60 / 60, zerophase=True)
    ax2.plot(t,trace.data, 'k', label='Filtered data')
    ax2.set_xlabel("[seconds]")
    ax3 = fig.add_subplot(313)
    ax3.plot(t_bef,data_bef,'k')
    ax3.plot(t_event, event,'b',label='Event')
    i, j = ax3.get_ylim()
    try:
        ax3.vlines(t_event[0], i, j, color='r', lw=2,
                   label="Event start", linestyles='dashed')
        ax3.vlines(t_event[-1], i, j, color='b', lw=2,
                   label="Event end", linestyles='dashed')
    except IndexError:
        pass
    i, j = ax2.get_ylim()
    try:
        ax2.vlines(on, i, j, color='r', lw=2,
                   label="Event start", linestyles='dashed')
        ax2.vlines(off, i, j, color='b', lw=2,
                   label="Event end", linestyles='dashed')
        ax2.legend(loc='upper right')
    except IndexError:
        pass
    fig.suptitle("Station ID:%s\n" % label2 + "\nDate:%s" % label1)
    if FI > -0.4:
        textstr = '\n'.join((
        r'$\mathrm{FI}=%.2f$' % (FI, ),
        r'$\mathrm{PF}=%.2f$' % (peakfreq, ),
        r'$\mathrm{CF}=%.2f$' % (centerfreq, ), # duration,interevent,peakamp,peak2peak,rmsa
        r'$\mathrm{dur}=%.2f$' % (duration , ),
        r'$\mathrm{ITime}=%.2f$' % (interevent, ),
        r'$\mathrm{PAmp}=%.2f$' % (peakamp, ),
        r'$\mathrm{P2P}=%.2f$' % (peak2peak, ),
        r'VT event'))
        ax3.text(1.01, 0.95, textstr, transform=ax3.transAxes, fontsize=10, verticalalignment='top')
    if FI < -1.3 :
        textstr = '\n'.join((
        r'$\mathrm{FI}=%.2f$' % (FI, ),
        r'$\mathrm{PF}=%.2f$' % (peakfreq, ),
        r'$\mathrm{CF}=%.2f$' % (centerfreq, ),
        r'$\mathrm{dur}=%.2f$' % (duration , ),
        r'$\mathrm{ITime}=%.2f$' % (interevent, ),
        r'$\mathrm{PAmp}=%.2f$' % (peakamp, ),
        r'$\mathrm{P2P}=%.2f$' % (peak2peak, ),
        r'LF event'))
        ax3.text(1.01, 0.95, textstr, transform=ax3.transAxes, fontsize=10, verticalalignment='top')
    if FI < -0.4 and FI > -1.3 :
        textstr = '\n'.join((
        r'$\mathrm{FI}=%.2f$' % (FI, ),
        r'$\mathrm{PF}=%.2f$' % (peakfreq, ),
        r'$\mathrm{CF}=%.2f$' % (centerfreq, ),
        r'$\mathrm{dur}=%.2f$' % (duration , ),
        r'$\mathrm{ITime}=%.2f$' % (interevent, ),
        r'$\mathrm{PAmp}=%.2f$' % (peakamp, ),
        r'$\mathrm{P2P}=%.2f$' % (peak2peak, ),
        r'HYB event'))
        ax3.text(1.01, 0.95, textstr, transform=ax3.transAxes, fontsize=10, verticalalignment='top')
    if FI  < -1.8:
        textstr = '\n'.join((
        r'$\mathrm{FI}=%.2f$' % (FI, ),
        r'$\mathrm{PF}=%.2f$' % (peakfreq, ),
        r'$\mathrm{CF}=%.2f$' % (centerfreq, ),
        r'$\mathrm{dur}=%.2f$' % (duration , ),
        r'$\mathrm{ITime}=%.2f$' % (interevent, ),
        r'$\mathrm{PAmp}=%.2f$' % (peakamp, ),
        r'$\mathrm{P2P}=%.2f$' % (peak2peak, ),
        r'EXP event'))
        ax3.text(1.01, 0.95, textstr, transform=ax3.transAxes, fontsize=10, verticalalignment='top')
    if show:
        plt.show()
