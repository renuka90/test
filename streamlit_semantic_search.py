# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:51:45 2020

@author: Renu
"""

import streamlit as st
from gensim.models import Word2Vec
import re
import pandas as pd
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt
#from sklearn.manifold import TSNE
#import numpy as np
#import matplotlib.cm as cm
#import webbrowser
#from IPython.display import HTML

st.title('Semantic Search Engine')
st.subheader('Find your relevant terms : similar or related')
# load model data
model = Word2Vec.load('C:/Thesis/Data/save/Master_Data/Model/paraModified/save_modified_para_12_articles_1.model')

pos_str = st.text_input('Enter keyword(s)')
#neg_str = st.text_input('(Optional) Specify as unlike the following word(s)')

pos_str = re.sub(' +',' ',  re.sub('\W', ' ', pos_str))
#neg_str = re.sub(' +',' ',  re.sub('\W', ' ', neg_str))

# any input that is NOT a-z, A-Z, 0-9,-,*
#pos_str = re.sub('[^a-zA-Z0-9-_*.]', '', pos_str)

#pos_str = pos_str.lower()

pos_words = pos_str.split(' ')
#neg_words = neg_str.split(' ')



if (len(pos_words[0]) > 0):

    df = pd.DataFrame(model.wv.most_similar(positive = [pos_str], topn=10), columns = ['SIMILAR_word', 'similarity_score'])
    df1 = df[['SIMILAR_word']]
    
   #df2 = df1.style.hide_index()
    link_list = []
    for i in df['SIMILAR_word']:
                     
        word = 'https://scholar.google.nl/scholar?hl=nl&as_sdt=0%2C5&q=' + i
    
        link_list.append(word)
        # rename column as SIMILAR for UI
    df1['SIMILAR'] = link_list
    
    #st.dataframe(df1)
    
    df1 = df1[['SIMILAR']]
    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        text = link.split('=')[3]
        return f'<a target="_blank" href="{link}">{text}</a>'

    # link is the column with hyperlinks
    df1['SIMILAR'] = df1['SIMILAR'].apply(make_clickable)
    
    html = (
    df1.style
    .set_properties(**{'border': '1px solid silver','font-size': '9pt', 'color':'red','font-family': 'Calibri'})
   # .bar(subset=['col4', 'col5'], color='lightblue')
    .render()
)
    df1 = df1.to_html(escape=False)
    st.write(df1, unsafe_allow_html=True)
        
        
