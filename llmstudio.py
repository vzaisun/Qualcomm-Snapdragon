from openai import OpenAI

class LMStudioClient:
    def __init__(self, config):
        
        self.api_key = config.get("LM_STUDIO_API_KEY", "lmstudio")
        self.base_url = config.get("LM_STUDIO_URL", "http://localhost:1234/v1")
        
        
        self.model = config.get("MODEL_NAME", "default_model_name") # Replace "default_model_name" as needed

        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, messages, temperature=0.7):
       
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        # Access the first choice's message content
        return resp.choices[0].message.content

def setup_la_studio_client(config):
    
    return LMStudioClient(config)


if __name__ == '__main__':
    
    example_config = {
        "LM_STUDIO_API_KEY": "lmstudio", # Default value, can be omitted or changed
        "LM_STUDIO_URL": "http://localhost:1234/v1", # Default value, can be omitted or changed
        "MODEL_NAME": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF" # Example model name
    }

    #
    client = setup_la_studio_client(example_config)

    # Example chat interaction
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    try:
        response = client.chat(messages)
        print(f"Assistant: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")

