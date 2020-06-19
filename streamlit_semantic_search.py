# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 00:51:45 2020

@author: Renu
"""
import streamlit as st
from gensim.models import Word2Vec
import textdistance as td # has a working Jaro text distance function
import re
import pandas as pd
import pickle
from PIL import Image

st.title('People Analytics: Semantic Search Tool')
st.markdown('<style>h1{color: #bc0031;}</style>', unsafe_allow_html=True)


st.markdown("""There is a vast body of literature on HRM and how to manage people, which can be useful for<br>
               designing and executing people analytics projects and to guide evidence-based decisions. <br>
                However, sometimes the right studies are difficult to find because different terms are used in <br>
                academic literature. This tool will help you to find relevant search terms and make it easier to<br>
                find relevant academic studies for the topic you are working on.
    """, unsafe_allow_html=True)


st.markdown("""Fill in your search term(s) below and the tool will provide you with terms that are similar or <br>
               related to your search term. By clicking on the search results, a Google Scholar search will be  <br>
                performed for that specific term.
    """, unsafe_allow_html=True)
st.subheader('Happy Searching and May You Find What You Need!')

# load model data
#model = Word2Vec.load('./data/word2vec_model1_96_percentile.model')
#model = Word2Vec.load('C:/Thesis/Data/save/Master_Data/Model/latest/word2vec/word2vec_model1_96_percentile.model')
model = pickle.load(open('./data/model_latest.model', 'rb'))

#get model vocab index
model_vocab = model.wv.index2word # ensure that this is basic list representing the model's vocabulary

# Function to find closest match in reference list
def closest_match(t, ref):
    scores = [td.jaro(t,i) for i in ref]
    return(ref[scores.index(max(scores))])

# Function to check list membership and take closest match if membership cannot be established
def check_and_fix_terms(ts, ref):
    s_td = [i if (i in ref) else closest_match(i, ref) for i in ts]
    return(s_td)

#get input word(s)
pos_str = st.text_input('Enter keyword(s)')
if (pos_str == ''):
    st.write(" ")
    
else:
    pos_str = pos_str.lower()
    pos_str = re.sub("^\s+|\s+$", "", pos_str, flags=re.UNICODE) # remove leading/trailing spaces
    
    
    # Tokenize: split the input
    word_list = pos_str.split(' ')
    
    # Ensure that all terms are in the vocabulary; replace if necessary. This will be our actual query.
    check_spell = check_and_fix_terms(word_list, model_vocab) 

    # Function to make keyword results clickable hyperlinks to google.scholar.com literature searches
    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for the link
        text = link.split('=')[3]
        return f'<a target="_blank" href="{link+" employee"}">{text}</a>'
     
    try:
        if word_list != check_spell:
            st.markdown('<p style="color:red"> Did you mean: {}</p>'.format(' '.join(check_spell)), unsafe_allow_html=True)
            st.markdown('<p style="color:Blue"> Showing result for : {}</p>'.format(' '.join(check_spell)), unsafe_allow_html=True)
            
        st.write('SIMILAR OR RELATED TO: ', ' '.join(check_spell))
        
        df = pd.DataFrame(model.wv.most_similar(positive = check_spell, topn=10), columns = ['SIMILAR_word', 'similarity'])
        
        df1 = df[['SIMILAR_word']]
        link_list = []
        for i in df['SIMILAR_word']:
           word = 'https://scholar.google.nl/scholar?hl=nl&as_sdt=0%2C5&q=' + i
           link_list.append(word)
             
        # rename column as SIMILAR for UI
        df1['RESULTS'] = link_list
        df1 = df1[['RESULTS']]
        df1['RESULTS'] = df1['RESULTS'].apply(make_clickable)
        df1 = df1.rename(index={0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'10'})
        df1 = df1.to_html(escape=False)
        st.write(df1, unsafe_allow_html=True)        
                
    except KeyError:
        st.markdown('<h4 style="color:#bc0031;"> SORRY, THE SEARCH TERM IS NOT AVAILABLE IN OUR DATABASE.</h4>', unsafe_allow_html=True) 
st.markdown("""This semantic search tool is developed by the UvA in collaboration with Bright & Company. <br>
               If you have any feedback or suggestions about this tool, please contact Corine Boon <br>
               (c.t.boon@uva.nl).
    """, unsafe_allow_html=True)
image = Image.open('./data/logo.PNG')
st.image(image, caption='', width=250)