import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suprimir avisos menores para garantizar una ejecución limpia en producción
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# Configuración inicial de Streamlit
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Visualización con Matplotlib, Seaborn y Streamlit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Barra lateral: configuración y controles interactivos
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    semilla = st.number_input(
        "Semilla aleatoria (Seed)",
        value=42,
        step=1,
        help="La semilla 42 genera los valores exactos descritos en las conclusiones del cuaderno."
    )
    
    st.divider()
    modo_vista = st.radio(
        "Modo de visualización:",
        options=["📜 Cuaderno Completo (Flujo continuo)", "📑 Vista por Pestañas (Tabs)"],
        index=0
    )
    mostrar_codigo = st.checkbox("Mostrar código fuente de cada celda", value=False)
    
    st.divider()
    st.markdown("### 📌 Índice de Secciones")
    st.markdown("""
    - [Importación y generación de datos](#importaci-n-y-generaci-n-de-datos)
    - [1. Gráfico de Líneas](#1-gr-fico-de-l-neas-tendencia-de-ventas)
    - [2. Gráfico de Barras](#2-gr-fico-de-barras-comparaci-n-de-categor-as)
    - [3. Gráfico de Dispersión](#3-gr-fico-de-dispersi-n-relaci-n-variables)
    - [4. Histograma](#4-histograma-distribuci-n-de-edades)
    - [5. Gráfico de Cajas](#5-gr-fico-de-cajas-distribuci-n-de-salarios)
    """)
    st.divider()
    st.caption("IABD · Visualización con Matplotlib, Seaborn y Streamlit")

# -----------------------------------------------------------------------------
# Generación de Datos Sintéticos (con caché de Streamlit)
# -----------------------------------------------------------------------------
@st.cache_data
def generar_datos_sinteticos(seed=42):
    np.random.seed(seed)
    
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ventas = [150, 200, 180, 220, 250, 230]
    categorias = ['A', 'B', 'C', 'D']
    valores_cat = [45, 88, 56, 72]
    x_scatter = np.random.rand(50) * 100
    y_scatter = x_scatter * 2 + np.random.randn(50) * 15
    edades = np.random.normal(loc=35, scale=10, size=200)
    salarios = [np.random.normal(50000, 10000, 100), np.random.normal(60000, 15000, 100)]

    df_ventas = pd.DataFrame({'Mes': meses, 'Ventas': ventas})
    df_cat = pd.DataFrame({'Categoría': categorias, 'Valor': valores_cat})
    df_scatter = pd.DataFrame({'X': x_scatter, 'Y': y_scatter})
    df_edades = pd.DataFrame({'Edad': edades})
    df_box = pd.DataFrame({
        'Departamento 1': salarios[0],
        'Departamento 2': salarios[1]
    }).melt(var_name='Departamento', value_name='Salario')

    return meses, ventas, categorias, valores_cat, x_scatter, y_scatter, edades, salarios, df_ventas, df_cat, df_scatter, df_edades, df_box

# Carga de datos
meses, ventas, categorias, valores_cat, x_scatter, y_scatter, edades, salarios, df_ventas, df_cat, df_scatter, df_edades, df_box = generar_datos_sinteticos(semilla)

# -----------------------------------------------------------------------------
# Título principal de la aplicación
# -----------------------------------------------------------------------------
st.title("📊 Visualización con Matplotlib, Seaborn y Streamlit")
st.markdown("Comparativa visual y metodológica entre **Matplotlib** y **Seaborn** implementada como aplicación interactiva en Streamlit.")

# =============================================================================
# FUNCIONES PARA RENDERIZAR CADA SECCIÓN
# =============================================================================

def render_seccion_datos():
    st.header("Importación y generación de datos")
    st.markdown("""
    En esta primera etapa se importan las librerías científicas (`numpy`, `pandas`, `matplotlib.pyplot`, `seaborn`) 
    y se generan los datos sintéticos estructurados en DataFrames de Pandas para alimentar cada gráfico:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("`df_ventas` (Tendencia de Ventas)")
        st.dataframe(df_ventas, use_container_width=True)
        st.subheader("`df_cat` (Comparación de Categorías)")
        st.dataframe(df_cat, use_container_width=True)
    with col2:
        st.subheader("`df_scatter` (Relación X e Y - Primeras 6 filas)")
        st.dataframe(df_scatter.head(6), use_container_width=True)
        st.subheader("`df_edades` (Distribución de Edades - Primeras 6 filas)")
        st.dataframe(df_edades.head(6), use_container_width=True)
        
    st.subheader("`df_box` (Muestra de Salarios por Departamento)")
    st.dataframe(df_box.sample(6, random_state=42), use_container_width=True)
    
    if mostrar_codigo:
        st.markdown("**Código de importación y generación:**")
        st.code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Generamos datos sintéticos
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
ventas = [150, 200, 180, 220, 250, 230]
categorias = ['A', 'B', 'C', 'D']
valores_cat = [45, 88, 56, 72]
x_scatter = np.random.rand(50) * 100
y_scatter = x_scatter * 2 + np.random.randn(50) * 15
edades = np.random.normal(loc=35, scale=10, size=200)
salarios = [np.random.normal(50000, 10000, 100), np.random.normal(60000, 15000, 100)]

df_ventas = pd.DataFrame({'Mes': meses, 'Ventas': ventas})
df_cat = pd.DataFrame({'Categoría': categorias, 'Valor': valores_cat})
df_scatter = pd.DataFrame({'X': x_scatter, 'Y': y_scatter})
df_edades = pd.DataFrame({'Edad': edades})
df_box = pd.DataFrame({'Departamento 1': salarios[0], 'Departamento 2': salarios[1]}).melt(var_name='Departamento', value_name='Salario')
        """, language="python")

def render_grafico_1():
    st.header("1. Gráfico de Líneas (`Tendencia de Ventas`)")
    st.info(
        "**Justificación y análisis:**\n\n"
        "Se utiliza porque el eje horizontal representa una variable temporal ordenada (`Ene` a `Jun`) y el eje vertical una magnitud numérica continua, "
        "lo que permite visualizar la evolución y el ritmo de cambio a lo largo del tiempo al conectar los puntos. "
        "En él se observa una tendencia general creciente durante el semestre, destacando un fuerte repunte inicial entre enero (150) y febrero (200), "
        "un leve retroceso en marzo (180), una recuperación sostenida hasta alcanzar el pico máximo en mayo (250) y una ligera caída en junio (230)."
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('1. Gráfico de Líneas: Tendencia de Ventas', fontsize=14, fontweight='bold')

    # Matplotlib
    axes[0].plot(meses, ventas, marker='o', color='b', linestyle='-')
    axes[0].set_title('Matplotlib')
    axes[0].grid(True)

    # Seaborn
    sns.lineplot(data=df_ventas, x='Mes', y='Ventas', marker='o', ax=axes[1])
    axes[1].set_title('Seaborn')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    if mostrar_codigo:
        st.code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('1. Gráfico de Líneas: Tendencia de Ventas', fontsize=14, fontweight='bold')

# Matplotlib
axes[0].plot(meses, ventas, marker='o', color='b', linestyle='-')
axes[0].set_title('Matplotlib')
axes[0].grid(True)

# Seaborn
sns.lineplot(data=df_ventas, x='Mes', y='Ventas', marker='o', ax=axes[1])
axes[1].set_title('Seaborn')

plt.tight_layout()
plt.show()
        """, language="python")

def render_grafico_2():
    st.header("2. Gráfico de Barras (`Comparación de Categorías`)")
    st.info(
        "**Justificación y análisis:**\n\n"
        "Se ha escogido porque el eje horizontal contiene variables categóricas discretas sin continuidad ni orden temporal (`A`, `B`, `C`, `D`), "
        "donde la altura de cada barra permite comparar magnitudes de forma directa sin sugerir progresión entre ellas. "
        "La visualización muestra que la categoría B lidera claramente con el valor más alto (88), seguida por la categoría D (72), "
        "mientras que la categoría A registra el menor rendimiento (45), situándose prácticamente a la mitad de la líder."
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('2. Gráfico de Barras: Comparación de Categorías', fontsize=14, fontweight='bold')

    # Matplotlib
    axes[0].bar(categorias, valores_cat, color='skyblue')
    axes[0].set_title('Matplotlib')

    # Seaborn
    sns.barplot(data=df_cat, x='Categoría', y='Valor', palette='Blues_d', hue='Categoría', legend=False, ax=axes[1])
    axes[1].set_title('Seaborn')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    if mostrar_codigo:
        st.code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('2. Gráfico de Barras: Comparación de Categorías', fontsize=14, fontweight='bold')

# Matplotlib
axes[0].bar(categorias, valores_cat, color='skyblue')
axes[0].set_title('Matplotlib')

# Seaborn
sns.barplot(data=df_cat, x='Categoría', y='Valor', palette='Blues_d', hue='Categoría', legend=False, ax=axes[1])
axes[1].set_title('Seaborn')

plt.tight_layout()
plt.show()
        """, language="python")

def render_grafico_3():
    st.header("3. Gráfico de Dispersión (`Relación Variables`)")
    st.info(
        "**Justificación y análisis:**\n\n"
        "Se emplea para analizar la correlación entre dos variables numéricas continuas (`X` e `Y` a lo largo de 50 observaciones) "
        "sin agrupar ni promediar los datos individuales. En el gráfico se aprecia una fuerte correlación lineal positiva, "
        "ya que a medida que aumenta el valor de X (de 0 a 100), el valor de Y crece proporcionalmente hasta aproximadamente el doble, "
        "formando una nube ascendente estrecha que evidencia una relación consistente con poca dispersión."
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('3. Gráfico de Dispersión: Relación Variables', fontsize=14, fontweight='bold')

    # Matplotlib
    axes[0].scatter(x_scatter, y_scatter, color='green', alpha=0.7)
    axes[0].set_title('Matplotlib')

    # Seaborn
    sns.scatterplot(data=df_scatter, x='X', y='Y', color='green', ax=axes[1])
    axes[1].set_title('Seaborn')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    if mostrar_codigo:
        st.code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('3. Gráfico de Dispersión: Relación Variables', fontsize=14, fontweight='bold')

# Matplotlib
axes[0].scatter(x_scatter, y_scatter, color='green', alpha=0.7)
axes[0].set_title('Matplotlib')

# Seaborn
sns.scatterplot(data=df_scatter, x='X', y='Y', color='green', ax=axes[1])
axes[1].set_title('Seaborn')

plt.tight_layout()
plt.show()
        """, language="python")

def render_grafico_4():
    st.header("4. Histograma (`Distribución de Edades`)")
    st.info(
        "**Justificación y análisis:**\n\n"
        "Se selecciona cuando se dispone de una única variable numérica con numerosos registros (200 edades) que necesitan agruparse en intervalos (*bins*) "
        "para revelar su frecuencia y estructura estadística. Los datos reflejan una distribución normal (campana de Gauss) centrada alrededor de los 35 años, "
        "con la mayor concentración de individuos entre los 25 y los 45 años y una caída simétrica hacia los extremos, "
        "perfil que se distingue con mayor suavidad en la versión de Seaborn gracias a su curva de densidad superpuesta (`kde`)."
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('4. Histograma: Distribución de Edades', fontsize=14, fontweight='bold')

    # Matplotlib
    axes[0].hist(edades, bins=20, color='orange', edgecolor='black')
    axes[0].set_title('Matplotlib')

    # Seaborn
    sns.histplot(data=df_edades, x='Edad', bins=20, kde=True, color='orange', ax=axes[1])
    axes[1].set_title('Seaborn')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    if mostrar_codigo:
        st.code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('4. Histograma: Distribución de Edades', fontsize=14, fontweight='bold')

# Matplotlib
axes[0].hist(edades, bins=20, color='orange', edgecolor='black')
axes[0].set_title('Matplotlib')

# Seaborn
sns.histplot(data=df_edades, x='Edad', bins=20, kde=True, color='orange', ax=axes[1])
axes[1].set_title('Seaborn')

plt.tight_layout()
plt.show()
        """, language="python")

def render_grafico_5():
    st.header("5. Gráfico de Cajas (`Distribución de Salarios`)")
    st.info(
        "**Justificación y análisis:**\n\n"
        "Es la herramienta idónea para resumir mediante cuartiles y comparar de un vistazo la distribución, simetría y dispersión de una variable numérica (`Salario`) "
        "entre distintos grupos (`Departamento 1` y `Departamento 2`). Permite observar que el Departamento 2 cuenta con salarios más altos "
        "—con una mediana cercana a los 60.000 frente a los 50.000 del Departamento 1—, pero también presenta una mayor desigualdad salarial reflejada "
        "en una caja y unos bigotes más alargados, además de mostrar puntos aislados fuera de los límites que identifican empleados con sueldos atípicos."
    )
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('5. Gráfico de Cajas: Distribución de Salarios', fontsize=14, fontweight='bold')

    # Matplotlib
    try:
        axes[0].boxplot(salarios, tick_labels=['Departamento 1', 'Departamento 2'])
    except TypeError:
        axes[0].boxplot(salarios, labels=['Departamento 1', 'Departamento 2'])
    axes[0].set_title('Matplotlib')

    # Seaborn
    sns.boxplot(data=df_box, x='Departamento', y='Salario', ax=axes[1])
    axes[1].set_title('Seaborn')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    if mostrar_codigo:
        st.code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('5. Gráfico de Cajas: Distribución de Salarios', fontsize=14, fontweight='bold')

# Matplotlib
axes[0].boxplot(salarios, tick_labels=['Departamento 1', 'Departamento 2'])
axes[0].set_title('Matplotlib')

# Seaborn
sns.boxplot(data=df_box, x='Departamento', y='Salario', ax=axes[1])
axes[1].set_title('Seaborn')

plt.tight_layout()
plt.show()
        """, language="python")

# =============================================================================
# RENDERIZADO SEGÚN EL MODO DE VISTA SELECCIONADO
# =============================================================================

if modo_vista == "📜 Cuaderno Completo (Flujo continuo)":
    # 0. Importación y datos
    render_seccion_datos()
    st.divider()
    # 1. Líneas
    render_grafico_1()
    st.divider()
    # 2. Barras
    render_grafico_2()
    st.divider()
    # 3. Dispersión
    render_grafico_3()
    st.divider()
    # 4. Histograma
    render_grafico_4()
    st.divider()
    # 5. Boxplot
    render_grafico_5()

else:
    # Vista en pestañas
    t0, t1, t2, t3, t4, t5 = st.tabs([
        "📋 Datos",
        "📈 1. Líneas",
        "📊 2. Barras",
        "🟢 3. Dispersión",
        "🟣 4. Histograma",
        "📦 5. Cajas"
    ])
    
    with t0:
        render_seccion_datos()
    with t1:
        render_grafico_1()
    with t2:
        render_grafico_2()
    with t3:
        render_grafico_3()
    with t4:
        render_grafico_4()
    with t5:
        render_grafico_5()
