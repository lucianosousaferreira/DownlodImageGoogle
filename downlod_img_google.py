from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
import os
import time
import pandas as pd
import requests

if not os.path.exists('DOWNLOADS-GOOGLE'):
    os.makedirs('DOWNLOADS-GOOGLE')

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--dns-prefetch-disable')

df = pd.read_excel('/home/luciano/Documentos/baixar.xlsx')
list_peq = df['pesquisa'].to_list()

driver = webdriver.Firefox(options=options)

def DownloadImageGooogle(pesquisa: list, qtd_img: int):
    for pesq in pesquisa:

        try:
            driver.get('https://www.google.com.br/imghp?hl=pt-BR&authuser=0&ogbl')

            elem = driver.find_element(By.NAME, "q")
            elem.clear()
            elem.send_keys(pesq)
            elem.send_keys(Keys.RETURN)
            time.sleep(2)
            for i in range(1,qtd_img + 1):
                element = driver.find_element(By.XPATH,'//*[@id="islrg"]/div[1]/div['+ str(i) +']/a[1]/div[1]/img')

                while element.is_displayed() == False:
                    time.sleep(1)

                driver.execute_script("arguments[0].click();", element)
                time.sleep(2)
                img = driver.find_element(By.XPATH,
                                          '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
                src = img.get_attribute('src')
                url = str(src)
                nome = pesq
                try:
                    resposta = requests.get(url)
                    if resposta.status_code == requests.codes.OK:
                        with open('DOWNLOADS-GOOGLE/'+ nome +'_'+ str(i) +'.jpg', 'wb') as imagem:
                            imagem.write(resposta.content)
                            print('Imagem salva! === > '+ nome +'_'+ str(i) +'.jpg === > |ok|')
                    else:
                        resposta.raise_for_status()

                    imagem.close()
                except Exception as e:
                    pass
        except NoSuchElementException:
                    pass


    driver.close()
    driver.quit()
    
DownloadImageGooogle(pesquisa=list_peq,qtd_img=10)
