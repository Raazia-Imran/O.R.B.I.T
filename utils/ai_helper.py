import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_API_TOKEN")

# --- SPEED OPTIMIZATION STRATEGY ---
# usin "Tiered Fallback":
# 1. Phi-3 Mini (Microsoft): The fastest robust model currently available free.
# 2. Gemma 2B (Google): Extremely lightweight backup.
# 3. Llama 3 8B (Meta): Reliable backup if others fail.
MODELS = [
    "microsoft/Phi-3-mini-4k-instruct",   # 🚀 SPEED KING (Primary)
    "google/gemma-2-2b-it",               # ⚡ FAST BACKUP
    "meta-llama/Meta-Llama-3-8B-Instruct" # 🛡️ STABLE BACKUP
]

def get_llm_response(prompt_text):
    """
    Tries multiple models until one succeeds.
    Optimized for HACKATHON SPEED (<3 seconds).
    """
    # 1. Strict "Speed" Instructions
    # We tell the AI to be brief. Generating 20 words takes 0.5s. Generating 100 takes 5s.
    system_instruction = (
        "You are a fast Business Analyst. "
        "Be extremely concise. "
        "Use bullet points. "
        "Max 50 words."
    )
    
    messages = [
        {"role": "user", "content": f"{system_instruction}\n\nTask: {prompt_text}"}
    ]

    # 2. Loop through fast models
    for model_id in MODELS:
        try:
            print(f"⚡ Attempting fast inference with: {model_id}...") # Keep this for your own sanity
            
            client = InferenceClient(model=model_id, token=HF_TOKEN)
            
            # 3. Speed Parameters
            response = client.chat_completion(
                messages, 
                max_tokens=150,   # Hard limit to stop long ramblings
                temperature=0.7,  # Slight creativity
                stream=False      # No streaming = simpler handling
            )
            
            # Success! Return immediately.
            return response.choices[0].message.content
            
        except Exception as e:
            # If this model fails, print error and immediately try the next one
            print(f"⚠️ {model_id} failed/busy: {e}")
            continue 
            
    # 4. Ultimate Fallback (If all APIs are down)
    return "⚠️ AI Traffic High. Please try again in 5 seconds."