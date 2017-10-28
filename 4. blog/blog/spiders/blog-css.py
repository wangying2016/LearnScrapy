import scrapy


class BlogSpiderCss(scrapy.Spider):
    name = 'blog-css'

    # 默认传入本人的博客名称，也可以使用 Spider 参数指定名称
    # scrapy crawl blog-css -a user=xxx -o blog-css.xml
    def __init__(self, user='u012814856', *args, **kwargs):
        super(BlogSpiderCss, self).__init__(*args, **kwargs)
        self.start_urls = [
            'http://blog.csdn.net/%s' % user
        ]

    def parse(self, response):
        for article in response.css('div.article_item'):
            yield {
                # 这里要区分该标题是否置顶，如果是置顶的，解析出来就会有两个元素
                # ['\r\n        ', '\r\n        思考的救赎（二）：三消游戏功能完善            \r\n        ']
                # 此时使用 ''.join 即可转换为 str 然后去除空白元素即可
                'title': ''.join(article.css('span.link_title a:not(font)::text').extract()
                                ).replace('\r\n', '').strip(),
                'view': article.css('span.link_view::text').extract_first().replace('(', '').replace(')', ''),
                'comment': article.css('span.link_comments::text').extract_first().replace('(', '').replace(')', ''),
            }
            next_page = response.css('#papelist > a:nth-last-child(2)::attr(href)').extract_first()
            if next_page is not None:
                yield scrapy.Request(response.urljoin(next_page))





