import streamlit as st
from numpy import *
from matplotlib.pyplot import *
import soundfile

def sp_audio(np_array, samplerate=44100):
    soundfile.write('temp.wav', np_array/3, samplerate)
    st.audio('temp.wav')

st.title('Signal-to-Noise Ratio (audio)')
snr=st.slider('SNR (dB)): ', -10.0, 40.0, 40.0)

signal,fe = soundfile.read('par8.wav')

t=arange(0,len(signal))/fe;
signal_power_dB=10*log10(var(signal)) #-14,4dB
noise = random.normal(0, 1, signal.shape)
noise_power_dB=10*log10(var(noise))   #0dB
SNR_dB=signal_power_dB-noise_power_dB #76dB
#Create a noisy signal with de SNR of x dB = increase the noise power by (76-x)dB
noise_ampl=noise*sqrt(10**((-14.4-snr)/10.0))
signal_plus_noise=signal+noise_ampl

sp_audio(signal_plus_noise,fe)

fig,ax=subplots(figsize=(10,4))
plot(t,signal_plus_noise);
xlabel('time [s]')
title('signal + noise');
text(0.5,0.75,'SNR [dB]='+str(around(snr,2)),fontsize='xx-large')
st.pyplot(fig)

with st.expander("Open for comments"):
   st.markdown('''SNR is defined as the ratio of the power of a signal to that of the additional 
               noise: ''')
   st.latex('''SNR = \sigma_x^2 / \sigma_n^2 ''')
   st.markdown('''or, in deciblels:''')
   st.latex('''SNR [dB]= 10 \ \log10(\sigma_x^2 / \sigma_n^2) ''')
   st.markdown('''The _SNR_ imposed above is obtained by measuring the power of the input speech, 
               and adding noise with unity power (i.e., 0 dB), multiplied by an amplitude 
               factor $\sigma_n$: ''')
   st.latex('''\sigma_n = \sqrt{\sigma_x^2 / SNR} ''')
   st.markdown('''After playing with the _SNR_ slider, it is clear that noise can be quickly seen 
   and heard when _SNR_ <40''')
