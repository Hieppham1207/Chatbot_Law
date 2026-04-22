from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ====== import hàm của bạn ======
from build_RAG import chatbot

# ====== request schema ======
class Query(BaseModel):
    question: str
@app.get("/")
def home():
    return {"message": "API is running"}
# ====== API endpoint ======
@app.post("/chat")
def chat(query: Query):
    answer, docs = chatbot(query.question)
    return {
        "question": query.question,
        "answer": answer,
        "docs": docs
    }
