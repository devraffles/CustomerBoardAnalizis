import streamlit as st
import pandas as pd
import plotly.express as px

# Colunas do csv
# Instancia,
# Tipo,
# Status,
# Usuarios ativos,
# Usuarios inativos,
# Total de usuarios,
# Limite de usuarios,
# Armazenamento (GB),
# Limite de armazenamento_(GB),
# Armazenamento adicional (GB),
# Visualizacao (minutos),
# Limite visualizacao (minutos),
# Visualizacao adicional (minutos),
# CDN (Total) (GB),
# CDN (Videos) (GB),
# CDN (Imagens) (GB),
# CDN (Downloads) (GB),
# CDN (Outros) (GB),
# Duracao total dos videos (minutos).

# Perguntas:
# Taxa de crescimento de usuários ativos
# Percentual de usuários ativos
# Utilização de armazenamento
# Utilização de visualização
# Distribuição do consumo de CDN por tipo (vídeos, imagens, downloads, outros).
# Média de visualização por usuário ativo
# Média de duração dos vídeos por usuário ativo

# Filtros de Usuários:
# Faixa de Usuários Ativos: Permite filtrar instâncias com um determinado número de usuários ativos.
# Faixa de Usuários Inativos: Permite filtrar instâncias com um determinado número de usuários inativos.
# Faixa de Total de Usuários: Permite filtrar instâncias com um determinado número total de usuários.

# Filtros de Limites:
# Limite de Usuários: Filtrar instâncias com um limite específico de usuários.
# Limite de Armazenamento (GB): Filtrar instâncias com um limite específico de armazenamento.
# Limite de Visualização (minutos): Filtrar instâncias com um limite específico de visualização.

# Filtros de Uso de Recursos:
# Faixa de Armazenamento (GB): Permite analisar instâncias que utilizam uma determinada quantidade de armazenamento.
# Faixa de Armazenamento Adicional (GB): Permite analisar instâncias com uma determinada quantidade de armazenamento adicional.
# Faixa de Visualização (minutos): Permite analisar instâncias com um determinado tempo de visualização.
# Faixa de Visualização Adicional (minutos): Permite analisar instâncias com um determinado tempo de visualização adicional.
# Faixa de CDN (Total) (GB): Permite analisar instâncias com um determinado consumo total de CDN.
# Faixa de CDN (Videos) (GB): Permite analisar instâncias com um determinado consumo de CDN para vídeos.
# Faixa de CDN (Imagens) (GB): Permite analisar instâncias com um determinado consumo de CDN para imagens.
# Faixa de CDN (Downloads) (GB): Permite analisar instâncias com um determinado consumo de CDN para downloads.
# Faixa de CDN (Outros) (GB): Permite analisar instâncias com um determinado consumo de CDN para outros tipos de conteúdo.
# Faixa de Duração Total dos Vídeos (minutos): Permite analisar instâncias com uma determinada duração total de vídeos.

st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Análise do arquivo CSV")
    uploaded_file = st.file_uploader("Coloque seu arquivo aqui")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",", decimal=".")
    
    df

st.header("Bem-vindo ao CustomerBoardAnalizis", divider="red")
st.write("O CustomerBoardAnalizis visa fornecer uma visão completa e acionável do comportamento e utilização dos clientes, permitindo que diferentes perfis de usuários (analistas, gerentes, executivos, desenvolvedores) obtenham insights relevantes para suas respectivas áreas de atuação.")

st.write("Para isso coloquei o arquivo para ser analizado")