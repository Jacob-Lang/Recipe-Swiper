import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown, Image, HTML
from webbrowser import open_new as wb_open_new

class Swiper():
    """This allows a user to play the MAB via widget buttons."""
    
    def __init__(self, df,  model):
        self.df = df
        self.model = model
               
        # widget buttons for each action
        self.swipe_right = widgets.Button(description='Yes please! :D')
        self.swipe_left = widgets.Button(description='No thanks. :|')
        self.clicked_recipes_button = widgets.Button(description='See my liked recipes')
        
        self.swipe_left.on_click(lambda _ : self.left())
        self.swipe_right.on_click(lambda _ : self.right())
        self.clicked_recipes_button.on_click(lambda _ : self.open_liked_recipe_links())

        self.recipe_html = widgets.HTML()
        self.swipe_buttons_box = widgets.HBox([self.swipe_left, self.swipe_right], layout=widgets.Layout(justify_content='center'))
        self.empty_space_html = widgets.HTML("<br> <br> <br>")
        self.clicked_recipes_button_box = widgets.VBox([self.empty_space_html, 
                                                        widgets.HBox([self.clicked_recipes_button], layout=widgets.Layout(justify_content='center'))
                                                       ]
                                                      )
        
        self.click_count = 0 
        self.liked_recipes = []
        
        
    def right(self):
        reward = 1
        page_url = self.df.loc[self.action.numpy(), 'page_url']
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)
        self.click_count += 1
        # store liked recipe
        self.liked_recipes.append(page_url)

    def left(self):
        reward = 0
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)
        self.click_count += 1
        
    def open_liked_recipe_links(self):
        for recipe in self.liked_recipes:
            wb_open_new(recipe)

    def run(self):
        
        # page header
        display(HTML("<h1 align=\"center\"> Recipe Swiper </h2>"))
        display(HTML("<center> Looking for love in a plate of food </center>"))
        display(HTML("<br> <br> <br>"))
        
        display(self.recipe_html)
        display(self.swipe_buttons_box)
        display(self.clicked_recipes_button_box)


        # first recipe
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)
    
    def reset():
        # add button for reset
        pass
            
    def get_recipe_html(self, action):
        title = self.df.loc[action.numpy(), 'title']
        summary = self.df.loc[action.numpy(), 'summary']
        image_url = self.df.loc[action.numpy(), 'image_url']
        page_url = self.df.loc[action.numpy(), 'page_url']

        html = "<h2 align=\"center\"> " + title +  "</h2>" \
                + "<center>" + summary +  "<center> <br>" \
                + "<p style=\"text-align:center;\"> <a href=" + page_url + "> <img src=" + image_url + " alt=\"recipe_img\" class=\"center\"> </a> </p> "
        
        return html
 