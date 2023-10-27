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

## Tabelas
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

## Gráficos 
fig_mapa_receita = px.scatter_geo(receita_estados, 
                                    lat='lat', 
                                    lon='lon', 
                                    scope='south america', 
                                    size='Preço',
                                    template='seaborn',
                                    hover_name='Local da compra',
                                    hover_data= {'lat':False, 'lon':False},
                                    title='Receita por estado'
                                )

## Visualização do Streamlit
coluna1, coluna2 = st.columns(2)
with coluna1: 
    st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapa_receita)
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))

st.dataframe(dados)
