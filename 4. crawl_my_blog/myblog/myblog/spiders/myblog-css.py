import scrapy


class MyBlogScpiderCss(scrapy.Spider):
    name = 'myblog-css'
    start_urls = [
        'http://blog.csdn.net/u012814856',
    ]

    def parse(self, response):
        pass