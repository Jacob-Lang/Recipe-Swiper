import numpy as np

def evaluate(df, model_gen, n_runs=20, n_steps=20, key_words=['spicy', 'chinese', 'fish', 'easy', 'indian']):
    """Evaluates the performance of the model with a reward simulation: If key word appears then reward!"""
    
    N_kws = len(key_words)

    rewards = np.zeros((N_kws, n_runs, n_steps))

    for kw, key_word in enumerate(key_words):

        for run in range(n_runs):

            model = model_gen()

            for step in range(n_steps):
                
                action = model.call()

                if key_word in (df.loc[action.numpy(), 'summary'].lower()
                                + ' ' 
                                + df.loc[action.numpy(), 'title'].lower() 
                                + ' ' 
                                + (' '.join([tag for tag in df.loc[action.numpy(), 'tags']])).lower()):
                    reward = 1
                else:
                    reward = 0

                rewards[kw, run, step] = reward

                model.train_step((action, reward))

    average_total_reward = np.mean(np.sum(rewards, axis=2))
    
    return average_total_reward