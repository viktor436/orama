import json
import pandas as pd

def find_match(url,first_json_list):
    sec = url.split("_")[1].split(".")[0]
    for i in first_json_list:
        first = i["pic"].split("_")[1].split(".")[0]
        if first == sec:
            return i["text"]
    return "NaN"

with open('C:/Users/vikto/Desktop/results.json', 'r') as f:
    first_json_list = json.load(f)

second_jsonl = []
with open('C:/Users/vikto/Desktop/messages.jsonl', 'r') as f:
    for line in f:
        second_jsonl.append(json.loads(line))

def map_text_to_jsonl_corrected(first_json_list, second_jsonl):
    print(second_jsonl[0]['messages'])
    for j,message_set in enumerate(second_jsonl):
        for j2,m in  enumerate(message_set['messages']):
            if isinstance(m['content'],list):
                content = m['content'][0]["image_url"]["url"]
                print(content)
                second_jsonl[j]['messages'][3]["content"] = find_match(content,first_json_list)        
    return second_jsonl

updated_jsonl = map_text_to_jsonl_corrected(first_json_list, second_jsonl)

output_file_path = 'C:/Users/vikto/Desktop/train2.jsonl'
with open(output_file_path, 'w') as f:
    for item in updated_jsonl:
        f.write(json.dumps(item) + '\n')

output_file_path
