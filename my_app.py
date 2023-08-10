# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import pandas as pd
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_auth
from flask import Flask,request
import numpy as np
import plotly.graph_objects as go


from get_fft_figs import get_fft_reference
from get_park_figs import get_park_figures
from get_demodulacao_figs import get_demod_fig
from get_dwt_fig import get_fig_dwt



roxo_claro = "#753BBD"
roxo_escuro = "#4E008E"
cinza_claro = "#DDDAE8"


VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'admin'
}


novos_dados = {}
for bomba in ["Piranema_Bomba_B3", "Piranema_Soprador_S3", "Araras_Bomba_B1"]:
    dado_ae = pd.read_parquet(
        bomba + r"_2023-06-30 00:00:00_2023-07-01 00:00:00_ae.parquet"
    )
    dado_ml = pd.read_parquet(
        bomba + r"_2023-06-30 00:00:00_2023-07-01 00:00:00_ml.parquet"
    )
    novos_dados[bomba] = {}
    novos_dados[bomba]["ae"] = dado_ae.iloc[-1]
    novos_dados[bomba]["ml"] = dado_ml.iloc[-1][0]


# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dbc.themes.COSMO]  # [dmc.theme.DEFAULT_COLORS]

flask_server = Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    server=flask_server
)

server = app.server


@flask_server.route('/receive-data', methods=['POST'])
def receive_data():
    print(request.data.decode())
    # data = request.json  # Dados recebidos via POST em formato JSON
    # print(data)
    return 'Dados recebidos com sucesso!'




# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

titulo_principal = dmc.Title(
    "Central de monitoramento 2Neuron",
    color=roxo_escuro,
    size="h1",
    align="center",
)


selecionar_bomba = dmc.Select(
            label="Select framework",
            placeholder="Select one",
            id="selecionar_bomba",
            value="Piranema_Bomba_B3",
            data=[
                {"value": "Piranema_Bomba_B3", "label": "(Piranema) Bomba B3"},
                {"value": "Piranema_Soprador_S3", "label": "(Piranema) Soprador S3"},
                {"value": "Araras_Bomba_B1", "label": "(Araras) Bomba B1"},
            ],
            style={"width": 200, "marginBottom": 10},
        )

# FFT
fft_titulo_text = dmc.Text("Analise da FFT da corrente", size="md")
grid_fft = dmc.Grid(
    [
        dmc.Col([dcc.Graph(figure={}, id="graph-fft-limite")], span=12),
    ],
    justify="center",
    align="center",
)

# Park
park_titulo_text = dmc.Text("Circulo de park", size="md")
grid_park = dmc.Grid(
    [
        dmc.Col([dcc.Graph(figure={}, id="graph-park-limite")], span=12),
    ],
    justify="center",
    align="center",
)

# Demodulacao
demod_titulo_text = dmc.Text("Espectro do sinal demodulado", size="md")
grid_demod = dmc.Grid(
    [
        dmc.Col([dcc.Graph(figure={}, id="graph-demod-limite")], span=12),
    ],
    justify="center",
    align="center",
)

# Dwt
dwt_titulo_text = dmc.Text("Coeficiente da Wavelet", size="md")
grid_dwt = dmc.Grid(
    [
        dmc.Col([dcc.Graph(figure={}, id="graph-dwt-limite")], span=12),
    ],
    justify="center",
    align="center",
)

# Container dos gráficos
container_graphs = dmc.Container(
    [
        # radio_group,
        # grid_1,
        fft_titulo_text,
        grid_fft,
        demod_titulo_text,
        grid_demod,
        dwt_titulo_text,
        grid_dwt,
        park_titulo_text,
        grid_park,
    ],
    fluid=True,
)


# color="#960CE4")
tag_ativo = html.Div(
    [
        html.Div(
            [
                "CCM X",
                html.Br(),
                "Motor Bx",
                html.Br(),
            ],
            style={
                "whiteSpace": "pre-line",
                "font-size": "24px",
                "background-color": roxo_escuro,
                "color": "white",
                "height": "50%",
                "width": "100%",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
            },
        ),
        html.Div(
            [
                "Tensão nominal",
                html.Br(),
                "Potência nominal",
                html.Br(),
                "Velocidade nominal",
            ],
            style={
                "whiteSpace": "pre-line",
                "font-size": "18px",
                "background-color": roxo_escuro,
                "color": "white",
                "height": "50%",
                "width": "100%",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
            },
        ),
    ]
)


# color="#960CE4")
var_condicao = html.Div(
    ["Motor {}".format("operando em condição normal")],
    style={
        "whiteSpace": "pre-line",
        "font-size": "24px",
        "background-color": cinza_claro,
        "color": roxo_claro,
        "height": "100%",
        "width": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
    },
)


# color="#960CE4")
var_atualizacao = html.Div(
    ["Dados atualizados em", html.Br(), "07/08/2023 13:25"],
    style={
        "whiteSpace": "pre-line",
        "font-size": "24px",
        "background-color": cinza_claro,
        "color": roxo_claro,
        "height": "100%",
        "width": "100%",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",
    },
)

style_divisoria = {
    "whiteSpace": "pre-line",
    "font-size": "24px",
    "background-color": roxo_claro,
    "color": cinza_claro,
    "height": "100%",
    "width": "100%",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
}

style_variavel = {
    "whiteSpace": "pre-line",
    "font-size": "24px",
    "background-color": cinza_claro,
    "color": roxo_claro,
    "height": "100%",
    "width": "100%",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
}

style_gauge = {
    "font-size": "18px",
    "background-color": "white",
    "color": roxo_escuro,
    "height": "100%",
    "width": "100%",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center",
}


def get_gauge_energia(
    valor, val_nominal, label, val_inf_label, val_inf_style, tol=2
):
    return html.Div(
        [
            daq.Gauge(
                showCurrentValue=False,
                color={
                    "gradient": False,
                    "ranges": {
                        roxo_claro: [0, val_nominal],
                        "red": [val_nominal, int(val_nominal * 2)],
                    },
                },
                value=valor,
                label=label,
                max=int(val_nominal * 2),
                min=0,
                size=130,
            ),
            html.Div([val_inf_label.format(val_nominal)], style=val_inf_style),
        ]
    )


def get_gauge_fp(valor, val_limite, label, val_inf_style):
    return html.Div(
        [
            daq.Gauge(
                showCurrentValue=False,
                color={
                    "gradient": True,
                    "ranges": {
                        "red": [0, val_limite],
                        roxo_claro: [val_limite, 1],
                    },
                },
                value=valor,
                label=label,
                max=1,
                min=0,
                size=130,
            ),
            html.Div(["{:.2f}".format(valor)], style=val_inf_style),
        ]
    )


var_corrente_media = get_gauge_energia(
    valor=100,
    val_nominal=100,
    label={"label": "Corrente média", "style": style_gauge},
    val_inf_label="{:.2f} A",
    val_inf_style=style_gauge,
)


var_tensao_media = get_gauge_energia(
    valor=100,
    val_nominal=100,
    label={"label": "Tensão média", "style": style_gauge},
    val_inf_label="{:.2f} V",
    val_inf_style=style_gauge,
)

var_potencia_ativa_media = get_gauge_energia(
    valor=100,
    val_nominal=100,
    label={"label": "Potência ativa média", "style": style_gauge},
    val_inf_label="{:.2f} kW",
    val_inf_style=style_gauge,
)

var_potencia_aparente_media = get_gauge_energia(
    valor=100,
    val_nominal=100,
    label={"label": "Potência aparente média", "style": style_gauge},
    val_inf_label="{:.2f} VA",
    val_inf_style=style_gauge,
)

var_frequencia_media = get_gauge_energia(
    valor=60,
    val_nominal=60,
    label={"label": "Frequência", "style": style_gauge},
    val_inf_label="{:.2f} Hz",
    val_inf_style=style_gauge,
)

var_fator_potencia = get_gauge_fp(
    valor=0.6,
    val_limite=0.75,
    label={"label": "Fator de potência", "style": style_gauge},
    val_inf_style=style_gauge,
)

var_carga_media = get_gauge_energia(
    valor=100,
    val_nominal=100,
    label={"label": "Carga", "style": style_gauge},
    val_inf_label="{:.2f} %",
    val_inf_style=style_gauge,
)

var_consumo_mes = html.Div(
    [
        "Consumo de energia ativa",
        html.Br(),
        "{:.2f} kW".format(200),
        html.Br(),
        "Consumo de energia reativa",
        html.Br(),
        "{:.2f} kVAr".format(200),
    ],
    style=style_variavel,
)

info_linha_1 = dmc.Grid(
    [
        # Dados do ativo
        dmc.Col([tag_ativo], span=3),
        # Corrente média
        dmc.Col([var_condicao], span=3),
        # Corrente média
        dmc.Col([var_atualizacao], span=3),
        dmc.Col([var_consumo_mes], span=3),
    ]
)

info_linha_2p1 = dmc.Grid(
    [
        # -Linha 2
        # Corrente média
        dmc.Col([var_corrente_media], span=1),
        # Tensão média
        dmc.Col([var_tensao_media], span=1),
        # Potência Ativa média
        dmc.Col([var_potencia_ativa_media], span=1),
        dmc.Col([var_fator_potencia], span=1),
        # dmc.Col([var_potencia_aparente_media], span=2),
        # dmc.Col([var_frequencia_media], span=2),
    ],
    columns=4,
)


info_linha_2p2 = dmc.Grid(
    [
        # -Linha 2
        # Corrente média
        # dmc.Col([var_corrente_media], span=2),
        # # Tensão média
        # dmc.Col([var_tensao_media], span=2),
        # # Potência Ativa média
        # dmc.Col([var_potencia_ativa_media], span=2),
        # dmc.Col([var_fator_potencia], span=2),
        dmc.Col([var_potencia_aparente_media], span=1),
        dmc.Col([var_frequencia_media], span=1),
        dmc.Col([var_carga_media], span=1),
    ],
    columns=3,
)


# Gráficos da energia da fundamental e do ruido espectral
def get_random_graph(value, titulo):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(20), y=np.random.rand(20), mode="lines", name="entrada"
        )
    )
    fig.add_hline(y=0.1)
    fig.update_layout(title=titulo)
    return fig


fig_ruido_espectral = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Ruído espectral"), id="graph_id"
)
fig_energia_fundamental = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Energia da fundamental"),
    id="graph_id",
)

fig_carga = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Carga"), id="graph_id"
)
fig_fator_potencia = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Fator de potência"), id="graph_id"
)




info_linha_3 = dmc.Grid(
    [
        # -Linha 2
        # Corrente média
        dmc.Col([fig_carga], span=6),
        # Tensão média
        dmc.Col([fig_fator_potencia], span=6),
    ],
    columns=12,
)


info_linha_4 = dmc.Grid(
    [
        # -Linha 2
        # Corrente média
        dmc.Col([fig_ruido_espectral], span=6),
        # Tensão média
        dmc.Col([fig_energia_fundamental], span=6),
    ],
    columns=12,
)


detalhes = {
    "Corrente": {
        "Fase A": [276.21, "A"],
        "Fase B": [273.21, "A"],
        "Fase C": [276.22, "A"],
        "Desbalanceamento": [4, "%"],
    },
    "Tensão-Fase": {
        "Fase A": [276.21, "V"],
        "Fase B": [273.21, "V"],
        "Fase C": [276.22, "V"],
        "Desbalanceamento": [4, "%"],
    },
    "Tensão-Linha": {
        "Fase AB": [276.21, "V"],
        "Fase BC": [273.21, "V"],
        "Fase CA": [276.22, "V"],
        "Desbalanceamento": [4, "%"],
    },
    "Ângulo de fase da corrente": {
        "Fase AB": [276.21, "º"],
        "Fase BC": [273.21, "º"],
        "Fase CA": [276.22, "º"],
        "Desvio máximo": [4, "º"],
    },
    "Ângulo de fase da tensão": {
        "Fase AB": [276.21, "º"],
        "Fase BC": [273.21, "º"],
        "Fase CA": [276.22, "º"],
        "Desvio máximo": [4, "º"],
    },
    "Potência ativa": {
        "Fase A": [276.21, "kW"],
        "Fase B": [273.21, "kW"],
        "Fase C": [276.22, "kW"],
        "Total": [4, "kW"],
    },
    "Potência reativa": {
        "Fase A": [276.21, "kVar"],
        "Fase B": [273.21, "kVar"],
        "Fase C": [276.22, "kVar"],
        "Total": [4, "kVar"],
    },
    "Potência Aparente": {
        "Fase A": [276.21, "kVA"],
        "Fase B": [273.21, "kVA"],
        "Fase C": [276.22, "kVA"],
        "Total": [4, "kVA"],
    },
    "Fator de Potência": {
        "Fase A": [0.6, ""],
        "Fase B": [0.7, ""],
        "Fase C": [0.8, ""],
        "Média": [4, ""],
    },
}


teste_detalhes = html.Div(["teste", dmc.Grid([
    dmc.Col(["teste", html.Br(), "teste"], span=1),
    dmc.Col(["teste", html.Br(), "teste"], span=1),
    dmc.Col(["teste", html.Br(), "teste"], span=1)
], columns=3)])

sessao_detalhes = []
for info_type in detalhes:
    detalhes_div = []
    for fase in detalhes[info_type]:
        detalhes_div.append(
            dmc.Col(
                [
                    html.B(fase),
                    html.Br(),
                    "{0:.2f}".format(detalhes[info_type][fase][0])
                    + " "
                    + detalhes[info_type][fase][1],
                ],
                span=1,
            )
        )
    sessao_detalhes.append(
        html.Div(
            [
                html.Div([info_type], style=style_variavel),
                dmc.Grid(detalhes_div, columns=len(detalhes_div)),
            ]
        )
    )


# distorçoes harmonicas

fig_distorcao_harmonica_corrente = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Fator de potência"), id="graph_id"
)

distorcao_harmonica_corrente = dmc.Grid(
    [
        
        dmc.Col(html.Div([
            html.Div(["Distorção maxima na corrente"], style=style_variavel),
            html.Div([str(5)+"%"], style=style_variavel)
            ]), span=2),
        # -Linha 2
        # Corrente média
        dmc.Col([fig_distorcao_harmonica_corrente], span=6),
    ],
    columns=8,
    justify="center",
    align="center",
    gutter="xl",
)

fig_distorcao_harmonica_tensao = dcc.Graph(
    figure=get_random_graph(value=2, titulo="Fator de potência"), id="graph_id"
)
distorcao_harmonica_tensao = dmc.Grid(
    [
        dmc.Col(html.Div([
            html.Div([
                "Distorção maxima na tensão", html.Br(),
                str(5)+"%"], style=style_variavel),
            ]), span=2),
        # -Linha 2
        # tensão média
        dmc.Col([fig_distorcao_harmonica_tensao], span=6),
    ],
    columns=8,
    justify="center",
    align="center",
    gutter="xl",
)

grid_distorcoes_harmonicas = html.Div(
    [
        distorcao_harmonica_corrente,
        distorcao_harmonica_tensao]
)

graficos_finais = dbc.Container([
    dbc.Row(
    [
        dbc.Col([fig_distorcao_harmonica_tensao]),
        dbc.Col([fig_distorcao_harmonica_tensao]),
    ]
    ),
    dbc.Row(
    [
        dbc.Col([fig_distorcao_harmonica_tensao]),
        dbc.Col([fig_distorcao_harmonica_tensao]),
    ]
    )
])


# Container da analize de emergia
info_ativo = html.Div(
    [
        info_linha_1,
        info_linha_2p1,
        info_linha_2p2,
        info_linha_3,
        info_linha_4,
        dmc.Text("Detalhes", size="h2", style=style_divisoria),
        html.Div(sessao_detalhes),
        html.Br(),
        dmc.Text("Distorçoes Harmonicas", size="h2", style=style_divisoria),
        grid_distorcoes_harmonicas,
        html.Br(),
        dmc.Text("Gráficos", size="h2", style=style_divisoria),
        graficos_finais
    ]
)

analise_energia_container = dbc.Container(
    [info_ativo],
    className="p-4",
)

tab_container = dbc.Container(
    [
        titulo_principal,
        selecionar_bomba,
        dbc.Tabs(
            id="tabs",
            active_tab="tab-1",
            children=[
                dbc.Tab(label="Analise de energia", tab_id="tab-1"),
                dbc.Tab(label="Analise MCSA", tab_id="tab-2"),
            ],
        ),
        html.Hr(),
        html.Div(id="content"),
    ],
    fluid=True,
)


@app.callback(
    Output("content", "children"),
    Input("tabs", "active_tab"),
)
def render_content(active_tab):
    if active_tab == "tab-2":
        return container_graphs

    elif active_tab == "tab-1":
        return analise_energia_container


# App layout
app.layout = tab_container


# os graficos são dezenhados dentro do callback
# Add controls to build the interaction
@callback(
    [
        Output(component_id="graph-fft-limite", component_property="figure"),
        Output(component_id="graph-park-limite", component_property="figure"),
        Output(component_id="graph-demod-limite", component_property="figure"),
        Output(component_id="graph-dwt-limite", component_property="figure"),
    ],
    Input(
        component_id="selecionar_bomba", component_property="value"
    ),
)
def update_graficos_limite(bomba):
    fft = get_fft_reference(bomba, novos_dados[bomba]["ml"], std_mult=2)
    park = get_park_figures(bomba, novos_dados[bomba]["ae"])
    demod = get_demod_fig(bomba, novos_dados[bomba]["ml"], std_mult=2)
    dwt = get_fig_dwt(bomba, novos_dados[bomba]["ml"], std_mult=2)
    return fft, park, demod, dwt


# Run the App
if __name__ == "__main__":
    app.run(debug=True)
