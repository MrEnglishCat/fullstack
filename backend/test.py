import datetime
import os.path

import requests
import json
import pandas as pd
from retry import retry
# pip install openpyxl
# pip install xlsxwriter

print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))



# from pprint import pprint
#
# import requests
# from fake_useragent import UserAgent
#
# proxies = 'ЗАПИШИТЕ-СЮДА-СВОЙ-ПРОКСИ-В-НУЖНОМ-ФОРМАТЕ'
#
# #
# #
# # def get_headers():
# #     return {
# #          "User-Agent": UserAgent().random,
# #          "Access-Control-Allow-Credentials": "true",
# #          "Access-Control-Allow-Headers":"Authorization,Accept,Origin,DNT,User-Agent,Content-Type,Wb-AppType,Wb-AppVersion,Xwbuid,Site-Locale,X-Clientinfo,Storage-Type,Data-Version,Model-Version,__wbl, x-captcha-id",
# #          "Access-Control-Allow-Methods":"GET,OPTIONS",
# #          "Access-control-Allow-Origin":"https://www.wildberries.ru",
# #          "Content-Encoding":"gzip",
# #          "Content-Type":"application/json charset=utf-8"
# #      }
# #
# # response = requests.get(
# #     "https://www.wildberries.by/",
# #     headers=get_headers(),
# # )
# #
# #
# # print(response.text)
#
# import requests
#
# headers = {
#     'accept': '*/*',
#     'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ky;q=0.7',
#     'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTA3MzUwMzYsInVzZXIiOiIyNTkzNjM5NCIsInNoYXJkX2tleSI6IjkiLCJjbGllbnRfaWQiOiJ3YiIsInNlc3Npb25faWQiOiI1MWNhOGVkMzY0NmQ0NGNkYmRkMDljZWRmNmUzMDFmNiIsInZhbGlkYXRpb25fa2V5IjoiZmIyN2UwNGI5M2YzMWQ3ODczMWY2ZGM0ZTdmZmY5MTZjM2Q2YzgxNWM0NzU0YWRjMjRmNjllYWJkZGViOGI2NSIsInBob25lIjoiWENKWU1qWUt3RlkvUENvTG5oaW8xQT09IiwidXNlcl9yZWdpc3RyYXRpb25fZHQiOjE2NzA5NzkxOTIsInZlcnNpb24iOjJ9.XOHWMBEa2MoHkH9aj33oyDi2-oB1DL6rLvAjrCyhFvgby8ec3qSKqbvY-_owgK9Y9qrrJ_EjgX_6or01Z1DGbnrFQ-L2vxkCcjNz3RxWWX-8GywBNfLeyUAGOCfzUS1x7Ezf4OP_mt2RG8BBP_5PDqCF6ELkXsVmRQoF9b6J4WQhfNqZvRo84CbjhVIXnwo7BsNKKwchFVBHLYZBxlGJFfPBo3EgT4U4dcaFiM_albLI7dFpbvSsVUmFW4ctjjnp2tjU0gJBmivgXKex5UIqlRj5QowXyviTg4UzAle7F9XytUx1N6Ie-arFCSGqjoK0R3Xeou09IBb-lSdYIAE6LA',
#     'cache-control': 'no-cache',
#     'origin': 'https://www.wildberries.by',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://www.wildberries.by/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury',
#     'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
# }
#
# response = requests.get(
#     'https://catalog.wb.ru/catalog/electronic38/v2/catalog?ab_testing=false&appType=1&cat=9468&curr=byn&dest=-68617&hide_dtype=10;13;14&lang=ru&page=1&sort=popular&spp=30&uclusters=1&uiv=0&uv=AQMAAQIEAAMCAAEACbnFwDg9wMQ9Pww_xEAEu4a6rrlZvR9AFbdxO6Y8GDrPQNe_pr7qwR9AakaHxNnAXUF7QP67zUWYQYlCNMEfRIa_BcNGuTG_JDnov7M_00BcPpI37cCXwEO91byTwUpBOz01Q7y--UM5RDm-8MCowost57_zOOm_xb1Fx4_CakGgN_i6YLiLwzY_ZcAmusNBRD1FwFc5jDutPnmxw8EZt1xEQMIcuM-xGrwyx4M-0kMDxD9C00ClxQy9x8TtR3a3hbjmOJNEvcReQiyvZrzLQEWwDMEJxJC48LjxuPrHUEXHwObASLQaPx1GrjvqQxGjTqwbtlQ60j3cPCw8IDDrQtwBCAAA',
#     headers=headers,
# )
# # /catalog/{shard}/v2/catalog?
# pprint(response.json())
# #
# # def get_category():
# #     url = 'https://catalog.wb.ru/catalog/electronic14/v2/catalog?ab_testing=false&appType=1&cat=9468&curr=rub&dest=-1185367&sort=popular&spp=30'
# #
# #     headers = {
# #         'Accept': '*/*',
# #         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
# #         'Connection': 'keep-alive',
# #         'DNT': '1',
# #         'Origin': 'https://www.wildberries.ru',
# #         'Referer': 'https://www.wildberries.ru/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury',
# #         'Sec-Fetch-Dest': 'empty',
# #         'Sec-Fetch-Mode': 'cors',
# #         'Sec-Fetch-Site': 'cross-site',
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
# #         'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
# #         'sec-ch-ua-mobile': '?0',
# #         'sec-ch-ua-platform': '"Windows"',
# #     }
# #
# #     # response = requests.get(url=url, headers=headers, proxies=proxies)
# #     response = requests.get(url=url, headers=headers)
# #     print(response)
# #     return response.json()
# #
# #
# # def format_items(response):
# #     products = []
# #
# #     products_raw = response.get('data', {}).get('products', None)
# #
# #     if products_raw != None and len(products_raw) > 0:
# #         for product in products_raw:
# #             print(product.get('name', None))
# #             products.append({
# #                 'brand': product.get('brand', None),
# #                 'name': product.get('name', None),
# #                 'id': product.get('id', None),
# #                 'reviewRating': product.get('reviewRating', None),
# #                 'feedbacks': product.get('feedbacks', None),
# #             })
# #
# #     return products
# #
# #
# # def main():
# #     response = get_category()
# #
# #     products = format_items(response)
# #
# #     print(products)
# #
# # if __name__ == '__main__':
# #     main()