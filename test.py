import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import openai

openai.api_key = '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'

# get csv from to df https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/edit?usp=sharing
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1ZafspjnRJuDjLRKotQ8awLTGcf3RLxrBEh2JtqRGh0Y/export?format=csv')
# get csv from https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/edit?usp=sharing to df
df2 = pd.read_csv('https://docs.google.com/spreadsheets/d/1A-6z5Fe30C266rK-6TnQm6CNOGCOnjK6s4hwfRIDMhQ/export?format=csv')
# combine df1 and df2
df = pd.concat([df1, df2], axis=0)
# Remove all the '%" in the average column
df['Average'] = df['Average'].str.replace('%', '')
df['Average'] = df['Average'].str.replace('~', '')
df['Average'] = df['Average'].str.replace(',', '')
# remove all + in the average column
df['Average'] = df['Average'].str.replace('+', '')
# remove all ? in the average column
df['Average'] = df['Average'].str.replace('?', '')
# Delete rows where average  NaN
df = df.dropna(how = 'any', subset=['Average'])
# if Type (101/105) column is empty, fill it with '101'
df['Type (101/105)'] = df['Type (101/105)'].fillna('101')

# for each row
for index, row in df.iterrows():
    try:
        df['Average'] = df['Average'].astype(float)
    except ValueError as error:
        question = "What is this person's average in the Ontario High School System Estimate: \n" + str(error)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= question,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        res = response.choices[0].text
        print(question)
        print(res)
        # keep only numerical values and symbolols with in res using regex
        res = (''.join((ch if ch in '0123456789.' else ' ') for ch in res))
        # clear white space from res
        res = res.strip()
        print(res)
        res = [float(i) for i in res.split()]

        df.loc[index, 'Average'] = res[0]


 




# for index, row in df.iterrows():
#     if not row['Average'].isnumeric():
#         print(row['Average'])
