from transformers import pipeline
import torch

MAX_TOKENS = 1024
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")


def format_response(messages):
    wordToReplace = "<|assistant|>"
    lastIndex = messages.rfind(wordToReplace)
    if lastIndex != -1:
        return messages[lastIndex + len(wordToReplace):]

def ask_the_little_llama(messages, temperature=0.7):
    r"""Interact with tinyLlama 1B (locally)"""
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, truncation=True)
    outputs = pipe(prompt, max_new_tokens=MAX_TOKENS, do_sample=True, temperature=temperature)
    return format_response(outputs[0]["generated_text"])
