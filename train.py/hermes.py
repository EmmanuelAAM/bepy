# Code to inference Hermes with HF Transformers
# Requires pytorch, transformers, bitsandbytes, sentencepiece, protobuf, and flash-attn packages

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import LlamaTokenizer, MixtralForCausalLM
# import bitsandbytes, flash_attn

tokenizer = LlamaTokenizer.from_pretrained('NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO', trust_remote_code=True)
model = MixtralForCausalLM.from_pretrained(
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=False,
    load_in_4bit=True,
    use_flash_attention_2=True
)

def parse_messages(messages):
    chat = ""
    for message in messages:
        chat+= f"<|im_start|>{message['role']}\n {message['message']}<|im_end|>"

def ask_hermes(messages):
    chat = parse_messages(messages)
    input_ids = tokenizer.apply_chat_template(chat, return_tensors="pt").input_ids.to("cuda")
    generated_ids = model.generate(input_ids, max_new_tokens=750, temperature=0.8, repetition_penalty=1.1, do_sample=True, eos_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
    return response
