
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Mapa de iPhones robados", layout="wide")

st.title("📍 Mapa colaborativo de iPhones robados")

st.subheader("🔓 Compartir mi ubicación actual (modo 'móvil robado')")

st.markdown("""
Para obtener tu ubicación automáticamente desde tu móvil, haz clic en el siguiente botón y copia tus coordenadas:

👉 [Obtener mi ubicación actual](https://www.google.com/maps) 

Una vez abierta la app de Google Maps:
1. Toca el punto azul que representa tu ubicación.
2. Copia la latitud y longitud.
3. Pega los valores en el formulario manualmente aquí abajo.
""")

# Cargar base de datos
DB_PATH = "database.csv"
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        f.write("modelo,imei,latitud,longitud,fecha,hora,comentarios\n")

df = pd.read_csv(DB_PATH)

# Mostrar mapa
st.subheader("🗺️ Mapa de reportes")
if not df.empty:
    st.map(df.rename(columns={"latitud": "latitude", "longitud": "longitude"}))
else:
    st.info("Aún no hay reportes. Sé el primero en agregar uno.")

# Formulario
st.subheader("📝 Reportar un móvil robado")

with st.form("form_reporte"):
    col1, col2 = st.columns(2)
    with col1:
        modelo = st.text_input("Modelo del iPhone")
        imei = st.text_input("IMEI (opcional)")
        lat = st.number_input("Latitud", format="%.6f")
    with col2:
        comentarios = st.text_area("Comentarios (opcional)")
        lon = st.number_input("Longitud", format="%.6f")
        now = datetime.datetime.now()
        fecha = st.date_input("Fecha del robo", now.date())
        hora = st.time_input("Hora aproximada", now.time())

    submitted = st.form_submit_button("📌 Agregar reporte")

    if submitted:
        nuevo_reporte = pd.DataFrame([{
            "modelo": modelo,
            "imei": imei,
            "latitud": lat,
            "longitud": lon,
            "fecha": fecha,
            "hora": hora,
            "comentarios": comentarios
        }])
        nuevo_reporte.to_csv(DB_PATH, mode="a", header=False, index=False)
        st.success("Reporte agregado correctamente.")
        st.rerun()
