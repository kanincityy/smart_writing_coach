from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from data_preparation import clean_text  
import evaluate
from transformers import set_seed

# Set random seed for reproducibility
set_seed(42)  

# Load cleaned data
train_df = pd.read_csv('data/train.csv')
train_df = train_df[['cleaned_text', 'label']].rename(columns={'cleaned_text': 'text', 'label': 'label'})
train_df = train_df.dropna(subset=['text', 'label'])
val_df = pd.read_csv('data/val.csv')
val_df = val_df[['cleaned_text', 'label']].rename(columns={'cleaned_text': 'text', 'label': 'label'})
val_df = val_df.dropna(subset=['text', 'label'])
test_df = pd.read_csv('data/test.csv')
test_df = test_df[['cleaned_text', 'label']].rename(columns={'cleaned_text': 'text', 'label': 'label'})
test_df = test_df.dropna(subset=['text', 'label'])

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize function
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=512)

# Create Dataset objects for Hugging Face
train_texts = train_df['text'].tolist()
train_labels = train_df['label'].tolist()
val_texts = val_df['text'].tolist()
val_labels = val_df['label'].tolist()
labels = sorted(train_df['label'].unique())
labels = sorted(train_df['label'].unique())
label2id = {str(label): int(i) for i, label in enumerate(labels)}
id2label = {int(i): str(label) for i, label in enumerate(labels)}

train_dataset = Dataset.from_dict({'text': train_texts, 'label': train_labels})
val_dataset = Dataset.from_dict({'text': val_texts, 'label': val_labels})

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

# Set format for PyTorch
train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

# Load pretrained model for sequence classification
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased', 
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

# Define metrics
metric = evaluate.load('accuracy')

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy='epoch',
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='accuracy'
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# Train
trainer.train()
# Save the model
trainer.save_model('./models/level_estimator_model')
# Save the tokenizer
tokenizer.save_pretrained('./models/level_estimator_tokenizer')
# Save the label mappings
import json
with open('./models/label2id.json', 'w') as f:
    json.dump(label2id, f)
with open('./models/id2label.json', 'w') as f:
    json.dump(id2label, f)

# Prepare test dataset
test_texts = test_df['text'].tolist()
test_labels = test_df['label'].tolist()
test_dataset = Dataset.from_dict({'text': test_texts, 'label': test_labels})
test_dataset = test_dataset.map(tokenize_function, batched=True)
test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

# Evaluate the model
test_predictions = trainer.predict(test_dataset)
preds = test_predictions.predictions.argmax(-1)
labels = test_predictions.label_ids