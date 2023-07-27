import openai

# Set your OpenAI API key here
openai.api_key = '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'

def chat_with_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the language model engine
        prompt=prompt,
        max_tokens=150  # Adjust the max_tokens parameter as needed for the desired response length
    )
    return response.choices[0].text.strip()
