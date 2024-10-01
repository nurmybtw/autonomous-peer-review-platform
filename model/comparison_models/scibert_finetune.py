import pandas as pd
from datasets import Dataset
from ast import literal_eval
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, TrainingArguments, Trainer
import wandb
from ..train_utils.labels_encoder import LabelsEncoder
from ..train_utils.compute_metrics import compute_metrics

################### Dataset Prep ######################

train_set = pd.read_csv('./../data/arxiv_balanced_twothreelabel_train.csv')
train_set["categories"] = train_set["categories"].apply(lambda x: literal_eval(x))
train_set.rename(columns={'abstract': 'text', 'categories': 'labels'}, inplace=True)
train_set.drop(columns=['id', 'authors', 'title', 'primary_category'], inplace=True)

test_set = pd.read_csv('./../data/arxiv_balanced_twothreelabel_test.csv')
test_set["categories"] = test_set["categories"].apply(lambda x: literal_eval(x))
test_set.rename(columns={'abstract': 'text', 'categories': 'labels'}, inplace=True)
test_set.drop(columns=['id', 'authors', 'title', 'primary_category'], inplace=True)

train_dataset = Dataset.from_pandas(train_set)
test_dataset = Dataset.from_pandas(test_set)

################### Labels Encoding ######################

labels_encoder = LabelsEncoder(task_config='multi-label-classification')

def encode_labels(examples):
    examples['labels'] = labels_encoder(examples['labels'], return_tensors=False)
    return examples

train_dataset = train_dataset.map(encode_labels)
test_dataset = test_dataset.map(encode_labels)


################### Pre-Tokenization ######################

tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

train_ds = train_dataset.map(tokenize_function, batched=True)
test_ds = test_dataset.map(tokenize_function, batched=True)

train_ds.shuffle(seed=42)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

################### wandb.ai login ######################

# Please insert your wandb.ai api_key for vizualization (used by huggingface)
WANDB_API_KEY = ''
wandb.login(key=WANDB_API_KEY)

################### Model Init ######################

model = AutoModelForSequenceClassification.from_pretrained(
    'allenai/scibert_scivocab_uncased', 
    num_labels=len(labels_encoder)
)
model.config.problem_type = 'multi_label_classification'

################### Training ######################

training_args = TrainingArguments(
    output_dir='scibert-ft',
    eval_strategy="epoch",
    num_train_epochs=2,
    save_steps=20000
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()

trainer.save_state()