from google import genai 

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello to Raghu"
)

print(response.text)