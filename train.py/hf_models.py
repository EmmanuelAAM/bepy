import requests

API_URL = "https://wawwaqur03n8rwit.us-east-1.aws.endpoints.huggingface.cloud"
headers = {"Accept" : "application/json", "Authorization": "Bearer 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", "Content-Type": "application/json" }

def parse_messages(messages):
    chat = ""
    for message in messages:
        chat+= f"<|im_start|>{message['role']}\n {message['content']}<|im_end|>"
    return {
        "inputs": f"{chat}<|im_start|>assistant\n"
    }

# ask models from huggingFace inference api
def ask_hf(messages):
    r"""Interact with models from huggingFace inference api"""
    response = requests.post(API_URL, headers=headers, json=parse_messages(messages))
    json_response = response.json()
    print(json_response)
    generated_text = json_response[0]["generated_text"]
    # Split the text at the separator
    parts = generated_text.split("<|im_start|>assistant")
    return parts[1].strip()
    