import json
import pprint

def store_info(info_list):
    with open("kakao_novel_info.json", "wt", encoding="utf-8") as f:
        novel_data = []
        for info in info_list:
            novel_dict = {
                "platform": info.platform,
                "title": info.title,
                "agegrade": info.agegrade,
                "category": info.category,
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