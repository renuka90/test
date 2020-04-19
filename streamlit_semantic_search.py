# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:51:45 2020

@author: Renu
"""

import streamlit as st
from gensim.models import Word2Vec
import re
import pandas as pd


st.title('Semantic Search Engine Staging testing')
st.subheader('Find your relevant terms : similar or related')
# load model data
model = Word2Vec.load('./data/article_data.model')

pos_str = st.text_input('Enter keyword(s)')
pos_str = pos_str.lower()
# remove spaces both in the beginning and in the end of of string
pos_str = re.sub("^\s+|\s+$", "", pos_str, flags=re.UNICODE)

# any input that is NOT a-z, A-Z, 0-9,-,*
pos_str = re.sub('[^a-zA-Z0-9-_*.]', ' ', pos_str)
pos_str = re.sub(' +',' ',  re.sub('\W', ' ', pos_str))
#lemmatizer = WordNetLemmatizer() 

#pos_words = lemmatizer.lemmatize(pos_str)
pos_words= pos_str.split(' ')

st.text('Your input')
st.write('SIMILAR TO ', pos_str)

if (len(pos_words[0]) > 0):

    df = pd.DataFrame(model.wv.most_similar(positive = pos_words, topn=10), columns = ['SIMILAR_word', 'similarity'])
    df1 = df[['SIMILAR_word']]
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

    df1 = df1.to_html(escape=False)
    st.write(df1, unsafe_allow_html=True)
        
