import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from googletrans import Translator

st.markdown("""
<style>
    body {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        color: #4bb629;
        font-size: 36px;
        margin: 20px 0;
    }
    .header {
        text-align: center;
        color: #00796B;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .text-output {
        background-color: #e3f2fd;
        border: 1px solid #4A90E2;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        font-family: 'Georgia', serif;
        font-size: 18px;
        color: #333;
        line-height: 1.5;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

st.markdown("<h1 class='title'>Reconocimiento Óptico de Caracteres</h1>", unsafe_allow_html=True)
st.subheader("Elige la fuente de la imagen: cámara o archivo")

cam_ = st.checkbox("Usar Cámara")
if cam_:
    img_file_buffer = st.camera_input("📸 Toma una Foto")
else:
    img_file_buffer = None

with st.sidebar:
    st.subheader("Procesamiento para Cámara")
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'))

bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    st.image(bg_image, caption='Imagen cargada.', use_column_width=True)

    with open(bg_image.name, 'wb') as f:
        f.write(bg_image.read())
    
    st.success(f"Imagen guardada como {bg_image.name}")
    img_cv = cv2.imread(bg_image.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("<h2 class='header'>Texto Reconocido:</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-output'>{text}</div>", unsafe_allow_html=True)

if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("<h2 class='header'>Texto Reconocido:</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-output'>{text}</div>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Parámetros de Traducción")
    
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass
    
    translator = Translator()
    
    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )
    input_language = {
        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }[in_lang]
    
    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"),
    )
    output_language = {
        "Inglés": "en",
        "Español": "es",
        "Bengalí": "bn",
        "Coreano": "ko",
        "Mandarín": "zh-cn",
        "Japonés": "ja"
    }[out_lang]
    
    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "Reino Unido",
            "Estados Unidos",
            "Canadá",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )
    
    tld = {
        "Default": "com",
        "India": "co.in",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za"
    }[english_accent]

    display_output_text = st.checkbox("Mostrar texto de salida")

    if st.button("Convertir"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
      
        if display_output_text:
            st.markdown("## Texto de salida:")
            st.markdown(f"<div class='text-output'>{output_text}</div>", unsafe_allow_html=True)




 
    
    
