import time
from pprint import pprint
import requests
from soupsieve.pretty import pretty
from db_connect import store_db_kakao_pg_copy
from DB_processing import store_db
from sort_data import sort_data, info_supplement_parallel
from sort_data import info_supplement
from store import store_info
from store import load_data
from store import store_final
import json
from bs4 import BeautifulSoup as bs
import concurrent.futures
import copy


url = 'https://bff-page.kakao.com/graphql/'

max_worker = 50

headers = {
    # "Content-Type": "application/json",
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

def get_nested_value(data_dict, path, default=None):
    """
    중첩된 딕셔너리와 리스트에서 안전하게 값을 가져옵니다.
    path: 키와 인덱스의 리스트 (예: ["props", "pageProps", "queries", 0, "totalCount"])
    """
    current = data_dict
    for key_or_index in path:
        if isinstance(current, dict):
            current = current.get(key_or_index)
        elif isinstance(current, list):
            try:
                current = current[key_or_index]
            except (IndexError, TypeError): # TypeError for non-integer index
                return default
        else:
            return default

        if current is None and key_or_index != path[-1]: # 경로의 마지막이 아닌데 None이면 중간에 끊김
            return default
    return current


def get_last_page_num():
    retry = 10
    url = "https://page.kakao.com/menu/10011/screen/84"

    for attempt in range(1, retry + 1):
        try:
            print(f"[{attempt}/{retry}] 요청 중...")

            page = requests.get(url, headers=headers, timeout=10)
            if page.status_code != 200:
                raise Exception(f"비정상 응답 코드: {page.status_code}")

            soup = bs(page.text, "lxml")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag:
                raise ValueError("__NEXT_DATA__ 스크립트 태그가 없음")

            data = json.loads(script_tag.string)
            # pprint(data)

            path_to_total_count = [
                "props", "pageProps", "initialProps", "dehydratedState",
                "queries", 0, "state", "data", "staticLandingGenreLayout",
                "sections", 0, "totalCount"
            ]

            total_count = get_nested_value(data, path_to_total_count)
            result = round(int(total_count) / 24)

            pprint(f"총 {total_count}개 작품")
            pprint(f"총 {result}페이지")
            time.sleep(5)
            return result

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            if attempt == retry:
                print("🚫 최대 재시도 횟수 초과. 실패.")
                return None
            time.sleep(1.5)  # 재시도 간 대기


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
    store_db_kakao_pg_copy()
