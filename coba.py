from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://shopee.co.id/kapstok-baju-stainless-6-kait-gantungan-baju-stainless-muran-i.145589728.6442847024'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)

data = []

try:
    WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopee-product-rating"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    containers = soup.find_all('div', class_='shopee-product-rating')

    for container in containers:
        review_div = container.find('div', class_='shopee-product-rating')
        if review_div:
            data.append(review_div.text.strip())

except Exception as e:
    print(f"Terjadi kesalahan: {e}")

if data: 
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("hns.csv", index=False, encoding='utf-8-sig')
    print(f"berhasil simpan {len(data)} ulasan ke 'hns.csv'")
else:
    print("Tidak ada ulasan")