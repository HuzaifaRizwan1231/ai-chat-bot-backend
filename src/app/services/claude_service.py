import anthropic
from config import MAX_TOKEN
from config import CLAUDE_API_KEY
from utils.response_builder import ResponseBuilder

client = anthropic.Anthropic(api_key = CLAUDE_API_KEY)

def claudeChatCompletion(model, text):
    try:    
        message = client.messages.create(
            model=model,
            max_tokens=MAX_TOKEN,
            messages=[
                {"role": "user", "content": text}
            ]
        )
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(message.content[0].text).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        # Logging the error
        print(response)
        return response