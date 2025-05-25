import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Lista para armazenar os dataframes
dfs = []

# Sidebar para upload dos arquivos
with st.sidebar:
    uploaded_files = st.file_uploader(
        "Coloque seu arquivo CSV", accept_multiple_files=True
    )

    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        
        df = df.dropna(how="all", axis=1)

        df["Status"] = df["Status"].astype('string')
        df["Tipo"] = df["Tipo"].astype('string')
        
        df["Usuarios ativos"] = df["Usuarios ativos"].astype(float)
        df["Usuarios inativos"] = df["Usuarios inativos"].astype(float)
        df["Total de usuarios"] = df["Total de usuarios"].astype(float)
        df["Limite de usuarios"] = df["Limite de usuarios"].astype(float)
        df["Visualizacao (minutos)"] = df["Visualizacao (minutos)"].astype(float)
        df["Duracao total dos videos (minutos)"] = df["Duracao total dos videos (minutos)"].astype(float)
        
        dfs.append(df)

# Opções de seleção
opcao = {
    "graficos": ["Linha", "Barras", "Pizza", "Histograma", "Dispersão", "Área", "Candlestick"],
    "opcoes": ["Instancia", "Tipo", "Status"],
    "opcoes_filtro": [
        "Usuarios ativos",
        "Usuarios inativos",
        "Total de usuarios",
        "Limite de usuarios",
        "Armazenamento (GB)",
        "Limite de armazenamento_(GB)",
        "Armazenamento adicional (GB)",
        "Visualizacao (minutos)",
        "Limite visualizacao (minutos)",
        "Visualizacao adicional (minutos)",
        "CDN (Total) (GB)",
        "CDN (Videos) (GB)",
        "CDN (Imagens) (GB)",
        "CDN (Downloads) (GB)",
        "CDN (Outros) (GB)",
        "Duracao total dos videos (minutos)"
    ]
}

# Sidebar para seleção de gráfico, agrupamento e agregação
with st.sidebar:
    add_select = st.selectbox(
        "Selecione o tipo de gráfico",
        opcao["graficos"],
        index=None,
        placeholder="Clique e selecione"
    )

    select_usu_tipe = st.selectbox(
        "Agrupar por",
        opcao["opcoes"],
        index=None,
        placeholder="Clique e selecione"
    )

    add_filter = st.selectbox(
        "Escolha seu filtro X",
        opcao["opcoes_filtro"],
        index=None,
        placeholder="Clique e selecione"
    )

    def filtro_box(filtro_escolhido=""):
        novos_itens = opcao["opcoes_filtro"].copy()
        try:
            novos_itens.remove(filtro_escolhido)
            return novos_itens
        except:
            return novos_itens

    add_filter_coparacao = st.selectbox(
        "Escolha seu filtro Y",
        filtro_box(add_filter),
        index=None,
        placeholder="Clique e selecione"
    )

    agg_func = st.selectbox(
        "Selecione a forma de agrupamento de dados",
        ["Soma", "Média", "Máximo", "Mínimo"],
        index=0
    )

# Mapeamento das funções de agregação
agg_map = {
    "Soma": "sum",
    "Máximo": "max",
    "Média": "mean",
    "Mínimo": "min"
}

# Função principal do Dashboard
def DashBoard(coluna_x, coluna_y):
    for df in dfs:
        if coluna_x in df.columns and coluna_y in df.columns:
            if pd.api.types.is_numeric_dtype(df[coluna_x]) and pd.api.types.is_numeric_dtype(df[coluna_y]):

                df_grouped = df.groupby(select_usu_tipe).agg({
                    coluna_x: agg_map[agg_func],
                    coluna_y: agg_map[agg_func]
                }).reset_index()

                if add_select == "Linha":
                    graph = px.line(
                        df_grouped,
                        x=coluna_x,
                        y=coluna_y,
                        color=select_usu_tipe,
                        title=f"{coluna_x} X {coluna_y} ({agg_func})"
                    )
                    st.plotly_chart(graph)
                
                elif add_select == "Pizza":
                    # Agrupa pela categoria e soma a métrica
                    df_grouped = df.groupby(select_usu_tipe).agg({
                        add_filter: agg_map[agg_func]
                    }).reset_index()

                    fig = px.pie(
                        df_grouped,
                        names=select_usu_tipe,
                        values=add_filter,
                        title=f"{add_filter} por {select_usu_tipe} ({agg_func})"
                    )
                    st.plotly_chart(fig)

                elif add_select == "Dispersão":
                    graph = px.scatter(
                        df_grouped,
                        x=coluna_x,
                        y=coluna_y,
                        color=select_usu_tipe,
                        title=f"{coluna_x} X {coluna_y} ({agg_func})"
                    )
                    st.plotly_chart(graph)

                elif add_select == "Barras":
                    graph = px.bar(
                        df_grouped,
                        x=coluna_x,
                        y=coluna_y,
                        color=select_usu_tipe,
                        title=f"{coluna_x} X {coluna_y} ({agg_func})"
                    )
                    st.plotly_chart(graph)

                elif add_select == "Histograma":
                    graph = px.histogram(
                        df_grouped,
                        x=coluna_x,
                        y=coluna_y,
                        color=select_usu_tipe,
                        title=f"{coluna_x} X {coluna_y} ({agg_func})"
                    )
                    st.plotly_chart(graph)

                elif add_select == "Área":
                    graph = px.area(
                        df_grouped,
                        x=coluna_x,
                        y=coluna_y,
                        color=select_usu_tipe,
                        title=f"{coluna_x} X {coluna_y} (Área - {agg_func})"
                    )
                    st.plotly_chart(graph)

                elif add_select == "Candlestick":
                    try:
                        df_candle = df.groupby(select_usu_tipe).agg({
                            coluna_x: 'first',
                            coluna_y: ['min', 'max', 'first', 'last']
                        }).reset_index()

                        df_candle.columns = [select_usu_tipe, 'X', 'low', 'high', 'open', 'close']

                        fig = go.Figure(data=[go.Candlestick(
                            x=df_candle[select_usu_tipe],
                            open=df_candle['open'],
                            high=df_candle['high'],
                            low=df_candle['low'],
                            close=df_candle['close']
                        )])

                        fig.update_layout(title=f'Candlestick {coluna_x} X {coluna_y}')
                        st.plotly_chart(fig)

                    except Exception as e:
                        st.error(f"Erro ao gerar candlestick: {e}")

# Executa se as seleções estiverem feitas
if add_filter and add_filter_coparacao and add_select and select_usu_tipe:
    DashBoard(add_filter, add_filter_coparacao)
