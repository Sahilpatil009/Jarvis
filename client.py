from openai import OpenAI

# pip install openai
# if you save the key under a different enviroment variable name, you can do something like:
client = OpenAI(
  api_key="sk-proj--Wx17ehGk2PnwmzCHcDwT3BlbkFJMj6bYTk9jG1bqZaFTcj",

)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud."},
    {"role": "user", "content": "What is coding"}
  ]
)

print(completion.choices[0].message.content)