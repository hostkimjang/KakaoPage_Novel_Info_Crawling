import time
import requests

from DB_processing import store_db
from sort_data import sort_data
from sort_data import info_supplement
from store import store_info
from store import load_data
from store import store_final
from bs4 import BeautifulSoup as bs


url = 'https://bff-page.kakao.com/graphql/'

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# GraphQL 쿼리 파일 읽기
with open("kakao_graphql_query.txt", "r", encoding="utf-8") as file:
    query = file.read()

# pprint.pprint(query)

variables = {
    "sectionId": "static-landing-Genre-section-Layout-11-0-update-false-84",
    "param": {
        "categoryUid": 11,
        "subcategoryUid": "0",
        "sortType": "update", #latest, update
        "isComplete": False,
        "screenUid": 84,
        "page": 0
    }
}

def get_last_page_num():
    url = f"https://page.kakao.com/menu/10011/screen/84"
    page = requests.get(url)
    soup = bs(page.text, "lxml")
    last_page = soup.select(f"#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div.flex.h-44pxr.w-full.flex-row.items-center.justify-between.bg-bg-a-10.px-15pxr > div.flex.h-full.flex-1.items-center.space-x-8pxr > span")
    for element in last_page:
        total = element.text
    print(total)
    num = total.replace("개", "").replace(",", "")
    result = round(int(num) / 24)
    print(result)
    return result + 1

def get_novel_info_full(last_num):
    for page in range(0, last_num):
        variables["param"]["page"] = page

        data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(
            url=url,
            headers=headers,
            json=data
        )

        sort_data(response, novel_list)

        print(f"Page {page} response:")
        time.sleep(1)

    store_info(novel_list)

def get_novel_more_info(novel_list):
    novel_list = load_data()
    info_supplement(novel_list)
    store_final(novel_list)
    store_db()


novel_list = []
#last_num = 100
last_num = get_last_page_num()     #모든 소설의 정보를 얻을건가용?
get_novel_info_full(last_num)      #소설 정보를 얻어봐용
get_novel_more_info(novel_list)    #소설 정보를 보충해봐용