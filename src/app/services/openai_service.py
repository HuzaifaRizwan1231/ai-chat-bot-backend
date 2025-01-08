import openai

def openaiChatCompletion(model, text):
    try:    
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": "Mergestack is a very good company providing IT services"},
                {"role": "user", "content": text}
            ]
        )
        return {"success": True, "message": completion.choices[0].message.content, "statusCode": 200}

    except Exception as e:
        response = {"success": False, "message":e.response.json().get('error', {}).get('message', str(e)), "statusCode": e.response.status_code}
        # Logging the error
        print(response)
        return response