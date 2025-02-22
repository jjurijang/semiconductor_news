import os
import csv
import urllib.request
import json
from datetime import datetime

csv_filename = "news_data.csv"
header = ["DateTime", "Title", "Link", "Description", "PubDate"]

def fetch_news():
    # 네이버 검색 API 설정
    display = 100  # 가져올 뉴스 개수
    start = 1
    sort = "date"
    search = "반도체"

    # GitHub Actions 등에서 API 키를 환경변수로 받아오기
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    enc_text = urllib.parse.quote(search)
    url = f"https://openapi.naver.com/v1/search/news?query={enc_text}&display={display}&start={start}&sort={sort}"

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(req)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body.decode("utf-8"))
        return data.get("items", [])
    else:
        print("❌ Error Code:", rescode)
        return []

def main():
    items = fetch_news()
    if not items:
        print("❌ 가져올 뉴스가 없거나 에러가 발생했습니다.")
        return

    # CSV가 아예 없으면, 먼저 헤더만 만든 파일 생성
    if not os.path.exists(csv_filename):
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    # 1) 기존 CSV 읽어오기
    existing_rows = []
    with open(csv_filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # 헤더 건너뛰기
        for row in reader:
            existing_rows.append(row)

    # 2) 새로운 뉴스 100개 받아서, 기존 데이터 뒤에 추가
    #    (원한다면 중복 체크 로직도 여기에 넣을 수 있음)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in items:
        title = item["title"]
        link = item["link"]
        desc = item["description"]
        pub_date = item["pubDate"]
        existing_rows.append([now_str, title, link, desc, pub_date])

    # 3) 전체에서 마지막 100개만 추출 → 항상 100개만 유지
    if len(existing_rows) > 100:
        existing_rows = existing_rows[-100:]

    # 4) 파일을 `r+`로 열어서, 맨 앞부터 다시 쓰고, 나머지 내용 잘라내기(truncate)
    with open(csv_filename, "r+", newline="", encoding="utf-8") as f:
        # 파일 포인터를 맨 앞으로 이동
        f.seek(0)

        # 기존 내용 지우기
        f.truncate()

        writer = csv.writer(f)
        # 헤더 다시 쓰기
        writer.writerow(header)
        # 최신 100개 데이터 쓰기
        for row in existing_rows:
            writer.writerow(row)

    print("✅ 뉴스 데이터 CSV 저장 완료! (항상 최신 100개 유지)")

if __name__ == "__main__":
    main()
