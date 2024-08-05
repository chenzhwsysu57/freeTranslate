import urllib
import pyperclip as clip 
import tagui as t 
import sys 
import time 
if sys.platform == 'darwin':
    MODIFIER = '[cmd]'
elif sys.platform == 'linux':
    MODIFIER = '[ctrl]'
else:
    raise NotImplementedError(f"{sys.platform} not implmented!")

def wait_until_present( selector):
    start_time = time.time()
    timeout = 20
    while time.time() - start_time < timeout:
        if t.present(selector):
            return True
        time.sleep(1)  # 等待1秒后再次检查
        print(f"waiting for {selector}...", end="")
    t.close()
    raise TimeoutError(f"超过等待时间 {timeout} 秒，无法找到元素 {selector}")


def batch_test_translate(inputs, dest):
    t.init(visual_automation=True)

    # url = f'https://translate.google.com/?sl=zh-CN&tl=en&text={encoded_text}&op=translate'
    if dest == 'en':
        url = f'https://translate.google.com/?sl=zh-CN&tl=en&text=%3Ctag%3E&op=translate'
    if dest == 'cn':
        url = f'https://translate.google.com/?sl=en&tl=zh-CN&text=%3Ctag%3E&op=translate'
    t.url(url)
    t.keyboard('[esc]')

    # 处理 input 
    input_doc = "" 
    for input in inputs:
        input_doc += input 
        if input != inputs[len(inputs) - 1]:
            input_doc += "\n\n" 

    clip.copy(f"{input_doc}<tag>")
    # try:
    #     wait_until_present('<tag>') 
    # except:
    #     raise Exception("init page: <tag> not found")
    wait_until_present('<tag>') 
    
    t.click('<tag>')
    t.keyboard(f'{MODIFIER}a')
    t.keyboard(f'{MODIFIER}v')
    # t.click('Copy translation')
    wait_until_present('复制译文')
    try:
        t.click('复制译文')
    except:
        raise Exception("result page: 复制译文 not found")
    t.close()

    translated_doc = clip.paste().replace('<tag>',"")
    translated_doc = translated_doc.replace('<标签>', "")
    # 处理 results，组装成 list
    return_list = translated_doc.split("\n\n")

    return return_list


import json
def count_words(text):
    '''计算文本中的字符数'''
    return len(text)

def json_to_csv(json_path, dest, *fields):
    '''
    翻译 JSON 文件中的指定字段，并在每次翻译后立即写回 JSON 文件。

    参数:
    - json_path: JSON 文件的路径。
    - dest: 目标语言。
    - fields: 需要翻译的字段名称。
    '''

    # 读取 JSON 文件
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            print(f"Loading {json_path}")
            data = json.load(file)
            print("Done")
    except FileNotFoundError:
        print(f"Error: The file at {json_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file at {json_path} is not a valid JSON.")
        return

    # 用于收集所有需要翻译的文本
    to_translate = []
    indices = []
    total_word_count = 0

    for i, item in enumerate(data):
        for field in fields:
            original_text = item.get(field)
            translated_text = item.get(f"{field}_{dest}")
            if len(original_text) > 4900: # 有的单段超长
                continue
            if original_text and not translated_text:
                word_count = count_words(original_text)
                if total_word_count + word_count > 4500:
                    try:
                        # 进行翻译
                        translated_chunk = batch_test_translate(to_translate, dest)
                        for (i, field), translated_text in zip(indices, translated_chunk):
                            data[i][f"{field}_{dest}"] = translated_text

                        # 翻译后立即写回文件
                        with open(json_path, 'w', encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=4)
                        print(f"Translations written to {json_path}")

                    except Exception as e:
                        print(f"Translation failed: {e}")
                        return

                    # 重置累积列表和计数
                    to_translate = []
                    indices = []
                    total_word_count = 0

                # 添加当前文本到待翻译列表
                to_translate.append(original_text)
                indices.append((i, field))
                total_word_count += word_count

    # 翻译剩余的文本
    if to_translate:
        try:
            translated_chunk = batch_test_translate(to_translate, dest)
            for (i, field), translated_text in zip(indices, translated_chunk):
                data[i][f"{field}_{dest}"] = translated_text

            # 翻译后立即写回文件
            with open(json_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            # print(f"Translations written to {json_path}")

        except Exception as e:
            print(f"Translation failed: {e}")

# 示例用法
dest = 'cn'
fields = ['instruction', 'input', 'output']
json_path = 'MedInstruct-52k_en_52000.json'

while True:
    try:
        json_to_csv(json_path, dest, *fields)
    except:
        t.wait(20)
