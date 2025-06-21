
import streamlit as st
import pandas as pd
import datetime
import os
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Mapa de iPhones robados", layout="wide")

st.title("📍 Mapa colaborativo de iPhones robados")
st.subheader("🔓 Compartir mi ubicación actual (modo 'móvil robado')")

# Solicitar ubicación
coords = st_javascript("""
new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            resolve({latitude: position.coords.latitude, longitude: position.coords.longitude});
        },
        (err) => {
            resolve({error: err.message});
        }
    );
});
""")

# Feedback claro según resultado de geolocalización
if coords is None:
    st.info("Solicitando acceso a la ubicación...")
elif "error" in coords:
    st.warning(f"Error al obtener ubicación: {coords['error']}")
elif "latitude" in coords:
    st.success(f"Ubicación detectada: {coords['latitude']}, {coords['longitude']}")
    if st.button("📍 Enviar esta ubicación al mapa"):
        nuevo_reporte = pd.DataFrame([{
            "modelo": "Seguimiento en tiempo real",
            "imei": "",
            "latitud": coords['latitude'],
            "longitud": coords['longitude'],
            "fecha": datetime.datetime.now().date(),
            "hora": datetime.datetime.now().time(),
            "comentarios": "Ubicación enviada en tiempo real"
        }])
        nuevo_reporte.to_csv("database.csv", mode="a", header=False, index=False)
        st.success("Ubicación enviada correctamente.")
        st.rerun()

# Debug opcional (mostrar contenido crudo de coords)
st.write("DEBUG: ", coords)

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
