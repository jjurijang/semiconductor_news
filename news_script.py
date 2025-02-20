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

    # CSV 파일 이름
    csv_filename = "news_data.csv"
    header = ["DateTime", "Title", "Link", "Description", "PubDate"]

    # CSV 파일이 이미 존재하는지 확인
    file_exist = os.path.isfile(csv_filename)

    # CSV 파일 열기 (추가 모드)
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 파일이 존재하지 않으면 헤더 추가
        if not file_exist:
            writer.writerow(header)

        # 뉴스 데이터 추가
        for item in items:
            title = item["title"]
            link = item["link"]
            description = item["description"]
            pubDate = item["pubDate"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([timestamp, title, link, description, pubDate])

    print("✅ 뉴스 데이터 CSV 저장 완료!")

else:
    print("❌ Error Code:", rescode)
