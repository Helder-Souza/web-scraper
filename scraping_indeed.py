import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv
import send_email

def scrap():
    url = "https://br.indeed.com/jobs?q=desenvolvedor+java&l=remoto&fromage=7"
    start = 0
    vagas = []
    while(True):
        driver = request(url)
        jobs = driver.find_elements(By.CLASS_NAME, "jobTitle")
        get_jobs(jobs, vagas)
        if(start == 0):
            count_vagas = driver.find_elements(By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount")
            tag = count_vagas[0].find_element(By.TAG_NAME, "span")
            job_count = tag.text.strip().replace("+ de", "").replace(" vagas", "")
        start = start+10
        if(start <= int(job_count)):
            url = url[:67] + f"&start={start}"
            continue
        else:
            break
    driver.quit()
    write_csv(vagas)

def get_jobs(jobs, vagas):
    for job in jobs:
        try:
            link_element = job.find_element(By.TAG_NAME, "a")
            job_title = link_element.text.strip()
            job_link = link_element.get_attribute("href")
            vagas.append([job_title, job_link])
        except Exception as e:
            print(f"Erro ao processar vaga: {e}")
    
def write_csv(input):
    headerList = ['Vaga', 'Link']
    with open('vagas_indeed.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headerList)
        writer.writerows(input)

def request(url):
    options = uc.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    return driver

if __name__ == "__main__":
    scrap()
    send_email.main()