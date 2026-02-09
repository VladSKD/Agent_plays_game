# Download ollama from https://ollama.com/
# and then install python package:
#   pip install ollama

import ollama

# We'll use 'qwen3-vl:4b'
model_name = "qwen3-vl:4b"

prompt = "What is the reason of life? Respond in one word only."

# Generate the response
response = ollama.generate(
    model=model_name, 
    prompt=prompt
)

# The response is a dictionary; we grab the 'response' key
answer = response['response'].strip()

print(f"The answer is: {answer}")

# Example output:
# The answer is: meaning