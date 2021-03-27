import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown, Image, HTML

class Swiper():
    """This allows a user to play the MAB via widget buttons."""
    
    def __init__(self, df,  model):
        self.df = df
        self.model = model
        
    def run(self):
        
        # page header
        display(HTML("<h1 align=\"center\"> Recipe Swiper </h2>"))
        display(HTML("<center> Looking for love in a plate of food <br> <br> <br> </center>"))
                
        # widget buttons for each action
        self.swipe_right = widgets.Button(description='Yes please! :D')
        self.swipe_left = widgets.Button(description='No thanks. :|')
        
        buttons = widgets.HBox([self.swipe_left, self.swipe_right], layout=widgets.Layout(justify_content='center'))
        output = widgets.Output(layout=widgets.Layout(height='500px'))      
        # display buttons
        display(widgets.VBox([output, buttons]))
        
        # first recipe
        self.action = self.model.call()

        with output:
            self.display_recipe(self.action)
            clear_output(wait=True)
    
        
        def right(self):
            reward = 1
            self.model.train_step((self.action, reward))
            self.action = self.model.call()
            with output:
                self.display_recipe(self.action)
                clear_output(wait=True)
                
        def left(self):
            reward = 0
            self.model.train_step((self.action, reward))
            self.action = self.model.call()
            with output:
                self.display_recipe(self.action)
                clear_output(wait=True)
        
        self.swipe_left.on_click(lambda _ : left(self))
        self.swipe_right.on_click(lambda _ : right(self))
        
        def reset():
            # add button for reset
            pass
            
    def display_recipe(self, action):
        title = self.df.loc[action.numpy(), 'title']
        summary = self.df.loc[action.numpy(), 'summary']
        image_url = self.df.loc[action.numpy(), 'image_url']
        page_url = self.df.loc[action.numpy(), 'page_url']

#         display(Markdown(title))
#         display(Markdown(summary))
#         display(Image(url=url))

        display(HTML("<h2 align=\"center\"> " + title +  "</h2>"))
        display(HTML("<center>" + summary +  "<center>"))
        display(HTML("<p style=\"text-align:center;\"> <a href=" + page_url + "> <img src=" + image_url + " alt=\"recipe_img\" class=\"center\"> </a> </p> "))

        