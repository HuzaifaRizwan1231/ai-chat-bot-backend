import openai, json, asyncio
from utils.response_builder import ResponseBuilder
from utils.mergestack_chat_assistant import MergeStackChatAssistant
from utils.pycrypto import encrypt
from fastapi.responses import StreamingResponse

global mergestackInstance
mergestackInstance = None

def openaiMergestackChatAssistant(model, text):
    global mergestackInstance
    try:
        if mergestackInstance is None:
            mergestackInstance = MergeStackChatAssistant(model)            
            
        # Adding the user message to the thread
        openai.beta.threads.messages.create(
            mergestackInstance.thread.id,
            role="user",
            content=text,
        )
        # Poll and run to get the response
        response = mergestackInstance.pollAndRun()
        encrypted_data = encrypt(response.content[0].text.value)
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(encrypted_data).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        # Logging the error
        print(e)
        return response

def openaiChatCompletion(model, text):
    try:    
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": "Mergestack is a very good company providing IT services"},
                {"role": "user", "content": text}
            ],
        )
        encrypted_data = encrypt(completion.choices[0].message.content)
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(encrypted_data).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        # Logging the error
        print(response)
        return response
    
async def openaiChatStream(model, text):
    async def generate_openai_response():
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                stream=True
        )

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {json.dumps({'text': content})}\n\n"
                    # To handle fast state update on the frontend
                    # await asyncio.sleep(0.07)
                    
        except Exception as e:
            yield f"data: {json.dumps({'text': str(e)})}\n\n"

    # Return as streaming response
    return StreamingResponse(generate_openai_response(), media_type="text/event-stream")