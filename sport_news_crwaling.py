import requests
from bs4 import BeautifulSoup
import redis
import time
import json
import collections


class NewsCrwaling:

    def __init__(self):
        self.rconn = redis.StrictRedis(host='ec2-3-34-134-147.ap-northeast-2.compute.amazonaws.com', port=6379, db=1,
                                       decode_responses=True)
        self.redis_data_expire_time = 252000

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
            esports='/esports/index.nhn'
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
                    news_data = {'title': title.text, 'url': base_url + title.get('href')}
                    news_dict.update({rank + 1: news_data})



            elif web_site_name == "daum":
                for rank, title in enumerate(titles):
                    news_data = {'title': title.text, 'url': title.get('href')}
                    news_dict.update({rank + 1: news_data})

            print(web_site_name, category, news_dict)
            news_dict = json.dumps(news_dict, ensure_ascii=False).encode('utf-8')
            key = web_site_name + ':' + category
            self.rconn.set(key, news_dict, self.redis_data_expire_time)

    def main(self):
        self.daum_sports_crwaling
        self.naver_sports_crwaling


if __name__ == "__main__":git
    news_crwaling = NewsCrwaling()

    while (True):
       news_crwaling.main()

       time.sleep(600)
