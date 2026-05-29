import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard TEA - Grande Rio", layout="wide")
st.title("🗺️ Mapeamento de Centros de Atendimento TEA")
st.markdown("Visualização da rede de suporte e identificação de vazios assistenciais no Grande Rio.")

# 2. Carregar os Dados
@st.cache_data
def load_data():
    # Lê a planilha que geramos no Colab
    return pd.read_csv("cnes_pronto_dashboard.csv")

df = load_data()

# 3. Filtros na Barra Lateral
st.sidebar.header("Filtros de Busca")
municipios = df["MUNICIPIO"].unique().tolist()
municipio_selecionado = st.sidebar.multiselect(
    "Selecione o Município:",
    options=municipios,
    default=municipios
)

# Aplica o filtro
df_filtrado = df[df["MUNICIPIO"].isin(municipio_selecionado)]

# 4. Estrutura Visual (Mapa à esquerda, Dados à direita)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Distribuição Espacial")
    # Centraliza o mapa na Região Metropolitana do Rio
    mapa = folium.Map(location=[-22.9068, -43.1729], zoom_start=10)
    
    # Insere os pontos no mapa
    for _, row in df_filtrado.iterrows():
        popup_texto = f"<b>{row['NOME_FANTASIA']}</b><br>{row['RUA']}, {row['BAIRRO']}<br>{row['MUNICIPIO']}"
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=6,                 # Define o tamanho do ponto
            color="#005b96",          # Cor da linha da borda (azul escuro)
            weight=1,                 # Espessura da borda
            fill=True,                # Ativa o preenchimento
            fill_color="#03396c",     # Cor de dentro do ponto
            fill_opacity=0.7,         # Nível de transparência (0.0 a 1.0)
            popup=folium.Popup(popup_texto, max_width=300),
            tooltip="Clique para ver detalhes"
        ).add_to(mapa)
        
    st_folium(mapa, width=700, height=500)

with col2:
    st.subheader("Indicadores Assistenciais")
    st.info(f"**Total de Estabelecimentos Visíveis:** {len(df_filtrado)}")
    # Mostra uma tabela resumida das clínicas filtradas
    st.dataframe(df_filtrado[['NOME_FANTASIA', 'MUNICIPIO']], use_container_width=True)
    
st.caption("Fonte dos Dados: CNES / DATASUS")
