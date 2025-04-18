import pandas as pd
import streamlit as st 
import plotly.express as px 


#Leitura do DataFrame
df = pd.read_csv("DadosClientes.csv",encoding='latin1')
#Exclsão de Linhas vazias
df = df.dropna(how="all", axis=1)

#Conversão das colunas Object para String
df["Status"] = df["Status"].astype('string')
df["Tipo"] = df["Tipo"].astype('string')
df.info()


#Arrays de todas as colunas do dataframe para utilização no select e no multiselect
# de forma que vao agir dinamicamente  
OPÇÕES_PRINCIPAIS = {
    "Principal": ["Usuario", "Armazenamento", "CDN", "Vizualização"],
    "Usuario": {
        "Usuarios_Geral": ["Usuarios ativos", "Usuariosinativos", "Total de usuarios", "Limite de usuarios"],
        "Conteudos_relacionados_Usuario": [
            "Status", "Armazenamento (GB)", "Limite de armazenamento_(GB)", "Armazenamento adicional (GB)",
            "Visualizacao (minutos)", "Limite visualizacao (minutos)", "Tipo",
            "Visualizacao adicional (minutos)", "CDN (Total) (GB)", "CDN (Videos) (GB)", "CDN (Imagens) (GB)",
            "CDN (Downloads) (GB)", "CDN (Outros) (GB)", "Duracao total dos videos (minutos)"
        ]
    }
}

#Criação da função dinamica para gerar graficos conforme a seleção do usuario
def DashBoardUsu(coluna_x, coluna_y, box):
    if coluna_x in df.columns and coluna_y in df.columns:
        if pd.api.types.is_numeric_dtype(df[coluna_x]) and pd.api.types.is_numeric_dtype(df[coluna_y]):
            linha = px.line(df, x=coluna_x, y=coluna_y, title=f"{coluna_x} X {coluna_y}")
            box.plotly_chart(linha)
        
#Criação do select principal
with st.sidebar:
    add_select = st.selectbox(
        "Selecione o tipo de grafico",
        OPÇÕES_PRINCIPAIS["Principal"],
        index=None,
        placeholder="Clique e selecione", 
    )
    
#Criação da condicional de usuarios        
if add_select == "Usuario":
    #Criação das colunas no streamlit
    col1, col2 = st.columns(2)  
    
    #Criação do sidebar de usuarios
    with st.sidebar:
        add_select_usu = st.selectbox(
            "Escolha seu filtro",
            OPÇÕES_PRINCIPAIS["Usuario"]["Usuarios_Geral"],
            index=None,
            placeholder="Clique e selecione",
        )
        
        
        #Criação do sidebar de multiselects que contrapõe o select de usuarios
        usu_select_all = st.multiselect(
            "Escolha seu filtro",
            OPÇÕES_PRINCIPAIS["Usuario"]["Conteudos_relacionados_Usuario"]
        )
    
    #Chamada da função
    if add_select_usu and usu_select_all:
        DashBoardUsu(add_select_usu, usu_select_all[0], col1)

