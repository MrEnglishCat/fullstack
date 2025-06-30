import os
import time

import requests
from fake_useragent import UserAgent
from urllib.parse import urlparse

from sqlalchemy.orm import Session

# from backend.parser.db import engine, ProductCard, Base
from .db import engine, ProductCard, Base
# from backend.parser.utils import FilesHandler
from .utils import FilesHandler


class WB:
    MAIN_MENU_URL = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
    CATALOG_URL = 'https://catalog.wb.ru/catalog/{shard}/v2/catalog?ab_testing=false&appType=1&{query}&curr=byn&dest=-59202&hide_dtype=10;13;14&lang=ru&page={page}&sort=popular&spp=30'
    MAIN_FILEPATH = os.path.dirname(os.path.abspath(__file__))
    BASE_FILEPATH = f"{MAIN_FILEPATH}/data"
    CONFIG_FILEPATH = f"{MAIN_FILEPATH}/config"
    MAX_PAGE = 5
    RESULT = []

    def __init__(self, user_input=None):
        self.user_input = user_input
        self.all_catalogs_path = {}
        FilesHandler.checking_folder(type(self).BASE_FILEPATH)

    def get_main_menu_catalogs_wb(self):
        '''https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json'''

        def __recursive_search(data):
            for item in data:
                if "childs" not in item:
                    self.all_catalogs_path.setdefault(
                        item.get("url"),
                        item
                    )
                else:
                    __recursive_search(item["childs"])

        response_json: list = self.__request(self.MAIN_MENU_URL, self.__get_headers())
        if response_json:
            FilesHandler.write_json(f"{type(self).BASE_FILEPATH}/main-menu-ru-ru-v3.json", response_json)
            for item in response_json:
                if "childs" in item:

                    __recursive_search(item["childs"])

                else:
                    self.all_catalogs_path.setdefault(
                        item.get("url"),
                        item
                    )

            FilesHandler.write_json(
                f"{type(self).BASE_FILEPATH}/all_catalogs_path.json", self.all_catalogs_path
            )
        else:
            print("[INFO] Неуспешный запрос.")

    def __request(self, url: str, headers: dict) -> None | dict:
        for times in range(3):
            proxies = FilesHandler.read_json(f"{type(self).CONFIG_FILEPATH}/test_proxies.json")
            print(self.MAIN_FILEPATH)
            result = list(f"http://{item.get("ip")}:{item.get("port")}" for item in proxies)
            # response = requests.get(url, headers=headers, proxies={"http":result[random.randint(0, len(result)-1)]})
            response = requests.get(url, headers=headers, )

            if response.status_code == 200:
                return response.json()
            else:
                time.sleep(times)
                print(f"[INFO {times + 1}/3] Status code: {response.status_code}. {response.url}")

    def __get_headers(self) -> dict:
        return {
            "User-Agent": UserAgent().random,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Accept,Origin,DNT,User-Agent,Content-Type,Wb-AppType,Wb-AppVersion,Xwbuid,Site-Locale,X-Clientinfo,Storage-Type,Data-Version,Model-Version,__wbl, x-captcha-id",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-control-Allow-Origin": "https://www.wildberries.ru",
            "Content-Encoding": "gzip",
            "Content-Type": "application/json charset=utf-8"
        }

    def __get_catalog_headers(self) -> dict:
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ky;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
            'user-agent': UserAgent().random,
        }

    def __check_user_input(self, user_input: str):

        url = urlparse(user_input)
        if url.path in self.all_catalogs_path.keys():
            return url.path
        return False

    def __get_data_catalog_url(self, page, catalog_data):
        response = self.__request(
            self.CATALOG_URL.format(shard=catalog_data.get("shard"), query=catalog_data.get("query"), page=page),
            self.__get_catalog_headers()
        )
        if response:
            for product in response.get("data", {}).get("products", []):
                type(self).RESULT.append(
                    {
                        "Название": product.get("name"),
                        "Цена": a[0].get("price").get("basic") / 100 if (a := product.get("sizes")) else "не указана",
                        "Цена со скидкой": a[0].get("price").get("total") / 100 if (
                            a := product.get("sizes")) else "не указана",
                        "Рейтинг": product.get("reviewRating"),
                        "Количество отзывов": product.get("feedbacks"),
                    }
                )

        time.sleep(2)

    def get_user_input(self, user_input=None):
        """https://www.wildberries.by/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury"""
        # user_input_catalog = input("Введите ссылку на каталог продукции WB:")
        user_input_catalog = user_input
        if (a := self.__check_user_input(user_input_catalog)):
            catalog_data = self.all_catalogs_path.get(a)
            for page in range(1, self.MAX_PAGE):
                self.__get_data_catalog_url(page, catalog_data)
                print(f"[INFO] Страница {page}/{self.MAX_PAGE} обработана.")

            FilesHandler.write_json(f"{type(self).BASE_FILEPATH}/result.json", type(self).RESULT)

        else:
            print("Такого каталога нету.")

    def add_to_db(self):
        add_to_db = []
        if not type(self).RESULT:
            type(self).RESULT = FilesHandler.read_json(f"{type(self).BASE_FILEPATH}/result.json")

        for product in type(self).RESULT:
            add_to_db.append(
                ProductCard(
                    name=product.get("Название"),
                    price=product.get("Цена"),
                    sale_price=product.get("Цена со скидкой"),
                    rating=product.get("Рейтинг"),
                    review_count=product.get("Количество отзывов"),
                )
            )
        with Session(engine) as session:
            session.add_all(add_to_db)

            session.commit()

    def run(self):

        self.get_main_menu_catalogs_wb()
        self.get_user_input(self.user_input)

        self.add_to_db()


if __name__ == '__main__':
    wb = WB()
    wb.run()

    # headers = {
    #     'accept': '*/*',
    #     'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ky;q=0.7',
    #     'access-control-request-headers': 'authorization',
    #     'access-control-request-method': 'GET',
    #     'cache-control': 'no-cache',
    #     'origin': 'https://www.wildberries.by',
    #     'pragma': 'no-cache',
    #     'priority': 'u=1, i',
    #     'referer': 'https://www.wildberries.by/catalog/elektronika/igry-i-razvlecheniya/aksessuary/garnitury',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'cross-site',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
    # }
    #
    # response = requests.options(
    #     'https://catalog.wb.ru/catalog/electronic38/v2/catalog?ab_testing=false&appType=1&cat=9468&curr=byn&dest=-68617&hide_dtype=10;13;14&lang=ru&page=1&sort=popular&spp=30&uclusters=1&uiv=0&uv=AQMAAQIEAAMCAAEACbnFwDg9wMQ9Pww_xEAEu4a6rrlZvR9AFbdxO6Y8GDrPQNe_pr7qwR9AakaHxNnAXUF7QP67zUWYQYlCNMEfRIa_BcNGuTG_JDnov7M_00BcPpI37cCXwEO91byTwUpBOz01Q7y--UM5RDm-8MCowost57_zOOm_xb1Fx4_CakGgN_i6YLiLwzY_ZcAmusNBRD1FwFc5jDutPnmxw8EZt1xEQMIcuM-xGrwyx4M-0kMDxD9C00ClxQy9x8TtR3a3hbjmOJNEvcReQiyvZrzLQEWwDMEJxJC48LjxuPrHUEXHwObASLQaPx1GrjvqQxGjTqwbtlQ60j3cPCw8IDDrQtwBCAAA',
    #     headers=headers,
    # )
    #
    # print(response.text)

    # c = '''https://catalog.wb.ru/catalog/electronic38/catalog?appType=1&curr=rub&dest=-1075831,-77677,-398551,12358499' \
    #           f'&locale=ru&page=0' \
    #           f'®ions=64,83,4,38,80,33,70,82,86,30,69,1,48,22,66,31,40&sort=popular&spp=0&cat=9468'''
    #
    #
    # def __get_headers() -> dict:
    #     return {
    #         "User-Agent": UserAgent().random,
    #         "Access-Control-Allow-Credentials": "true",
    #         "Access-Control-Allow-Headers": "Authorization,Accept,Origin,DNT,User-Agent,Content-Type,Wb-AppType,Wb-AppVersion,Xwbuid,Site-Locale,X-Clientinfo,Storage-Type,Data-Version,Model-Version,__wbl, x-captcha-id",
    #         "Access-Control-Allow-Methods": "GET,OPTIONS",
    #         "Access-control-Allow-Origin": "https://www.wildberries.ru",
    #         "Content-Encoding": "gzip",
    #         "Content-Type": "application/json charset=utf-8"
    #     }
    #
    #
    # headers = {
    #     'accept': '*/*',
    #     'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ky;q=0.7',
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
    #     'x-captcha-id': 'Catalog 1|1|1750771003|AA==|5cb982f42bd241bb8bed0a8a84f56f0f|tH0Bk8lwE6flVd0yNDALJtvmCDjwLe2WhbEhzgMnp5Q',
    # }
    #
    # response = requests.get(
    #     'https://catalog.wb.ru/catalog/electronic38/v2/catalog?ab_testing=false&appType=1&cat=9468&curr=byn&dest=-59202&hide_dtype=10;13;14&lang=ru&page=1&sort=popular&spp=30',
    #     # f'https://catalog.wb.ru/catalog/{shard}/v2/catalog?ab_testing=false&appType=1&{query}&curr=byn&dest=-59202&hide_dtype=10;13;14&lang=ru&page={page}&sort=popular&spp=30',
    #     headers=headers,
    # )
    #
    # print(response.json().get('data', {}).get('products', []))
