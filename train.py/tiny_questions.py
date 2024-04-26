from transformers import pipeline
import time
import torch

RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

def process_promp(messages):
    processing_time = time.time()
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.4, top_p=0.95, top_k=50)
    processing_time = (time.time() - processing_time) / 60 
    print(YELLOW + f"Processed In {processing_time} Seconds. \n")    
    return outputs

def read_user_input(messages: list[dict[str, str]]):
    user_input = input("User (insert 'exit' to end this file proccess): ")
    if(user_input != 'exit'):
        messages.append({"role": "user", "content": user_input})
        response = process_promp(messages)
        print_messages(response)
        read_user_input(response)
    return

def print_messages(output):
    print(GREEN + output[0]["generated_text"]+"\n")

def start_chat():
        messages = [
            {
                "role": "system",
                "content": "You are a highly knowledgeable and friendly chatbot equipped with extensive information across various domains. Your goal is to understand and respond to user inquiries with accuracy and clarity. You're adept at providing detailed explanations, concise summaries, and insightful responses. Your interactions are always respectful, helpful, and focused on delivering the most relevant information to the user.",
            }
        ]
        read_user_input(messages) 

start_chat()