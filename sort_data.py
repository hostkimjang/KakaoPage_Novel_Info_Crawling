import pprint
from info import set_novel_info

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
            free_type = "None"
        else:
            free_type = i['badgeList'][0]
        new_status = i['statusBadge']
        thumbnail = i['thumbnail']

        novel_info = set_novel_info("KakaoPage",
                                    title,
                                    ageGrade,
                                    category,
                                    view,
                                    id,
                                    content_type,
                                    free_type,
                                    new_status,
                                    thumbnail)
        novel_list.append(novel_info)
