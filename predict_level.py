import torch
from transformers import BertForSequenceClassification, BertTokenizer
import json

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_path = 'path/to/save/level_estimator_model'
tokenizer_path = 'path/to/save/level_estimator_tokenizer'
label2id_path = 'path/to/save/label2id.json'
id2label_path = 'path/to/save/id2label.json'

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
model.to(device)
model.eval()

with open(label2id_path) as f:
    label2id = json.load(f)
with open(id2label_path) as f:
    id2label = json.load(f)

def predict_level(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = logits.argmax(dim=-1).item()
    # id2label keys might be strings from JSON, so cast predicted_label to str
    return id2label.get(str(predicted_label), "Unknown")

# Example
text = "This is an example essay to predict the proficiency level."
print(f"Predicted proficiency level: {predict_level(text)}")