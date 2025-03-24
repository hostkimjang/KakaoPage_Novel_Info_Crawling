import concurrent.futures
import pprint
import time
import datetime
import requests
from info import set_novel_info
import re

max_retries = 3

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def sort_data(response, novel_list):
    res = response.json()
    #pprint.pprint(res)
    for group in res["data"]["staticLandingGenreSection"]["groups"]:
        items = group["items"]

    for i in items:
        meta = i['eventLog']['eventMeta']

        title = i['title']
        ageGrade = i['ageGrade']
        category = meta['subcategory']
        view = i['subtitleList'][0]
        id = meta['id']
        content_type = meta['category']
        if not i['badgeList']:
            free_type = "Free_None"
        else:
            free_type = i['badgeList'][0]
        new_status = i['statusBadge']
        thumbnail = i['thumbnail']
        locate = f"https://page.kakao.com/content/{id}"

        novel_info = set_novel_info("KakaoPage",
                                    title,
                                    "not_ready_info",
                                    "not_ready_author",
                                    ageGrade,
                                    category,
                                    "not_ready_tag",
                                    view,
                                    "not_ready_chapter",
                                    id,
                                    locate,
                                    content_type,
                                    free_type,
                                    new_status,
                                    "not_ready_lastupdate",
                                    thumbnail)
        novel_list.append(novel_info)


def info_supplement_parallel(novel_list, max_workers=10):

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 각 소설을 병렬로 처리합니다.
        futures = [executor.submit(process_novel, novel) for novel in novel_list]
        count = 0
        # 각 작업이 완료되는 즉시 메시지를 출력합니다.
        for future in concurrent.futures.as_completed(futures):
            result = future.result()  # 결과를 가져옵니다.
            count += 1
            print(f"{count}번째 데이터가 추가되었습니다.")
            # 실시간 처리 중 데이터 확인
            # pprint.pprint(result, sort_dicts=False)
    end = time.time()
    result = datetime.timedelta(seconds=end - start)
    pprint.pprint(f"크롤러 동작 시간 : {result}")




def process_novel(novel):
    id = novel['id']
    url = "https://bff-page.kakao.com/graphql/"
    variables = {"seriesId": id}
    with open("kakao_graphql_query_detail.txt", "r", encoding="utf-8") as file:
        query = file.read()

    data = {
        "query": query,
        "variables": variables
    }

    response = make_request(url, headers, data)
    if response is not None:
        data = response.json()
        try:
            content = data["data"]["contentHomeOverview"]["content"]
            description = content["description"]
            author = content["authors"]
            view = content["serviceProperty"]["viewCount"]
            last_update = content["lastSlideAddedDate"]
            chapter = data["data"]["contentHomeProductList"]["totalCount"]
            info = re.sub(r'\s+', ' ', description).replace('"', '')
            novel["info"] = info
            novel["author"] = author
            novel["view"] = view
            novel["chapter"] = chapter
            novel["lastupdate_date"] = last_update
        except Exception as e:
            print(f"Error processing novel id {id}: {e}")
    return novel


def info_supplement(novel_list):
    count = 1
    for novel in novel_list:
        id = novel['id']
        url = f"https://bff-page.kakao.com/graphql/"

        variables = {
	        "seriesId": id
        }

        with open("kakao_graphql_query_detail.txt", "r", encoding="utf-8") as file:
            query = file.read()

        data = {
            "query": query,
            "variables": variables
        }

        response = make_request(url, headers, data)
        if response is not None:
            data = response.json()
            #pprint.pprint(data)

            description = data["data"]["contentHomeOverview"]["content"]["description"]
            author = data["data"]["contentHomeOverview"]["content"]["authors"]
            view = data["data"]["contentHomeOverview"]["content"]["serviceProperty"]["viewCount"]
            last_update = data["data"]["contentHomeOverview"]["content"]["lastSlideAddedDate"]
            chapter = data["data"]["contentHomeProductList"]["totalCount"]
            info = re.sub(r'\s+', ' ', description).replace('"', '')

            novel["info"] = info
            novel["author"] = author
            novel["view"] = view
            novel["chapter"] = chapter
            novel["lastupdate_date"] = last_update

            pprint.pprint(novel, sort_dicts=False)
            print(f"{count}번째 데이터가 추가되었습니다.")
            count += 1


def make_request(url, headers, data):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(url=url, headers=headers, json=data)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외가 발생합니다.
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying...")
            retries += 1
            time.sleep(3)  # 재시도 전에 잠시 기다립니다.

    print("Max retries reached. Unable to make request.")
    return None


