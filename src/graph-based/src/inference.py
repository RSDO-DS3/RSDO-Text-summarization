from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import nltk
nltk.download('punkt')


def summarize(model, text: str, n: int):
    # tokenize
    sentences = nltk.sent_tokenize(text, language='slovene')

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