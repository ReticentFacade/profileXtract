import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='Z5CRDODMMISEEL4EF8179D0AVUUZ78ICRO6XLZC679UGA7UX07K8F56TF3G5H0UWUH4HTX3BRZ5FGLTP')

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class LinkedinProfilesSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls(api_key = crawler.settings.get('SCRAPINGBEE_API_KEY'))
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class LinkedinProfilesDownloaderMiddleware:
    def __init__(self, api_key):
        self.client = ScrapingBeeClient(api_key=api_key)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(api_key=crawler.settings.get('SCRAPINGBEE_API_KEY'))

    def process_request(self, request, spider):
        print(request.headers)
        if 'scrapingbee' in request.meta:
            # Use ScrapingBee to fetch the page
            # response = self.client.get(request.url)
            response = self.client.get(request.url, params={'premium_proxy': 'True'})
            return scrapy.http.HtmlResponse(url = response.url, body = response.content, encoding = "utf-8")

    def process_response(self, request, response, spider):
        print(f'response.status ------>', response.status)  # Print the response status code
        print(f'response.url ------>', response.url)     # Print the response URL
        # print(response.text)    # Print the response content
        return response

    def process_exception(self, request, exception, spider):
        pass

    # def spider_opened(self, spider):
    #     spider.logger.info("Spider opened: %s" % spider.name)
