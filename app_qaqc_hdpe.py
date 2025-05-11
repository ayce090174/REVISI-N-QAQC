
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="App QA/QC HDPE", layout="wide")

st.title("Sistema QA/QC - Registro de Uniones HDPE")

# Inicialización de datos
if "data" not in st.session_state:
    st.session_state.data = []

# Formulario de ingreso
with st.form("Ingreso de Unión"):
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("Fecha", value=datetime.today())
        hora = st.time_input("Hora", value=datetime.now().time())
        operador = st.text_input("Operador")
        certificado = st.text_input("N° Certificado Operador")
    with col2:
        maquina = st.text_input("Máquina")
        calibracion = st.text_input("Registro Calibración")
        tipo_union = st.selectbox("Tipo de Unión", ["Butt Fusion", "Electrofusión"])
        n_union = st.text_input("N° de Unión")
    with col3:
        estado = st.selectbox("Estado", ["Aprobada", "Rechazada", "Observada"])
        observacion = st.text_input("Observación")
        temp_plato = st.number_input("T° Plato Calefactor (°C)", min_value=0)
        ensayo = st.text_input("Tipo Ensayo Destructivo")
        por_ejecutar = st.number_input("Por Ejecutar (m)", min_value=0)

    submitted = st.form_submit_button("Registrar Unión")
    if submitted:
        nueva_fila = {
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Hora": hora.strftime("%H:%M"),
            "Operador": operador,
            "N° Certificado Operador": certificado,
            "Máquina": maquina,
            "Registro Calibración": calibracion,
            "Tipo de Unión": tipo_union,
            "N° de Unión": n_union,
            "Estado": estado,
            "Observación": observacion,
            "T° Plato Calefactor (°C)": temp_plato,
            "Tipo Ensayo Destructivo": ensayo,
            "Por Ejecutar (m)": por_ejecutar
        }
        st.session_state.data.append(nueva_fila)
        st.success("Unión registrada correctamente.")

# Mostrar tabla de registros
st.subheader("Registros Ingresados")
df = pd.DataFrame(st.session_state.data)
st.dataframe(df)

# Exportación
st.download_button("Descargar Excel", data=df.to_csv(index=False).encode("utf-8"), file_name="registros_qaqc.csv", mime="text/csv")
