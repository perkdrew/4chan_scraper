import json

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

#Export data
filename = "4chan_scrape.csv"

class pepeSpider(scrapy.Spider):
    name = "pepe_spider"
    allowed_domains = ["4chan.org"]
    start_urls = ["http://boards.4channel.org/adv/", #Advice
                    "http://boards.4chan.org/pol/", #Politically Incorrect
                    "http://boards.4chan.org/b/", #Random
                    "http://boards.4chan.org/s4s/", #Sh*t 4chan Says 
                    "http://boards.4chan.org/r9k/"] #ROBOT9001
    rules = (Rule(LinkExtractor(allow=(),
                                restrict_xpaths=("//div[@class='next']")),
                                callback="parse",
                                follow=True),
                                )

    page_num = 2

    def parse(self,response):
        start_urls = ["http://boards.4channel.org/adv/", #Advice
                    "http://boards.4chan.org/pol/", #Politically Incorrect
                    "http://boards.4chan.org/b/", #Random
                    "http://boards.4chan.org/s4s/", #Sh*t 4chan Says
                    "http://boards.4chan.org/r9k/"] #ROBOT9001
        
        custom_settings = {
        "DOWNLOAD_DELAY" : "5",
        "USER_AGENT" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "DOWNLOAD_TIMEOUT" : "60" 
        }
        
        items = []
        
        board_name = response.xpath("/html/body/div[3]/div[2]/text()").extract()[0]
        posts = response.xpath("//blockquote/text()").extract()
        
        for post in posts:
            item = {}
            item[board_name] = post
            items.append(item)

        with open(filename, "a+") as f:
            f.write(json.dumps(items))

        yield items

        for threads in start_urls:
            next_page = threads +str(pepeSpider.page_num)+ "/"
            if pepeSpider.page_num <= 50:
                pepeSpider.page_num += 1
                yield response.follow(next_page, callback=self.parse)


# intitiate
process = CrawlerProcess()

# tell the process which spider to use
process.crawl(pepeSpider)

# strart the crawl
process.start()