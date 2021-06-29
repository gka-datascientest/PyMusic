# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import numpy as np

st.markdown("<h1 style='text-align: center; color: #FF6600;'>Système de Recommandation Musical</h1>", unsafe_allow_html=True)
st.subheader("Cette application propose des **_musiques positives_** en fonction des 3 dernières écoutes de votre playlist")

df = pd.read_csv('data_soixante_dix.csv')

artistList = df['artists'].tolist()

artist_new = []
for i in range(len(artistList)):
    artist_new.append(artistList[i].replace("'","").replace("\"","").replace("[","").replace("]","").replace("$",""))
df['artists'] = artist_new

st.markdown('##')

st.write("Saisissez vos 3 derniers sons écoutés et choisissez l'artiste associé dans le menu déroulant")
firstsong = st.text_input('Première Chanson')
firstartist = st.selectbox("Choisissez l'Artiste", df[df.name == firstsong].artists.unique(), key=3)
secondsong = st.text_input('Deuxième Chanson')
secondartist = st.selectbox("Choisissez l'Artiste", df[df.name == secondsong].artists.unique(),key=1)
thirdsong = st.text_input('Troisième Chanson')
thirdartist = st.selectbox("Choisissez l'Artiste", df[df.name == thirdsong].artists.unique(), key=2)

songs = pd.Series([firstsong, secondsong, thirdsong])
artists = pd.Series([firstartist, secondartist, thirdartist])

mood = df[(df.name.isin(songs)) & (df.artists.isin(artists))].valence.mean()

if mood < 0.3 :
    new_valence = [0.6 , 0.8]
    st.error('Votre Mood est de {}'.format(mood))
    st.image('faire-un-smiley-qui-pleure.jpg', width = 250)
    st.subheader('**_Votre moral est au plus bas, il va falloir remonter tout ca !_**')
elif mood < 0.5 :
    new_valence = [0.8 , 1]
    st.warning('Votre Mood est de {}'.format(mood))
    st.image('pas top.jpg', width = 250)
    st.subheader("**_C'est pas si pire, mais la marge de progression reste importante !_**")
elif mood < 0.7 :
    new_valence = [0.8 , 1]
    st.info('Votre Mood est de {}'.format(mood))
    st.image('pas mal.jpg', width = 250)
    st.subheader("**_C'est déjà pas mal, mais vous et moi savons que vous pouvez encore mieux faire !_**")
else :
    st.success('Votre mood est de {}'.format(mood))
    st.balloons()
    st.image('au top.jpg', width = 250)
    st.subheader('**_Vous êtes au top, continuez sur votre lancée !_**')


st.sidebar.markdown('##')

st.sidebar.write("**_Quelle décennie vous fait envie ?_**")
    
periode = st.sidebar.selectbox('Choisissez une période', ('Années 70', 'Années 80', 'Années 90', 'Années 2000', 'Années 2010'))

st.sidebar.markdown('##')

if periode == 'Années 70':
    df_year = df[df.year < 1980]
elif periode == 'Années 80':
    df_year = df[(df.year < 1990) & (df.year > 1979)]
elif periode == 'Années 90':
    df_year = df[(df.year < 2000) & (df.year > 1989)]
elif periode == 'Années 2000':
    df_year = df[(df.year < 2010) & (df.year > 1999)]
else :
    df_year = df[(df.year > 2009)]


if mood < 0.7 :
    df_valence = df_year[(df_year.valence < new_valence[1]) & (df_year.valence > new_valence[0])]
    
    proposition = df_valence.sample(3)[['artists', 'name']]
    
    st.markdown('##')
    
    st.text('Voici 3 nouvelles chansons qui vous redonneront le moral')
    st.write(proposition.iloc[0,0], ' : ',proposition.iloc[0,1])
    st.write(proposition.iloc[1,0], ' : ',proposition.iloc[1,1])
    st.write(proposition.iloc[2,0], ' : ',proposition.iloc[2,1])
    
    st.sidebar.write("--")
    
    st.sidebar.markdown('##')

st.sidebar.text('La recommandation ne vous plaît pas ?')
st.sidebar.text("Actualisez là !")

st.sidebar.button('CLICK ME !')
