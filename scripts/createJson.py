import json

# Define the base URL for the images
base_url = "https://github.com/viktor436/orama/blob/main/resources/frame_"

# The number range for the image URLs
start_number = 0
end_number = 140

# Initialize the list to store the JSONL lines
jsonl_data = []

# Loop over the range of image numbers
for i in range(start_number, end_number + 1):
    # Format the image number with leading zeros
    image_number = f"{i:04d}"
    
    # Create the JSON structure for each message
    entry = {
        "messages": [
            {"role": "system", "content": "You are an assistant that identifies uncommon cheeses."},
            {"role": "user", "content": "What is this cheese?"},
            {"role": "user", "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"{base_url}{image_number}.jpg"
                    }
                }
            ]},
            {"role": "assistant", "content": "Danbo"}
        ]
    }
    
    # Convert the entry to a JSON string and append it to the list
    jsonl_data.append(json.dumps(entry))

# Define the output file path
output_file_path = 'C:/Users/vikto/Desktop/messages.jsonl'

# Write the JSONL data to the file
with open(output_file_path, 'w') as jsonl_file:
    for line in jsonl_data:
        jsonl_file.write(line + '\n')

# Return the path to the generated JSONL file
output_file_path
