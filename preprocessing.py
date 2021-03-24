import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

import spacy
nlp = spacy.load('en_core_web_md')
N_EMB_DIM = 300  # text embedding dimension from spacy



def embed_mix(X_title, X_summary, X_tags, proportions):
    
    alpha_title, alpha_summary, alpha_tags = proportions
    X = alpha_title*X_title + alpha_summary*X_summary + alpha_tags*X_tags
    
    return X

def preprocess(df, alpha_title=0.2, alpha_summary=0.1, alpha_tags=0.7, embed_dim=16):
    
    X_title = np.stack(df['title'].apply(lambda x : nlp(x).vector))
    X_summary = np.stack(df['title'].apply(lambda x : nlp(x).vector))
    X_tags = np.stack(df['title'].apply(lambda x : nlp(x).vector))

    
    X = embed_mix(X_title, X_summary, X_tags, [alpha_title, alpha_summary, alpha_tags])
        
    # dimensionality reduction with PCA
    pca = PCA(n_components=embed_dim).fit(X)
    X = pca.transform(X)

    # normalise and add unit dimension
    X = X/np.linalg.norm(X, axis=1, keepdims=True)
    X = np.concatenate([X, np.ones((X.shape[0], 1))], axis=1)
    
    return X



