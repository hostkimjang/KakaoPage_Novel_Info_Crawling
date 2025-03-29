import time
from pprint import pprint
import requests
from DB_processing import store_db
from sort_data import sort_data, info_supplement_parallel
from sort_data import info_supplement
from store import store_info
from store import load_data
from store import store_final
from bs4 import BeautifulSoup as bs
import concurrent.futures
import copy


url = 'https://bff-page.kakao.com/graphql/'

max_worker = 50

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
    total = 0
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
        pprint(page)
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

def get_novel_info_full_parallel(novel_list, last_num, max_workers=10):
    """병렬 처리로 여러 페이지를 동시에 가져옵니다."""

    def process_page(page_num):
        # 각 스레드에서 사용할 복사본 생성
        local_variables = copy.deepcopy(variables)
        local_variables["param"]["page"] = page_num

        data = {
            "query": query,
            "variables": local_variables
        }

        try:
            response = requests.post(
                url=url,
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                page_novels = []
                sort_data(response, page_novels)
                print(f"Page {page_num} response: {len(page_novels)} novels")
                return page_novels
            else:
                print(f"Error on page {page_num}: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception on page {page_num}: {e}")
            return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 모든 페이지 작업 제출
        future_to_page = {executor.submit(process_page, page): page for page in range(0, last_num)}

        # 결과 수집
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                page_novels = future.result()
                novel_list.extend(page_novels)
                print(f"Current total: {len(novel_list)} novels")
            except Exception as e:
                print(f"Error collecting results from page {page}: {e}")

    store_info(novel_list)
    return novel_list


def get_novel_more_info(novel_list):
    novel_list = load_data()
    info_supplement_parallel(novel_list, max_workers=max_worker)
    # info_supplement(novel_list)
    store_final(novel_list)

if __name__ == '__main__':
    novel_list = []
    #last_num = 100
    last_num = get_last_page_num()     #모든 소설의 정보를 얻을건가용?
    #get_novel_info_full(last_num)      #소설 정보를 얻어봐용
    get_novel_info_full_parallel(novel_list, last_num, max_workers=10)  # 병렬 처리로 실행
    get_novel_more_info(novel_list)    #소설 정보를 보충해봐용
    store_db()
