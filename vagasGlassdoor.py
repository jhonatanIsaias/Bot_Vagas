import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.vagas.com.br')

time.sleep(5)
# PARTE 1 : SELECIONAR BARRA DE PESQUISA PASSANDO O TIPO DA VAGA E A LOCALIZAÇÃO
wait = WebDriverWait(driver,20)
search_box = wait.until(EC.presence_of_element_located((By.ID,'nova-home-search')))
search_box.send_keys('estagio TI')
search_box.send_keys(Keys.RETURN)

time.sleep(10)

#PARTE 2 SELECIONADO AS VAGAS DA PRIMEIRA PÁGINA

jobs = []

#list_jobs_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'JobsList_jobsList__lqjTr')))

element_jobs = wait.until(EC.presence_of_element_located((By.ID,'todasVagas')))

job_cards = element_jobs.find_elements(By.TAG_NAME,'li')
print(len(job_cards))

time.sleep(10)


for card in job_cards:
    try:
        # Título da vaga
        title =  card.find_element( By.CLASS_NAME, 'link-detalhes-vaga').get_attribute('title')

        # Nome da empresa
        company = card.find_element(By.CLASS_NAME, 'emprVaga').text

        # Localização da vaga
        location = card.find_element(By.CLASS_NAME, 'vaga-local').text

        # Tempo de publicação
        time_posted = card.find_element(By.CLASS_NAME, 'data-publicacao').text

        # Link para a vaga
        job_link = card.find_element(By.CLASS_NAME, 'link-detalhes-vaga').get_attribute('href')

        # Adiciona os dados a uma lista de dicionários
        jobs.append({
            'Título': title,
            'Empresa': company,
            'Localização': location,
            'Tempo de Publicação': time_posted,
            'Link': job_link
        })
    except Exception as e:
        print(f"Erro ao coletar informações de um card: {e}")

print(jobs)
#PARTE 3 MANIPULANDO DADOS COM O PANDAS

vagas_df = pd.DataFrame(jobs)

vagas_df.to_csv('vagas',index=False)

