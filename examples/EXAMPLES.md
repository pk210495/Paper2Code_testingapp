# Example: Using the Paper2Code Chatbot

This directory contains example files to help you get started with the Paper2Code chatbot.

## Available Examples

### 1. Transformer Paper
- **File**: `Transformer_cleaned.json`
- **Source**: "Attention Is All You Need" (Vaswani et al., 2017)
- **Description**: The seminal Transformer architecture paper
- **Estimated Time**: 10-15 minutes
- **Estimated Cost**: $0.50-$1.50 (with gpt-4)

## How to Use Examples

### Using the Web Chatbot

1. **Start the chatbot**:
   ```bash
   streamlit run chatbot_app.py
   ```

2. **Upload the example file**:
   - Click "Browse files"
   - Select `examples/Transformer_cleaned.json`

3. **Configure**:
   - Paper Name: `Transformer`
   - Model: Select your Azure OpenAI deployment

4. **Generate**:
   - Click "🚀 Generate Code"
   - Wait for the three stages to complete
   - Download the ZIP file

### Using Command Line (OpenAI)

```bash
cd scripts
bash run.sh
```

The output will be in `outputs/Transformer_repo/`

## What You'll Get

After processing, you'll receive a complete code repository with:

```
Transformer_repo/
├── config.yaml              # Configuration with hyperparameters
├── main.py                  # Main entry point
├── model.py                 # Transformer model implementation
├── dataset_loader.py        # Data loading utilities
├── trainer.py               # Training loop
├── evaluation.py            # Evaluation metrics
└── README.md                # Documentation
```

## Expected Output Examples

### 1. Planning Stage Output
- Overall implementation plan
- Architecture design
- Task breakdown
- Configuration template

### 2. Analysis Stage Output
- Detailed logic analysis for each component
- Dependency analysis
- Implementation notes

### 3. Coding Stage Output
- Complete Python implementation
- Well-documented code
- Modular structure
- Following best practices

## Tips for Best Results

### Paper Preparation
- Use cleaned JSON format (remove unnecessary metadata)
- Ensure the paper has clear methodology and experimental sections
- Papers with detailed hyperparameters work better

### Model Selection
- **gpt-4**: Best quality, higher cost
- **gpt-4-turbo**: Good balance of speed and quality
- **gpt-35-turbo**: Faster, lower cost, may need more guidance

### Cost Management
- Start with simpler papers to understand the process
- Use smaller models for initial testing
- Monitor Azure OpenAI usage dashboard
- Set spending alerts in Azure

## Troubleshooting Examples

### Example Not Processing?

1. **Check JSON Format**:
   ```bash
   python -c "import json; json.load(open('examples/Transformer_cleaned.json'))"
   ```

2. **Verify Azure Credentials**:
   ```bash
   python verify_setup.py
   ```

3. **Check Logs**:
   - Look for error messages in the Streamlit interface
   - Check `outputs/*/cost_info.log` for API errors

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Azure OpenAI credentials not set"**
```bash
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_DEPLOYMENT="your-deployment"
```

**"Processing failed at planning stage"**
- Check your Azure OpenAI deployment is active
- Verify you have sufficient quota
- Try a simpler paper first

## Next Steps

After successfully processing an example:

1. **Review the Generated Code**:
   - Examine the implementation approach
   - Check if it matches the paper's methodology
   - Verify configuration values

2. **Customize as Needed**:
   - Adjust hyperparameters in `config.yaml`
   - Add dataset-specific code
   - Modify for your use case

3. **Run the Code**:
   - Install dependencies from generated requirements
   - Prepare your dataset
   - Execute the training script

4. **Try Your Own Paper**:
   - Convert your paper to JSON
   - Upload and process
   - Compare results

## Additional Resources

- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [CHATBOT_README.md](../CHATBOT_README.md) - Detailed chatbot documentation
- [README.md](../README.md) - Main project documentation

## Feedback

If you encounter issues or have suggestions for improving the examples, please open an issue on the repository.
