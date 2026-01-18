# Capstone_Project

'Volcanic event characterization using seismic signals: An example from Lascar Volcano, Chile'
Amplitude, Frequency and time domain analysis of seismic signals. Description and calculation of nine parameters to determine the characteristics of different waveforms.

As a general structure:
1. Data processing
2. STA/LTA Method
3. Seismic signal identification
4. Event classification
5. Noise awareness and Swarm detection
6. Volcano-tectonic events location

The input data is MSEED collected from six stations at different locations, some of the data has a sample rate of 200 Hz so I will downsample it and then apply a bandpass filter (Data Prosessing). As a result I'll get data of 100Hz for all stations.

STA/LTA Method> this ratio will recognize abrupt changes in the amplitude of the wavelength comparing a small window (STA) over alarge window (LTA), the anomalous value should ecxeeds an stblished threshold. This ratio is necessary to identify possible volcano-related seismic events.

Seismic signal identification> To identify volcano-seismic signals and diferenciate them from tectonic events I will use nine metrics:
1. Temporal metrics> event length, time between events (gap), and event rate.
2. Amplitude metrics> maximum amplitude, phase amplitude, and Root-Mean-Square Amplitude (RMSa)
3. Spectral metrics> maximum frequency, center frequency, and Frequency Index (FI) 

Event Classification> to classify volcanic seismic signals into Volcano Tectonic (VT), Long Period events (LP), Hybrid events (HYB), or Explosion earthquakes (EXP) I will use RMSa and FI metrics. 
I separated a group of data as a calibration set (manual classification). This will help us to stablish a threshold for event identification during the automatication of event classification. The computation of the mean, standard deviation, and cluster analysis are vital to get the breakpoints for RMSa and FI values.

Noise and Swarms> I will compare the data from all stations to gather all possible sources of noise, remove it, and enhance the data quality. To achieve it I'll use RMSa, Maximum Frequency, Phase amplitude, Center Frequency, Event Length, and FI. The set of events recorded at least in three stations will be considered as true volcanic events. On the other hand, I'll use Event Rate metric to identify earthquake swarms.

VT Events Location> The aim is apply Grid Method described by (Gottschämmer & Surono, 2000) which consist on establish a grid over the study location and set the parameters to calculate at each point of the grid (Assuming isotropic radiation and Vp constant), the resolution of the location estimation will depend on the separation of each grid point. In order to apply the grid method I need to calculate the distance between stations and each gridpoint, and the source time (tHmn). The source time can be obtained from the calculation of the arrival time (tarr) minus the ratio betweeen the location matrix (Dmn) over the velocity of the medium (Vguess)
tHmn = tarr[s] - Dmn[m] / Vguess[m/s]
The tarr variable is the time at which the event start and Dmn can be calculated using the formula 'Distance between two points' over a sphere (Haversine formula). Vguess can only be estimated to do that I will try different velocities. I have to calculate the velocity (distance (Dmn) over time (tarr)) and then calculate the standard deviation of each point of that velocity matrix. At the end, the source location will be chosen as the grid point with the minimum standard deviation value for that Vguess  


