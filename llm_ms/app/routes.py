from flask import request, jsonify
from app import app, db
import requests
import os

@app.route('/generate-description', methods=['POST'])
def generate_description():
    
    data = request.get_json()
    s3_url = data.get('url')

    if not s3_url:
        return jsonify({"error": "URL is required"}), 400
    
    description = call_openai_api(s3_url)

    return jsonify({"description": description}), 200

def call_openai_api(s3_url):
    openai_api_key = os.getenv('OPENAI_API_KEY')  
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json',
    }
    
    prompt = f"Generate a short description of an image hosted at this URL: {s3_url}. The image is a photograph."

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 60  
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return "Error generating description"
