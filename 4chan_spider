
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess


class PeppySpider(scrapy.Spider):
    name = "peppy_spider"

    def start_requests(self):
        urls = ["http://boards.4chan.org/pol/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # either go with csv or ptf
        csv_file = "4chan_boards.csv"
        with open(csv_file, "wb") as fout:
            fout.write(response.body)

# intitiate
process = CrawlerProcess()

# tell the process which spider to use
process.crawl(PeppySpider)

# strart the crawl
process.start()