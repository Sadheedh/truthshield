from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
import torch.nn.functional as F

import os
from serpapi import GoogleSearch

# Adding SerpAPI
SERPAPI_KEY = "993eefbdef9ee1603ad7aa7d83615c2b0410e208fd3c8e799cc1240d13473e0c"

def search_with_serpapi(query, num_results=3):
    if not SERPAPI_KEY:
        return []

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])[:num_results]

    return [{
        "title": item.get("title", ""),
        "url": item.get("link", ""),
        "snippet": item.get("snippet", "")
    } for item in organic]



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

# Updated /predict route
@app.post("/predict")
def predict(claim: Claim):
    snippets = search_with_serpapi(claim.claim)

    evidence_text = " ".join([s['snippet'] for s in snippets]) or "No supporting evidence."
    combined_input = f"{claim.claim} [SEP] {evidence_text}"

    inputs = tokenizer(combined_input, return_tensors="pt", truncation=True, padding=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidence, pred = torch.max(probs, dim=1)

    label = "real" if pred.item() == 1 else "fake"

    explanation = (
        "Claim supported by trusted sources." if label == "real"
        else "No trusted source confirms the claim."
    )

    return {
        "claim": claim.claim,
        "prediction": label,
        "confidence": round(confidence.item(), 2),
        "explanation": explanation,
        "evidence_snippets": snippets
    }
