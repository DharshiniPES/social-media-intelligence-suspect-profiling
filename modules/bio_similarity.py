from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def bio_score(bio1, bio2):

    bio1 = bio1 or ""

    bio2 = bio2 or ""

    emb1 = model.encode([bio1])

    emb2 = model.encode([bio2])

    score = cosine_similarity(
        emb1,
        emb2
    )[0][0]

    return score