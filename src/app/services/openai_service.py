import openai
from utils.response_builder import ResponseBuilder
from utils.mergestack_chat_assistant import MergeStackChatAssistant

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
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(response.content[0].text.value).setStatusCode(200).build()

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
        return ResponseBuilder().setSuccess(True).setMessage("Response Generated Successfully").setData(completion.choices[0].message.content).setStatusCode(200).build()

    except Exception as e:
        response = ResponseBuilder().setSuccess(False).setMessage("An Error Occured").setError(str(e)).setStatusCode(500).build()
        # Logging the error
        print(response)
        return response