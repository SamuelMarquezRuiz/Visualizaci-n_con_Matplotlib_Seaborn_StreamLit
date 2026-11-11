import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard de Gráficos", layout="wide")
sns.set_theme(style="whitegrid")

st.title("Visualización de 5 Gráficos con Streamlit")
st.markdown("Comparativa visual utilizando Matplotlib y Seaborn encapsulados en Streamlit.")

# --- Generación de Datos ---
@st.cache_data
def load_data():
    np.random.seed(42)
    df_ventas = pd.DataFrame({'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'], 'Ventas': [150, 200, 180, 220, 250, 230]})
    df_cat = pd.DataFrame({'Categoría': ['A', 'B', 'C', 'D'], 'Valor': [45, 88, 56, 72]})
    df_scatter = pd.DataFrame({'X': np.random.rand(50) * 100, 'Y': (np.random.rand(50) * 100) * 2 + np.random.randn(50) * 15})
    df_edades = pd.DataFrame({'Edad': np.random.normal(35, 10, 200)})
    df_box = pd.DataFrame({
        'Departamento 1': np.random.normal(50000, 10000, 100), 
        'Departamento 2': np.random.normal(60000, 15000, 100)
    }).melt(var_name='Departamento', value_name='Salario')
    
    return df_ventas, df_cat, df_scatter, df_edades, df_box

df_ventas, df_cat, df_scatter, df_edades, df_box = load_data()

# --- Diseño en Columnas ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Gráfico de Líneas (Ventas)")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=df_ventas, x='Mes', y='Ventas', marker='o', ax=ax)
    st.pyplot(fig)

with col2:
    st.header("2. Gráfico de Barras (Categorías)")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_cat, x='Categoría', y='Valor', ax=ax, palette='viridis')
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.header("3. Gráfico de Dispersión")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df_scatter, x='X', y='Y', ax=ax, color='crimson')
    st.pyplot(fig)

with col4:
    st.header("4. Histograma (Edades)")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df_edades, x='Edad', bins=20, kde=True, ax=ax, color='teal')
    st.pyplot(fig)

st.header("5. Gráfico de Cajas (Salarios por Depto)")
fig, ax = plt.subplots(figsize=(10, 4))
sns.boxplot(data=df_box, x='Departamento', y='Salario', ax=ax, palette='Set2')
st.pyplot(fig)