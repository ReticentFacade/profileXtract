import scrapy

class LinkedinProfileSpider(scrapy.Spider):
    name = "linkedin_profile_spider"
    allowed_domains = ["linkedin.com"]
    # handle_httpstatus_list=[999]

    def start_requests(self):
        profile_list = ["reidhoffman", "williamhgates"]
        for profile in profile_list:
            linkedin_ppl_url = f"https://www.linkedin.com/in/{profile}"
            yield scrapy.Request(url = linkedin_ppl_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_ppl_url, 'scrapingbee': True})

    def parse_profile(self, response):
        item = {}
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']

        """
            SUMMARY SECTION:
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        yield item