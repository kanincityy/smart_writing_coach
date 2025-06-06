# Smart Writing Coach

---

## Overview 

*Smart Writing Coach* is an AI-powered tool that provides level-appropriate feedback on English writing samples. It helps learners improve their writing skills with personalised corrections, explanations, and next-step suggestions based on CEFR levels.

---

## Features  

- Fine-tuned BERT model for CEFR level classification  
- Level-appropriate feedback tone (gentle/direct)  
- Edit tracking with explanations  
- Personalised learning suggestions  
- User-friendly interface 

---

## Installation  

```bash
git clone https://github.com/yourusername/smart_writing_coach.git
cd smart_writing_coach
pip install -r requirements.txt
```

---

## Usage

# Train the model

```bash
python finetune_bert.py
```
# Run inference on sample text

```bash
python inference.py --input "Your text here"
```

# Launch the app (if applicable)
```bash
streamlit run app.py
```

---

## Model Saving & Loading

The trained model and tokenizer are saved to ./models/level_estimator_model and ./models/level_estimator_tokenizer respectively. You can load them using:

```bash
python
from transformers import BertForSequenceClassification, BertTokenizer

model = BertForSequenceClassification.from_pretrained('./models/level_estimator_model')
tokenizer = BertTokenizer.from_pretrained('./models/level_estimator_tokenizer')
```

---

## Data Preparation
Prepare your datasets as CSV files with columns cleaned_text and label. Clean text by removing noise and tokenizing properly. Example preprocessing scripts are available in data_preparation.py.

---

## Evaluation
The model is evaluated using accuracy metric on validation and test sets. Run evaluation with:

```bash
python evaluate_model.py --test_data ./data/test.csv
```

--- 

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Author
