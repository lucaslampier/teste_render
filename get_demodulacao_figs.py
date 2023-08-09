import pickle
import pandas as pd
import numpy as np
from hilbert import hilbert
import plotly.graph_objects as go

def normalize_data(x):
    return (x - np.mean(x))/np.std(x)

def calcular_fft(x):
    x = x*np.hamming(len(x))
    return np.abs(np.fft.rfft(x))

def calculatr_frequencia_fundamental(x):
    max_loc = np.argmax(np.abs(np.fft.rfft(x)))
    return max_loc

def demodulate_signal_hilbert(x, fs):
    z= hilbert(x) #form the analytical signal from the received vector
    inst_phase = np.unwrap(np.angle(z))#instaneous phase

    t = np.arange(len(inst_phase))/fs
    p = np.poly1d(np.polyfit(t,inst_phase,1)) #linearly fit the instaneous phase
    estimated = p(t) #re-evaluate the offset term using the fitted values
    offsetTerm = estimated
    
    demodulated = inst_phase - offsetTerm 
    
    return demodulated

def fft_demod(x,fs):
    return(calcular_fft(demodulate_signal_hilbert(x, fs)))

def get_demod_fig(bomba, corrente_ml, std_mult = 1):
    dbfile = open('references_demodulado.pickle', 'rb')
    # source, destination
    references = pickle.load(dbfile)                   
    dbfile.close()
    
    references = pd.DataFrame(references)
    
    fund_loc = calculatr_frequencia_fundamental(corrente_ml)
    
    sel_batch = references[(
        (references['freq_princ'] == fund_loc) &
        (references['ativo'] == bomba)
    )]
    
    if len(sel_batch) == 0:
        return None
    
    fft_mean = sel_batch['fft_media'].iloc[0]
    fft_std = sel_batch['fft_std'].iloc[0]
    
    fft_input = fft_demod(normalize_data(corrente_ml), 8000)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(fft_mean))*8/18, 
                        y=20*np.log10(fft_input),
                        mode='lines',
                        name='entrada'))
    fig.add_trace(go.Scatter(
                        x=np.arange(len(fft_mean))*8/18, 
                        y=20*np.log10(fft_mean + std_mult*fft_std),
                        mode='lines',
                        name='limite'))

    # fig.show()
    
    return fig