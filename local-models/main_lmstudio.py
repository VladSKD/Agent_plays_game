# First, install the lmstudio package if you haven't already:
#   pip install lmstudio

import lmstudio as lms

# Get a handle to a model (loads it if not already in memory)
model = lms.llm("qwen/qwen3-vl-4b")

prompt = """
What is the reason of life? Respond in one word only.
"""

answer = str(model.respond(prompt))
print(f"The answer is: {answer}")

# Example output:
# The answer is: Purpose