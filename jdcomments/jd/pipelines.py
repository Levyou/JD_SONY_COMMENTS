# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import re


class GoodsPipeline(object):
    def __init__(self):
        # 以写入的方式创建或者打开一个文件
        self.file = codecs.open("data.json", "wb", encoding="utf-8")

    def process_item(self, item, spider):
        for i in range(0, len(item['price'])):
            if (re.match('https', item['url'][i])):
                item['url'][i] = item['url'][i]
            else:
                item['url'][i] = str('https:') + item['url'][i]
            with open('product_url.txt', 'a') as f:
                f.write(item['url'][i] + '\n')

            url = item['url'][i]
            title = item['title'][i]
            price = item['price'][i]
            comment_num = item['comment_num'][i]

            goods = {'title': title, 'price': price, 'url': url, 'comment_num': comment_num}
            line = json.dumps(dict(goods), ensure_ascii=False) + '\n'
            self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class CommentPipeline(object):
    def __init__(self):
        self.file = codecs.open('mydata1.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):

        for j in range(0, len(item['content'])):
            user_name = item['user_name'][j]
            content = item['content'][j]
            phone_name = item['phone_name'][j]
            score = item['score'][int(j/10)]
            goods1 = {}
            if int(score[0]) == 3:
                goods1 = {'score': '好评', 'phone_name': phone_name, 'user_name': user_name, 'content': content}
            elif int(score[0]) == 2:
                goods1 = {'score': '中评', 'phone_name': phone_name, 'user_name': user_name, 'content': content}
            elif int(score[0]) == 1:
                goods1 = {'score': '差评', 'phone_name': phone_name, 'user_name': user_name, 'content': content}

            i = json.dumps(dict(goods1), ensure_ascii=False)
            self.file.write(i+'\n')
        return item

    def close_spider(self, spider):
        self.file.close()
