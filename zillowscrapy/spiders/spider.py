import scrapy, time
from zillowscrapy.items import ZillowItem


class MySpider(scrapy.Spider):
    name = 'zillowscrapy'
    allowed_domains = ['zillow.com']
    
    # start_urls = ['http://www.zillow.com/homes/for_sale/South-Bend IN/fsba,fsbo_lt/house,apartment_duplex_type/31471_rid/1-_beds/5000-25000_price/19-97_mp/pricea_sort/38.345425,-87.009659,37.68545,-88.19069_rect/9_zm/0_mmm/']

    url_template= "http://www.zillow.com/homes/for_sale/%s/fsba,fsbo_lt/%s_duplex_type/%d-_beds/%s_price/pricea_sort/0_mmm/"
    
    def __init__(self):
        self.city_name = "South-Bend IN"
        self.price = [5000, 25000]
        self.beds = 1
        self.home_type = ["house", "apartment"]

    def start_requests(self):
        url = self.url_template % (self.city_name.replace(" ", "-"), ",".join(self.home_type), self.beds, "-".join([str(item) for item in self.price]))
        
        print url
        yield scrapy.Request(url=url, callback=self.parse)
  
    # end start_urls

    def parse(self, response):    
        urls = response.xpath('//ul[@class="photo-cards"]/li/article/div/a/@href').extract()
        for url in urls:            
            request = scrapy.Request(response.urljoin(url) , callback=self.parse_page)      
            yield request

        nextpage = response.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first() 
        request1 = scrapy.Request(response.urljoin(nextpage))
        yield request1
    def parse_page(self , response):
        item = ZillowItem()

        state = response.xpath('//li[@id="region-state"]/a/text()').extract_first()
        city = response.xpath('//li[@id="region-city"]/a/text()').extract_first()
        zipcode = response.xpath('//li[@id="region-zipcode"]/a/text()').extract_first()
        neighborhood = response.xpath('//li[@id="region-neighborhood"]/a/text()').extract_first()
        lot = response.xpath('//li[contains(text(),"Lot:")]/text()').extract_first()
        if lot:
            lot = lot.split(':')[-1].strip()
        mls = response.xpath('//li[contains(text(),"MLS #")]/text()').extract_first()
        year = response.xpath('//li[contains(text(),"Built in")]/text()').extract_first() 
        yearArr = year.split(" ")     
        price = response.xpath('//div[@class="main-row  home-summary-row"]/span/text()').extract_first()
        z = response.xpath('//div[@class="zest-value"]/text()').extract()
        zestimate = ""
        zestimate_rent = ""
        if len(z) > 0:
            zestimate = z[0][1:]
        if len(z) > 1:
            zestimate_rent  = z[1][1:-3]
        bed_bath = response.xpath('//span[@class="addr_bbs"]/text()').extract()
        bed = [bed.split(' ')[0] for bed in bed_bath if 'bed' in bed]
        bath = [bath.split(' ')[0] for bath in bed_bath if 'bath' in bath]
        address = response.xpath('//h1/text()').extract_first().replace(',', '')
        desc = response.xpath('//div[@class="zsg-content-component"]/div/text()').extract_first()
        agent_name = response.xpath('//span[@class="snl name notranslate"]/text()').extract_first()        
        if not agent_name:
            agent_name = response.xpath('//span[@class="snl name notranslate"]/a/text()').extract_first()
        agent_number = response.xpath('//span[@class="snl name notranslate"]/../span[@class="snl phone"]/text()').extract_first()
        listing_type = response.xpath('//div[@class=" status-icon-row for-sale-row home-summary-row"]/text()').extract()[1]
        if not listing_type.strip():
            listing_type = response.xpath('//div[@class=" status-icon-row for-sale-row home-summary-row"]/span[2]/text()').extract_first()
        types = ['Single Family', 'Duplex', 'Triplex', 'Quadruplex', 'Condominium', 'Cooperative', 'Mobile', 'Multi Family']
        li_elems = response.xpath('//li/text()').extract()
        temp = 0
        for ptype in types:            
            for text in li_elems:
                if ptype == text:
                    property_type = ptype
                    item['property_type'] = property_type
                    temp = 1
                    break
            if temp == 1:
                break       
        image_url = response.xpath('//ul[@class="photo-wall-content"]/li/div/img/@src').extract_first()
        item['image_url'] = self.manual(image_url)
        item['state'] = self.manual(state)
        item['city'] = self.manual(city)
        item['zipcode'] = self.manual(zipcode)
        item['neighborhood'] = self.manual(neighborhood)
        item['lot'] = self.manual(lot)
        if mls is not None:
            mlsArr = mls.split(":")
            item['mls'] = mlsArr[1]
        else:
            item['mls'] = ''
        item['year'] = self.manual(yearArr[2])
        item['price'] = self.manual(price.strip()[1:])
        item['zestimate'] = self.manual(zestimate)
        item['zestimate_rent'] = self.manual(zestimate_rent)
        item['bed'] = self.manual(bed[0])
        item['bath'] = self.manual(bath[0])
        item['address'] = self.manual(address)
        item['desc'] = self.manual(desc)
        item['agent_name'] = self.manual(agent_name)
        item['agent_number'] = self.manual(agent_number)
        item['listing_type'] = self.manual(listing_type)
        item['timestamp'] = self.manual(time.strftime("%d %b %Y %H:%M:%S"))
        item['url'] = self.manual(response.url)

        return item

    def manual(self,var_str):
        if var_str is None:
            return ""
        return var_str