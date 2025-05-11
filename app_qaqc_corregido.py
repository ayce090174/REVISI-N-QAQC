
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="App QA/QC HDPE", layout="wide")
st.title("Sistema QA/QC - DEMO Online")

# Verifica si el archivo CSV existe
if not os.path.exists("demo_qaqc_data.csv"):
    st.error("⚠️ El archivo de datos 'demo_qaqc_data.csv' no fue encontrado. Por favor súbelo al mismo repositorio.")
else:
    # Cargar datos
    df = pd.read_csv("demo_qaqc_data.csv")

    # Filtros
    st.subheader("🔍 Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        fechas = st.multiselect("Fecha", sorted(df["Fecha"].dropna().unique()))
        operadores = st.multiselect("Operador", sorted(df["Operador"].dropna().unique()))
    with col2:
        estados = st.multiselect("Estado", sorted(df["Estado"].dropna().unique()))
        maquinas = st.multiselect("Máquina", sorted(df["Máquina"].dropna().unique()))

    # Aplicar filtros
    df_filtrado = df.copy()
    if fechas:
        df_filtrado = df_filtrado[df_filtrado["Fecha"].isin(fechas)]
    if operadores:
        df_filtrado = df_filtrado[df_filtrado["Operador"].isin(operadores)]
    if estados:
        df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estados)]
    if maquinas:
        df_filtrado = df_filtrado[df_filtrado["Máquina"].isin(maquinas)]

    # Mostrar tabla
    st.subheader("📋 Registros QA/QC")
    st.dataframe(df_filtrado, use_container_width=True)

    # Descargar CSV
    st.download_button(
        label="📥 Descargar Excel filtrado",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="registros_qaqc.csv",
        mime="text/csv"
    )
