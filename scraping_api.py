import requests
from datetime import datetime
import pandas as pd
import os

def save_data(data, csv_file="shopee_reviews.csv", excel_file="shopee_reviews.xlsx"):
    """Fungsi untuk menyimpan data ke CSV dan Excel dengan mode append"""
    if not data:  # Jika tidak ada data, skip
        return
        
    # Buat DataFrame dari data baru
    df_new = pd.DataFrame(data, columns=[
        "username", "comment", "rating", "submit_time", 
        "model_name", "product_name"
    ])
    
    # Untuk CSV
    if os.path.exists(csv_file):
        # Jika file sudah ada, baca file lama dan gabungkan dengan data baru
        df_old = pd.read_csv(csv_file)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    # Simpan ke CSV
    df_combined.to_csv(csv_file, index=False)
    
    # # Untuk Excel
    # if os.path.exists(excel_file):
    #     # Jika file sudah ada, baca file lama dan gabungkan dengan data baru
    #     df_old = pd.read_excel(excel_file)
    #     df_combined = pd.concat([df_old, df_new], ignore_index=True)
    # else:
    #     df_combined = df_new
    
    # # Simpan ke Excel
    # df_combined.to_excel(excel_file, index=False)
    
    print(f"Data tersimpan ke {csv_file} dan {excel_file}")

url = "https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new"

shopid = 145589728
userid = 145591552
limit = 10  # Maksimum limit per request
offset = 0
itemid = 28414764389

params = {
    'limit': limit,
    'offset': offset,
    'shopid': shopid,
    'userid': userid,
    'itemid': itemid
}

data = []
target_reviews = 10  # Jumlah target ulasan yang ingin dikumpulkan

session = requests.Session()
session.headers.update({
    'Cookie': '_gcl_au=1.1.307313397.1746255068; _gid=GA1.3.1581922160.1748479596; _ga=GA1.3.1820688933.1747467912; SPC_IA=1; SPC_EC=.eXBIMTFWSXhzQnZaamlPTmWcJUxSSrngTeoNTQBJMVCQr4Wgxa0zwhmu3euo0tdCRyJ2hoC5eBdiemsKuVPiENGRh6zhe37RKj9/2Bl3fOhLbZmLF2BX1YDrQSFZEsvYqY1T8VTst5DRoHoq5l1x0ZQd6v142BS/bmtty98ERL0g++iHJ7L3v0Zh8Mxxq/G6DhO88lLwqmtvrl5bdVYoYM/YlOl2TQmCPggtq51dpDOG4zjblIN310DTJRdB3vJ/aIukNbtAE5yAIGm7qlEJaQ==; SPC_F=jKMiIHEY4dwQ1JZ9G0r9dUt29C46nCAv; SPC_U=644695807; SPC_T_ID=pj0ojbcEO5WyJEk5xdEDDRN3RqARrj2J29nFNVomQB263HbZI9ybPeVN0l0Q4SScPAHUvwMWLhoYrs4DQH2sLP4/9j41rfKH+IFDehH5qg2t8yJPYYHemBdDW77G7RWoOX64c+x1Sbe/RHQSmXfpCKsHas6sFL5IXw5rMkt6Gf0='
})

print("Memulai pengumpulan data...")

while len(data) < target_reviews:
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Tampilkan progress
    print("=" * 50)
    print(f"Progress Pengumpulan Data:")
    print(f"Offset: {offset}")
    print(f"Data terkumpul: {len(data)}/{target_reviews} ulasan")
    print("=" * 50)
    
    try:
        response = session.get(url, params=params)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"Error: API request failed with status code {response.status_code}")
            break
            
        try:
            response_data = response.json()
        except ValueError:
            print("Error: Invalid JSON response from API")
            break
            
        # Validate response structure
        if not response_data or 'data' not in response_data or 'items' not in response_data['data']:
            print("Error: Unexpected API response structure")
            print("Response:", response_data)
            break
            
        items = response_data['data']['items']
        
        if not items:  # Jika tidak ada data lagi
            print("Tidak ada data lagi yang tersedia")
            break
            
        # List untuk menyimpan data dari batch ini
        batch_data = []
        
        for item in items:
            try:
                # Validate required fields
                if not all(key in item for key in ['author_username', 'comment', 'rating_star', 'submit_time']):
                    print(f"Warning: Skipping item with missing required fields")
                    continue
                    
                comment = item['comment'].strip()
                
                # Skip jika comment kosong
                if not comment:
                    continue
                    
                # Bersihkan comment dari enter dan double enter
                comment = ". ".join(comment.split('\n'))  # Ganti semua whitespace dengan spasi tunggal
                comment = ". ".join(filter(None, comment.split(". ")))  # Bersihkan titik berurutan
                
                # Format waktu
                submit_time = datetime.fromtimestamp(item['submit_time']).strftime('%Y-%m-%d %H:%M:%S')
                
                # Ambil data produk dengan safe access
                product_items = item.get('product_items', [])
                model_name = product_items[0].get('model_name', '') if product_items else ""
                product_name = product_items[0].get('name', '') if product_items else ""
                
                batch_data.append({
                    "username": item['author_username'],
                    "comment": comment,
                    "rating": item['rating_star'],
                    "submit_time": submit_time,
                    "model_name": model_name,
                    "product_name": product_name
                })
            except Exception as e:
                print(f"Warning: Error processing item: {str(e)}")
                continue
        
        # Tambahkan data batch ke data keseluruhan
        data.extend(batch_data)
        
        # Simpan data setelah setiap batch
        save_data(batch_data)
        
        # Update offset untuk request berikutnya
        offset += limit
        params['offset'] = offset
        
    except Exception as e:
        print(f"Error saat mengambil data: {str(e)}")
        break

print(f"\nPengumpulan data selesai. Total data terkumpul: {len(data)}")