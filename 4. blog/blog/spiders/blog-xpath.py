import scrapy


class BlogSpiderXPath(scrapy.Spider):
    name = 'blog-xpath'
    start_urls = [
        'http://blog.csdn.net/u012814856'
    ]

    def parse(self, response):
        for article in response.xpath('//div[@class="list_item article_item"]'):
            yield {
                'title': ''.join(article.xpath('.//span[@class="link_title"]/a/text()'
                                               ).extract()).replace('\r\n', '').strip(),
                'view': article.xpath('.//span[@class="link_view"]/text()'
                                      ).extract_first().replace('(', '').replace(')', '').strip(),
                'comment': article.xpath('.//span[@class="link_comments"]/text()'
                                         ).extract_first().replace('(', '').replace(')', '').strip()
            }
            next_page = response.xpath('//*[@id="papelist"]/a[6]/@href').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))
