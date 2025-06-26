import sqlite3
import json
import os
import time
from datetime import datetime
from pprint import pprint


def load_finish_data():
    with open('kakao_novel_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        pprint(f"총 {len(data)}개 데이터 로드 완료")
        return data

def change_log(result):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_directory = 'DB_Processing_Log'

    # 디렉터리가 없으면 생성
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, f'{timestamp}-log.json')

    def datetime_convert(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError(f'Type {type(obj)} not supported.')

    with open(log_file_path, 'w', encoding='utf-8') as f :
        json.dump(result, f, ensure_ascii=False, indent=4, default=datetime_convert)



def store_db():
    novel_list = load_finish_data()
    conn = sqlite3.connect('kakao_page.db')
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS novel (
            id INTEGER PRIMARY KEY,
            platform TEXT, 
            title TEXT, 
            author TEXT, 
            info TEXT, 
            agegrade TEXT, 
            category TEXT, 
            hashtag TEXT, 
            views INTEGER DEFAULT 0, 
            chapter INTEGER DEFAULT 0, 
            thumbnail TEXT, 
            content_type TEXT, 
            free_type TEXT, 
            new_status TEXT,
            updatedate DATETIME, 
            del INTEGER DEFAULT 0,
            locate TEXT, 
            crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    count = 1
    total = []
    start_time = time.time()
    dt = datetime.now()
    for novel in novel_list:
        if novel is None:
            print("데이터가 없습니다 또는 삭제, 작업이 정상으로 완료되지 않음.")
            continue

        # lastupdate_date가 누락된 경우 건너뛰기 (선택사항)
        if "lastupdate_date" not in novel or novel["lastupdate_date"] is None:
            print(f"ID {novel.get('id', 'Unknown')}: lastupdate_date 누락, 건너뛰기")
            continue

        novel["lastupdate_date"] = novel["lastupdate_date"].isoformat() if isinstance(novel["lastupdate_date"],datetime) else novel["lastupdate_date"]
        novel["crawl_timestamp"] = dt

        existing_record = cur.execute("SELECT * FROM novel WHERE id=?", (novel["id"],)).fetchone()

        if existing_record:
            print(f"{novel['id']}는 이미 존재합니다. 레코드를 업데이트하거나 무시합니다.")

            column = existing_record  # 기존 데이터 저장
            changes = {}

            pprint(novel)
            novel.setdefault("hashtag", "")
            novel.setdefault("chapter", 0)
            novel.setdefault("view", 0)
            novel.setdefault("new_status", "")
            novel.setdefault("content_type", "")
            novel.setdefault("free_type", "")
            novel.setdefault("agegrade", "")
            novel.setdefault("category", "")
            novel.setdefault("author", "")
            novel.setdefault("title", "")
            novel.setdefault("info", "")
            novel.setdefault("thumbnail", "")
            novel.setdefault("locate", "")


            # 변경 사항 확인 (필요할 때만 업데이트)
            fields = [
                ("platform", 1), ("title", 2), ("author", 3), ("info", 4), ("agegrade", 5),
                ("category", 6), ("hashtag", 7), ("view", 8), ("chapter", 9),
                ("thumbnail", 10), ("content_type", 11), ("free_type", 12),
                ("new_status", 13), ("lastupdate_date", 14), ("crawl_timestamp", 15)
            ]

            for field, index in fields:
                if column[index] != novel[field]:
                    changes[field] = {"before": column[index], "after": novel[field]}

            if changes:
                print(f"변경된 사항: {changes}")
                total.append({"ID": novel["id"], "Changes": changes})

                cur.execute("""
                    UPDATE novel 
                    SET title=?, author=?, info=?, views=?, chapter=?, thumbnail=?, 
                        hashtag=?, category=?, agegrade=?, content_type=?, free_type=?, new_status=?, updatedate=?, crawl_timestamp=?, locate=?
                    WHERE id=?
                """, (
                    novel["title"], novel["author"], novel["info"], novel["view"], novel["chapter"],
                    novel["thumbnail"], novel["hashtag"], novel["category"], novel["agegrade"],
                    novel["content_type"], novel["free_type"], novel["new_status"], novel["lastupdate_date"], novel["crawl_timestamp"], novel["locate"], novel["id"]
                ))
        else:
            print(f"ID:{novel['id']}는 존재하지 않습니다. 새 레코드를 삽입합니다.")
            cur.execute("""
                INSERT INTO novel
                (id, platform, title, author, info, agegrade, category, hashtag, views, chapter,
                 thumbnail, content_type, free_type, new_status, updatedate, crawl_timestamp, locate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                novel["id"], novel["platform"], novel["title"], novel["author"], novel["info"], novel["agegrade"],
                novel["category"], novel["tag"], novel["view"], novel["chapter"],
                novel["thumbnail"], novel["content_type"], novel["free_type"], novel["new_status"],
                novel["lastupdate_date"], novel["crawl_timestamp"], novel["locate"]
            ))

        print(f"{count}/{len(novel_list)}번째 데이터 저장 완료")
        count += 1

    end_time = time.time()
    print(f"총 {end_time - start_time:.2f}초 소요")
    print("데이터 저장 완료")

    conn.commit()
    conn.close()

    if total:
        change_log(total)  # 변경 사항이 있을 때만 로그 생성


if __name__ == '__main__':
    store_db()