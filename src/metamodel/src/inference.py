import string

def filter_text(content, lem_sl, stopwords):
    content_filtered = []
    for token in content.split():
        lemma = lem_sl.lemmatize(token)
        if lemma not in stopwords:
            content_filtered.append(lemma.lower())
    content_filtered = ' '.join(content_filtered)
    content_filtered = ''.join([i for i in content_filtered if not i.isdigit()])  # remove digits
    content_filtered = content_filtered.translate(str.maketrans('', '', string.punctuation))
    return content_filtered


def get_recommended_model(d2v_model, metamodel, preprocessed_text):
    # preprocess and score
    doc_vector = d2v_model.infer_vector(preprocessed_text)
    scores = metamodel.predict(doc_vector.reshape(1, -1))

    # Scores in group of four: verify the correct order: t5-article, graph-based, hybrid-long, sumbasic
    t5_article = scores[:, 0:4]
    graph_based = scores[:, 4:8]
    hybrid_long = scores[:, 8:12]
    sumbasic = scores[:, 12:]

    averages = [
        ('t5-article', t5_article.mean()),
        ('graph-based', graph_based.mean()),
        ('hybrid-long', hybrid_long.mean()),
        ('sumbasic', sumbasic.mean())
    ]
    averages.sort(key=lambda x: x[1], reverse=True)

    return averages[0][0]