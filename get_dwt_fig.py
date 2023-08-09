import pickle
import pandas as pd
import numpy as np
import pywt
import plotly.graph_objects as go


def normalize_data(x):
    return (x - np.mean(x)) / np.std(x)


def calcular_fft(x):
    x = x * np.hamming(len(x))
    return np.abs(np.fft.rfft(x))


def calculatr_frequencia_fundamental(x):
    max_loc = np.argmax(np.abs(np.fft.rfft(x)))
    return max_loc


# aplicar a transformada de wavelet nos dados das bombas e calcular a energia do sinal (10 níveis)
def calc_energia_wavelet(x):
    # x = x*np.hanning(len(x))
    coeffs = pywt.wavedec(
        x, "db10", mode="smooth"
    )  # sempre usar o nível máximo #, level=9)
    w = pywt.Wavelet("db10")
    return np.array(
        [np.sum(coef[w.dec_len: -w.dec_len] ** 2) for coef in coeffs]
    ) / len(x)


def get_fig_dwt(bomba, corrente_ml, std_mult=1):
    dbfile = open(
        "references_dwt.pickle",
        "rb",
    )
    references = pickle.load(dbfile)
    dbfile.close()

    references = pd.DataFrame(references)

    fund_loc = calculatr_frequencia_fundamental(corrente_ml)

    sel_batch = references[
        (
            (references["freq_princ"] == fund_loc)
            & (references["ativo"] == bomba)
        )
    ]

    if len(sel_batch) == 0:
        return None

    fft_mean = sel_batch["fft_media"].iloc[0]
    fft_std = sel_batch["fft_std"].iloc[0]

    fft_input = calc_energia_wavelet(normalize_data(corrente_ml))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(len(fft_mean)),
            y=fft_input,
            mode="lines",
            name="entrada",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=np.arange(len(fft_mean)),
            y=fft_mean + std_mult * fft_std,
            mode="lines",
            name="limite",
        )
    )

    return fig
