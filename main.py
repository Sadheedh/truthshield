from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and tokenizer from local folder
model = DistilBertForSequenceClassification.from_pretrained("./distilbert_fakenews_model")
tokenizer = DistilBertTokenizerFast.from_pretrained("./distilbert_fakenews_model")
model.eval()

# Request body format
class Claim(BaseModel):
    claim: str

# Root endpoint
@app.get("/")
def read_root():
    return {"status": "Fake News Detection API is running!"}

# Prediction endpoint
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
