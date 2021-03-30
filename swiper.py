import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown, Image, HTML

class Swiper():
    """This allows a user to play the MAB via widget buttons."""
    
    def __init__(self, df,  model):
        self.df = df
        self.model = model
               
        # widget buttons for each action
        self.swipe_right = widgets.Button(description='Yes please! :D')
        self.swipe_left = widgets.Button(description='No thanks. :|')
        
        self.recipe_html = widgets.HTML()
        self.buttons = widgets.HBox([self.swipe_left, self.swipe_right], layout=widgets.Layout(justify_content='center'))
            
        self.swipe_left.on_click(lambda _ : self.left())
        self.swipe_right.on_click(lambda _ : self.right())
        
    def right(self):
        reward = 1
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)

    def left(self):
        reward = 0
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)

    def run(self):
        
        # page header
        display(HTML("<h1 align=\"center\"> Recipe Swiper </h2>"))
        display(HTML("<center> Looking for love in a plate of food <br> <br> <br> </center>"))
        
        display(self.recipe_html)
        display(self.buttons)

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
 