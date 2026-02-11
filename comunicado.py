import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import os

# ==========================
# CONFIGURAÇÕES
# ==========================

URL_ALVO = "https://aguasdorio.com.br/comunicados/"
PALAVRA_CHAVE = "Nova Iguaçu"

EMAIL_REMETENTE = "contaservico.horadoqa@gmail.com"
EMAIL_SENHA = os.getenv('EMAIL_PASSWORD')
EMAIL_DESTINO = "horadoqa@gmail.com"

SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587


# ==========================
# FUNÇÃO PARA ENVIAR EMAIL
# ==========================

def enviar_email(titulo_encontrado, link):
    assunto = f"Encontrado: {PALAVRA_CHAVE}"

    corpo = f"""
A palavra '{PALAVRA_CHAVE}' foi encontrada!

Título encontrado:
{titulo_encontrado}

Link:
{link}

Data/Hora: {datetime.datetime.now()}
"""

    mensagem = MIMEMultipart()
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINO
    mensagem["Subject"] = assunto
    mensagem.attach(MIMEText(corpo, "plain"))

    contexto = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
        servidor.starttls(context=contexto)
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(
            EMAIL_REMETENTE,
            EMAIL_DESTINO,
            mensagem.as_string()
        )

    print("Email enviado com sucesso!")


# ==========================
# FUNÇÃO PRINCIPAL
# ==========================

def verificar_site():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(URL_ALVO)
        driver.implicitly_wait(10)

        # Pega todos os h5 com class card-title
        titulos = driver.find_elements(By.CSS_SELECTOR, "h5.card-title")

        encontrado = False

        for titulo in titulos:
            texto = titulo.text.strip()
            # Pega o link do elemento pai <a>
            try:
                link = titulo.find_element(By.XPATH, "..").get_attribute("href")
            except:
                link = "Link não encontrado"

            print("Encontrado na página:", texto, "| Link:", link)

            if PALAVRA_CHAVE.lower() in texto.lower():
                enviar_email(texto, link)
                encontrado = True
                break

        if not encontrado:
            print("Palavra não encontrada hoje.")

    except Exception as e:
        print("Erro:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    verificar_site()
