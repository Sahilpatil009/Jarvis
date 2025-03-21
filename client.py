import google.generativeai as genai

genai.configure(api_key="AIzaSyCxGm_EFvP3GCPs2xS6E806ck2G_RHB_uw")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "content": "what is coding"},
        {"role": "model", "parts": "You are virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    ]
)

response = model.generate_content("What is coding")
print(response.text)
