import urllib.request
import json
import csv
import os
from datetime import datetime

# 네이버 검색 API 설정
display = 100  # 가져올 뉴스 개수
start = 1
sort = "date"
search = "반도체"

# 환경변수에서 API 키 가져오기 (GitHub Actions 등에서 사용)
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

    # CSV 파일 이름
    csv_filename = "news_data.csv"
    header = ["DateTime", "Title", "Link", "Description", "PubDate"]

    # 이렇게 하면 매번 실행할 때마다 CSV가 새로 작성되므로, 
    # 항상 최신 100개의 뉴스만 보관됩니다.
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # 헤더 작성

        # 최신 뉴스 데이터 100개를 그대로 작성
        for item in items:
            title = item["title"]
            link = item["link"]
            description = item["description"]
            pubDate = item["pubDate"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([timestamp, title, link, description, pubDate])

    print("✅ 뉴스 데이터 CSV 저장 완료! (최신 100개)")
