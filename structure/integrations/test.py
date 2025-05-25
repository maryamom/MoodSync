from openai_config import OpenAIConfig

openai_config = OpenAIConfig()

# Example messages for an agent
messages = [ {"role": "user", "content": "What is the weather like today?"}]

# Create a chat completion
response = openai_config.create_chat_completion(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

# Output the result
if response:
        print(response)
