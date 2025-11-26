import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Carregar os dados
@st.cache_data
def load_data():
    with open('assets/cleanedData.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['dataNascimento'] = pd.to_datetime(df['dataNascimento'])
    df['anoEntrada'] = pd.to_numeric(df['anoEntrada'])
    df['anoSaida'] = pd.to_numeric(df['anoSaida'])
    df['siglaSexo'] = df['siglaSexo'].map({'M': 'Masculino', 'F': 'Feminino'}).fillna(df['siglaSexo'])
    return df

@st.cache_data
def load_legislaturas():
    with open('assets/legislaturas.json', 'r') as f:
        legislaturas_data = json.load(f)
    return {l['idLegislatura']: {'inicio': int(l['dataInicio'][:4]), 'fim': int(l['dataFim'][:4])} for l in legislaturas_data['dados']}

df = load_data()
legislaturas = load_legislaturas()

st.title('Dashboard da Câmara dos Deputados')

# Opção de filtro
filter_option = st.radio("Filtrar por:", ('Ano', 'Legislatura'))

if filter_option == 'Legislatura':
    # Filtro de legislaturas
    min_leg = min(legislaturas.keys())
    max_leg = max(legislaturas.keys())
    selected_leg = st.slider('Selecione a legislatura', min_leg, max_leg, (min_leg, max_leg))
    
    start_year = legislaturas[selected_leg[0]]['inicio']
    end_year = legislaturas[selected_leg[1]]['fim']
    
    filtered_df = df[(df['anoEntrada'] <= end_year) & (df['anoSaida'] >= start_year)]

else:
    # Filtro de anos
    min_year = int(df['anoEntrada'].min())
    max_year = int(df['anoSaida'].max())
    year_range = st.slider('Selecione o intervalo de anos', min_year, max_year, (min_year, max_year))
    
    # Filtrar o DataFrame com base no intervalo de anos
    filtered_df = df[(df['anoEntrada'] <= year_range[1]) & (df['anoSaida'] >= year_range[0])]

# Gráfico de Gênero
st.header('Divisão por Gênero')
gender_count = filtered_df['siglaSexo'].value_counts().reset_index()
gender_count.columns = ['Gênero', 'Contagem']
fig_gender = px.pie(gender_count, names='Gênero', values='Contagem', title='Divisão por Gênero', color='Gênero', color_discrete_map={'Feminino': '#f63366', 'Masculino': '#0068c9'})
st.plotly_chart(fig_gender)

# Gráfico de Estado
st.header('Divisão por Estado')
state_count = filtered_df['ufNascimento'].value_counts().reset_index()
state_count.columns = ['Estado', 'Contagem']
fig_state = px.bar(state_count, x='Estado', y='Contagem', title='Divisão por Estado')
st.plotly_chart(fig_state)

# Divisão por Região Socioeconômica
st.header('Divisão por Região Socioeconômica')
def get_region(state):
    if state in ['AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC']:
        return 'Norte'
    elif state in ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']:
        return 'Nordeste'
    elif state in ['MT', 'MS', 'GO', 'DF']:
        return 'Centro-Oeste'
    elif state in ['SP', 'RJ', 'ES', 'MG']:
        return 'Sudeste'
    elif state in ['PR', 'SC', 'RS']:
        return 'Sul'
    else:
        return 'Não Informado'

filtered_df['Regiao'] = filtered_df['ufNascimento'].apply(get_region)
region_count = filtered_df['Regiao'].value_counts().reset_index()
region_count.columns = ['Região', 'Contagem']
fig_region = px.bar(region_count, x='Região', y='Contagem', title='Divisão por Região Socioeconômica')
st.plotly_chart(fig_region)

# Tempo de Permanência
st.header('Tempo de Permanência dos Deputados')
filtered_df['tempoPermanencia'] = filtered_df['anoSaida'] - filtered_df['anoEntrada']
avg_tenure = filtered_df.groupby('nome')['tempoPermanencia'].mean().reset_index()
fig_tenure = px.histogram(avg_tenure, x='tempoPermanencia', title='Distribuição do Tempo de Permanencia')
st.plotly_chart(fig_tenure)

# Idade Média dos Deputados
st.header('Idade Média dos Deputados ao Longo dos Anos')
filtered_df['idade'] = filtered_df.apply(lambda row: row['anoEntrada'] - row['dataNascimento'].year, axis=1)
avg_age_by_year = filtered_df.groupby('anoEntrada')['idade'].mean().reset_index()
fig_age = px.line(avg_age_by_year, x='anoEntrada', y='idade', title='Idade Média dos Deputados por Ano de Entrada')
st.plotly_chart(fig_age)

# Profissões mais presentes
st.header('Profissões Mais Presentes')
profession_count = filtered_df['tituloProfissao'].value_counts().nlargest(10).reset_index()
profession_count.columns = ['Profissão', 'Contagem']
fig_profession = px.bar(profession_count, x='Profissão', y='Contagem', title='Top 10 Profissões')
st.plotly_chart(fig_profession)
