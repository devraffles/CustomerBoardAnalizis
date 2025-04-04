import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Análise do arquivo CSV")
    uploaded_files = st.file_uploader("Coloque seu arquivo aqui", accept_multiple_files=True)

if uploaded_files is not None:
    for file in uploaded_files:
        try:
            engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

            df = pd.read_csv(file, sep=",", decimal=".")
            
            table_name = file.name[:5]
            
            inspector = inspect(engine)
            schemas = inspector.get_schema_names()
            metadata = MetaData()
            metadata.reflect(bind=engine)

            for schema in schemas:
                for table_names in inspector.get_table_names(schema=schema):
                    if table_name == table_names:
                        base = declarative_base()
                        table = metadata.tables.get(table_name)
                        if table is not None:
                            base.metadata.drop_all(engine, [table], checkfirst=True)
                            
                        df.to_sql(table_name, engine, if_exists='append', index=False)
                    else:
                        df.to_sql(table_name, engine, if_exists='append', index=False)
            
            df

        except Exception as e:
            st.error(f"Ocorreu um erro {e}")
            
else:
    st.header("Bem-vindo ao CustomerBoardAnalizis", divider="red")
    st.write("O CustomerBoardAnalizis visa fornecer uma visão completa e acionável do comportamento e utilização dos clientes, permitindo que diferentes perfis de usuários (analistas, gerentes, executivos, desenvolvedores) obtenham insights relevantes para suas respectivas áreas de atuação.")
