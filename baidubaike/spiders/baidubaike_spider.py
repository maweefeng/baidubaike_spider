# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from baidubaike.items import BaidubaikeItem

#爬取的次数
spider_num = 0
#爬取的最大次数
spider_max_num = 1000

class BaidubaikeSpiderSpider(scrapy.Spider):
    name = 'baidubaike_spider'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/%E8%8A%AC%E5%85%B0/397486']
        
    def parse(self, response):
        global spider_num,spider_max_num
        html = etree.HTML(response.text)
        title = html.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
        summary = html.xpath('//div[@class="lemma-summary"]')[0].xpath('string(.)').strip()
    
        baikeItem = BaidubaikeItem()
        baikeItem['title'] = title
        baikeItem['summary'] = summary
        print(baikeItem)
        yield baikeItem

        next_link_list = html.xpath('//div[@class="lemma-summary"]//a[starts-with(@href,"/item/")]')
       
        for item in next_link_list:
            link = item.xpath('./@href')[0]
            spider_num= spider_num+1
            if spider_num>spider_max_num:
                break
            yield scrapy.Request('https://baike.baidu.com'+link,callback=self.parse)


        




        
