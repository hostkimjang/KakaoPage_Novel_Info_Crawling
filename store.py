import json
import pprint

def store_info(info_list):
    with open("kakao_novel_info.json", "wt", encoding="utf-8") as f:
        novel_data = []
        for info in info_list:
            novel_dict = {
                "platform": info.platform,
                "title": info.title,
                "info": info.info,
                "author": info.author,
                "agegrade": info.agegrade,
                "category": info.category,
                "tag": info.tag,
                "view": info.view,
                "id": info.id,
                "content_type": info.content_type,
                "free_type": info.free_type,
                "new_status": info.new_status,
                "thumbnail": info.thumbnail
            }
            novel_data.append(novel_dict)
        json.dump(novel_data, f, ensure_ascii=False, indent=4)

    count = len(info_list)
    print(f"총 {count}개의 데이터가 저장되었습니다.")
    print("store is done")

def store_final(info_list):
    with open("kakao_novel_final.json", "wt", encoding="utf-8") as f:
        json.dump(info_list, f, ensure_ascii=False, indent=4)
    print("store is done")


def load_data():
    with open("kakao_novel_info.json", "rt", encoding="utf-8") as f:
        data = json.load(f)
        print("load is done")
        count = len(data)
        print(f"총 {count}개의 데이터가 로드되었습니다.")
    return data

