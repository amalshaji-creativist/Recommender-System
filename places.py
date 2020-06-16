# -*- coding: utf-8 -*-
import scrapy


class PlacesSpider(scrapy.Spider):
    name = 'places'
    allowed_domains = ['www.yatra.com']
    start_urls = ['https://www.yatra.com/india-tour-packages/destinations-1']
    
    """
    def start_requests(self):
        yield scrapy.Request(url='https://www.yatra.com/india-tour-packages/destinations-1',callback=self.parse, headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
"""

    def parse(self, response):
        places=response.xpath("//div[@class='caption']")
        for place in places:
            name = place.xpath(".//h3/text()").get()
            link = place.xpath(".//div/a/@href").get()
            
            #absolute_url=f"https://www.worldometers.info{link}"
            #absolute_url =response.urljoin(link)
            
            #yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link , callback=self.parse_place,meta={'place_name':name})
            
        next_page = response.xpath("//div[@class='paging']/a[2]/@href").get()
        if next_page:
                yield scrapy.Request(url=next_page,callback=self.parse)
        
    def parse_place(self,response):
        #logging.info(response.url)
        name=response.request.meta['place_name']
        rows =response.xpath("//li[@class='tab-article cls_CP nChild']")
        for row in rows:
             #pack=row.xpath(".//div[2]/span/a/h3/text()").get()
             linktopage=row.xpath(".//div/span/a/@href").get()
             price=row.xpath(".//div/span[2]/div/text()").get()
             #emi_option=row.xpath(".//div/span[2]/p[1]/text()").get()
            
             if linktopage:
              yield response.follow(url=linktopage, callback=self.parse_inner,meta={'place':name,'price':price})
           
    def parse_inner(self,response):  
        place=response.request.meta['place']
        pack=response.xpath("//div[@id='navDockDiv']/span/h1/text()").get()
        price=response.request.meta['price']
        rows =response.xpath("//section[@id='itinerary']/ul/li/span")
        time=response.xpath("//div[@id='navDockDiv']/span/span/span[2]/text()").get()
        emi=response.xpath("//ul[@class='pad20 block']/li[3]/p/text()[2]").get()
        text=''
        for row in rows:
            days=row.xpath(".//div")
            for day in days:
                text=text + (day.xpath(".//text()").get())
        yield{
                'place':place,
                'package_name':pack,
                'price':price,
                'time':time,
                'about_trip':text,
                'emi':emi
               
                }
            
            
            
            
