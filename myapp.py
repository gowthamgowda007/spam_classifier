# -*- coding: utf-8 -*-
"""myapp.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GogUM5FqjSXe_ebA54DiRC27kA74_h_N

##Importing library
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset=pd.read_csv('spam.csv',encoding='latin-1')
dataset.sample(5)

df=pd.DataFrame(dataset)
df.sample(5)

df.shape

"""##DATA CLEANING"""

df.info()

df.drop(columns=['Unnamed: 2',	'Unnamed: 4'], inplace=True)

df.sample(5)

df.sample(5)

df.rename(columns={'v1':'target', 'v2':'text'},inplace=True)
df.sample(5)

from sklearn.preprocessing import LabelEncoder
encoder=LabelEncoder()
df['target']=encoder.fit_transform(df['target'])
df.sample(5)

df.sample(5)

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates(keep='first',inplace=True)

df.shape



"""##Exploratory data analysis"""

df['target'].value_counts()

plt.pie(df['target'].value_counts(), labels=['ham','spam'],autopct='%0.2f')

!pip install nltk
import nltk
nltk.download('punkt')

df['number_of_characters']=df['text'].apply(len)

df['number_of_words']=df['text'].apply(lambda x: len(nltk.word_tokenize(x)))

df['number_of_sentence']=df['text'].apply(lambda x:len( nltk.sent_tokenize(x)))
df.sample(5)

df[df['target'] == 0][['number_of_characters', 'number_of_words', 'number_of_sentence']].describe()

df[df['target'] == 1][['number_of_characters', 'number_of_words', 'number_of_sentence']].describe()

import seaborn as sns
sns.histplot(df[df['target']==0]['number_of_characters'],color='green')
sns.histplot(df[df['target']==1]['number_of_characters'],color='red')

sns.histplot(df[df['target']==0]['number_of_words'],color='green')
sns.histplot(df[df['target']==1]['number_of_words'],color='red')

sns.histplot(df[df['target']==0]['number_of_sentence'],color='green')
sns.histplot(df[df['target']==1]['number_of_sentence'],color='red')

sns.pairplot(df,hue='target')

df['target'] = pd.to_numeric(df['target'], errors='coerce')
numerical_features = df.select_dtypes(include=['number']).columns
correlation_matrix = df[numerical_features].corr()
sns.heatmap(correlation_matrix, annot=True)

df.sample(5)

"""##3 DATA PREPROCESSING
1.lower case
"""

import nltk
import string
from nltk.corpus import stopwords

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
      if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text=y[:]
    y.clear()

    for i in text:
      y.append(ps.stem(i))

    return " ".join(y)

!pip install nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

df['tarnsfored_text']=df['text'].apply(transform_text)

df.head()

from wordcloud import WordCloud
wc=WordCloud(width=500,height=500,min_font_size=10, background_color='white')

spam_wc=df[df['target']==1]['tarnsfored_text'].str.cat(sep=" ")
plt.imshow(wc.generate(spam_wc))

spam_wc=df[df['target']==0]['tarnsfored_text'].str.cat(sep=" ")
plt.imshow(wc.generate(spam_wc))

spam_corpus=[]
for msg in df[df['target']==1]['tarnsfored_text'].tolist():
  for word in msg.split():
    spam_corpus.append(word)

from collections import Counter
spam_corpus_df = pd.DataFrame(Counter(spam_corpus).most_common(30), columns=['transformed_text', 'count']) # Changed column name to 'transformed_text'

# Generate the barplot
sns.barplot(x='transformed_text', y='count', data=spam_corpus_df) # Use the correct column names and the DataFrame
plt.xticks(rotation='vertical')
plt.show()

"""###Model Building"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
tfidf=TfidfVectorizer()
X=tfidf.fit_transform(df['tarnsfored_text']).toarray()
X

X.shape

y=df['target'].values
y

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=2)

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score

gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(X_train,y_train)
y_pred1 = gnb.predict(X_test)
print(accuracy_score(y_test,y_pred1))
print(confusion_matrix(y_test,y_pred1))
print(precision_score(y_test,y_pred1))

mnb.fit(X_train,y_train)
y_pred2 = mnb.predict(X_test)
print(accuracy_score(y_test,y_pred2))
print(confusion_matrix(y_test,y_pred2))
print(precision_score(y_test,y_pred2))

bnb.fit(X_train,y_train)
y_pred3 = bnb.predict(X_test)
print(accuracy_score(y_test,y_pred3))
print(confusion_matrix(y_test,y_pred3))
print(precision_score(y_test,y_pred3))

# prompt: include logistic regression,decsion tree and randomforest svm and knn

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

logreg = LogisticRegression()
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
svm = SVC()
knn = KNeighborsClassifier()

clfs={
    'gnb':gnb,
    'mnb':mnb,
    'bnb':bnb,
    'logreg':logreg,
    'decision_tree':decision_tree,
    'random_forest':random_forest,
    'svm':svm,
    'knn':knn

}

def train_model(clf, X_train, y_train, X_test, y_test, model_name):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    return accuracy, precision

train_model(svm, X_train, y_train, X_test, y_test, 'svm')

accuracy_scores=[]
precision_scores=[]

for name, clf in clfs.items():
    current_accuracy, current_precision = train_model(clf, X_train, y_train, X_test, y_test, name)

    print('for' ,name)
    print('accuracy', current_accuracy)
    print('precision', current_precision)

    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

performance_df=pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)
performance_df

import pickle
pickle.dump(tfidf,open('vectorizer.pkl','wb'))
pickle.dump(mnb,open('model.pkl','wb'))

import nltk

# Ensure Punkt tokenizer is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')