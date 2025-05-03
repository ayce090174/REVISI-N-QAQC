
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
from io import BytesIO
from fpdf import FPDF

st.set_page_config(layout="wide")
st.sidebar.title("Navegación")
seccion = st.sidebar.radio("Ir a:", ["Ingreso", "Reportes", "Exportar"])

csv_path = "registros_hdpe.csv"

def cargar_datos():
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=["Fecha", "Hora", "Operador", "Máquina", "Unión", "Estado", "Observaciones"])

def guardar_datos(df):
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

df = cargar_datos()

if seccion == "Ingreso":
    with st.form("registro_form"):
        st.subheader("📋 Ingreso de Uniones Múltiples")
        fecha = st.date_input("Fecha", datetime.today())
        operador = st.text_input("Operador")
        maquina = st.text_input("Máquina")
        cantidad_uniones = st.number_input("Cantidad de uniones", min_value=1, max_value=50, value=1)

        registros = []
        for i in range(cantidad_uniones):
            st.markdown("---")
st.subheader(f"Unión #{i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                hora = st.time_input(f"Hora unión #{i+1}", value=time(8, 0), key=f"hora_{i}")
            with col2:
                estado = st.selectbox(f"Estado unión #{i+1}", ["Aprobado", "Rechazado", "Observado"], key=f"estado_{i}")
            with col3:
                observacion = st.text_input(f"Observación #{i+1}", key=f"obs_{i}")
            
            registros.append({
                "Fecha": fecha,
                "Hora": hora.strftime("%H:%M"),
                "Operador": operador,
                "Máquina": maquina,
                "Unión": 1,
                "Estado": estado,
                "Observaciones": observacion
            })

        submitted = st.form_submit_button("Registrar")
        if submitted:
            df = pd.concat([df, pd.DataFrame(registros)], ignore_index=True)
            guardar_datos(df)
            st.success(f"✅ {len(registros)} uniones registradas exitosamente.")

if seccion == "Reportes":
    st.subheader("📋 Registros")
    st.dataframe(df)

    st.subheader("📊 Indicadores")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de uniones", int(df["Unión"].astype(int).sum()) if not df.empty else 0)
    with col2:
        st.metric("Aprobadas", int((df["Estado"] == "Aprobado").sum()) if not df.empty else 0)
    with col3:
        st.metric("Rechazadas / Observadas", int((df["Estado"] != "Aprobado").sum()) if not df.empty else 0)

    if not df.empty:
        st.subheader("📈 Producción por Operador")
        fig1, ax1 = plt.subplots()
        df.groupby("Operador")["Unión"].sum().plot(kind="bar", color="green", ax=ax1)
        ax1.set_ylabel("Cantidad de Uniones")
        st.pyplot(fig1)

        st.subheader("📉 Producción por Máquina")
        fig2, ax2 = plt.subplots()
        df.groupby("Máquina")["Unión"].sum().plot(kind="bar", color="blue", ax=ax2)
        ax2.set_ylabel("Cantidad de Uniones")
        st.pyplot(fig2)

        st.subheader("🕒 Producción por Hora")
        fig3, ax3 = plt.subplots()
        df.groupby("Hora")["Unión"].sum().sort_index().plot(kind="bar", color="purple", ax=ax3)
        ax3.set_ylabel("Cantidad de Uniones")
        st.pyplot(fig3)

        st.subheader("📊 Distribución por Estado")
        fig4, ax4 = plt.subplots()
        df["Estado"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax4)
        ax4.set_ylabel("")
        ax4.set_title("Distribución de Estados")
        st.pyplot(fig4)

if seccion == "Exportar":
    st.subheader("📤 Exportar Datos")
    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    buffer.seek(0)
    st.download_button("📥 Descargar Excel", data=buffer, file_name="registro_hdpe.csv", mime="text/csv")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Reporte QA/QC HDPE", ln=True, align="C")
            self.ln(10)

    if st.button("📄 Descargar PDF con KPIs"):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Total de uniones: {int(df['Unión'].astype(int).sum())}", ln=True)
        pdf.cell(0, 10, f"Aprobadas: {df[df['Estado'] == 'Aprobado'].shape[0]}", ln=True)
        pdf.cell(0, 10, f"Rechazadas/Observadas: {df[df['Estado'].isin(['Rechazado','Observado'])].shape[0]}", ln=True)
        pdf.ln(10)
        pdf.output("reporte_hdpe.pdf")
        with open("reporte_hdpe.pdf", "rb") as f:
            st.download_button("⬇️ Descargar PDF", f, file_name="reporte_hdpe.pdf", mime="application/pdf")
