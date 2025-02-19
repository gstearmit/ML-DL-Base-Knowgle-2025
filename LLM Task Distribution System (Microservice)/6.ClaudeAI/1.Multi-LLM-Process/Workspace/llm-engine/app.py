# app.py
import os
import logging
from flask import Flask, request, jsonify
import openai
import anthropic
from google.cloud import aiplatform

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure API keys
openai.api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        model_name = data.get('model', 'gpt-4')
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
            
        response = process_with_model(model_name, prompt)
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

def process_with_model(model_name, prompt):
    if model_name.startswith('gpt'):
        return process_with_openai(model_name, prompt)
    elif model_name.startswith('claude'):
        return process_with_anthropic(prompt)
    elif model_name.startswith('gemini'):
        return process_with_google(prompt)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def process_with_openai(model_name, prompt):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2048
    )
    return {
        "model": model_name,
        "response": response.choices[0].message.content,
        "provider": "openai"
    }

def process_with_anthropic(prompt):
    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        temperature=0.7,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return {
        "model": "claude-3",
        "response": response.content,
        "provider": "anthropic"
    }

def process_with_google(prompt):
    client = aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    response = client.generate_text(
        model_name="gemini-pro",
        prompt=prompt,
        max_output_tokens=2048,
        temperature=0.7
    )
    return {
        "model": "gemini-pro",
        "response": response.text,
        "provider": "google"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)