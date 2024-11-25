import streamlit as st
import requests
import json



LLM_MAPPING = {
    "healthcare": "microsoft/phi-3-medium-128k-instruct:free",
    "mathematics": "meta-llama/llama-3.1-8b-instruct",
    "programming": "huggingfaceh4/zephyr-7b-beta:free",
    "creative writing": "mistralai/mistral-7b-instruct:free",
    "science": "qwen/qwen-2-7b-instruct:free",
    "reasoning": "meta-llama/llama-3.1-8b-instruct",
    "education": "meta-llama/llama-3.1-405b-instruct:free",  
    "general knowledge": "huggingfaceh4/zephyr-7b-beta:free",  
    "travel": "mistralai/mistral-7b-instruct:free",  
    "entertainment": "qwen/qwen-2-7b-instruct:free",
    "finance": "microsoft/phi-3-medium-128k-instruct:free",
    "technology": "google/gemma-2-9b-it:free",
    "shopping": "huggingfaceh4/zephyr-7b-beta:free",
    "history": "meta-llama/llama-3.1-8b-instruct",
    "geography": "qwen/qwen-2-7b-instruct:free",
    "art": "mistralai/mistral-7b-instruct:free",
    "music": "mistralai/mistral-7b-instruct:free",
    "sports": "huggingfaceh4/zephyr-7b-beta:free",
    "fitness": "meta-llama/llama-3.1-70b-instruct:free",
    "food": "mistralai/mistral-7b-instruct:free",
    "childcare": "huggingfaceh4/zephyr-7b-beta:free",
    "language": "meta-llama/llama-3.2-3b-instruct:free",
    "business": "microsoft/phi-3-medium-128k-instruct:free",
    "marketing": "huggingfaceh4/zephyr-7b-beta:free",
    "job": "meta-llama/llama-3.1-405b-instruct:free",
    "diy": "huggingfaceh4/zephyr-7b-beta:free",
    "dating": "meta-llama/llama-3.1-70b-instruct:free",
    "psychology": "meta-llama/llama-3.1-405b-instruct",
    "law": "microsoft/phi-3-medium-128k-instruct:free",
    "environment": "meta-llama/llama-3.1-405b-instruct:free",
    "astronomy": "qwen/qwen-2-7b-instruct:free",
    "fashion": "mistralai/mistral-7b-instruct:free",
    "gaming": "qwen/qwen-2-7b-instruct:free",
    "mythology": "mistralai/mistral-7b-instruct:free",
    "religion": "mistralai/mistral-7b-instruct:free",
    "pets": "meta-llama/llama-3.1-70b-instruct:free"
}

OPENROUTER_API_KEY = "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"
YOUR_APP_NAME = "AiGator"  

def detect_intent(query):
    data = {
        "model": "google/gemma-2-9b-it:free",  
        "messages": [
            {
                "role": "user",
                "content": f"""Classify the intent i.e the domain of the user query from this list: 
                (healthcare, mathematics, programming, creative writing, science, reasoning, education, 
                general knowledge, travel, entertainment, finance, technology, shopping, history, 
                geography, art, music, sports, fitness, food, childcare, language, business, 
                marketing, job, diy, dating, psychology, law, environment, astronomy, fashion, 
                gaming, mythology, religion, pets). 
                Reply with only one word from the given list above without any special characters: '{query}'"""
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        intent = response_data["choices"][0]["message"]["content"].strip().lower()
        intent = intent.strip(".:;")  
        return intent
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def fetch_response(query, llm_name):
    data = {
        "model": llm_name,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        response_data = response.json()
        print("response data is; ", response_data)
        if response.status_code == 200:
            return response_data["choices"][0]["message"]["content"].strip()
        elif response.status_code == 429:  
            return None            
        else:
            print("response-data", response_data)
            return None
        
    except Exception as e: 
        print(e)

st.title("AiGator - Smart Router")

user_query = st.text_input("Enter your query:")

if st.button("Ask"):
    if user_query:
        with st.spinner("Detecting intent..."):
            try:
                intent = detect_intent(user_query)
                intent = intent.strip(".:,")  
                st.success(f"Detected Intent: {intent.capitalize()}")

                selected_llm = LLM_MAPPING.get(intent)
                if not selected_llm:
                    st.error(f"No LLM found for intent: {intent}")
                else:
                    st.info(f"Using Model: {selected_llm}")

                    with st.spinner("Fetching response from LLM..."):
                        response = fetch_response(user_query, selected_llm)
                        st.write("### Response")
                        if response:
                            st.write(response)
                        else:
                            st.error("Rate Limit Exceeded try again in a minute")

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("Please enter a query.")
