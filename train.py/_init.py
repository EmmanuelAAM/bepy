# from chatgpt import ask_the_gpt
from hf_models import ask_hf
from readRepo import read_repository_files
from tinyLlama import ask_the_little_llama
import time

FILES = read_repository_files(r'C:\Users\EJ359MZ\Projects\Repos\SDM\code\nodejs\services\web-service\client\src\components')

RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[96m'
SYSTEM_PROMP = {
                "role": "system",
                "content": "You are a senior javascript developer with a deep understanding of modern web development and the best practices on the javascript ecosystem",
            }

def tasks(file):
    return [
        # ✍️ Write description
        {"role": "user", "content": f"file content: \n content´´\n{file['content']}\n´´content\nWrite a description of the component."},
        # 📃 List Props
        {"role": "user", "content": f"file content: \n content´´\n{file['content']}\n´´content\nList the props of the react component using the format: 1. prop name: type."},
        # # 📃 List funtions
        {"role": "user", "content": f"file content: \n content´´\n{file['content']}\n´´content\nList the functions inside of the react component using the format: 1. functionName(params): return type."},
        # # 📈 Find possible improvements
        {"role": "user", "content": f"file content: \n content´´\n{file['content']}\n´´content\nIs any possible improvement in this code?"},
        # # 🚩 Find possible Issues
        {"role": "user", "content": f"file content: \n content´´\n{file['content']}\n´´content\nIs any possible problem in this code?"},
        ]

def side_fact_cheking(answer, task ):
    messages = [SYSTEM_PROMP, task, {"role": "assistant", "content": f"Answer: \n{answer}\n"}]
    messages.append({"role": "user", "content": f"Is that answer correct?"})
    answer = ask_the_little_llama(messages=messages)
    write_output_in_file(answer, "TinyLlama Annotations:", "")
    print(f"\n Fact Check Answer{answer}")

def write_output_in_file(answer, header, specific_task):
    with open('output.txt', 'a') as f:
        f.write(f"{header}\n{specific_task}\n{answer}.\n\n")

def process_promp(messages):
    processing_time = time.time()    
    answer = ask_hf(messages=messages)
    processing_time = (time.time() - processing_time) / 60 #'
    print(RED + f"Processed In {processing_time} {'Minutes' if processing_time > 1 else 'Seconds'}. \n")
    return answer

def proccess_files():
    print(YELLOW + "\nDocumentor: Starting the wigle wigle, go get a CostaRican ☕ while you wait, my love ❤️")
    print(YELLOW + "I got it from here, ya tu' sabe bebé! 💃 🎶 \n\n")
    for file in FILES:
        answer = ''
        print(BLUE + f"\nFilename: {file['name']} \n")
        for task in tasks(file):
            messages = [SYSTEM_PROMP]
            messages.append(task)
            current_task = task['content'].split('´´content')
            answer = process_promp(messages)
            write_output_in_file(answer, f"-- File Name: {file['name']}", f"{current_task[1]}:")
            print(YELLOW + f"- Task: {current_task[1]}")
            print(GREEN + f"- Answer: \n{answer}")
            # side_fact_cheking(answer, task['content'])
    print(GREEN+'\n__** Colorín colorado, este cuento se ha acabado 🤙🏼 **__')

proccess_files()