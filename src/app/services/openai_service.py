import openai
from utils.response_builder import ResponseBuilder
from utils.mergestack_chat_assistant import MergeStackChatAssistant
from utils.pycrypto import encrypt

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