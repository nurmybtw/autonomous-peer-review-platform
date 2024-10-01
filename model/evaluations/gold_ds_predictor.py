import json
import os
import re
from tqdm import tqdm
import numpy as np

class GoldDatasetPredictor:
    def __init__(self, embedding_function, embedding_dim, similarity_function, dataset_dir, preds_dir, algo_name):
        self.embedding_function = embedding_function
        self.embedding_dim = embedding_dim
        self.similarity_function = similarity_function
        self.dataset_dir = dataset_dir
        self.preds_dir = preds_dir
        self.algo_name = algo_name
    
    def precompute_embeddings(self):
        embeddings = {}
        for i in tqdm(range(1, 11)):
            dataset_variation_dir = f'd_20_{i}'
            embeddings[dataset_variation_dir] = {
                'papers': {},
                'reviewers': {}
            }

            submissions_file = os.path.join(self.dataset_dir, dataset_variation_dir, 'submissions.json')
            papers = json.load(open(submissions_file, 'r'))
            for paper_id, paper in papers.items():
                content = 'Title: ' + paper['content']['title'] + '. Abstract: ' + paper['content']['abstract']
                embeddings[dataset_variation_dir]['papers'][paper_id] = self.embedding_function(content)
            
            reviewers_dir = os.path.join(self.dataset_dir, dataset_variation_dir, 'archives')
            pattern = re.compile(r'~(.+)\.jsonl')
            for filename in os.listdir(reviewers_dir):
                match = pattern.match(filename)
                reviewer_id = match.group(1)
                embeddings[dataset_variation_dir]['reviewers'][reviewer_id] = {}
                reviewer_file = open(os.path.join(reviewers_dir, filename), 'r')
                for line in reviewer_file:
                    paper = json.loads(line)
                    content = 'Title: ' + paper['content']['title'] + '. Abstract: ' + paper['content']['abstract']
                    embeddings[dataset_variation_dir]['reviewers'][reviewer_id][paper['id']] = self.embedding_function(content)
        self.embeddings = embeddings
    
    def predict(self):
        average = lambda lst: sum(lst) / len(lst) if len(lst) > 0 else 0
        progress_bar = tqdm(total=10, desc="Processing", ncols=10, ascii=True, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        for dataset_variation, embeddings in self.embeddings.items():
            similarities = {}
            for reviewer_id, reviewer_embeddings in embeddings['reviewers'].items():
                similarities[reviewer_id] = {}
                reviewer_embeddings_arr = np.zeros((len(reviewer_embeddings.keys()), self.embedding_dim), dtype=np.float32)
                for i, (reviewer_paper_id, reviewer_paper_embedding) in enumerate(reviewer_embeddings.items()):
                    reviewer_embeddings_arr[i,:] = reviewer_paper_embedding
                for paper_id, paper_embedding in embeddings['papers'].items():
                    scores = self.similarity_function(paper_embedding, reviewer_embeddings_arr).numpy()[0,:].tolist()
                    scores.sort(reverse=True)
                    similarities[reviewer_id][paper_id] = average(scores[:3])
            json.dump(similarities, open(os.path.join(self.preds_dir, f'{self.algo_name}_{dataset_variation}_ta.json'), 'w'))
            progress_bar.update(1)