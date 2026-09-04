import os
import time
import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from pydub import AudioSegment

# Configuración de página con ícono y título personalizado
st.set_page_config(
    page_title="Convertidor Multiformato v2.0",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados (Animaciones, Gradientes y Ocultar Menú)
st.markdown("""
    <style>
    /* Ocultar menú superior y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo principal con gradiente suave */
    .stApp {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
    }

    /* Estilo de la barra lateral */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Botones de navegación en la barra lateral */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: white;
        color: #2c3e50;
        font-weight: 600;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.08);
        padding: 10px 16px;
        text-align: left;
        margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
    }

    div[data-testid="stSidebar"] .stButton > button:hover {
        background: #f0f4f8;
        transform: translateX(3px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        color: #00f2fe;
    }

    /* Tarjetas contenedoras modernas */
    div.stCard {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }

    /* Botones de acción principales (Convertir) */
    .main .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,242,254,0.4);
    }
    
    .main .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,242,254,0.6);
        color: white;
    }

    /* Encabezados */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal con ícono animado
st.markdown("<h1 style='text-align: center;'>🔄 Convertidor de Archivos v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a5568;'>Transforma tus archivos al instante de forma rápida, segura y privada.</p>", unsafe_allow_html=True)
st.write("---")

# Estado de la categoría en la sesión
if "categoria" not in st.session_state:
    st.session_state.categoria = "🖼️ Imágenes"

# Menú lateral interactivo con botones estilizados
st.sidebar.markdown("<h3 style='text-align: center;'>Categorías</h3>", unsafe_allow_html=True)

if st.sidebar.button("🖼️ Imágenes", use_container_width=True):
    st.session_state.categoria = "🖼️ Imágenes"

if st.sidebar.button("📄 PDF a Imagen", use_container_width=True):
    st.session_state.categoria = "📄 PDF a Imagen"

if st.sidebar.button("🎵 Audio", use_container_width=True):
    st.session_state.categoria = "🎵 Audio"

categoria = st.session_state.categoria

# --- CATEGORÍA: IMÁGENES ---
if categoria == "🖼️ Imágenes":
    st.markdown("### 🖼️ Conversión de Imágenes")
    
    archivo = st.file_uploader("Arrastra o selecciona tu imagen", type=["png", "jpg", "jpeg", "webp", "bmp"])
    
    if archivo:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(archivo, caption="Vista previa del archivo original", use_container_width=True)
            
        with col2:
            formato_salida = st.selectbox("Selecciona el formato de salida:", ["PNG", "JPEG", "WEBP", "BMP", "PDF"])
            
            if st.button("✨ Convertir Imagen"):
                with st.spinner("Procesando y optimizando imagen..."):
                    time.sleep(1) # Simulación de animación
                    img = Image.open(archivo)
                    if formato_salida in ["JPEG", "PDF"] and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    nombre_base = os.path.splitext(archivo.name)[0]
                    ext = formato_salida.lower()
                    nombre_salida = f"{nombre_base}.{ext}"
                    img.save(nombre_salida, format=formato_salida)
                    
                st.success("¡Conversión completada con éxito!")
                st.balloons() # Animación de celebración
                
                with open(nombre_salida, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar Imagen Convertida",
                        data=f,
                        file_name=nombre_salida,
                        mime=f"image/{ext}" if ext != "pdf" else "application/pdf"
                    )

# --- CATEGORÍA: DOCUMENTOS ---
elif categoria == "📄 PDF a Imagen":
    st.markdown("### 📄 Convertir Documentos PDF a Imagen")
    archivo = st.file_uploader("Carga tu archivo PDF", type=["pdf"])
    
    if archivo:
        if st.button("✨ Convertir Primera Página a PNG"):
            with st.spinner("Extrayendo página del PDF..."):
                time.sleep(1)
                imagenes = convert_from_bytes(archivo.read())
                if imagenes:
                    nombre_salida = f"{os.path.splitext(archivo.name)[0]}_pagina1.png"
                    imagenes[0].save(nombre_salida, "PNG")
                    
            st.success("¡Página convertida exitosamente!")
            st.balloons()
            
            with open(nombre_salida, "rb") as f:
                st.download_button("⬇️ Descargar Imagen PNG", f, file_name=nombre_salida, mime="image/png")

# --- CATEGORÍA: AUDIO ---
elif categoria == "🎵 Audio":
    st.markdown("### 🎵 Conversión de Archivos de Audio")
    archivo = st.file_uploader("Carga tu pista de audio", type=["mp3", "wav", "ogg", "flac"])
    
    if archivo:
        formato_salida = st.selectbox("Selecciona el nuevo formato:", ["mp3", "wav", "ogg"])
        if st.button("✨ Convertir Audio"):
            with st.spinner("Procesando archivo de audio..."):
                fmt_origen = os.path.splitext(archivo.name)[1].replace(".", "")
                audio = AudioSegment.from_file(archivo, format=fmt_origen)
                
                nombre_salida = f"{os.path.splitext(archivo.name)[0]}.{formato_salida}"
                audio.export(nombre_salida, format=formato_salida)
                
            st.success("¡Audio convertido correctamente!")
            st.balloons()
            
            with open(nombre_salida, "rb") as f:
                st.download_button("⬇️ Descargar Pista de Audio", f, file_name=nombre_salida, mime=f"audio/{formato_salida}")