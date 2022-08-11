import string
from collections import Counter

import nltk
import numpy as np
from lemmagen3 import Lemmatizer
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')


def filter_text(slovene_lemmatizer, slovene_stopwords, content):
    content_filtered = []
    for token in word_tokenize(content, language='slovene'):
        lemma = slovene_lemmatizer.lemmatize(token)
        if lemma not in slovene_stopwords:
            content_filtered.append(lemma.lower())
    content_filtered = ' '.join(content_filtered)
    content_filtered = ''.join([i for i in content_filtered if not i.isdigit()])  # remove digits
    content_filtered = content_filtered.translate(str.maketrans('', '', string.punctuation))
    return content_filtered


def update_word_probabilities(word_probabilities, lemmatized_sentence):
    tokenized_lemmatized_sentence = word_tokenize(lemmatized_sentence, language='slovene')
    for lemma in tokenized_lemmatized_sentence:
        word_probabilities[lemma] = word_probabilities[lemma] * word_probabilities[lemma]
    return word_probabilities


def get_best_sentence(text_sentences, lemmatized_sentences, word_probabilities):
    sentence_weights = []
    for idx_sent, (text_sent, lemma_sent) in enumerate(zip(text_sentences, lemmatized_sentences)):
        tokenized_lemmatized_sentences = word_tokenize(lemma_sent, language='slovene')
        sent_weight = [word_probabilities[lemma] for lemma in tokenized_lemmatized_sentences]
        sentence_weights.append((np.mean(sent_weight), idx_sent, text_sent, lemma_sent))
    sentence_weights.sort(reverse=True)
    return sentence_weights[0]


def get_summary_length(sent_num):
    if sent_num == 1:
        return 1
    elif 1 < sent_num < 10:
        return 2
    elif 10 < sent_num < 30:
        return 3
    elif 30 < sent_num < 50:
        return 5
    elif 50 < sent_num < 100:
        return 6
    else:
        return 7


def summarize(text):
    """
    Implementation of sumbasic: https://www.cs.bgu.ac.il/~elhadad/nlp09/sumbasic.pdf
    """

    # tools and resources
    slovene_lemmatizer = Lemmatizer('sl')
    slovene_stopwords = set(stopwords.words('slovene'))

    # candidates
    candidates = []

    # preprocess text into sentences
    text_sentences = sent_tokenize(text, language='slovene')
    summary_length = get_summary_length(len(text_sentences))
    text_sentences_copy = text_sentences.copy()
    lemmatized_sentences = [filter_text(slovene_lemmatizer, slovene_stopwords, s) for s in text_sentences]
    tokenized_text = word_tokenize(" ".join(lemmatized_sentences), language='slovene')

    # compute probability distribution
    counter = Counter(tokenized_text)
    word_probabilities = {w: n / len(tokenized_text) for w, n in counter.items()}

    while len(candidates) < summary_length:
        # assign weights to sentences
        sent_weight, idx_sent, text_sent, lemma_sent = get_best_sentence(text_sentences, lemmatized_sentences,
                                                                         word_probabilities)
        # assign candidate
        candidates.append(text_sent)

        # update word probabilities
        word_probabilities = update_word_probabilities(word_probabilities, lemmatized_sentences[idx_sent])

        # remove sentence from text and lemmas
        text_sentences.remove(text_sent)
        lemmatized_sentences.remove(lemma_sent)

    # reorder
    pos_candidates = []
    for can in candidates:
        pos_candidates.append((text_sentences_copy.index(can), can))
    pos_candidates.sort()
    reordered_candidates = [can for _, can in pos_candidates]

    return " ".join(reordered_candidates)
