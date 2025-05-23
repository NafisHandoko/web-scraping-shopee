# Impor library yang diperlukan
from bs4 import BeautifulSoup  # Untuk parsing HTML
from selenium import webdriver  # Untuk otomasi browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time  # Untuk menambahkan jeda waktu
import pandas as pd  # Untuk pengolahan data

# URL halaman ulasan Shopee yang akan di-scrape
url = 'https://shopee.co.id/buyer/145591552/rating?shop_id=145589728'

# Konfigurasi opsi browser Chrome untuk menghindari deteksi sebagai browser otomatis
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Memulai dengan jendela browser yang dimaksimalkan
options.add_argument("--disable-blink-features=AutomationControlled")  # Menonaktifkan tanda otomasi
options.add_argument("--disable-notifications")  # Menonaktifkan notifikasi browser
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Menyembunyikan info otomasi
options.add_experimental_option("useAutomationExtension", False)  # Menonaktifkan ekstensi otomasi
driver = webdriver.Chrome(options=options)  # Inisialisasi driver Chrome dengan opsi

# Mengatur user agent kustom untuk meniru browser normal
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# Navigasi ke URL target
driver.get(url)

print("Waiting for page to load...")
time.sleep(5)  # Tunggu hingga halaman dimuat sepenuhnya

# Inisialisasi list kosong untuk menyimpan data yang di-scrape
data = []
page = 1
max_pages = 20  # Jumlah maksimum halaman yang akan di-scrape

# Loop scraping utama - lanjutkan sampai mencapai max_pages atau tidak dapat menemukan halaman lagi
while page <= max_pages:
    print(f"Scraping page {page}")
    # Berikan waktu agar konten dinamis dimuat
    time.sleep(3)

    # Parse sumber halaman dengan BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Pilih semua elemen ulasan
    reviews = soup.select(
        "div.shopee-product-comment-list div.shopee-product-rating")
    # Filter duplikat (setengah dari ulasan, karena mungkin ada duplikat di DOM)
    reviews = reviews[:len(reviews) // 2]

    # Ekstrak data dari setiap ulasan
    for review in reviews:
        review_element = review.select_one("div.shopee-product-rating__time + div")
        product_element = review.select_one("a.IlUtxL")
        time_variant = review.select_one("div.shopee-product-rating__time")
        rating_elements = review.select("svg.icon-rating-solid--active")
        rating_count = len(rating_elements)  # Hitung jumlah bintang yang terisi untuk rating

        # Ekstrak info waktu dan varian
        time_text = time_variant.text.strip().split(" | ")[0]
        variant_name = time_variant.text.strip().split(" | ")[1]
        # Ekstrak detail produk
        product_name = product_element.text.strip()
        product_url = product_element['href']
        # Periksa apakah elemen ulasan ada dan memiliki style yang diharapkan
        if review_element and 'position: relative' in review_element.get('style', ''):
            # Tambahkan data yang diekstrak ke list kita
            data.append({
                "product_name": product_name,
                "product_url": product_url,
                "time_text": time_text,
                "rating_count": rating_count,
                "variant_name": variant_name,
                "review_text": review_element.text.strip()
            })
            
    try:
        if page < max_pages:
            # Coba berbagai selektor untuk tombol halaman berikutnya - ini menangani variasi UI yang berbeda
            next_button = None
            try:
                # Percobaan pertama: cari tombol dengan "Laman berikutnya"
                next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
            except NoSuchElementException:
                try:
                    # Percobaan kedua: cari tombol panah kanan
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.shopee-icon-button--right")
                except NoSuchElementException:
                    try:
                        # Percobaan ketiga: periksa semua tombol pagination untuk yang memiliki "next" atau "right" di kelas
                        pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "div.shopee-page-controller button")
                        for button in pagination_buttons:
                            if "next" in button.get_attribute("class").lower() or "right" in button.get_attribute("class").lower():
                                next_button = button
                                break
                    except:
                        pass
            
            # Jika kita menemukan tombol berikutnya dan dapat diklik, pindah ke halaman selanjutnya
            if next_button and next_button.is_enabled():
                next_button.click()
                print(f"Navigated to page {page + 1}")
                time.sleep(3)  # Tunggu halaman berikutnya dimuat
            else:
                print("No more pages available or next button not found")
                break
        else:
            print(f"Reached maximum number of pages ({max_pages})")
    except Exception as e:
        print(f"Error navigating to next page: {str(e)}")
        break
        
    page += 1

# Laporkan hasil dan simpan data
print(f"Total reviews collected: {len(data)}")
if data:
    # Buat pandas DataFrame dari data yang dikumpulkan
    df = pd.DataFrame(data, columns=["product_name", "product_url", "time_text", "rating_count", "variant_name", "review_text"])
    # Simpan data ke format CSV
    df.to_csv("hns.csv", index=False)
    print("Data saved to hns.csv")
    
    # Simpan ke format Excel
    df.to_excel("hns.xlsx", index=False)
    print("Data saved to hns.xlsx")
else:
    print("No data collected")

# Tutup browser
driver.quit()
