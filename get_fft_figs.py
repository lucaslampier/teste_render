import pandas as pd
import pickle

import plotly.graph_objects as go
import numpy as np
from process_data_fft import processar_corrente

def get_fft_reference(bomba, corrente_ml, std_mult=2):
    fft_input, fft_referencia = processar_corrente(bomba, corrente_ml, std_mult)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                        x=np.arange(len(fft_input))*8/18,
                        y=20*np.log10(fft_input),
                        mode='lines',
                        name='FFT da corrente normalizada',
                        line=dict(color='blue')),
                    )
    
    fig.add_trace(go.Scatter(
                        x=np.arange(len(fft_referencia))*8/18,
                        y=20*np.log10(fft_referencia),
                        mode='lines',
                        name='Limite superior',
                        line=dict(color='red')),
                    )
    return fig
        
        
def main():
    fig = get_fft('Piranema_Bomba_B3')
    fig.show()

if __name__ == '__main__':
    main()