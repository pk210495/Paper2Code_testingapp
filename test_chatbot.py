"""
Simple test script to validate the Azure OpenAI client setup.
This script checks if the Azure OpenAI client can be initialized properly.
"""

import os
import sys

# Add codes directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codes'))


def test_azure_client_initialization():
    """Test that Azure OpenAI client can be initialized with environment variables."""
    print("Testing Azure OpenAI Client Initialization...")
    
    # Check for required environment variables
    required_vars = {
        'AZURE_OPENAI_API_KEY': 'test-key-12345',
        'AZURE_OPENAI_ENDPOINT': 'https://test-resource.openai.azure.com/',
        'AZURE_OPENAI_DEPLOYMENT': 'test-deployment'
    }
    
    # Set test environment variables
    for var, value in required_vars.items():
        os.environ[var] = value
    
    try:
        from azure_openai_client import AzureOpenAIClient
        
        # Try to initialize the client
        client = AzureOpenAIClient()
        
        print("✓ Azure OpenAI client initialized successfully")
        print(f"  - Endpoint: {client.api_base}")
        print(f"  - Deployment: {client.deployment_name}")
        print(f"  - API Version: {client.api_version}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to initialize Azure OpenAI client: {e}")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("\nTesting Module Imports...")
    
    modules = [
        'azure_openai_client',
        'utils',
    ]
    
    all_success = True
    for module in modules:
        try:
            __import__(module)
            print(f"✓ Successfully imported {module}")
        except Exception as e:
            print(f"✗ Failed to import {module}: {e}")
            all_success = False
    
    return all_success


def test_config_loading():
    """Test configuration file loading."""
    print("\nTesting Configuration Loading...")
    
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), 'app_config.yaml')
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print("✓ Configuration file loaded successfully")
        print(f"  - App title: {config.get('app', {}).get('title')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Paper2Code Chatbot - Component Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Config Loading", test_config_loading()))
    results.append(("Azure Client Init", test_azure_client_initialization()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
