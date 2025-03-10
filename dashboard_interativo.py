import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 📌 Carregar os dados (garantindo que esteja correto)
@st.cache_data
def carregar_dados():
    return pd.read_csv("life_expectancy_cleaned.csv")  # Certifique-se de que esse arquivo existe

df_cleaned = carregar_dados()

# Criando a coluna com a diferença de expectativa de vida entre mulheres e homens
df_cleaned["Life_Expectancy_Gap"] = df_cleaned["Female_Life_Expectancy"] - df_cleaned["Male_Life_Expectancy"]

# 📊 Introdução ao Dashboard
st.title("🌍 Dashboard - Expectativa de Vida Global")
st.markdown(
    """
    🔍 **O que você pode explorar aqui?**
    - 📊 **Comparação entre expectativa de vida de homens e mulheres**  
    - 🌍 **Mapa interativo da expectativa de vida mundial**  
    - 📉 **Países com maior e menor diferença entre gêneros**  
    - 📈 **Previsão vs. Expectativa de Vida Real**  
    """
)

# 📌 Seção 1: Comparação entre Expectativa Masculina e Feminina
st.subheader("📊 Comparação da Expectativa de Vida entre Gêneros")
fig1 = px.scatter(df_cleaned, x="Male_Life_Expectancy", y="Female_Life_Expectancy",
                  title="Expectativa de Vida: Homens vs Mulheres",
                  labels={"Male_Life_Expectancy": "Expectativa de Vida Masculina", 
                          "Female_Life_Expectancy": "Expectativa de Vida Feminina"},
                  hover_name="Country")
st.plotly_chart(fig1)

st.markdown("📌 **Observação:** Em praticamente todos os países, a expectativa de vida das mulheres é maior que a dos homens.")

# 📌 Seção 2: Mapa Global com Filtro por Região
st.subheader("🌍 Mapa Global da Expectativa de Vida")

# Adicionando um filtro por região
paises_selecionados = st.multiselect("Selecione países específicos (opcional)", df_cleaned["Country"].unique())

if paises_selecionados:
    df_mapa = df_cleaned[df_cleaned["Country"].isin(paises_selecionados)]
else:
    df_mapa = df_cleaned

fig2 = px.choropleth(df_mapa, locations="Country", locationmode="country names",
                     color="Life_Expectancy_Both", hover_name="Country",
                     title="Mapa da Expectativa de Vida por País",
                     color_continuous_scale="Viridis")
st.plotly_chart(fig2)

st.markdown("📌 **Curiosidade:** Países como Japão e Suíça têm as maiores expectativas de vida, enquanto países africanos apresentam valores menores.")

# 📌 Seção 3: Diferença da Expectativa de Vida
st.subheader("📉 Top 10 Países com Maior e Menor Diferença na Expectativa de Vida")
top_10_gap = df_cleaned.nlargest(10, 'Life_Expectancy_Gap')
bottom_10_gap = df_cleaned.nsmallest(10, 'Life_Expectancy_Gap')

fig3, axes = plt.subplots(1, 2, figsize=(15,5))

sns.barplot(y=top_10_gap["Country"], x=top_10_gap["Life_Expectancy_Gap"], ax=axes[0])
axes[0].set_title("🔺 Países com Maior Diferença")

sns.barplot(y=bottom_10_gap["Country"], x=bottom_10_gap["Life_Expectancy_Gap"], ax=axes[1])
axes[1].set_title("🔻 Países com Menor Diferença")

st.pyplot(fig3)

st.markdown("""
📌 **O que isso significa?**
- 🔺 **Países como Rússia e Ucrânia apresentam as maiores diferenças**, provavelmente devido a fatores como tabagismo, alcoolismo e condições de trabalho masculinas.  
- 🔻 **Países árabes como Qatar e Emirados Árabes têm diferenças mínimas**, possivelmente por conta de estilos de vida mais equilibrados.
""")

# 📌 Seção 4: Comparação entre Expectativa Real e Prevista
st.subheader("📈 Comparação: Expectativa Real vs Modelo")
fig5, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x=df_cleaned["Life_Expectancy_Both"], y=df_cleaned["Predicted_Life_Expectancy"])
plt.xlabel("Expectativa de Vida Real")
plt.ylabel("Expectativa de Vida Prevista pelo Modelo")
plt.title("Comparação entre Valores Reais e Previstos")
plt.axline((0, 0), slope=1, color="red", linestyle="--")
st.pyplot(fig5)

st.markdown("""
📌 **Resultados do modelo de Machine Learning**  
✅ **Precisão:** O modelo tem um **R² de 99.98%**, ou seja, consegue prever a expectativa de vida com altíssima precisão.  
✅ **Conclusão:** A expectativa de vida geral de um país **é praticamente uma média ponderada entre a expectativa de vida masculina e feminina**.
""")
