from models.gpt_engine import GPTEngine, ChatGPT, PhoGPT

import argparse
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

parser = argparse.ArgumentParser(description="Run the FastAPI server")
parser.add_argument("--port", type=int, default=8000, help="Port number")
parser.add_argument("--model", type=str, default="chatgpt", help="Model to use for the API")
args = parser.parse_args()

# Create an instance of FastAPI
app = FastAPI()

# Define a class for the request body
class EmailContent(BaseModel):
    email_content: str

# Selecting AI model
if args.model == "chatgpt":
    model = ChatGPT()
elif args.model == "phogpt":
    model = PhoGPT()
else:
    raise ValueError("Invalid model name. Please choose 'chatgpt' or 'phogpt")

# Define the root route
@app.get("/")
def read_root():
    return {"Project": "Email Assistant API"}

@app.post("/api/sentiment_analysis")
def sentiment_analysis(mail: EmailContent):
    return {"response": model.sentiment_analysis(mail.email_content)}

@app.post("/api/content_summary")
def content_summary(mail: EmailContent):
    return {"response": model.content_summary(mail.email_content)}

@app.post("/api/generate_reply")
def generate_reply(mail: EmailContent):
    return {"response": model.generate_reply(mail.email_content)}

@app.post("/api/analyze")
def analyze_email(mail: EmailContent):
    sentiment = model.sentiment_analysis(mail.email_content)
    summary = model.content_summary(mail.email_content)
    reply = model.generate_reply(mail.email_content)

    return {
        "sentiment": sentiment,
        "summary": summary,
        "reply": reply
    }

uvicorn.run(app, host="localhost", port=args.port, log_level="info")