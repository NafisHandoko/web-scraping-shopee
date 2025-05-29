import requests
from datetime import datetime

url = "https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new"


shopid = 145589728
userid = 145591552
limit = 1
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

session = requests.Session()
session.headers.update({'Cookie': '_gcl_au=1.1.307313397.1746255068; _gid=GA1.3.1581922160.1748479596; _ga=GA1.3.1820688933.1747467912; SPC_IA=1; SPC_EC=.eXBIMTFWSXhzQnZaamlPTmWcJUxSSrngTeoNTQBJMVCQr4Wgxa0zwhmu3euo0tdCRyJ2hoC5eBdiemsKuVPiENGRh6zhe37RKj9/2Bl3fOhLbZmLF2BX1YDrQSFZEsvYqY1T8VTst5DRoHoq5l1x0ZQd6v142BS/bmtty98ERL0g++iHJ7L3v0Zh8Mxxq/G6DhO88lLwqmtvrl5bdVYoYM/YlOl2TQmCPggtq51dpDOG4zjblIN310DTJRdB3vJ/aIukNbtAE5yAIGm7qlEJaQ==; SPC_F=jKMiIHEY4dwQ1JZ9G0r9dUt29C46nCAv; SPC_U=644695807; SPC_T_ID=pj0ojbcEO5WyJEk5xdEDDRN3RqARrj2J29nFNVomQB263HbZI9ybPeVN0l0Q4SScPAHUvwMWLhoYrs4DQH2sLP4/9j41rfKH+IFDehH5qg2t8yJPYYHemBdDW77G7RWoOX64c+x1Sbe/RHQSmXfpCKsHas6sFL5IXw5rMkt6Gf0='})


response = session.get(url, params=params).json()
print(response['data']['items'][0]['author_username'])
print(response['data']['items'][0]['comment'])
print(response['data']['items'][0]['rating_star'])
from datetime import datetime
print(datetime.fromtimestamp(response['data']['items'][0]['submit_time']).strftime('%Y-%m-%d %H:%M:%S'))
print(response['data']['items'][0]['product_items'][0]['model_name'])
print(response['data']['items'][0]['product_items'][0]['name'])