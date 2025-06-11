from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F

app = FastAPI()

model = DistilBertForSequenceClassification.from_pretrained("./distilbert_fakenews_model")
tokenizer = DistilBertTokenizerFast.from_pretrained("./distilbert_fakenews_model")
model.eval()

class Claim(BaseModel):
    claim: str

@app.post("/predict")
def predict(claim: Claim):
    inputs = tokenizer(claim.claim, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidence, pred = torch.max(probs, dim=1)

    label = "real" if pred.item() == 1 else "fake"
    return {
        "claim": claim.claim,
        "prediction": label,
        "confidence": round(confidence.item(), 2),
        "explanation": "AI prediction based on learned linguistic patterns."
    }

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Fake News Detection API is running!"}

# ✅ Main route to make predictions
@app.post("/predict")
def predict(news: NewsInput):
    inputs = tokenizer(news.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    label = "Fake" if prediction == 1 else "Real"
    return {"prediction": label}
