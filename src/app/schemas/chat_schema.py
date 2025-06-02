from pydantic import BaseModel

class chatCompletionRequestSchema(BaseModel):
    model: str
    text: str