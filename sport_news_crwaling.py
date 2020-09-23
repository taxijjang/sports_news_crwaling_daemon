import requests
from bs4 import BeautifulSoup
import redis
import time
from daemon import runner

class NewsCrwaling:

    def __init__(self):
        self.rconn = redis.StrictRedis(host='ec2-3-34-134-147.ap-northeast-2.compute.amazonaws.com', port=6379, db=1,
                                       decode_responses=True)
    @property
    def naver_sports_crwaling(self):
        web_site_name = 'naver'
        base_url = "https://sports.news.naver.com"

        sport_news_category_urls = dict(
            baseball='/kbaseball/index.nhn',
            wbaseball='/wbaseball/index.nhn',
            football='/kfootball/index.nhn',
            wfootball='/wfootball/index.nhn',
            basketball='/basketball/index.nhn',
            volleyball='/volleyball/index.nhn',
            golf='/golf/index.nhn',
            general='/general/index.nhn',
            esports='/esports/index.nhn',
        )

        select_location = '#content > div > div.home_feature > div.feature_side > div > ol'
        a_tag_class_name = 'link_news_end'
        self.crwaling_operator(web_site_name=web_site_name,
                               base_url=base_url,
                               sport_news_category_urls=sport_news_category_urls,
                               select_location=select_location,
                               a_tag_class_name=a_tag_class_name)

    @property
    def daum_sports_crwaling(self):
        web_site_name = 'daum'
        base_url = "https://sports.daum.net/"

        sport_news_category_urls = dict(
            soccer='soccer',
            baseball='baseball',
            worldbaseball='worldbaseball',
            golf='golf',
            basketball='basketball',
            volleyball='volleyball',
            general='general',
            esports='esports',
        )
        select_location = '#cSub > div > div.top_rank > ol:nth-child(3)'
        a_tag_class_name = 'link_txt'

        self.crwaling_operator(web_site_name=web_site_name,
                               base_url=base_url,
                               sport_news_category_urls=sport_news_category_urls,
                               select_location=select_location,
                               a_tag_class_name=a_tag_class_name)

    def crwaling_operator(self, web_site_name: str, base_url: str, sport_news_category_urls: dict, select_location: str,
                          a_tag_class_name: str) -> None:
        for category, sport_news_category_url in sport_news_category_urls.items():
            req = requests.get(base_url + sport_news_category_url)
            html = req.text

            soup = BeautifulSoup(html, 'html.parser')

            news = soup.select(
                select_location
            )
            titles = news[0].find_all('a', class_=a_tag_class_name)

            news_dict = dict()
            if web_site_name == "naver":
                for rank, title in enumerate(titles):
                    #print(f"{rank + 1}위 : {title.text} , 주소 : {base_url + title.get('href')}")
                    news_dict.update({title.text: base_url + title.get('href')})
                    self.rconn.hset(web_site_name + ':' + category, title.text, base_url + title.get('href'))

            elif web_site_name == "daum":
                for rank, title in enumerate(titles):
                    #print(f"{rank + 1}위 : {title.text} , 주소 : {title.get('href')}")
                    news_dict.update({title.text: title.get('href')})
                    self.rconn.hset(web_site_name + ':' + category, title.text, base_url + title.get('href'))

    def main(self):
        self.daum_sports_crwaling
        self.naver_sports_crwaling

if __name__=="__main__":
    news_crwaling = NewsCrwaling()

    while(True):
        news_crwaling.main()

        time.sleep(600)
