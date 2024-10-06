import json

base_url = "https://github.com/viktor436/orama/blob/main/resources/frame_"

start_number = 0
end_number = 259

jsonl_data = []

for i in range(start_number, end_number + 1):
    image_number = f"{i:04d}"   
    entry = {
        "messages": [
            {"role": "system", "content": "You are an assistant that identifies uncommon cheeses."},
            {"role": "user", "content": "What is this cheese?"},
            {"role": "user", "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{base_url}{image_number}.jpeg"
                    }
                }
            ]},
            {"role": "assistant", "content": "Danbo"}
        ]
    }
    
    jsonl_data.append(json.dumps(entry))

output_file_path = 'C:/Users/vikto/Desktop/messages.jsonl'

with open(output_file_path, 'w') as jsonl_file:
    for line in jsonl_data:
        jsonl_file.write(line + '\n')

output_file_path
