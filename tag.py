import tagui as t
import pyperclip as clip
import json
import urllib.parse
import sys 
if sys.platform == 'darwin':
    MODIFIER = '[cmd]'
elif sys.platform == 'linux':
    MODIFIER = '[ctrl]'
else:
    raise NotImplementedError(f"{sys.platform} not implmented!")

def translate(input):
    t.init(visual_automation=True)
    encoded_text = urllib.parse.quote(input, safe="")
    # url = f'https://translate.google.com/?sl=zh-CN&tl=en&text={encoded_text}&op=translate'
    url = f'https://translate.google.com/?sl=zh-CN&tl=en&text=%3Ctag%3E&op=translate'
    t.url(url)
    t.keyboard('[esc]')
    
    clip.copy(f"{input}<tag>")
    t.click('<tag>')
    t.keyboard(f'{MODIFIER}a')
    t.keyboard(f'{MODIFIER}v')
    # t.click('Copy translation')
    t.click('复制译文')
    t.close()
    while clip.paste() == input:
        pass

    print(f"result: {clip.paste().replace('<tag>','')}")
    return clip.paste().replace('<tag>',"")


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
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file at {json_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file at {json_path} is not a valid JSON.")
        return

    # 遍历数据中的每个项目
    for item in data:
        for field in fields:
            original_text = item.get(field)
            translated_text = item.get(f"{field}_{dest}")

            if not translated_text:  # 检查是否已经翻译
                try:
                    # 进行翻译
                    print(f"translating...{original_text}", end=" ")
                    translated_text = translate(original_text)
                    # print(translated_text)
                    item[f"{field}_{dest}"] = translated_text  # 写入翻译结果

                    # 翻译后立即写回文件
                    with open(json_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Translation failed for {field}: {e}")

# 示例用法

dest = 'en'
fields = ['query', 'answer']
json_path = 'merged_data.json'
json_to_csv(json_path, dest, *fields)