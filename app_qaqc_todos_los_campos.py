
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="App QA/QC HDPE", layout="wide")
st.title("Sistema QA/QC HDPE - DEMO ONLINE")

# Verificar si el CSV está presente
if not os.path.exists("demo_qaqc_data.csv"):
    st.error("⚠️ El archivo 'demo_qaqc_data.csv' no fue encontrado.")
else:
    df = pd.read_csv("demo_qaqc_data.csv")

    # Mostrar filtros
    st.subheader("🔍 Filtros de búsqueda")
    col1, col2, col3 = st.columns(3)
    with col1:
        fechas = st.multiselect("Fecha", sorted(df["Fecha"].dropna().unique()))
        operadores = st.multiselect("Operador", sorted(df["Operador"].dropna().unique()))
        maquinas = st.multiselect("Máquina", sorted(df["Máquina"].dropna().unique()))
    with col2:
        estados = st.multiselect("Estado", sorted(df["Estado"].dropna().unique()))
        tipos_union = st.multiselect("Tipo de Unión", sorted(df["Tipo de Unión"].dropna().unique()))
        certificados = st.multiselect("N° Certificado Operador", sorted(df["N° Certificado Operador"].dropna().unique()))
    with col3:
        ensayos = st.multiselect("Tipo Ensayo Destructivo", sorted(df["Tipo Ensayo Destructivo"].dropna().unique()))
        temperaturas = st.slider("T° Plato Calefactor (°C)", min_value=150, max_value=250, value=(150, 250))
        por_ejecutar = st.slider("Por Ejecutar (m)", min_value=0, max_value=20, value=(0, 20))

    # Aplicar filtros
    df_filtrado = df.copy()
    if fechas:
        df_filtrado = df_filtrado[df_filtrado["Fecha"].isin(fechas)]
    if operadores:
        df_filtrado = df_filtrado[df_filtrado["Operador"].isin(operadores)]
    if maquinas:
        df_filtrado = df_filtrado[df_filtrado["Máquina"].isin(maquinas)]
    if estados:
        df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estados)]
    if tipos_union:
        df_filtrado = df_filtrado[df_filtrado["Tipo de Unión"].isin(tipos_union)]
    if certificados:
        df_filtrado = df_filtrado[df_filtrado["N° Certificado Operador"].isin(certificados)]
    if ensayos:
        df_filtrado = df_filtrado[df_filtrado["Tipo Ensayo Destructivo"].isin(ensayos)]
    df_filtrado = df_filtrado[
        (df_filtrado["T° Plato Calefactor (°C)"] >= temperaturas[0]) &
        (df_filtrado["T° Plato Calefactor (°C)"] <= temperaturas[1]) &
        (df_filtrado["Por Ejecutar (m)"] >= por_ejecutar[0]) &
        (df_filtrado["Por Ejecutar (m)"] <= por_ejecutar[1])
    ]

    # Mostrar resultados
    st.subheader("📋 Registros Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

    # Exportar CSV
    st.download_button(
        label="📥 Descargar Registros en Excel",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="registros_qaqc_filtrados.csv",
        mime="text/csv"
    )
