from client import model

response=model.invoke(
    "What are the capital of madhaya pradesh?"
)

print(response.content)
