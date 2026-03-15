import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from essay_grader import EssayGrader
from generate_feedback import FeedbackGenerator

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found.", file=sys.stderr)
    exit(1)

app = FastAPI()  
grader = EssayGrader()
feedback_gen = FeedbackGenerator(api_key=OPENAI_API_KEY)

class PredictRequest(BaseModel):
    essay_text: str

class FeedbackRequest(BaseModel):
    essay_text: str
    scores: dict
    teacher: str = "You are a balanced teacher who gives honest, constructive feedback."

@app.post("/predict_scores")
def predict_scores(req: PredictRequest):
    scores = grader.predict_scores(req.essay_text)
    return scores

@app.post("/generate_feedback")
def generate_feedback(req: FeedbackRequest):
    feedback = feedback_gen.generate_feedback(req.essay_text, req.scores, req.teacher)
    return {"feedback": feedback}