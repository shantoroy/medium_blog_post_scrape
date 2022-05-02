# import nltk
from nltk import PorterStemmer
import pandas as pd
# from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
# from nltk.tokenize import word_tokenize

df = pd.read_json('related_data_rm_duplicacy.json')
QATags = df.content
# print(QATags)
QATags = list(QATags)
# print(QATags[:10])

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
port = PorterStemmer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    # print(stop_free)
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    # print(punc_free)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    stem = " ".join(port.stem(word) for word in normalized.split())
    remove_non_english = stem.encode("ascii", errors="ignore").decode()
    return remove_non_english


Text_clean = [clean(doc).split() for doc in QATags]


# word_dict = gensim.corpora.Dictionary(Text_clean)
# print(word_dict)

dictionary = corpora.Dictionary(Text_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in Text_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
f = open("post_content_topic_analysis.txt", "w+")
for x in range(5,16):
    ldamodel = Lda(doc_term_matrix, num_topics=x, id2word = dictionary, passes=100, iterations=15000)
    f.write(f"\n\nNo of Topics : {x}\n\n")
    print(f"\n\nNo of Topics : {x}\n\n")
    for idx, topic in ldamodel.print_topics(-1):
        f.write('\nTopic: {} ---- Words: {}'.format(idx, topic))
        print('Topic: {} ---- Words: {}'.format(idx, topic))

    f.write('-' * 200)
f.close()
