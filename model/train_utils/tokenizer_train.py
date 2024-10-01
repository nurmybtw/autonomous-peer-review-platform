import os
import pandas as pd
from pathlib import Path
from tokenizers import BertWordPieceTokenizer

train_set = pd.read_csv('./data/arxiv_balanced_twothreelabel_train.csv')

os.mkdir('./data')
text = []
file_count = 0
for i, entry in train_set.iterrows():
    text.append(entry['title'] + ' ' + entry['abstract'])
    if len(text) == 10000:
        with open(f'./data/text_{file_count}.txt', 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(text))
        text = []
        file_count += 1

paths = [str(x) for x in Path('./data').glob('**/*.txt')]

tokenizer = BertWordPieceTokenizer(
    clean_text=True,
    handle_chinese_chars=True,
    strip_accents=True,
    lowercase=True
)

tokenizer.train( 
    files=paths,
    vocab_size=50000, 
    min_frequency=5,
    limit_alphabet=1000, 
    wordpieces_prefix='##',
    special_tokens=['[UNK]', '[PAD]']
)

tokenizer.save_model('./data', 'custom-wp-vocab-50k')