import yaml
# Assuming src.servers.lmstudio contains the function setup_lm_studio_client
from src.servers.lmstudio import setup_lm_studio_client 

class ModelInterface:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        
        self.model_provider_name = self.config.get('MODEL_PROVIDER', None)
        self.client = None  
        self._setup_client()

    def _setup_client(self):
        if not self.model_provider_name:
            raise ValueError('MODEL_PROVIDER is not set in config')
        
        
        if self.model_provider_name.lower() == 'lmstudio':
        
            self.client = setup_lm_studio_client(self.config)
            return self.client
        else:
            raise ValueError(f'Unsupported model provider: {self.model_provider_name}')

    
    def chat_completion(self, messages, temperature=0.7):
        if not self.client:
            raise ValueError('Model client is not set up')
        
        
        if self.model_provider_name.lower() == 'lmstudio':
            return self.client.chat(messages, temperature=temperature)
        else:
            # This part is technically redundant if _setup_client is called in __init__
            raise ValueError(f'Unsupported model provider: {self.model_provider_name}')
