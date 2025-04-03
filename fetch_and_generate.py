import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://aict.snu.ac.kr/?p=92"
base_url = "https://aict.snu.ac.kr"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

items = soup.select(".gallery_list li")[:5]

now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")
rss_items = ""

for item in items:
    title_tag = item.select_one("span.title a")
    title = title_tag.text.strip()
    raw_link = title_tag["href"]
    link = base_url + raw_link if not raw_link.startswith("http") else raw_link

    img_tag = item.select_one("span.photo img")
    img_url = base_url + img_tag["src"] if img_tag else ""

    rss_items += f"""
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <pubDate>{now}</pubDate>
    <description><![CDATA[
      <img src="{img_url}" width="500"><br>
      <a href="{link}">{title}</a>
    ]]></description>
  </item>
"""

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>AICT 게시판 최신 5개</title>
  <link>{url}</link>
  <description>서울대 AICT 최근 게시물</description>
  <lastBuildDate>{now}</lastBuildDate>
{rss_items}
</channel>
</rss>"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("✅ feed.xml 생성 완료")
