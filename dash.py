import pandas as pd
import streamlit as st 
import plotly.express as px 

dfs = []

with st.sidebar:
    uploaded_files = st.file_uploader(
        "Coloque seu arquivo CSV", accept_multiple_files=True
    )

    #Leitura e Importação do DataFrame
    for uploaded_file in uploaded_files:
        #Leitura do DataFrame do arquivo
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        
        #Exclsão de Linhas vazias
        df = df.dropna(how="all", axis=1)

        #Conversão das colunas Object para String
        df["Status"] = df["Status"].astype('string')
        df["Tipo"] = df["Tipo"].astype('string')
        df["Usuarios ativos"] = df["Usuarios ativos"].astype(float)
        df["Usuarios inativos"] = df["Usuarios inativos"].astype(float)
        df["Total de usuarios"] = df["Total de usuarios"].astype(float)
        df["Limite de usuarios"] = df["Limite de usuarios"].astype(float)
        df["Visualizacao (minutos)"] = df["Visualizacao (minutos)"].astype(float)
        df["Duracao total dos videos (minutos)"] = df["Duracao total dos videos (minutos)"].astype(float)
        
        dfs.append(df)

#Arrays de todas as colunas do dataframe para utilização no select e no multiselect
# de forma que vao agir dinamicamente  
opcao = {
    "graficos": ["Linha", "Barras", "Pizza", "Dispersão", "Área", "Candlestick"],
    "opcoes": [
        "Instancia",
        "Tipo",
        "Status"
    ],
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

#Criação da função dinamica para gerar graficos conforme a seleção do usuario
def DashBoard(coluna_x, coluna_y):
    for df in dfs:
        if coluna_x in df.columns and coluna_y in df.columns:
            if pd.api.types.is_numeric_dtype(df[coluna_x]) and pd.api.types.is_numeric_dtype(df[coluna_y]):
                
                if add_select == "Linha":
                    graph = px.line(df, x=coluna_x, y=coluna_y, color=df[select_usu_tipe], title=f"{coluna_x} X {coluna_y}")
                    st.plotly_chart(graph)
                    
                if add_select == "Pizza":
                    graph = px.pie(df, values=coluna_x, names=df[select_usu_tipe], title=f"{coluna_x}")
                    graph.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(graph)
                    
                    graph = px.pie(df, values=coluna_y, names=df[select_usu_tipe], title=f"{coluna_y}")
                    graph.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(graph)
        
#Criação do select principal
with st.sidebar:
    add_select = st.selectbox(
        "Selecione o tipo de grafico",
        opcao["graficos"],
        index=None,
        placeholder="Clique e selecione", 
    )

def filtro_box(filtro_escolhido = ""):
    novos_itens = opcao["opcoes_filtro"]
    try:
        novos_itens.remove(filtro_escolhido)
        return novos_itens
    except:
        return

#Criação do sidebar de usuarios
with st.sidebar:
    select_usu_tipe = st.selectbox(
        "Escolha seu tipo",
        opcao["opcoes"],
        index=None,
        placeholder="Clique e selecione"
    )
    
    add_filter = st.selectbox(
        "Escolha seu filtro",
        opcao["opcoes_filtro"],
        index=None,
        placeholder="Clique e selecione"
    )
    
    #Criação do sidebar de multiselects que contrapõe o select de usuarios
    add_filter_coparacao = st.selectbox(
        "Escolha seu filtro",
        filtro_box(add_filter),
        index=None,
        placeholder="Clique e selecione"
    )

#Chamada da função
if add_filter and add_filter_coparacao:
    DashBoard(add_filter, add_filter_coparacao)

