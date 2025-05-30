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
        "cmtid", "author_username", "model_name", "product_name", 
        "rating_star", "comment", "submit_time"
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
    
    # Untuk Excel
    if os.path.exists(excel_file):
        # Jika file sudah ada, baca file lama dan gabungkan dengan data baru
        df_old = pd.read_excel(excel_file)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    # Simpan ke Excel
    df_combined.to_excel(excel_file, index=False)
    
    print(f"Data tersimpan ke {csv_file} dan {excel_file}")

url = "https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new"

shopid = 145589728
userid = 145591552
limit = 5  # Maksimum limit per request
offset = 0
# itemid = 28414764389

params = {
    'limit': limit,
    'offset': offset,
    'shopid': shopid,
    'userid': userid
    # 'itemid': itemid
}

data = []
target_reviews = 1000  # Jumlah target ulasan yang ingin dikumpulkan

session = requests.Session()
session.headers.update({
    'Cookie': '_gcl_au=1.1.307313397.1746255068; _fbp=fb.2.1746255068099.25272698245431466; _QPWSDCXHZQA=0dd632c7-7e11-4832-d574-ca6586fbb90f; REC7iLP4Q=e1719331-e580-418f-8f4a-e9844355bb5e; REC_T_ID=fe92ab86-27ea-11f0-a19e-2e541f10bb14; SPC_F=jKMiIHEY4dwQ1JZ9G0r9dUt29C46nCAv; __LOCALE__null=ID; _med=affiliates; csrftoken=yQ4VpIfhcQX7Ah5k9H9hX4eKwumdWx6W; _sapid=64752649b8c933216128ea4b9c97a005a2e369c1dfa09d1fe75d20c8; SPC_CLIENTID=jKMiIHEY4dwQ1JZ9ixpkyberunjqvyvw; SPC_ST=.OGZhSkNNUG51Z2I1YU1GOUA3qYFqMZvzJOd68BfumjiXe/MoKWJKLsdenJqWb2AaCf139mh9fwusHYpLL89f8xdRXlM9Tfeoe7lx7xA4gVCxw5Kf21tSwz9iJ0djeF0D36RuaGvLGAjyks59uKXrYJg552ISWvApNNb3puZaWqfJJN1Pa/PhQXrgOOJIBLr3dG81pPJK7flQGUcWcuMzvAdF19klANmf+sdxnDIsmqNzhCV4Fz71RWkeSLtBdkg1GmSNcbXbRSTOQarAOoT4hw==; SPC_U=644695807; SPC_R_T_ID=pj0ojbcEO5WyJEk5xdEDDRN3RqARrj2J29nFNVomQB263HbZI9ybPeVN0l0Q4SScPAHUvwMWLhoYrs4DQH2sLP4/9j41rfKH+IFDehH5qg2t8yJPYYHemBdDW77G7RWoOX64c+x1Sbe/RHQSmXfpCKsHas6sFL5IXw5rMkt6Gf0=; SPC_R_T_IV=TWN6bVl2SjNydlJHYnVGSA==; SPC_T_ID=pj0ojbcEO5WyJEk5xdEDDRN3RqARrj2J29nFNVomQB263HbZI9ybPeVN0l0Q4SScPAHUvwMWLhoYrs4DQH2sLP4/9j41rfKH+IFDehH5qg2t8yJPYYHemBdDW77G7RWoOX64c+x1Sbe/RHQSmXfpCKsHas6sFL5IXw5rMkt6Gf0=; SPC_T_IV=TWN6bVl2SjNydlJHYnVGSA==; SPC_CDS_CHAT=f8550895-a1e8-4ad6-b64e-958dc3613350; SPC_IA=1; SPC_SI=kJUuaAAAAABKeWxpQzYyev5qtAAAAAAARmhVUExuT0k=; _gid=GA1.3.1581922160.1748479596; SPC_SEC_SI=v1-Rmo5aGxNZHU2Y3hHWHEyUO5wvtcoXXqYOie+M9UzBVfUY6aJBagAuzhBJgj0uL9poPMh9/sjzCwqDcf5/EG+bwAdOIzoEA8cFUzTC0nGhE8=; AMP_TOKEN=%24NOT_FOUND; AC_CERT_D=U2FsdGVkX18/VdFtRDwTNUTXes27ok1YI87haL2lJHMD0+UQB1riqKQw2BpauoTEDacvThOyRMbDCC72LwQj+DLeN6r70kLSEjphcl1mpoVdpGcNMomDIdp6iRJgbpl0a+DuP6s6cyFIYgDAmU+SHENxhF/7fWCfAhLIMUXdC9GQz9Z/DKi34ACqqlZvMtsqngGjfIgicJlBV4+80EdCElsxmWPRq8xARZPplDw9ZaiXaxIoHxT4o1qxvpOn2rWFnhU9jdK32/lmO49o4UTuGrLvU9lL+gaAQsKDn+zYRboB/1oDKzMobzzxcsG9W2FB6yWVONSApUfpUBekzvUNKGP9Opwcmn/d1se0fKbZqX5LOlmBqmN1KAJyRI6boZKqPoePGvaz4MvRjC4qpRgexlbaXrSIW9Hgj19IrLSCx6dWlmkJp5a6zcpG8+LzTVUWnJXQ/1aTWFl3Nkv58c+q0SfgdV8HWSZJshTJT6ySkr3RsrhQ2fl55k7Ce5//9EBYIBYmEi6ruWjVqXUNDFbMK5/VAIfPCXoIEFbFJyT/UQN2Gk4OHSkPF4GQUw1rmC4IB9XFBvCcz1g8SKWX/7iPpzXofIOh6ogque5mtJw6I7VMdgV25AwuzaDtrqMuTC2WGjYlk9HT5COrx0yASdOxyarQjO03zcyBEa9c9tq+bsvpFvxMk6FlFwc5JM4Un9nlp2ZxtMKsGfqXufzqkP0BJ856sZfX0uCze1dhmlsUPHZElwDlLCPbVJidUq9DBUN7IZTtIeBn+UntjUbo9+fZK1FpxPLVhcHuE2YpKCVIFPpWJ05+b4I2SKxy+YtIeCj9Nn0u0ge9O/E5fXMmjxDVv5PqCzdQaXjUeguG3r3rWf9uFg5b+xOaFNUVS1WnlhR2IBvUxx+VxOVIIE2EsbAXdXcAfVEedstCC8Fqy2/0k1PPveDhiOgGjc6GAY5ru+bjf2rHkF+VQF8hO0tcMfytGZANPahuF9WGj4/udf4vH+p0Pxk3kVFo5KbjFHAPWy9kAeVzS46FUVdfzG+mcxWdcado6T3vNh8LLeVofqsGPEhqmZX06SVRzfHNd3q3UTK+0u/SOSt7KC0NmQ9iNruzwyqMBUtjttTHMEHneEasKbg=; _ga=GA1.3.1820688933.1747467912; shopee_webUnique_ccd=l4rzl3fe%2FTmjniicsKIqDQ%3D%3D%7C3mDqV0%2FjHeCsrW%2BkLgw5ir1iDkR3ZdfRQkAAKXmTV9eqnmly%2BfItizQzrRSk2Dwsi%2FxEJpUiuVk%3D%7CiNB0CcLPmfmbcdQa%7C08%7C3; ds=50d0b79f7a7d8843a60f61e5226e2951; _ga_SW6D8G0HXK=GS2.1.s1748593044$o20$g1$t1748595253$j60$l0$h0; SPC_EC=.YlZoQlBLZDVxRmpqSGNZTk91EUhl3EqvoluDe4MXv42OCidtn7Ou2cj8XE7vbnb2gTjZXxICbF5rRYHECiqZxuNYMByvJJYtbS6HdsULFW9zK9N2VIvuQhku4ojty6PHMo7WPaR1dFW02WOk6EGyUVhkVXCGSb1gk3dDKSHtBami1lvxbMv9DApzfzV9n9iUzqrBK7ajRcQZcfaD96g4ZYTBOUHyKhvsLoosXxCwNG2v/l2QWn9ur9nGhe0R8lkV2ula/bVqHBWzlDy9qbcoFQ=='
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
                
                # Bersihkan comment dari enter dan double enter jika ada
                if comment:
                    comment = ". ".join(comment.split('\n'))  # Ganti semua whitespace dengan spasi tunggal
                    comment = ". ".join(filter(None, comment.split(". ")))  # Bersihkan titik berurutan
                
                # Format waktu
                submit_time = datetime.fromtimestamp(item['submit_time']).strftime('%Y-%m-%d %H:%M:%S')
                
                # Ambil data produk dengan safe access
                product_items = item.get('product_items', [])
                model_name = product_items[0].get('model_name', '') if product_items else ""
                product_name = product_items[0].get('name', '') if product_items else ""
                
                batch_data.append({
                    "cmtid": item['cmtid'],
                    "author_username": item['author_username'],
                    "model_name": model_name,
                    "product_name": product_name,
                    "rating_star": item['rating_star'],
                    "comment": comment,
                    "submit_time": submit_time
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
        print(response.text)
        break

print(f"\nPengumpulan data selesai. Total data terkumpul: {len(data)}")