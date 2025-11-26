import streamlit as st
from utils import load_json_to_df, dataframe_section

st.set_page_config(layout="wide")

st.title("Análise da Representatividade e Perfil Profissional na Câmara dos Deputados.")

st.markdown('''
            Erick Carpes, Gabriel Domingues e Leonardo Gemin.

            **Introdução:**
            
            Este projeto realiza uma análise exploratória de dados sobre os deputados da Câmara dos Deputados do Brasil. Utilizando dados de diversas fontes, criamos um dashboard interativo que permite visualizar informações como a distribuição de gênero, estado de origem, tempo de mandato e profissões mais comuns dos deputados ao longo do tempo. A flexibilidade dos filtros de tempo permite que o usuário explore os dados de acordo com seu interesse, seja por um período de anos específico ou por legislaturas.

            **Pergunta:**
            
            O senso comum realmente está certo?

            **Metodologia CRISP-DM**
            - Fase 1: Compreensão do Negócio
            - Fase 2: Compreensão dos Dados 
            - Fase 3: Preparação dos Dados

            **Tecnologias: (Python Librarys)**
            - Streamlit
            - Pandas
            - Plotly
            
            **Referências: (Arquivos JSON públicos da câmara dos deputados)**
            - `deputados.json`
            - `deputadosProfissoes.json`
            - `legislaturas.json`

            **Gráficos no Dashboard:**
            - **Divisão por Gênero:** Gráfico de pizza mostrando a proporção de deputados por gênero.
            - **Divisão por Estado:** Gráfico de barras mostrando a quantidade de deputados por estado de nascimento.
            - **Divisão por Região Socioeconômica:** Gráfico de barras mostrando a quantidade de deputados por região socioeconômica.
            - **Tempo de Permanência dos Deputados:** Histograma mostrando a distribuição do tempo de mandato dos deputados.
            - **Idade Média dos Deputados ao Longo dos Anos:** Gráfico de linha mostrando a idade média dos deputados por ano de entrada.
            - **Profissões Mais Presentes:** Gráfico de barras mostrando as 10 profissões mais comuns entre os deputados.

            **Período de Análise:**
            O Dataframe final contém dados dos anos de 1826 à 2025, podendo ser filtrados pelo usuário no dashboard.

            ### Dataframe utilizado para análise:
            ''')

df = load_json_to_df("./assets/cleanedData.json")
dataframe_section(df)