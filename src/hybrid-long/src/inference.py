from nltk import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import nltk
nltk.download('punkt')


def abs_summarize(tokenizer, model, text, device):
    input_ids = tokenizer(f"summarize: {text}", return_tensors="pt", max_length=512, truncation=True).input_ids
    input_ids = input_ids.to(device)
    outputs = model.generate(input_ids, max_length=256, no_repeat_ngram_size=5, num_beams=5)
    decoded_preds = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded_preds


def chunk_text(text, chunk_size=512):
    # tokenize text
    sentences = sent_tokenize(text, language='slovene')

    # split into chunks
    chunked_list = []
    tmp_list = []
    tmp_size = 0
    for s in sentences:
        tmp_size += len(s.split())
        tmp_list.append(s)
        if tmp_size > chunk_size:
            chunked_list.append(" ".join(tmp_list))
            tmp_list = []
            tmp_size = 0
    return chunked_list


def ext_summarize(model, text: str, n: int):
    # tokenize
    sentences = nltk.sent_tokenize(text, language='slovene')

    # Compute the sentence embeddings
    embeddings = model.encode(sentences, convert_to_numpy=True, batch_size=128)

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


def summarize(abs_tokenizer, abs_model, ext_model, text, device):
    hybrid_parts = 7
    hybrid_chunk_size = len(text.split()) // hybrid_parts
    hybrid_chunked_text = chunk_text(text, chunk_size=hybrid_chunk_size)
    extractive_summary = []
    for chk in hybrid_chunked_text:
        chk_summary = ext_summarize(ext_model, chk, n=10)
        extractive_summary.append(chk_summary)

    hybrid_summary = []
    for ext in extractive_summary:
        hybrid_summary.append(abs_summarize(abs_tokenizer, abs_model, ext, device))
    hybrid_summary = ' '.join(hybrid_summary)

    return hybrid_summary