import streamlit as st

import cohere
co = cohere.Client("kisfjnNLG6V7fG0sSCpqs1ZoL1pf5a5sLH81oYv2")

st.title('SMART SUMMARY')
st.header("TEAM - DATAGEEKS welcomes you to our Smart Summary tool")

import nltk
#nltk.download("popular")
st.header("Some famous Wikepedia links OR any public article link you want to summarize, by default NLP wikipedia is summarized")
st.subheader("https://en.wikipedia.org/wiki/Narendra_Modi")
st.subheader("https://en.wikipedia.org/wiki/Droupadi_Murmu")
st.subheader("https://en.wikipedia.org/wiki/Bharatiya_Janata_Party")
st.subheader("https://fr.wikipedia.org/wiki/Emmanuel_Macron")

import bs4 as bs
import urllib.request
import re

wl=st.text_input("Enter the wikepedia link you want to get summary for") or "https://en.wikipedia.org/wiki/Natural_language_processing"
LoS = st.slider('In How many lines you want the summary?', 1, 30, 23)

st.subheader("Technology used- NL ToolKit, BS4, LXML , developed in Python by Sumit Pandey")


scraped_data = urllib.request.urlopen(wl)
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text


artTxt=article_text

print(len(article_text))
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)





formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)





#print(len(formatted_article_text))
sentence_list = nltk.sent_tokenize(article_text)




stopwords = nltk.corpus.stopwords.words('french')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1



maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)



sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]





import heapq
summary_sentences = heapq.nlargest(LoS, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
prompt=artTxt
#print(summary)
#if (st.button("Click To view Summary"):
st.write(summary)



st.subheader("If the article is in other language, see below in english!!")

from googletrans import Translator

translator = Translator()

translated_text = translator.translate(summary)
#if (st.button("Click To view English Summary",key=2):
#st.write(translated_text.text)
flag=st.button("Click To view (translated) English Summary",key=2)
if (flag):
    st.write(translated_text.text)
   
response = co.generate( 
    model='xlarge', 
    prompt = prompt,
    max_tokens=80, 
    temperature=0.8,
    stop_sequences=["--"])

sweetsummary = response.generations[0].text
st.subheader("Conclusive summary below: with help of COHERE")
st.write(sweetsummary)

import time
tss=time.time()
print(tss)
print(wl)
st.write(tss)
