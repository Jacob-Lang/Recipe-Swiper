import tensorflow as tf

class LinUCBModel(tf.keras.Model):
    """Implements the LinUCB agent with only shared parameters - i.e. theta=0, beta!=0"""
    def __init__(self, action_contexts, alpha=0.1, **kwargs):
        super(LinUCBModel, self).__init__()
        
        
        self.action_contexts = tf.expand_dims(tf.constant(action_contexts, dtype=tf.float32), axis=-1)
        self.n_actions = tf.constant(action_contexts.shape[0], dtype=tf.int32) 
        self.context_dim = tf.constant(action_contexts.shape[1], dtype=tf.int32)
        
        self.alpha = alpha

        self.A0 = tf.Variable(tf.eye(self.context_dim, dtype=tf.float32))
        self.b0 = tf.Variable(tf.constant_initializer(0)(shape=(self.context_dim, 1), dtype=tf.float32))
        
        self.step_count = tf.Variable(tf.constant_initializer(1)(shape=(), dtype=tf.int32))
        self.no_repeats_mask = tf.Variable(tf.constant_initializer(1)(shape=(self.n_actions,), dtype=tf.float32))
  
    
    def linucbs(self):
        
        beta = tf.matmul(tf.linalg.inv(self.A0), self.b0)
        
        s = tf.matmul(
            tf.transpose(self.action_contexts, perm=[0,2,1]),
            tf.matmul(
                tf.broadcast_to(tf.linalg.inv(self.A0), (self.n_actions, self.context_dim, self.context_dim)),
                self.action_contexts
            )
        )
        
        p = tf.matmul(
            tf.transpose(self.action_contexts, perm=[0,2,1]),
            tf.broadcast_to(beta, (self.n_actions, self.context_dim, 1))
        ) + self.alpha + tf.math.sqrt(s)
        
        p = tf.squeeze(p)
        
        return p
    
    @tf.function()
    def call(self):
        
        # add random choosing to break ties.
        def choose_max():
            action = tf.reshape(tf.math.argmax(self.linucbs()*self.no_repeats_mask, output_type=tf.int32), ())
            return action
        
        def choose_random():
            action = tf.random.uniform((), minval=0, maxval=self.n_actions, dtype=tf.int32)
            return action
        
        action = tf.cond(self.step_count>1, choose_max, choose_random)
        
        # update repeat penalty so same action not chosen twice
        indices = tf.expand_dims(tf.expand_dims(action,axis=0),axis=0)
        updates = tf.constant([0], dtype=tf.float32)
        self.no_repeats_mask.scatter_nd_update(indices, updates)
        
        self.step_count.assign_add(tf.constant(1, dtype=tf.int32))
        
        return action
                      
    @tf.function()
    def train_step(self, event):
        """The Model learns by observing historical (action, reward) pairs."""
        
        # no user context in this setting. 
        action, reward = event
        # just get context of action that was chosen
        begin = tf.concat([tf.expand_dims(action, axis=0), tf.constant([0, 0], dtype=tf.int32)], axis=0)
        size = tf.constant([1,-1,-1], dtype=tf.int32)
        context = tf.squeeze(tf.slice(self.action_contexts, begin, size), axis=0)

        self.A0.assign_add(tf.matmul(context, tf.transpose(context)))
        self.b0.assign_add(tf.cast(reward, dtype=tf.float32)*context)
       
        return {}