# -*- coding: utf-8 -*-
import re
import urllib
import scrapy
from selenium import webdriver
from jd.items import GoodsItem, CommentItem


class GoodsSpider(scrapy.Spider):
    name = 'goods'

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(30)

    def closed(self,spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        start_urls = ['https://search.jd.com/Search?keyword=sony手机&enc=utf-8&page={}'.format(str(i)) for i in range(1,2,2)]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    # for i in range(1, 3):
    #     url = 'https://search.jd.com/Search?keyword=sony手机&enc=utf-8&page=' + str(i)
    #     # url = 'https://search.jd.com/s_new.php?keyword=sony%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&ev=exbrand_%E7%B4%A2%E5%B0%BC%EF%BC%88SONY%EF%BC%89%5E&page=2&s=31&scrolling=y&log_id=1534162019.55054&tpl=3_M&show_items=7265677,8266119,1988240435,6475660,26623635135,1997980261,27042603323,12481158400,30499946618,1986195992,17763031987,1988286243,26359789773,28571767372,23328214745,1995981507,30723861528,18550391667,23171931445,26625507006,1996918229,1985157292,26218204201,1990831939,25607748241,26435071883,1985956223,1998112505,1994936703,19223544186'
    #     start_urls.append(url)

    def parse(self, response):
        item = GoodsItem()
        item['title'] = response.xpath('//li[@class="gl-item"]/div/div[@class="p-name p-name-type-2"]/a/@title').extract()
        item['price'] = response.xpath("//div[@class='p-price']/strong/i/text()").extract()
        item['url'] = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        item['comment_num'] = response.css('.p-commit a::text').extract()
        yield item


class CommentSpider(scrapy.Spider):
    name = 'comment'

    def start_requests(self):
        start_urls = []

        url_1 = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2&productId='
        url_2 = '&score='
        url_3 = '&sortType=5&'
        url_4 = 'page='
        url_5 = '&pageSize=10&isShadowSku=0&rid=0&fold=1'
        links = open("product_url.txt").readlines()
        id = re.findall(r'(\d+)\.html$', links[0])
        # score = 3

        for score in range(1, 4):
            page = 0
            comment_url_first = url_1 + str(id[0]) + url_2 + str(score) + url_3 + url_4 + str(page) + url_5
            # 页码数获取
            comment_data = urllib.request.urlopen(comment_url_first).read().decode("utf-8", "ignore")
            comment_page_num = re.findall(r'"maxPage":(\d+),', comment_data)
            for i in range(0, int(comment_page_num[0])):
                # comment_url = 'http://club.jd.com/review/' + str(id[0]) + '-2-' + str(i) + '-' + str(score) + '.html'
                comment_url = url_1+str(id[0])+url_2+str(score)+url_3+url_4+str(i)+url_5
                start_urls.append(comment_url)
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = CommentItem()
        # item['content'] = response.re('{"id":')
        # item['user_name'] = response.css('.u-name::text').extract()
        # # 评论内容
        # item['content'] = response.xpath('//div[@class="comment-content"]/dl/dd/text()').extract()
        # # 手机名称
        # item['phone_name'] = response.xpath('//div[@class="dl-extra"]/dl/dd/text()').extract()

        item['score'] = re.findall(r'testId":"A","score":(\d)', response.text)

        item['user_name'] = re.findall(r'"nickname":"(.*?)",', response.text)
        # 评论内容
        item['content'] = re.findall(r'topped":0,"guid":.*?content":"(.*?)","creationTime', response.text)
        # 手机名称
        item['phone_name'] = re.findall(r'referenceName":"(.*?)","referenceTime', response.text)
        yield item

