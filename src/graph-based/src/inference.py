from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import nltk
import os

NLTK_PATH = f'{os.path.abspath(os.getcwd())}/deps'
if NLTK_PATH not in nltk.data.path:
    nltk.data.path.append(NLTK_PATH)


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


def summarize(model, text: str):
    # tokenize
    sentences = nltk.sent_tokenize(text, language='slovene')

    # get summary length
    n = get_summary_length(len(sentences))

    # Compute the sentence embeddings
    embeddings = model.encode(sentences, convert_to_numpy=True, batch_size=8)

    # similarity matrix
    sim_mat = cosine_similarity(embeddings)

    # rescale
    scaler = MinMaxScaler(feature_range=(0, 1))
    sim_mat = scaler.fit_transform(sim_mat.flatten().reshape(-1, 1)).reshape(len(embeddings), len(embeddings))

    # calculate pagerank
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph, alpha=0.85, max_iter=500)  # number of cycles to converge
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # reorder sentences
    idx_sentences = []
    for _, sentence in ranked_sentences[:n]:
        idx = sentences.index(sentence)
        idx_sentences.append((idx, sentence))
    idx_sentences.sort()

    return " ".join([sent for _, sent in idx_sentences])