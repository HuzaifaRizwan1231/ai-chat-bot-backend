from fastapi import APIRouter
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from config import GEMINI_API_KEY, OPENAI_API_KEY, ALLOWED_OPENAI_MODELS, ALLOWED_GEMINI_MODELS
from schemas.chat_schema import chatCompletionRequestSchema
from services.gemini_service import geminiChatCompletion
from services.openai_service import openaiChatCompletion, openaiMergestackChatAssistant
from utils.response_builder import ResponseBuilder


# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)
openai.api_key = OPENAI_API_KEY

@router.post("/completion")
def chatCompletion(body: chatCompletionRequestSchema):
    if body.model in ALLOWED_GEMINI_MODELS:
        return geminiChatCompletion(body.model, body.text)
    elif body.model in ALLOWED_OPENAI_MODELS:
        return openaiChatCompletion(body.model, body.text) 
    elif body.model == "mergestack-chat-assistant":
        return openaiMergestackChatAssistant("gpt-4o",body.text)
    else:
        return ResponseBuilder().setSuccess(False).setMessage("Invalid model").setStatusCode(400).build()





