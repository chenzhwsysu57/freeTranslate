# use openai gpt4 to run
import argparse
import os
import dashscope
from openai import OpenAI
import json
from datetime import datetime
import sys
import random
import glob
import pickle

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
with open('datasets.pkl', 'rb') as f:
    datasets = pickle.load(f)

# datasets 从 13 开始

with open('prompt/prompt1.md', 'r') as f:
    prompt = f.read()

# len(datasets)
for i in range(124, len(datasets)):
    content = prompt.replace("{{paragraph}}", str(datasets[i]))

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a helpful assistant"},
            {"role": "user",    "content": content}
        ],
        max_tokens=2600,
    )
    input, output, dataset = completion.usage.prompt_tokens, completion.usage.completion_tokens, completion.choices[0].message.content
    # 写入文件
    filename = f"{input}_{output}_{i}_{i+1}.json"
    with open(filename, 'x') as f:
        f.write(dataset)
    # print(f"\033[1;35m[I]=============\n input {input}, output {output}, dataset: \033[0m{dataset}")