import scrapy


class BlogSpiderCss(scrapy.Spider):
    name = 'blog-css'
    start_urls = [
        'http://blog.csdn.net/u012814856'
    ]

    def parse(self, response):
        for article in response.css('div.article_item'):
            if len(article.css('font[color=red]')) > 0:
                title = ''.join(article.css('span[class=link_title] a::text').extract())
            else:
                title = article.css('span.link_title a::text').extract_first()
            yield {
               'title': title.replace('\r\n','').strip(),
               'view': article.css('span.link_view::text').extract_first().replace('(', '').replace(')', ''),
               'comment': article.css('span.link_comments::text').extract_first().replace('(', '').replace(')', ''),
            }
            next_page = response.css('#papelist > a:nth-last-child(2)::attr(href)').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))





