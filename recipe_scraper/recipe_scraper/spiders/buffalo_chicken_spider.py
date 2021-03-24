import scrapy
import re
import ast


class BuffaloChickenSpider(scrapy.Spider):
    name = 'buffalo_chicken'
    start_urls = ['https://www.bbcgoodfood.com/recipes/buffalo-chicken']

    def parse(self, response):

        header = response.css('div.post-header__container')

        tags = response.xpath("//body").xpath("@data-ad-settings").get()
        tags = re.search('"posttag":(.*)]', tags).group(1) + ']'
        tags = ast.literal_eval(tags)
    
        yield {
            'title': header.css('h1.post-header__title.heading-1::text').get(),
            'summary': header.css("div.mb-lg").css("div.editor-content").css('p::text').get().strip(),
            'tags' : tags,
            'image_url' : response.css('picture.image__picture').css('img.image__img::attr(src)').extract()[2],  
            'page_url' : response.request.url
        }

        
        
        
        
        