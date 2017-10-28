import scrapy


class BlogSpiderXPath(scrapy.Spider):
    name = 'blog-xpath'

    # 默认传入本人的博客名称，也可以使用 Spider 参数指定名称
    # scrapy crawl blog-xpath -a user=xxx -o blog-xpath.xml
    def __init__(self, user='u012814856', *args, **kwargs):
        super(BlogSpiderXPath, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://blog.csdn.net/%s' % user
        ]

    def parse(self, response):
        for article in response.xpath('//div[@class="list_item article_item"]'):
            yield {
                # 这里要区分该标题是否置顶，如果是置顶的，解析出来就会有两个元素
                # ['\r\n        ', '\r\n        思考的救赎（二）：三消游戏功能完善            \r\n        ']
                # 此时使用 ''.join 即可转换为 str 然后去除空白元素即可
                'title': ''.join(article.xpath('.//span[@class="link_title"]/a/text()'
                                               ).extract()).replace('\r\n', '').strip(),
                'view': article.xpath('.//span[@class="link_view"]/text()'
                                      ).extract_first().replace('(', '').replace(')', '').strip(),
                'comment': article.xpath('.//span[@class="link_comments"]/text()'
                                         ).extract_first().replace('(', '').replace(')', '').strip()
            }
            next_page = response.xpath('//*[@id="papelist"]/a[last() - 1]/@href'
                                       ).extract_first()
            print('This is %s' % next_page)
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))
