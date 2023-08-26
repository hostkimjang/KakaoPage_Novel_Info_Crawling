import pprint
import re
import time
import json
import requests
from info import set_novel_info
from bs4 import BeautifulSoup as bs


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def sort_data(response, novel_list):
    res = response.json()
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

        novel_info = set_novel_info("KakaoPage",
                                    title,
                                    "not_ready_info",
                                    "not_ready_author",
                                    ageGrade,
                                    category,
                                    "not_ready_tag",
                                    view,
                                    id,
                                    content_type,
                                    free_type,
                                    new_status,
                                    thumbnail)
        novel_list.append(novel_info)

def info_supplement(novel_list):
    count = 1
    for novel in novel_list:
        id = novel['id']
        url = f"https://page.kakao.com/_next/data/2.12.2/ko/content/{id}.json"
        response = requests.get(url=url, headers=headers)
        soup = bs(response.text, "lxml")
        element = soup.select("p")[0].text
        page = json.loads(element)

        description = page["pageProps"]["metaInfo"]["description"]
        author = page["pageProps"]["metaInfo"]["author"]
        tmp = page["pageProps"]["dehydratedState"]["queries"]
        for i in tmp:
            contentHomeAbout = i["state"]["data"]["contentHomeAbout"]
            keyword_list = contentHomeAbout["themeKeywordList"]
            keyword = [item["title"] for item in keyword_list]
            keywords_combined = ', '.join(keyword)

        info = description
        #info = re.sub(r'\s+', ' ', description).replace('"', '')
        novel["info"] = info
        novel["author"] = author
        if not keywords_combined:
            novel["tag"] = "Tag_None"
        else:
            novel["tag"] = keywords_combined
        pprint.pprint(novel, sort_dicts=False)
        print(f"{count}번째 데이터가 추가되었습니다.")
        count += 1
        time.sleep(1)


