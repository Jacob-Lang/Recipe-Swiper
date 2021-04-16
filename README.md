# Recipe Swiper!

An app that helps you find the perfect recipe! By providing yes/no feedback to a series of recipes an ML learns to recommend increasingly relevant recipes.  

[Try it here!](https://mybinder.org/v2/gh/Jacob-Lang/Recipe-Swiper/HEAD?urlpath=voila%2Frender%2Frecipe_swiper_app.ipynb)  

(This will be slow to load and doesn't render well on phones.)


## Recipes

The recipes in the pool are scraped from BBC Good Food (https://www.bbcgoodfood.com/) using scrapy. An obvious upgrade would be to add a filter for vegetarian food only but I'm afraid I haven't implemented this yet. 

## Contextual Bandit

The machine learning algorithm in this project is a LinUCB contextual bandit (https://arxiv.org/abs/1003.0146 implemented with Tensorflow in linucb.py). This algorithm balances exploration and exploitation to gain information about your preferences in recipe space and show you relevant recipes. 

## Voila app

The swiper app is implemented with ipywidgets in a juypyter notebook (recipe_swiper_app.ipynb) and then made into a web app using voila. A version of this app is hosted on mybinder: https://mybinder.org/v2/gh/Jacob-Lang/Recipe-Swiper/HEAD?urlpath=voila%2Frender%2Frecipe_swiper_app.ipynb (this is pretty well guaranteed to be SLOW to load - and doesn't render particularly well on phones.)

## Recreate

environment_dev.yml contains all packages required to run the whole repo.   
environment.yml is a minimal version of the environment requirements used by voila. 
