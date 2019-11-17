from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from vacancyparser import settings
from vacancyparser.spiders.hhru import HhruSpider
from vacancyparser.spiders.sjru import SjruSpider
import time
from datetime import timedelta


start_time = time.monotonic()

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)
    process.start()


end_time = time.monotonic()
print(timedelta(seconds=end_time - start_time))
