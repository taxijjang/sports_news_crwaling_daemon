import urllib.request
from bs4 import BeautifulSoup

url = "https://www.google.com"
soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
a_tags = soup.find_all('a')
result_list = []

for i in a_tags:
    result_list.append(i.get_text())

print(result_list)