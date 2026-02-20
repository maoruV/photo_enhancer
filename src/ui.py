import streamlit as st
import numpy as np
from config import CONFIG
from PIL import Image
import cv2
import io


def render_header():
    """Renderiza el encabezado de la aplicación."""
    st.title("✨ Mejorador de Calidad de Fotos")
    st.markdown("Sube una foto y mejora su calidad con IA (GFPGAN)")


def render_file_uploader():
    """
    Renderiza el componente de carga de archivos.
    
    Returns:
        UploadedFile o None
    """
    
    uploaded_file = st.file_uploader(
        "Selecciona una imagen", 
        type=CONFIG['allowed_extensions'],
        help="Sube una foto para mejorar su calidad"
    )
    return uploaded_file


def render_interactive_slider(original_image, restored_image):
    """
    Renderiza el comparador interactivo con slider.
    
    Args:
        original_image: Imagen original (PIL Image)
        restored_image: Imagen restaurada (PIL Image)
    """
    st.markdown("---")
    st.subheader("🔄 Comparador Interactivo")
    
    slider_value = st.slider(
        "Desliza para comparar",
        min_value=0,
        max_value=100,
        value=50,
        label_visibility="collapsed"
    )
    
    # Asegurar mismo tamaño
    if original_image.size != restored_image.size:
        restored_image = restored_image.resize(original_image.size, Image.LANCZOS)
    
    # Crear imagen dividida
    width = original_image.width
    split_pos = int(width * slider_value / 100)
    
    combined = Image.new('RGB', original_image.size)
    combined.paste(original_image.crop((0, 0, split_pos, original_image.height)), (0, 0))
    combined.paste(restored_image.crop((split_pos, 0, width, original_image.height)), (split_pos, 0))
    
    # Añadir línea divisoria
    combined_array = np.array(combined)
    cv2.line(combined_array, (split_pos, 0), (split_pos, combined.height), (255, 255, 255), 3)
    
    st.image(combined_array, width='stretch')


def render_download_button(restored_image):
    """
    Renderiza el botón de descarga.
    
    Args:
        restored_image: Imagen restaurada (PIL Image)
    """
    st.markdown("---")
    buf = io.BytesIO()
    restored_image.save(buf, format='PNG')
    st.download_button(
        label="💾 Descargar Imagen Mejorada",
        data=buf.getvalue(),
        file_name="foto_mejorada.png",
        mime="image/png",
        width='stretch'
    )


def render_instructions():
    """Renderiza las instrucciones de uso."""
    st.info("👆 Sube una imagen para comenzar")
    
    with st.expander("ℹ️ ¿Cómo funciona?"):
        st.markdown("""
        1. **Sube una foto** usando el botón de arriba
        2. **Selecciona opciones** de procesamiento (opcional):
           - 🔧 **Reparar grietas**: Elimina rayas y arañazos
           - ✨ **Mejorar fondo**: Mejora calidad del fondo (más lento)
        3. **Haz clic en "Mejorar Calidad"** y espera unos segundos
        4. **Compara los resultados** con el slider interactivo
        5. **Descarga** tu foto mejorada
        
        **Ideal para:**
        - 📸 Fotos antiguas o de baja resolución
        - 👤 Retratos y selfies
        - 🖼️ Imágenes con caras borrosas
        - 🔧 Fotos con grietas o arañazos
        """)

def render_footer():
    """Renderiza el pie de página."""
    # Contenido del footer
    footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #1f91dc;
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 12px;
}
</style>
<div class="footer">
    <p> <center>Desarrollado con esfuerzo y practica  con GFPGAN y Streamlit</center>|
</div>
"""
    st.markdown(footer, unsafe_allow_html=True)
    
    
    
    
    