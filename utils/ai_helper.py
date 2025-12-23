import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN")

# LIST OF MODELS TO TRY (If one fails, we try the next)
# These are currently the most reliable free "Chat" models
MODELS = [
    "Qwen/Qwen2.5-72B-Instruct",         # Best performance (Top Tier)
    "meta-llama/Llama-3.2-3B-Instruct",  # Extremely fast (Speed Tier)
    "google/gemma-2-2b-it"               # Google's lightweight model (Backup)
]

def get_llm_response(prompt_text):
    """
    Tries multiple models until one succeeds.
    """
    # 1. Prepare the chat message
    messages = [
        {"role": "user", "content": f"You are a business analyst. Be concise. Answer in 1 sentence.\n\nTask: {prompt_text}"}
    ]

    # 2. Loop through the models
    for model_id in MODELS:
        try:
            print(f"Trying model: {model_id}...") # Debug print for your terminal
            client = InferenceClient(model=model_id, token=HF_TOKEN)
            
            response = client.chat_completion(
                messages, 
                max_tokens=100, 
                temperature=0.5
            )
            
            # If successful, return the text immediately
            return response.choices[0].message.content
            
        except Exception as e:
            # If this model fails, print error and loop to the next one
            print(f"Model {model_id} failed: {e}")
            continue # Try next model
            
    # 3. If ALL models fail, return a safe fallback message
    return "⚠️ AI Service Busy: Please try again in 1 minute."