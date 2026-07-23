from google import genai

API_KEY = "API_KEY"

client = genai.Client(api_key=API_KEY)

print("Gemini Chat (type 'exit' to quit)\n")

while True:
    prompt = input("You: ")

    if prompt.lower() == "exit":
        break

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    print("Gemini:", response.text)

# for model in client.models.list():
#     print(model.name)
