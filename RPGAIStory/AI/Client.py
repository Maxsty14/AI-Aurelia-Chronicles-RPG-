# import google.genai as genai

# def GetModel(api_key):
#     return genai.Client(api_key=api_key)

# def AskModel(client, prompt):
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )
#     return response.text

import google.generativeai as genai

def GetModel(api_key):
    genai.configure(api_key=api_key)
    client = genai.GenerativeModel("gemini-3.1-flash-lite")
    chat = client.start_chat(history=[])
    return chat

def AskModel(chat, prompt):
    response = chat.send_message(prompt)
    return response.text

