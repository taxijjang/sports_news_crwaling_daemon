
from module import daemon
from sport_news_crwaling import NewsCrwaling
import time


class Sport_News_Crwaling_Daemon(daemon):
        def __init__(self):
                daemon.__init__(self, '/tmp/sport_news_crwaling_daemon.pid')
                self.news = NewsCrwaling()

        def run(self):
                while(True):
                        self.news.main()
                        time.sleep(600)

if __name__=="__main__":
        d = Sport_News_Crwaling_Daemon()
        d.start()


