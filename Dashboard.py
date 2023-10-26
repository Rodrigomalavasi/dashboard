import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
        
    return f'{prefixo} {valor:.2f} milhões'

url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

with st.sidebar:
    add_input = st.text_input('Pesquisar')
    add_button = st.button('Buscar')

    filtro_titulo = st.subheader('Filtros')
    for item in dados.columns:
        st.checkbox(item, key=item)
    
st.title('DASHBOARD DE VENDAS :shopping_trolley:')

coluna1, coluna2 = st.columns(2)
with coluna1: 
    st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

st.dataframe(dados)
