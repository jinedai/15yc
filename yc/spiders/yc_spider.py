#!/usr/bin/env python
# coding=utf-8

import scrapy,re,sys,urllib2
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector
from yc.items import ycItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider

reload(sys)       
sys.setdefaultencoding('gbk')  

class YcSpider(CrawlSpider) : #CrawlSpider用来遍布抓取，通过rules来查找所有符合的URL来爬取信息
    name = "yc"
    header = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; MI 5s Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.6.946 Mobile Safari/537.36',
    'Accept': '*/*', 
    'Referer': 'http://bs.6no.cc/jx/sapi.php?id=sZ11naKhqaajqayJt6ami6eWhZuFkZNjanRpaGNqYWpobXV9oJCDZ5zHswO0O0OO0O0O',
    'Accept-Encoding': 'gzip, deflate', 
    'Accept-Language': 'zh-CN,en-US;q=0.8', 
    'Range': 'bytes=0-1',
    'Connection': 'close'}
#    allowed_domains = ["15yc.com"]

    def start_requests(self):
        for i in range(1,2):
            url = "http://www.15yc.com/type/5/"+str(i)+".html"
            yield scrapy.Request(url, self.parse_page)

    def parse_page(self, response):
        sel_root = response.xpath('//a[@class="link-hover"]/@href')
        for sel in sel_root:
            mv_url = 'http://www.15yc.com' + sel.extract()
            yield scrapy.Request(mv_url, self.parse_info)

    def parse_info(self, response):
        play_url = response.xpath('//div[@class="show_player_gogo"]/ul/li[1]/a/@href').extract()[0]
        #print "play_url:"+play_url
        yield scrapy.Request(play_url, self.parse_frame)

    def parse_frame(self, response):
        frameurl = response.xpath('//iframe/@src').extract()[0]
        videoName = response.xpath('//h1[@class="title"]/text()').extract()[0]
        #videoName = re.sub("正在播放:", "", videoName)
        videoName = videoName[5:-1]

        #print 'frame_url:'+frameurl
        yield scrapy.Request(frameurl, self.parse_item, meta={'video_name':videoName})

    def parse_item(self,response):
        sel = response.xpath('//video/@src').extract()[0]
        if 'sgmp4.com' in sel:
            req = urllib2.Request(sel, headers = self.header) 
            currentPage=urllib2.urlopen(req).read().decode('utf8')

            pattern = re.compile(r'/ppvod/.*\.m3u8',re.S|re.I) 
            sel= re.findall(pattern, currentPage) 
            sel = 'http://ms.sgmp4.com'+sel[0]

        item = ycItem()
        item['videoname']=response.meta['video_name']
        item['videourl'] = sel
        yield item
