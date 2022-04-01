import streamlit as st
import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
from ast import literal_eval

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')



st.title('Never Have I Eaten :shrimp: :pineapple:')
st.header('Given a list of ingredients what can I cook!')
st.markdown("![Alt Text](https://media.giphy.com/media/cEsoz6GAoTubm/giphy.gif)")

st.write('Tell us what ingredients you have at home and we can suggest recipes for you to make!')
st.write('We can also filter this down depending on your skill level :zap:, dietary requirements :seedling: how much time you are willing to commit :watch: and what course you are looking to make 🍳')

ingred= ''

st.write("""
##### What ***ingredients*** do you have?
""")
ingred = st.text_input("separate ingredients with a comma. eg. eggs,rice,cheese")
if ingred:
    st.write('✔️')
elif ingred == '':
    st.write('🔮')

st.write("""
##### Select any ***dietary*** requirements!:seedling:
""")
options1 = ['vegetarian', 'vegan', 'none']
diet_requirements = st.selectbox('diet',options1)

st.write("""
##### How much ***time*** do you want to spend cooking?(in minutes):watch:
""")
n = st.slider('time', 0, 200)

st.write("""
##### What ***course*** would you like to make?🍳
""")
options = ['starter', 'main', 'dessert']
course = st.selectbox('course', options)

st.write("""
##### What is your ***skill level***:zap:?
""")
option = ['beginner','intermediate','advanced']
skill_level = st.selectbox('skill level', option)

submit = st.button("Show me recipe's")


#################################
diet= ''
skill= ''

if diet_requirements == 'vegetarian':
    diet = 'vegetarian'
elif diet_requirements == 'vegan':
    diet = 'vegan'
elif diet_requirements == 'none':
    diet = None

if skill_level == 'beginner':
    skill = 'beginner'
elif (skill_level == 'intermediate'):
    skill = 'intermediate'
elif (skill_level == 'advanced'):
    skill = 'advanced'


###########################################


# function to give recipe recommendations
@st.cache
def suggest_recipes(diet, n, course, skill, ingred):
    #load in the recipe dataset
    df = pd.read_csv('clean_recipe2_5.csv', converters={'ingredients_clean': literal_eval})


    #Defining the lemmatizer and stopwords list
    lemmatizer = WordNetLemmatizer()
    stpwrd = nltk.corpus.stopwords.words('english')
    stpwrd.extend(string.punctuation)

    #1: make text lowercase
    ingred = ingred.lower()
    # 2: tokenize each word
    ingred = word_tokenize(ingred)
    # 3: remove stopwords
    ingred = [word for word in ingred if word not in stpwrd]
    # 4: # Get rid of words containing non alphabet letters
    ingred = [word for word in ingred if word.isalpha()]
    # 5: lemmatize
    ingred = [lemmatizer.lemmatize(word) for word in ingred]


    # filter recipes to those less than or equal to users time
    recipe = df.loc[df['cook_time'] <= n]

    # filter by course type
    if course == 'starter':
       recipe = recipe[recipe['course'] == 'starter'].copy()
    elif course == 'main':
        recipe = recipe[recipe['course'] == 'main'].copy()
    elif course == 'dessert':
        recipe = recipe[recipe['course'] == 'dessert'].copy()

    # filter recipes to skill level
    if skill == 'beginner':
       recipe = recipe[recipe['skill_level'] == 'beginner'].copy()
    elif skill == 'intermediate':
        recipe = recipe[recipe['skill_level'] == 'intermediate'].copy()
    elif skill == 'advanced':
        recipe = recipe[recipe['skill_level'] == 'advanced'].copy()

    # filter recipes to only vegetarian or vegan
    if diet == 'vegetarian':
       recipe = recipe[recipe['vegetarian'] == 1].copy()
    elif diet == 'vegan':
        recipe = recipe[recipe['vegan'] == 1].copy()

    # matching ingredients between recipes and the users input
    recipe['match'] = recipe['ingredients_clean'].apply(lambda x: set(ingred).intersection(set(x)))
    recipe['count'] = recipe['match'].apply(lambda x: len(x))

    # sorting recipes by macth count and displaying top 5 matches
    recipe.sort_values(by='count', ascending=False, inplace = True)
    recipe = recipe[:5]

    recipe = recipe[['recipe_name', 'ingredients', 'recipe_urls','cook_time']]
    #recipe.set_index('recipe_name',inplace = True)

    return recipe

    ##################################
if submit:
    st.success('Get Cooking... 👨🏼‍🍳')

    recipe = suggest_recipes(diet, n, course, skill, ingred)
    recipe
