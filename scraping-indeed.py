import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv

def scrap():
    url = "https://br.indeed.com/jobs?q=desenvolvedor+java&l=remoto"

    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get(url)

    time.sleep(5)

    jobs = driver.find_elements(By.CLASS_NAME, "jobTitle")
    print(f"Encotradas {len(jobs)} vagas!")

    vagas = []

    for job in jobs:
        try:
            link_element = job.find_element(By.TAG_NAME, "a")
            job_title = link_element.text.strip()
            job_link = link_element.get_attribute("href")
            vagas.append([job_title, job_link])
            print(f"Título: {job_title}")
            print(f"Link: {job_link}\n")
        except Exception as e:
            print(f"Erro ao processar vaga: {e}")

    driver.quit()
    write_csv(vagas)

def write_csv(input):
    headerList = ['Vaga', 'Link']
    with open('vagas_indeed.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headerList)
        writer.writerows(input)

if __name__ == "__main__":
    scrap()