import numpy as np
import pickle
import pandas as pd

def normalize_data(x):
    return (x - np.mean(x))/np.std(x)

def calcular_fft(x):
    x = x*np.hamming(len(x))
    return np.abs(np.fft.rfft(x))

def calculatr_frequencia_fundamental(x):
    max_loc = np.argmax(np.abs(np.fft.rfft(x)))
    return max_loc

def processar_corrente(bomba, corrente_ml, std_mult = 2):
    fund_freq = calculatr_frequencia_fundamental(corrente_ml)
    sinal_norm = normalize_data(corrente_ml)
    fft_ml = calcular_fft(sinal_norm)
    
    dbfile = open('references_fft.pickle', 'rb')
    references = pickle.load(dbfile)                   
    dbfile.close()
    references = pd.DataFrame(references)

    sel_batch = references[(
        (references['freq_princ'] == fund_freq) &
        (references['ativo'] == bomba)
    )]

    fft_mean = sel_batch['fft_media'].iloc[0]
    fft_std = sel_batch['fft_std'].iloc[0]

    return fft_ml, (fft_mean + std_mult*fft_std)