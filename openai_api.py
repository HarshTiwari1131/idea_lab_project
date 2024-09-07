import openai
import json
import requests

with open('config.json') as config_file:
    config = json.load(config_file)
openai.api_key = config['openai_api_key']

def generate_chat_response(messages, model="gpt-4", temperature=0.7):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200:
        return response_json["choices"][0]["message"]["content"]
    else:
        print("Error:", response_json)
        return None
