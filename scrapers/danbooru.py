import requests
from bs4 import BeautifulSoup

result = requests.get("https://danbooru.donmai.us/")
#print(result.status_code) # 200 means accessible
src = result.content

soup = BeautifulSoup(src, 'lxml')
links = soup.find_all("a")

for link in links:
    print("NEW LINK")
    print(link)
