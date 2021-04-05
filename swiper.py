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
        
        self.swipe_left.on_click(lambda _ : self.left())
        self.swipe_right.on_click(lambda _ : self.right())

        self.recipe_html = widgets.HTML()
        self.swipe_buttons_box = widgets.HBox([self.swipe_left, self.swipe_right], layout=widgets.Layout(justify_content='center'))
        self.clicked_recipes_html_title = widgets.HTML("<br> <h3 align=\"center\"> Liked recipes: </h3>")
        self.clicked_recipes_html_content = widgets.HTML("")

    def right(self):
        
        reward = 1
        title = self.df.loc[self.action.numpy(), 'title']
        page_url = self.df.loc[self.action.numpy(), 'page_url']
        
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)

        self.clicked_recipes_html_content.value = "<a href={page_url} target=\"_blank\" rel=\"noopener noreferrer\"> <center> {title}  </center> </a>".format(title=title, page_url=page_url) + self.clicked_recipes_html_content.value
        

    def left(self):
        reward = 0
        self.model.train_step((self.action, reward))
        self.action = self.model.call()
        self.recipe_html.value = self.get_recipe_html(self.action)

    def run(self):
        
        # page header
        display(HTML("<h1 align=\"center\"> Recipe Swiper </h1>"))
        display(HTML("<center> Looking for love in a plate of food </center>"))
        display(HTML("<br>"))
        
        display(self.recipe_html)
        display(self.swipe_buttons_box)
        display(self.clicked_recipes_html_title)
        display(self.clicked_recipes_html_content)

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
                + "<p style=\"text-align:center;\"> <a href={page_url} target=\"_blank\" rel=\"noopener noreferrer\"> <img src={image_url} alt=\"recipe_img\" class=\"center\"> </a> </p> ".format(page_url=page_url, image_url=image_url)
        
        return html
 