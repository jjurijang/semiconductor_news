import urllib.request
import json
import sqlite3
import os

# 네이버 검색 API 설정
display = 10  # 가져올 뉴스 개수
start = 1
sort = "date"
search = "AI"

# 환경변수에서 API 키 가져오기 (GitHub Actions에서 사용)
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
encText = urllib.parse.quote(search)

url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&start={start}&sort={sort}"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    response_body = response.read()
    data = json.loads(response_body.decode("utf-8"))
    items = data["items"]

    # SQLite DB 저장
    conn = sqlite3.connect("news_data.db")
    curs = conn.cursor()

    curs.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            description TEXT,
            pubDate TEXT
        )
    """)

    for item in items:
        title = item["title"]
        link = item["link"]
        description = item["description"]
        pubDate = item["pubDate"]

        curs.execute("INSERT INTO news (title, link, description, pubDate) VALUES (?, ?, ?, ?)",
                     (title, link, description, pubDate))

    conn.commit()
    conn.close()
else:
    print("❌ Error Code:", rescode)
