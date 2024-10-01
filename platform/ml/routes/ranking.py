from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity

from model.model import pare

router = APIRouter()

class CorpusItem(BaseModel):
    author_id: int
    papers: List[str]

class Body(BaseModel):
    abstract: str
    corpus: List[CorpusItem]

@router.post("/")
def rank(body: Body):
    avg = lambda arr: sum(arr)/len(arr)
    abstract, corpus = body.abstract, body.corpus
    abstract_embedding = pare.get_embeddings([abstract])
    expertise_scores = []
    for entry in corpus:
        papers_embeddings = pare.get_embeddings(entry.papers)
        papers_scores = cosine_similarity(abstract_embedding, papers_embeddings)[0]
        expertise_scores.append(avg(sorted(papers_scores, reverse=True)[:3]))
    ranking = [{
        "author_id": entry.author_id, 
        "score": score} 
        for entry, score in zip(corpus, expertise_scores)]
    ranking.sort(key=lambda x: x['score'], reverse=True)
    return {"ranking": ranking}
