# autor: Elcio Mello
# Projeto: Envio de mensagem com preço pelo telegram

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import json

# ==========================
# CONFIGURAÇÕES
# ==========================

with open("config.json", encoding="utf-8") as arquivo:
    config = json.load(arquivo)

# ==========================
# DADOS
# ==========================

CPF = config["cpf"]
SENHA = config["senha"]

TOKEN = config["telegram_token"]
CHAT_ID = config["telegram_chat_id"]

# ==========================
# NAVEGADOR
# ==========================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

wait = WebDriverWait(driver, 20)

# atalhos
id = By.ID
esperar = wait.until

# ==========================
# LOGIN
# ==========================

driver.get("https://ead.sp.senai.br/")

esperar(
    EC.presence_of_element_located(
        (id, "txtUsuario")
    )
).send_keys(CPF)

driver.find_element(id, "btnAvancar").click()

esperar(
    EC.visibility_of_element_located(
        (id, "password")
    )
).send_keys(SENHA)

driver.find_element(
    By.XPATH,
    "//button[contains(.,'Acessar')]"
).click()

esperar(
    EC.url_contains("/Home/Index")
)

# ==========================
# FECHAR MODAL
# ==========================

esperar(
    EC.element_to_be_clickable(
        (id, "fecharFirstAccessModelButton")
    )
).click()

# ==========================
# CURSOS
# ==========================

esperar(
    lambda d: d.find_element(
        id,
        "contador-cursos"
    ).text == "(0)"
)

cursos = driver.find_element(
    id,
    "contador-cursos"
).text

mensagem = f"📚 SENAI EAD\n\nCursos matriculados: {cursos}"

print(mensagem)

# ==========================
# TELEGRAM
# ==========================

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    }
)

driver.quit()