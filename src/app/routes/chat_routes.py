from fastapi import APIRouter, UploadFile, File, Request
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from config import GEMINI_API_KEY, OPENAI_API_KEY, ALLOWED_OPENAI_MODELS, ALLOWED_GEMINI_MODELS, ALLOWED_CLAUDE_MODELS
from schemas.chat_schema import chatCompletionRequestSchema
from services.gemini_service import geminiChatCompletion
from services.openai_service import openaiChatCompletion, openaiMergestackChatAssistant
from services.claude_service import claudeChatCompletion
from services.assemblyai_service import assemblyaiTranscribe
from utils.response_builder import ResponseBuilder
from utils.pycrypto import decrypt
from utils.limiter import limiter


# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)
openai.api_key = OPENAI_API_KEY

@router.post("/completion")
@limiter.limit("1/minute")
def chatCompletion(request: Request, body: chatCompletionRequestSchema):
    
    body.text = decrypt(body.text)
    
    if body.model in ALLOWED_GEMINI_MODELS:
        return geminiChatCompletion(body.model, body.text)
    elif body.model in ALLOWED_OPENAI_MODELS:
        return openaiChatCompletion(body.model, body.text) 
    elif body.model in ALLOWED_CLAUDE_MODELS:
        return claudeChatCompletion(body.model,body.text)
    elif body.model == "mergestack-chat-assistant":
        return openaiMergestackChatAssistant("gpt-4o",body.text)
    else:
        return ResponseBuilder().setSuccess(False).setMessage("Invalid model").setStatusCode(400).build()
    
    
@router.post("/transcribe")
@limiter.limit("1/minute")
async def transcribe(request: Request , audio: UploadFile = File(...)):
    try:
        # Process the uploaded audio file
        audioContent = await audio.read()
        # Send the audio content as a file
        return assemblyaiTranscribe(audioContent)
    except Exception as e:
        return ResponseBuilder().setSuccess(False).setMessage("An Error Occurred").setError(str(e)).setStatusCode(500).build()





