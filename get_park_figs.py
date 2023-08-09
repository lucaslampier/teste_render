import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def normalize_data(x):
    return (x - np.mean(x))/np.std(x)

def calcular_fft(x):
    x = x*np.hamming(len(x))
    return np.abs(np.fft.rfft(x))

def calculatr_frequencia_fundamental(x):
    max_loc = np.argmax(np.abs(np.fft.rfft(x)))
    return max_loc

def calcular_iq_id(df):
    df["iD"] = (np.sqrt(2)/np.sqrt(3))*df["ae_corrente_l1"] - (np.sqrt(6))*df["ae_corrente_l2"] - (np.sqrt(6))*df["ae_corrente_l3"]
    df["iQ"] = (np.sqrt(2))*df["ae_corrente_l2"] - (np.sqrt(2))*df["ae_corrente_l3"]
    return df


def pol2cart(r,theta):
    '''
    Parameters:
    - r: float, vector amplitude
    - theta: float, vector angle
    Returns:
    - x: float, x coord. of vector end
    - y: float, y coord. of vector end
    '''

    z = r * np.exp(1j * theta)
    x, y = z.real, z.imag

    return x, y

def cart2pol(x, y):
    '''
    Parameters:
    - x: float, x coord. of vector end
    - y: float, y coord. of vector end
    Returns:
    - r: float, vector amplitude
    - theta: float, vector angle
    '''

    z = x + y * 1j
    r,theta = np.abs(z), np.angle(z)

    return r,theta

def get_mean_circle(df):
    # df = sinal_ae

    rs = []
    thetas = []
    for i in range(len(df)):
        # transformar de coordenadas retangulares para polares
        r,theta = cart2pol(df['iD'],df['iQ'])

        # ordenar os dados de acordo com o angulo
        order = np.argsort(theta)
        theta = theta[order]
        r = r[order]
        
        if ((theta[0] < -3.1) and (theta[-1] > 3.1)):
            thetas.append(theta)
            rs.append(r)
        
    thetas = np.array(thetas)
    rs = np.array(rs)

    return pol2cart(np.mean(rs,axis=0), np.mean(thetas,axis=0))


def get_park_figures(bomba, sinal_ae):
    dbfile = open('references_park.pickle', 'rb')
    # source, destination
    circulos = pickle.load(dbfile)                   
    dbfile.close()
    
    mean = np.mean(sinal_ae['ae_corrente_l1'])
    std = np.std(sinal_ae['ae_corrente_l1'])
    
    sinal_ae['ae_corrente_l1'] = sinal_ae['ae_corrente_l1']
    sinal_ae['ae_corrente_l2'] = sinal_ae['ae_corrente_l2']
    sinal_ae['ae_corrente_l3'] = sinal_ae['ae_corrente_l3']
    
    sinal_ae['ae_corrente_l1'] = (sinal_ae['ae_corrente_l1'] - mean)/std
    sinal_ae['ae_corrente_l2'] = (sinal_ae['ae_corrente_l2'] - mean)/std
    sinal_ae['ae_corrente_l3'] = (sinal_ae['ae_corrente_l3'] - mean)/std
    
    sinal_ae = calcular_iq_id(sinal_ae)

    # calcular o circulo de park médio do batch
    x,y = get_mean_circle(sinal_ae)    
    
    fig = go.Figure()
    # fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=circulos[bomba]['iD'],#df['iD'].iloc[i],
            y=circulos[bomba]['iQ'],#df['iQ'].iloc[i],
            mode='lines',
            name='referência'
            )
        )
    
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='Sinal atual'
            )
        )
    
    fig.update_layout(title = bomba)
    fig.update_layout(yaxis_range=[-5,5])
    fig.update_layout(xaxis_range=[-5,5])
    fig.update_layout(width=800)
    fig.update_layout(height=800)
    # fig.show()
    return fig
    