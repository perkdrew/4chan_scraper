import json

import scrapy

from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

filename = "4chan_dataset.txt"

class pepeSpider(scrapy.Spider):
    name = "pepe_spider"
    allowed_domains = ["4chan.org"]
    start_urls = ["http://boards.4channel.org/adv/", #Advice
                    "http://boards.4chan.org/pol/", #Politically Incorrect
                    "http://boards.4chan.org/b/", #Random
                    "http://boards.4chan.org/s4s/"] #Sh*t 4chan Says
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
                    "http://boards.4chan.org/s4s/"] #Sh*t 4chan Says
        items = {}
        
        boards = response.xpath("/html/body/div[3]/div[2]/text()").extract()
        posts = response.xpath("/html/body/form[2]/div[1]/div[@class='thread']/div[1]/div[1]/blockquote/text()").extract()
        
        if posts[0].startswith("https") or posts[0].startswith("\u2022") or posts[0].endswith(":"):
            del boards, posts

        else:    
            items["Boards"] = boards
            items["Posts"] = posts

            with open(filename, "a+") as f:
                f.write(json.dumps(items)+ "\n")

        yield items

        for threads in start_urls:
            next_page = threads +str(pepeSpider.page_num)+ "/"
            if pepeSpider.page_num <= 35:
                pepeSpider.page_num += 1
                yield response.follow(next_page, callback=self.parse)


# intitiate
process = CrawlerProcess({
                "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })

# tell the process which spider to use
process.crawl(pepeSpider)

# strart the crawl
process.start()