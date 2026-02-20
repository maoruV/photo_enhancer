import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='torchvision')

from gfpgan import GFPGANer
from config import CONFIG, CONFIG_REALESRGAN
from zeroscratches import EraseScratches
from src.utils import bgr_to_pil, pil_to_bgr
import streamlit as st
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet



class ImageEnhancer:
    """Clase para manejar el modelo GFPGAN y el procesamiento de imagenes."""
    def __init__(self):
        self.model = None
        self.model_with_bg = None
        self._scratch_eraser = None
        
    @property   
    def scratch_eraser(self):
        """Carga el modelo para eliminar arañazos"""
        if self._scratch_eraser is None:
            self._scratch_eraser = EraseScratches()
        return self._scratch_eraser
    
    def _remove_scratches(self, image_bgr):
        """Elimina rayas o grietas antes de pasar a GFPGAN."""
        pil_img = bgr_to_pil(image_bgr)
        restored_rgb = self.scratch_eraser.erase(pil_img)
        restored_bgr = pil_to_bgr(restored_rgb)
        return restored_bgr
    
    @st.cache_resource
    def load_model_simple(_self):
        """Carga GFPGAN para la mejora de cara"""
        model = GFPGANer(
            model_path=CONFIG["model_url"],
            upscale=CONFIG["upscale"],
            arch=CONFIG["arch"],
            channel_multiplier=CONFIG["channel_multiplier"],
            bg_upsampler=None
        )
        return model
    
    @st.cache_resource
    def load_model_with_background(_self):
        """Carga GFPGAN con RealESRGAN para mejorar la imagen y el fondo"""
        with st.spinner("Cargando GFPGAN + RealESRGAN..."):
            model_bg = RRDBNet(
                num_in_ch=3,      # 3 canales de entrada (RGB)
                num_out_ch=3,     # 3 canales de salida (RGB)
                num_feat=64,      # Número de canales intermedios
                num_block=23,     # Número de bloques RRDB
                num_grow_ch=32,   # Número de canales de crecimiento
                scale=2           # Factor de escalado
            )
        # Inicializa el upscaler con el modelo RRDBNet
        bg_upsampler = RealESRGANer(
            model_path=CONFIG_REALESRGAN["model_url"],
            model=model_bg,
            tile=CONFIG_REALESRGAN["tile"],
            tile_pad=CONFIG_REALESRGAN["tile_pad"],
            pre_pad=CONFIG_REALESRGAN["pre_pad"],
            half=CONFIG_REALESRGAN["half"],
            scale=CONFIG_REALESRGAN["scale"]
        )
        
        model = GFPGANer(
                model_path=CONFIG['model_url'],
                upscale=CONFIG['upscale'],
                arch=CONFIG['arch'],
                channel_multiplier=CONFIG['channel_multiplier'],
                bg_upsampler=bg_upsampler
            )
        return model
    
    def enhance(self, image_bgr, repair_scratches=False, enhance_background=False):
        """Mejora una imagen con opciones configurables.
        
        Args:
            image_bgr: Imagen en formato BGR
        """
        if repair_scratches:
            st.info("🔧 Reaparando grietas y arañazos...")
            image_bgr = self._remove_scratches(image_bgr)
            
        if enhance_background:
            st.info("✨ Mejorando caras y fondo...")
            if self.model_with_bg is None:
                self.model_with_bg = self.load_model_with_background()
            model = self.model_with_bg
        else:
            st.info("✨ Mejorando caras...")
            if self.model is None:
                self.model = self.load_model_simple()
            model = self.model
            
        _, _, restored_img = model.enhance(
            image_bgr,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=CONFIG["enhancement_weight"]
        )
        return restored_img
            
