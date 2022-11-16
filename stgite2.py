import streamlit as st
st.title('Sumit Pandey & team welcomes you on Smart Summary using techniques in NLTK')

import nltk
#nltk.download("popular")
st.header("Some famous wiki links you want to summarize")
st.subheader("https://en.wikipedia.org/wiki/Narendra_Modi")
st.subheader("https://en.wikipedia.org/wiki/Rahul_Gandhi")
st.subheader("https://en.wikipedia.org/wiki/Bharatiya_Janata_Party")
st.subheader("https://fr.wikipedia.org/wiki/Emmanuel_Macron")

import bs4 as bs
import urllib.request
import re

wl=st.text_input("enter the wikepedia link you want to get summary for")
LoS = st.slider('In How many lines you want the summary?', 1, 30, 25)


scraped_data = urllib.request.urlopen(wl)
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text





print(len(article_text))
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)





formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)





#print(len(formatted_article_text))
sentence_list = nltk.sent_tokenize(article_text)




stopwords = nltk.corpus.stopwords.words('english')

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

#print(summary)
st.write(summary)



st.subheader("If the article is in other language, see below in english!!")

from googletrans import Translator

translator = Translator()

translated_text = translator.translate(summary)
st.write(translated_text.text)