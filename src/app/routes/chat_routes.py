from fastapi import APIRouter
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from config import GEMINI_API_KEY, OPENAI_API_KEY
from schemas.chat_schema import chatCompletionRequestSchema
from services.gemini_service import geminiChatCompletion
from services.openai_service import openaiChatCompletion


# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)
openai.api_key = OPENAI_API_KEY

@router.post("/completion")
def chatCompletion(body: chatCompletionRequestSchema):
    if body.model == "gemini-1.5-flash":
        return geminiChatCompletion(body.model, body.text)
    elif body.model == "gpt-4o":
        return openaiChatCompletion(body.model, body.text)
    else:
        return {"success": False, "message": "Invalid model", "statusCode": 400}





