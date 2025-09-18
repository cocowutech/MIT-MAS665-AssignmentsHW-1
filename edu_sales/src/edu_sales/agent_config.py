# TO DO LIST - not a completed file, need to be updated
# pip install crewai crewai-tools pydantic requests langchain_openai langchain_google_genai langchain_anthropic

# Centralized configuration for all supported LLM providers
from typing import Dict
import os
import requests

class AgentConfig:
    def __init__(self):
        self.PROVIDER_CONFIG: Dict[str, Dict[str, str]] = {
            'openai': {
                'api_key_env': 'OPENAI_API_KEY',
                'base_url_env': 'OPENAI_API_BASE',
                'model_env': 'OPENAI_MODEL',
                'default_endpoint': 'https://api.openai.com/v1',
            },
            'gemini': {
                'api_key_env': 'GEMINI_API_KEY',
                'base_url_env': 'GEMINI_API_BASE',
                'model_env': 'GEMINI_MODEL',
                'default_endpoint': 'https://generativelanguage.googleapis.com/v1',
            },
            'anthropic': {
                'api_key_env': 'ANTHROPIC_API_KEY',
                'base_url_env': 'ANTHROPIC_API_BASE',
                'model_env': 'ANTHROPIC_MODEL',
                'default_endpoint': 'https://api.anthropic.com/v1',
            },
            'openrouter': {
                'api_key_env': 'OPENROUTER_API_KEY',
                'base_url_env': 'OPENROUTER_API_BASE',
                'model_env': 'OPENROUTER_MODEL',
                'default_endpoint': 'https://openrouter.ai/api/v1',
            },
        }

    @staticmethod
    def _check_endpoint(url: str, api_key: str) -> None:
        """
        Performs a lightweight endpoint check using the requests library.
        Raises an exception for non-2xx status codes or connection errors.
        """
        try:
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"LLM endpoint check failed: {e}")

    @staticmethod
    def get_llm_config() -> Dict[str, str]:
        """
        Dynamically determines and validates LLM configuration from environment variables.
        
        Returns:
            A dictionary containing the validated provider, api_key, base_url, and model.
        Raises:
            RuntimeError: If essential environment variables are missing or a provider is unsupported.
        """
        llm_provider = os.getenv('LLM_PROVIDER', '').lower()
        
        config: Dict[str, str] = {}
        
        if llm_provider and llm_provider in PROVIDER_CONFIG:
            # Use provider-specific configuration
            provider_data = PROVIDER_CONFIG[llm_provider]
            config['provider'] = llm_provider
            config['api_key'] = os.getenv(provider_data['api_key_env'], '')
            config['base_url'] = os.getenv(provider_data['base_url_env'], '') or provider_data['default_endpoint']
            config['model'] = os.getenv(provider_data['model_env'], '')
        else:
            # Fallback to general LLM environment variables
            config['provider'] = 'auto'
            config['api_key'] = os.getenv('LLM_API_KEY', '') or os.getenv('OPENAI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
            config['base_url'] = os.getenv('LLM_BASE_URL', '')
            config['model'] = os.getenv('LLM_MODEL', '')
            
            # In 'auto' mode, we need to infer the provider to get a default base_url
            if not config['base_url']:
                for provider, data in PROVIDER_CONFIG.items():
                    if os.getenv(data['api_key_env']):
                        config['base_url'] = data['default_endpoint']
                        break

        # Validate essential configuration
        if not config['api_key']:
            raise RuntimeError('Missing LLM API key. Set one of the following environment variables: LLM_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, etc.')
        if not config['model']:
            raise RuntimeError('Missing LLM model. Set one of the following environment variables: LLM_MODEL, OPENAI_MODEL, GEMINI_MODEL, etc.')
        if not config['base_url']:
            raise RuntimeError('Could not determine a base URL for the LLM. Please set LLM_BASE_URL.')

        print(f"Using provider: {config['provider']} | model: {config['model']}")
        
        _check_endpoint(config['base_url'], config['api_key'])
        
        return config

# Example of how to use the function
if __name__ == '__main__':
    try:
        llm_config = AgentConfig().get_llm_config()
        print("LLM Configuration loaded successfully.")
    except RuntimeError as e:
        print(f"Error: {e}")
