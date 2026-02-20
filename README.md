# ✨ IA Photo Enhancer - Restauración de Fotos con Inteligencia Artificial

Este proyecto es una aplicación web potente e intuitiva diseñada para restaurar y mejorar fotografías antiguas o dañadas utilizando modelos avanzados de Inteligencia Artificial.

## 🚀 ¿Cómo funciona?

La aplicación utiliza una combinación de redes neuronales especializadas para diferentes tareas de mejora:

- **Restauración de Rostros (GFPGAN):** Detecta y reconstruye rostros en baja resolución o dañados, devolviendo nitidez y detalles naturales.
- **Mejora de Fondo (Real-ESRGAN):** Escala la imagen y mejora la textura del fondo y elementos no faciales.
- **Reparación de Grietas (ZeroScratches):** Algoritmo especializado en eliminar rayones, manchas y grietas físicas de fotografías escaneadas.
- **Interfaz Streamlit:** Una experiencia de usuario fluida que permite comparar el "antes" y "después" en tiempo real.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1.  **Python 3.9 o superior** (Se recomienda 3.10 para mejor compatibilidad con PyTorch).
2.  **Git** (para clonar el repositorio).
3.  **Cuda (Opcional):** Si tienes una tarjeta gráfica NVIDIA, la aplicación funcionará mucho más rápido, aunque también es compatible con CPU.

---

## ⚙️ Instalación Paso a Paso

Sigue estos pasos para configurar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd photo_enhancer
```

### 2. Crear un entorno virtual (Recomendado)
Es una buena práctica para mantener las dependencias aisladas.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
Este paso instalará PyTorch, Streamlit y todos los modelos de IA necesarios.
```bash
pip install -r requirements.txt
```

---

## 🏃 Cómo Ejecutar la Aplicación

Una vez instaladas las dependencias, puedes iniciar la aplicación con el siguiente comando:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado (usualmente en `http://localhost:8501`).

### Pasos dentro de la app:
1.  **Subir Imagen:** Arrastra o selecciona la foto que deseas mejorar.
2.  **Configurar Opciones:** 
    - Activa **"Reparar grietas"** si la foto tiene arañazos o está rota.
    - Activa **"Mejorar calidad fondo"** para un escalado completo de la imagen.
3.  **Procesar:** Haz clic en el botón **"Mejorar Calidad"**.
4.  **Comparar y Descargar:** Usa el deslizador interactivo para ver los cambios y descarga el resultado final.

---

## 📁 Estructura del Proyecto

- `app.py`: Punto de entrada de la aplicación Streamlit.
- `src/models.py`: Lógica de carga y ejecución de los modelos de IA.
- `src/ui.py`: Componentes visuales de la interfaz.
- `src/utils.py`: Funciones auxiliares para procesamiento de imágenes.
- `requirements.txt`: Lista de todas las librerías necesarias.

---

## 📝 Notas
- La primera vez que ejecutes la aplicación, se descargarán automáticamente los pesos de los modelos de IA (GFPGAN, RealESRGAN, etc.). Esto puede tardar unos minutos dependiendo de tu conexión.
- El tiempo de procesamiento depende de la resolución de la imagen y de si estás usando CPU o GPU.
