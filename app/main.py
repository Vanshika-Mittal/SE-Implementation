from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import json

# Simple logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger("ml_api")

app = FastAPI()

class Payload(BaseModel):
    text: str

# Load a small transformer model (distilbert) for sentiment
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

@app.post('/predict')
async def predict(payload: Payload, request: Request):
    start = time.time()
    text = payload.text
    try:
        inputs = tokenizer(text, return_tensors='pt', truncation=True)
        with torch.no_grad():
            out = model(**inputs)
            probs = F.softmax(out.logits, dim=-1).squeeze().tolist()
            confidence = max(probs)
            label = int(torch.argmax(out.logits, dim=-1).item())
        latency = (time.time() - start) * 1000.0
        log_entry = {
            "path": str(request.url.path),
            "text_len": len(text),
            "latency_ms": latency,
            "confidence": confidence,
            "label": label,
            "timestamp": time.time()
        }
        logger.info(json.dumps(log_entry))
        return {"label": label, "confidence": confidence, "latency_ms": latency}
    except Exception as e:
        latency = (time.time() - start) * 1000.0
        logger.exception("prediction failed")
        return {"error": str(e), "latency_ms": latency}
