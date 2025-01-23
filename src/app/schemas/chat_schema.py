from pydantic import BaseModel

class chatCompletionRequestSchema(BaseModel):
    model: str
    text: str
    

class langchainCompletionRequestSchema(BaseModel):
    model: str
    text: str
    chatId: int