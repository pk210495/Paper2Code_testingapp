# Quick Start Guide - Paper2Code Chatbot

This guide will help you get started with the Paper2Code Chatbot application in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access with a deployed model
- A research paper in JSON format (or ability to convert PDF to JSON)

## Step 1: Install Dependencies

```bash
# Clone or navigate to the repository
cd Paper2Code_testingapp

# Install required packages
pip install -r requirements.txt
```

## Step 2: Configure Azure OpenAI

You need to set up three environment variables:

```bash
export AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
```

**Alternative**: Create a `.env` file (copy from `.env.template`):

```bash
cp .env.template .env
# Edit .env with your credentials
```

### Where to Find These Values

1. **API Key**: Azure Portal → Your OpenAI Resource → Keys and Endpoint → Key 1
2. **Endpoint**: Azure Portal → Your OpenAI Resource → Keys and Endpoint → Endpoint
3. **Deployment Name**: Azure Portal → Your OpenAI Resource → Model deployments → Your deployment name

## Step 3: Prepare Your Paper

The chatbot requires papers in JSON format (preprocessed with s2orc-doc2json).

### If you have a JSON file:
- Use it directly!

### If you have a PDF:
1. Set up s2orc-doc2json (see main README.md)
2. Convert PDF to JSON
3. Upload the generated JSON file

**Example JSON files** are available in the `examples/` directory.

## Step 4: Run the Chatbot

```bash
streamlit run chatbot_app.py
```

The application will open in your browser at `http://localhost:8501`

## Step 5: Generate Code

1. **Upload Paper**: Click "Browse files" and select your JSON file
2. **Enter Name**: Provide a descriptive name for your paper
3. **Select Model**: Choose your Azure OpenAI deployment model
4. **Generate**: Click "🚀 Generate Code"
5. **Wait**: The process takes 5-15 minutes depending on paper complexity
6. **Download**: Click "⬇️ Download Code" to get your generated repository

## What You'll Get

A complete code repository containing:
- Implementation of the paper's methodology
- Dataset loaders and preprocessing
- Model architecture
- Training scripts
- Evaluation code
- Configuration files
- Documentation

All packaged in a downloadable ZIP file!

## Example Usage

Try it with the included Transformer paper example:

```bash
# 1. Start the app
streamlit run chatbot_app.py

# 2. Upload this file:
examples/Transformer_cleaned.json

# 3. Enter name: Transformer

# 4. Click Generate Code

# 5. Wait for completion and download!
```

## Troubleshooting

### "Missing required environment variables"
- Ensure all three Azure OpenAI variables are set
- Check for typos in variable names
- Restart the terminal/application after setting variables

### "API call failed"
- Verify your Azure OpenAI credentials
- Check that your deployment is active
- Ensure you have sufficient quota

### "Processing stage failed"
- Check the error message in the expandable section
- Verify the JSON file format is correct
- Ensure the model supports the required features

## Cost Estimation

Approximate costs per paper (with gpt-4):
- Simple paper: $0.50 - $1.00
- Medium complexity: $1.00 - $2.00
- Complex paper: $2.00 - $5.00

Monitor your usage in the Azure Portal.

## Next Steps

- Read the full [CHATBOT_README.md](CHATBOT_README.md) for detailed information
- Check the main [README.md](README.md) for command-line usage
- Explore the generated code and customize as needed

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the detailed documentation
3. Check Azure OpenAI service status
4. Raise an issue on the repository

Happy coding! 🚀
