from openai import OpenAI
api_key = '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'
client = OpenAI(
  api_key=api_key, 
)

def ask_the_gpt(messages, model="gpt-4", temperature=0.7):
    r"""Interact with OpenAI API(Basic example)"""
    try:
        response = client.completions.create(
            model=model,
            prompt=messages,
            temperature=temperature
        )
        return response.choices[0].text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None