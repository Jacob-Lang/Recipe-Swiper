import scrapy
import re
import ast

class AmericanSpider(scrapy.Spider):
    name = 'american'
    start_urls = ['https://www.bbcgoodfood.com/recipes/collection/american-recipes']

    def parse(self, response):
        
        recipe_list = response.css('a.standard-card-new__article-title.qa-card-link')
        recipe_page_links = [recipe.css('a::attr(href)').get() for recipe in recipe_list]
        
        yield from response.follow_all(recipe_page_links, self.parse_recipe)
    
        next_page = response.css('li.pagination__arrow.pagination__arrow--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        
    def parse_recipe(self, response):
        
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