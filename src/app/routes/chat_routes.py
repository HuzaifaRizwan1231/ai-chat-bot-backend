from fastapi import APIRouter, UploadFile, File, Request
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from config.config import GEMINI_API_KEY, OPENAI_API_KEY, ALLOWED_OPENAI_MODELS, ALLOWED_GEMINI_MODELS, ALLOWED_CLAUDE_MODELS, ALLOWED_STREAM_MODELS
from schemas.chat_schema import chatCompletionRequestSchema, langchainCompletionRequestSchema, updateChatRequestSchema
from services.gemini_service import geminiChatCompletion
from services.openai_service import openaiChatCompletion, openaiChatStream, openaiMergestackChatAssistant
from services.claude_service import claudeChatCompletion
from services.assemblyai_service import assemblyaiTranscribe
from services.langchain_service import getLangchainResponse, getLangchainResponseMergestack
from services.database_service import insertChat, getAllChats, deleteChatRecord, updateChatRecord
from utils.response_builder import ResponseBuilder
from utils.pycrypto import decrypt
from utils.limiter import limiter
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize
router = APIRouter()
load_dotenv()

# API Keys
genai.configure(api_key=GEMINI_API_KEY)
openai.api_key = OPENAI_API_KEY

@router.post("/completion")
@limiter.limit("5/minute")
async def chatCompletion(request: Request, body: chatCompletionRequestSchema):
    
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
    
@router.post("/langchain-completion")
@limiter.limit("5/minute")
async def langchainChatCompletion(request: Request, body: langchainCompletionRequestSchema):
    
    text = body.text
    model = body.model
    chatId = body.chatId
    
    if model not in ALLOWED_OPENAI_MODELS + ALLOWED_GEMINI_MODELS + ALLOWED_CLAUDE_MODELS + ["mergestack-chat-assistant"]:
        return ResponseBuilder().setSuccess(False).setMessage("Invalid model").setStatusCode(400).build()
    
    text = decrypt(text)
    
    if model == "mergestack-chat-assistant":
        return getLangchainResponseMergestack("gpt-4o",text)
    
    if model in ALLOWED_OPENAI_MODELS:
        langchainModel = ChatOpenAI(model=model)
    elif model in ALLOWED_GEMINI_MODELS:
        langchainModel = ChatGoogleGenerativeAI(model=model, api_key=GEMINI_API_KEY)
    return getLangchainResponse(langchainModel, text, model, chatId)
    
        
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

@router.get("/stream")
@limiter.limit("5/minute")
async def chatStream(request: Request, model: str, text: str):

    if model in ALLOWED_STREAM_MODELS and model in ALLOWED_OPENAI_MODELS:
        return await openaiChatStream(model, text) 
    else:
        return ResponseBuilder().setSuccess(False).setMessage("Invalid model").setStatusCode(400).build()


@router.post("/create")
def createNewChat(request: Request):
    return insertChat()
   
@router.get("/get")
def fetchChats(request: Request):
    return getAllChats()
   
@router.delete("/delete")
def deleteChat(request: Request, chatId: int):
    return deleteChatRecord(chatId)
   
@router.post("/update")
def updateChat(request: Request, body: updateChatRequestSchema):
    return updateChatRecord(body)