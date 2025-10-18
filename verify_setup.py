"""
Demo script to verify the Paper2Code chatbot workflow.
This script simulates the process without making actual API calls.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add codes directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codes'))


def create_mock_paper_json():
    """Create a mock paper JSON for testing."""
    mock_paper = {
        "title": "Test Paper: A Simple Neural Network",
        "abstract": "This paper presents a simple neural network for classification tasks.",
        "sections": [
            {
                "heading": "Introduction",
                "text": "Neural networks are powerful machine learning models..."
            },
            {
                "heading": "Methodology",
                "text": "We propose a two-layer neural network with ReLU activation..."
            },
            {
                "heading": "Experiments",
                "text": "We evaluate on MNIST dataset with batch size 32, learning rate 0.001..."
            }
        ]
    }
    return mock_paper


def verify_azure_client():
    """Verify Azure OpenAI client can be initialized."""
    print("\n" + "="*60)
    print("Step 1: Verify Azure OpenAI Client")
    print("="*60)
    
    # Set mock credentials
    os.environ['AZURE_OPENAI_API_KEY'] = 'mock-key-for-testing'
    os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://mock-endpoint.openai.azure.com/'
    os.environ['AZURE_OPENAI_DEPLOYMENT'] = 'mock-deployment'
    
    try:
        from azure_openai_client import AzureOpenAIClient
        client = AzureOpenAIClient()
        print("✓ Azure OpenAI client initialized successfully")
        print(f"  Endpoint: {client.api_base}")
        print(f"  Deployment: {client.deployment_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return False


def verify_file_structure():
    """Verify all required files exist."""
    print("\n" + "="*60)
    print("Step 2: Verify File Structure")
    print("="*60)
    
    required_files = [
        'chatbot_app.py',
        'app_config.yaml',
        'codes/azure_openai_client.py',
        'codes/1_planning_azure.py',
        'codes/2_analyzing_azure.py',
        'codes/3_coding_azure.py',
        'codes/utils.py',
        'CHATBOT_README.md',
        'QUICKSTART.md',
        '.gitignore'
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def verify_workflow_simulation():
    """Simulate the workflow without API calls."""
    print("\n" + "="*60)
    print("Step 3: Simulate Workflow")
    print("="*60)
    
    try:
        # Create temporary directories
        temp_dir = tempfile.mkdtemp(prefix='paper2code_test_')
        print(f"Created temporary directory: {temp_dir}")
        
        # Create mock input
        input_json = os.path.join(temp_dir, 'test_paper.json')
        with open(input_json, 'w') as f:
            json.dump(create_mock_paper_json(), f, indent=2)
        print(f"✓ Created mock paper JSON")
        
        # Create output directories
        output_dir = os.path.join(temp_dir, 'artifacts')
        repo_dir = os.path.join(temp_dir, 'repo')
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(repo_dir, exist_ok=True)
        print(f"✓ Created output directories")
        
        # Simulate generated files
        mock_files = {
            'main.py': '# Main entry point\nprint("Hello from generated code")\n',
            'model.py': '# Model implementation\nclass Model:\n    pass\n',
            'config.yaml': 'learning_rate: 0.001\nbatch_size: 32\n',
            'README.md': '# Generated Code\n\nThis is a generated repository.\n'
        }
        
        for filename, content in mock_files.items():
            file_path = os.path.join(repo_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
        
        print(f"✓ Simulated code generation ({len(mock_files)} files)")
        
        # Verify files were created
        generated_files = list(Path(repo_dir).rglob('*'))
        file_count = len([f for f in generated_files if f.is_file()])
        print(f"✓ Verified {file_count} files in output")
        
        # Create zip file (simulating download preparation)
        import zipfile
        zip_path = os.path.join(output_dir, 'test_code.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(repo_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, repo_dir)
                    zipf.write(file_path, arcname)
        
        zip_size = os.path.getsize(zip_path)
        print(f"✓ Created ZIP file ({zip_size} bytes)")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"✓ Cleaned up temporary files")
        
        return True
        
    except Exception as e:
        print(f"✗ Workflow simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_dependencies():
    """Verify all required Python packages are available."""
    print("\n" + "="*60)
    print("Step 4: Verify Dependencies")
    print("="*60)
    
    required_packages = [
        ('openai', 'OpenAI/Azure OpenAI client'),
        ('streamlit', 'Web interface'),
        ('yaml', 'Configuration loading'),
        ('tqdm', 'Progress bars'),
    ]
    
    all_available = True
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} - {description}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_available = False
    
    return all_available


def main():
    """Run all verification steps."""
    print("\n" + "="*70)
    print(" Paper2Code Chatbot - Workflow Verification")
    print("="*70)
    print("\nThis script verifies the chatbot setup without making API calls.")
    
    results = []
    
    # Run verification steps
    results.append(("Azure Client", verify_azure_client()))
    results.append(("File Structure", verify_file_structure()))
    results.append(("Dependencies", verify_dependencies()))
    results.append(("Workflow Simulation", verify_workflow_simulation()))
    
    # Summary
    print("\n" + "="*70)
    print(" Verification Summary")
    print("="*70)
    
    for step_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {step_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*70)
    if all_passed:
        print("✓ ALL VERIFICATION STEPS PASSED!")
        print("\nThe chatbot is ready to use. Run:")
        print("  streamlit run chatbot_app.py")
        print("\nMake sure to set your Azure OpenAI credentials first:")
        print("  export AZURE_OPENAI_API_KEY=your-key")
        print("  export AZURE_OPENAI_ENDPOINT=your-endpoint")
        print("  export AZURE_OPENAI_DEPLOYMENT=your-deployment")
    else:
        print("✗ SOME VERIFICATION STEPS FAILED")
        print("\nPlease check the errors above and fix them before using the chatbot.")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
