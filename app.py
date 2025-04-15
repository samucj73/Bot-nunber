import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import os

@st.cache_data
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/chrome"

    driver = webdriver.Chrome(
        executable_path="/opt/render/project/.render/chromedriver/bin/chromedriver",
        options=chrome_options
    )
    return driver

def detectar_numeros(url):
    driver = iniciar_driver()
    driver.get(url)
    time.sleep(10)  # Espera o conteúdo carregar

    elementos = driver.find_elements(By.XPATH, "//*")
    resultados = []

    for el in elementos:
        texto = el.text.strip()
        if texto:
            numeros = re.findall(r'\b\d{1,2}\b', texto)
            if numeros:
                resultados.append({
                    "elemento": el.tag_name,
                    "classe": el.get_attribute("class"),
                    "id": el.get_attribute("id"),
                    "texto": texto,
                    "numeros": numeros
                })

    driver.quit()
    return resultados

# Interface Streamlit
st.set_page_config(page_title="Detector de Números da Roleta", layout="wide")
st.title("Detector de Números Sorteados (Roleta)")

url = st.text_input("Cole aqui o link da página do jogo")

if url:
    st.info("Coletando informações...")
    resultados = detectar_numeros(url)
    if resultados:
        for r in resultados:
            st.markdown(f"**Elemento:** `{r['elemento']}` | **Classe:** `{r['classe']}` | **ID:** `{r['id']}`")
            st.markdown(f"**Texto:** {r['texto']}")
            st.markdown(f"**Números encontrados:** {', '.join(r['numeros'])}")
            st.markdown("---")
    else:
        st.warning("Nenhum número detectado na página.")
