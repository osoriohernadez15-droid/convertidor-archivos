import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from pydub import AudioSegment
from pdf2image import convert_from_path
import tempfile
import os

# Configuración básica de la aplicación
st.set_page_config(
    page_title="Convertidor de Archivos Gratis - PNG, JPG, MP3, PDF",
    page_icon="🔄",
    layout="wide"
)

# ---------------------------------------------------------
# PUBLICIDAD DE ADSTERRA (BARRA LATERAL)
# ---------------------------------------------------------
with st.sidebar:
    st.header("Patrocinado")
    
    codigo_adsterra = """
    <div style="text-align: center;">
        <script type="text/javascript">
            atOptions = {
                'key' : '67b9aefc9d19cf7842d8c70ed4d7e904',
                'format' : 'iframe',
                'height' : 250,
                'width' : 300,
                'params' : {}
            };
        </script>
        <script type="text/javascript" src="https://www.highrevenueformat.com/67b9aefc9d19cf7842d8c70ed4d7e904/invoke.js"></script>
    </div>
    """
    
    components.html(codigo_adsterra, height=270)
    st.caption("Publicidad para mantener esta herramienta gratuita.")

# ---------------------------------------------------------
# APLICACIÓN PRINCIPAL - CONVERTIDOR DE ARCHIVOS
# ---------------------------------------------------------
st.title("🔄 Convertidor de Archivos Online Gratuito")
st.write("""
Bienvenido al **Convertidor de Archivos en Línea**. Esta herramienta gratuita te permite **convertir imágenes (PNG, JPG, WEBP), archivos de audio (MP3, WAV, OGG) y documentos PDF a imagen** de manera rápida, segura y sin necesidad de instalar ningún software en tu equipo.
""")

# Pestañas para organizar las herramientas
tab_img, tab_audio, tab_pdf = st.tabs(["🖼️ Convertir Imágenes", "🎵 Convertir Audio", "📄 Convertir PDF a Imagen"])

# --- TAB 1: CONVERTIDOR DE IMÁGENES ---
with tab_img:
    st.subheader("Convertidor de Imágenes Online (PNG, JPG, WEBP, BMP)")
    st.write("Cambia el formato de tus fotos e imágenes al instante.")
    img_file = st.file_uploader("Sube una imagen (PNG, JPG, WEBP, BMP)", type=["png", "jpg", "jpeg", "webp", "bmp"], key="img_up")
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Vista previa", width=250)
        
        target_format = st.selectbox("Convertir a:", ["PNG", "JPEG", "WEBP", "BMP"], key="img_fmt")
        
        if st.button("Convertir Imagen", key="btn_img"):
            buffer = tempfile.NamedTemporaryFile(delete=False, suffix=f".{target_format.lower()}")
            
            if target_format == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            img.save(buffer.name, format=target_format)
            
            with open(buffer.name, "rb") as file:
                st.download_button(
                    label=f"⬇️ Descargar en {target_format}",
                    data=file,
                    file_name=f"imagen_convertida.{target_format.lower()}",
                    mime=f"image/{target_format.lower()}"
                )

# --- TAB 2: CONVERTIDOR DE AUDIO ---
with tab_audio:
    st.subheader("Convertidor de Audio Gratis (MP3, WAV, OGG, FLAC)")
    st.write("Transforma tus archivos de sonido a formatos compatibles con cualquier reproductor.")
    audio_file = st.file_uploader("Sube un archivo de audio (MP3, WAV, OGG, FLAC)", type=["mp3", "wav", "ogg", "flac"], key="audio_up")
    
    if audio_file:
        st.audio(audio_file)
        audio_format = st.selectbox("Convertir a:", ["MP3", "WAV", "OGG"], key="audio_fmt")
        
        if st.button("Convertir Audio", key="btn_audio"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp_in:
                tmp_in.write(audio_file.read())
                in_path = tmp_in.name
                
            sound = AudioSegment.from_file(in_path)
            out_path = f"{in_path}_out.{audio_format.lower()}"
            sound.export(out_path, format=audio_format.lower())
            
            with open(out_path, "rb") as file:
                st.download_button(
                    label=f"⬇️ Descargar Audio en {audio_format}",
                    data=file,
                    file_name=f"audio_convertido.{audio_format.lower()}",
                    mime=f"audio/{audio_format.lower()}"
                )

# --- TAB 3: CONVERTIDOR DE PDF ---
with tab_pdf:
    st.subheader("Convertidor de PDF a Imagen PNG")
    st.write("Extrae las páginas de tus documentos PDF y conviértelas en imágenes PNG de alta calidad.")
    pdf_file = st.file_uploader("Sube un documento PDF", type=["pdf"], key="pdf_up")
    
    if pdf_file:
        if st.button("Convertir PDF", key="btn_pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(pdf_file.read())
                pdf_path = tmp_pdf.name
                
            images = convert_from_path(pdf_path)
            st.success(f"¡Se convirtieron {len(images)} página(s)!")
            
            for i, page_img in enumerate(images):
                buf = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                page_img.save(buf.name, format="PNG")
                
                with open(buf.name, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Descargar Página {i+1} (PNG)",
                        data=f,
                        file_name=f"pagina_{i+1}.png",
                        mime="image/png",
                        key=f"dl_pdf_{i}"
                    )

# Pie de página con información SEO
st.markdown("---")
st.markdown("### ¿Por qué utilizar nuestro Convertidor de Archivos Gratuito?")
st.markdown("""
* **100% Gratuito y sin registro:** Convierte tus archivos al instante sin necesidad de crear una cuenta.
* **Seguridad garantizada:** Tus archivos procesados se eliminan de nuestros servidores temporales de forma automática.
* **Soporte multiformato:** Soporta imágenes PNG, JPG, WEBP, audios MP3, WAV y documentos PDF.
""")
