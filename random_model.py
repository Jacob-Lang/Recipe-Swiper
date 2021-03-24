import tensorflow as tf

class RandomModel(tf.keras.Model):
    """Implements the random agent"""
    def __init__(self, n_actions, **kwargs):
        super(RandomModel, self).__init__()
        
        self.n_actions = tf.constant(n_actions, dtype=tf.int32) 
        
    @tf.function()
    def call(self):
        
        action = tf.random.uniform((), minval=0, maxval=self.n_actions, dtype=tf.int32)
           
        return action
                      
    @tf.function()
    def train_step(self, event):
        """The Model learns by observing historical (action, reward) pairs."""
        
        # the random agent does not learn
        
        return {}