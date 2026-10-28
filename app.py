
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from scipy.io import arff
from pathlib import Path

st.set_page_config(
    page_title="Experimento",
    page_icon="👋",
    layout = "wide"
)

st.title("📊 Mortalidad en Ataques Cardiacos")

st.write("Bienvenido a la aplicación de visualización de datos: Viaje Cósmico.")

archivo = st.file_uploader(
    "Seleccione un archivo",
    type=["csv", "xlsx", "arff"]
)

if archivo is not None:

    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    elif archivo.name.endswith(".arff"):
        import io
        # Leer el archivo cargado y convertirlo a texto
        contenido = archivo.getvalue().decode("utf-8-sig")
        # Crear un archivo de texto en memoria
        archivo_texto = io.StringIO(contenido)
        # Leer el archivo ARFF
        datos, metadata = arff.loadarff(archivo_texto)
        # Convertir a DataFrame
        df = pd.DataFrame(datos)
    else:
        df = pd.read_excel(archivo)
    
    # CONVERSIÓN DE BYTES A TEXTO
    # =====================================

    for columna in df.select_dtypes(include=["object"]).columns:

        df[columna] = df[columna].map(
            lambda x: x.decode("utf-8")
            if isinstance(x, bytes)
            else x)

    # =====================================
      # =====================================
    # GRÁFICA DE DIABETES
    # =====================================

    st.subheader("Descriptivo Diabetes")

    fig1, ax1 = plt.subplots(figsize=(4, 4))

    df["Diabetes"].value_counts().plot(kind="bar",ax=ax1)

    ax1.set_title("Distribución de Diabetes")
    ax1.set_xlabel("Diabetes")
    ax1.set_ylabel("Número de pacientes")

    plt.setp(ax1.get_xticklabels(), rotation=0)

    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # =====================================
    # GRÁFICA DE SEXO
    # =====================================

    st.subheader("Descriptivo Sexo")

    fig2, ax2 = plt.subplots(figsize=(4, 4))

    df["Sexo"].value_counts().plot(kind="barh",ax=ax2)

    ax2.set_title("Distribución por Sexo")
    ax2.set_xlabel("Sexo")
    ax2.set_ylabel("Número de pacientes")

    plt.setp(ax2.get_xticklabels(), rotation=0)

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # =====================================
    # ESTADÍSTICAS DESCRIPTIVAS
    # =====================================

    st.subheader("Estadísticas descriptivas")

    st.dataframe(df.describe(include="all"))

# =========================================
# INFORME EXPLORATORIO HTML
# =========================================

st.divider()

st.header("Informe exploratorio de los datos")

ruta_html = (Path(__file__).resolve().parent/ "mortalidad_ataque_cardiaco.html")

if ruta_html.exists():

    with open(
        ruta_html,
        "r",
        encoding="utf-8"
    ) as archivo_html:

        html = archivo_html.read()

    components.html(
        html,
        height=900,
        scrolling=True
    )

else:

    st.info("El informe exploratorio HTML "
        "todavía no está disponible.")
