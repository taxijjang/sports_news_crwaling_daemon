import requests
from bs4 import BeautifulSoup
import time
import sqlalchemy as db
import secret


class NewsCrwaling:

    def __init__(self):
        self.engine = db.create_engine(secret.SECRET['mysql'], echo=True)

    @property
    def naver_sports_crwaling(self):
        web_site_name = 'naver'
        base_url = "https://sports.news.naver.com/"

        sport_news_category_urls = dict(
            baseball='kbaseball/index.nhn',
            wbaseball='wbaseball/index.nhn',
            football='kfootball/index.nhn',
            wfootball='wfootball/index.nhn',
            basketball='basketball/index.nhn',
            volleyball='volleyball/index.nhn',
            golf='golf/index.nhn',
            general='general/index.nhn',
            esports='esports/index.nhn'
        )

        sport_news_category = list()
        for id, category in enumerate(sport_news_category_urls.keys()):
            sport_news_category.append({'category': category})

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
            baseball='baseball',
            wbaseball='worldbaseball',
            football='soccer',
            basketball='basketball',
            volleyball='volleyball',
            golf='golf',
            general='general',
            esports='esports',
        )

        sport_news_category = list()
        for id, category in enumerate(sport_news_category_urls.keys()):
            sport_news_category.append({'id': id + 1, 'category': category})

        select_location = '#cSub > div > div.top_rank > ol:nth-child(3)'
        a_tag_class_name = 'link_txt'

        self.crwaling_operator(web_site_name=web_site_name,
                               base_url=base_url,
                               sport_news_category_urls=sport_news_category_urls,
                               select_location=select_location,
                               a_tag_class_name=a_tag_class_name)

    def crwaling_operator(self, web_site_name, base_url, sport_news_category_urls, select_location,
                          a_tag_class_name):
        with self.engine.connect() as connection:
            connection.execute(f'TRUNCATE TABLE {web_site_name}_sports_news')
            sports_news_list = []

            for category, sport_news_category_url in sport_news_category_urls.items():
                req = requests.get(base_url + sport_news_category_url)
                html = req.text

                soup = BeautifulSoup(html, 'html.parser')

                news = soup.select(
                    select_location
                )
                titles = news[0].find_all('a', class_=a_tag_class_name)

                if web_site_name == "naver":
                    for rank, title in enumerate(titles):
                        sports_news_list.append({'flatform': web_site_name, 'category': category, 'rank': rank + 1,
                                                 'title': title.text,
                                                 'url': base_url + str(title.get('href')).lstrip('/')})

                elif web_site_name == "daum":
                    for rank, title in enumerate(titles):
                        sports_news_list.append({'flatform': web_site_name, 'category': category, 'rank': rank + 1,
                                                 'title': title.text,
                                                 'url': str(title.get('href')).lstrip('/')})

            table = db.Table(web_site_name+'_sports_news', db.MetaData(), autoload=True, autoload_with=self.engine)
            query = db.insert(table)
            result_proxy = connection.execute(query, sports_news_list)
            result_proxy.close()

    def main(self):
        self.daum_sports_crwaling
        self.naver_sports_crwaling


if __name__ == "__main__":
    news_crwaling = NewsCrwaling()

    while (True):
        news_crwaling.main()
        time.sleep(600)
