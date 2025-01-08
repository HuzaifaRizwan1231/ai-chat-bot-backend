import google.generativeai as genai

def geminiChatCompletion(model, text):
    try:     
        model = genai.GenerativeModel(model)
        response = model.generate_content(text, generation_config=genai.GenerationConfig(
            max_output_tokens=500,
            temperature=0.7,
        ))
        print(response)
        return {"success": True, "message": response.text, "statusCode": 200}

    except Exception as e:
        response = {"success": False, "message":"An Error Occured: " + str(e), "statusCode": 500}

        # Logging the error
        print(response)

        return response