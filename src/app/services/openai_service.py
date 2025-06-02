import openai
from utils.response_builder import ResponseBuilder

def openaiChatCompletion(model, text):
    try:    
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": "Mergestack is a very good company providing IT services"},
                {"role": "user", "content": text}
            ]
        )
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(completion.choices[0].message.content).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(e.response.json().get('error', {}).get('message', str(e))).setStatusCode(e.response.status_code).build()
        # Logging the error
        print(response)
        return response