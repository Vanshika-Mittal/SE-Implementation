import json
import shap
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# Helper prediction function for SHAP (wraps model to accept raw text)
def predict_texts(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        out = model(**inputs)
        probs = torch.nn.functional.softmax(out.logits, dim=-1).numpy()
    return probs

# Load a small sample logged inputs
logs = []
with open('analysis/sample_requests.json') as f:
    logs = json.load(f)

texts = [l['text'] for l in logs[:50]]

# Use KernelExplainer or TextExplainer -- here we use a simple kernel explain wrapper
explainer = shap.Explainer(predict_texts, tokenizer)
shap_values = explainer(texts)

# Save a small summary
for i, t in enumerate(texts[:10]):
    print(f"Text: {t}")
    print(shap_values[i].values)

