"""
Azure OpenAI API wrapper for Paper2Code application.
Provides compatibility layer to use Azure OpenAI instead of standard OpenAI API.
"""

import os
from openai import AzureOpenAI
import json


class AzureOpenAIClient:
    """Wrapper class for Azure OpenAI API that mimics OpenAI client interface."""
    
    def __init__(self, api_key=None, api_base=None, api_version=None, deployment_name=None):
        """
        Initialize Azure OpenAI client.
        
        Args:
            api_key: Azure OpenAI API key (falls back to AZURE_OPENAI_API_KEY env var)
            api_base: Azure OpenAI endpoint (falls back to AZURE_OPENAI_ENDPOINT env var)
            api_version: API version (falls back to AZURE_OPENAI_API_VERSION env var)
            deployment_name: Deployment name (falls back to AZURE_OPENAI_DEPLOYMENT env var)
        """
        self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        self.api_base = api_base or os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.api_version = api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment_name = deployment_name or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        
        if not self.api_key:
            raise ValueError("Azure OpenAI API key is required. Set AZURE_OPENAI_API_KEY environment variable.")
        if not self.api_base:
            raise ValueError("Azure OpenAI endpoint is required. Set AZURE_OPENAI_ENDPOINT environment variable.")
        if not self.deployment_name:
            raise ValueError("Azure OpenAI deployment name is required. Set AZURE_OPENAI_DEPLOYMENT environment variable.")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base
        )
        
        # Create a chat completions wrapper
        self.chat = ChatCompletions(self.client, self.deployment_name)


class ChatCompletions:
    """Chat completions wrapper to mimic OpenAI API structure."""
    
    def __init__(self, client, deployment_name):
        self.client = client
        self.deployment_name = deployment_name
        self.completions = self
    
    def create(self, model=None, messages=None, reasoning_effort=None, **kwargs):
        """
        Create a chat completion.
        
        Args:
            model: Model name (ignored for Azure, uses deployment_name instead)
            messages: List of message dictionaries
            reasoning_effort: Reasoning effort level (for o3-mini models)
            **kwargs: Additional arguments
            
        Returns:
            Completion response object
        """
        # For Azure OpenAI, we use the deployment name instead of model name
        params = {
            "model": self.deployment_name,
            "messages": messages,
            **kwargs
        }
        
        # Add reasoning_effort if provided (for o3-mini models)
        if reasoning_effort:
            params["reasoning_effort"] = reasoning_effort
        
        response = self.client.chat.completions.create(**params)
        return response


def get_azure_client():
    """
    Factory function to get Azure OpenAI client.
    
    Returns:
        AzureOpenAIClient instance
    """
    return AzureOpenAIClient()


def convert_to_azure_compatible(code_module):
    """
    Helper function to patch existing code to use Azure OpenAI.
    This can be used to make minimal changes to existing scripts.
    
    Args:
        code_module: Module object to patch
    """
    # This is a placeholder for potential future use
    pass
