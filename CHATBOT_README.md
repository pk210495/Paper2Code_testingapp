# Paper2Code Chatbot Application

A web-based chatbot interface for the Paper2Code system, allowing users to upload research papers and receive generated code implementations.

## Features

- 📤 **Upload Research Papers**: Upload papers in JSON format (preprocessed with s2orc-doc2json)
- 🤖 **AI-Powered Code Generation**: Uses Azure OpenAI to generate complete code repositories
- 📦 **Download Generated Code**: Download all generated files as a ZIP archive
- 🎯 **Three-Stage Pipeline**: Planning → Analysis → Code Generation
- 💬 **Interactive Web Interface**: Built with Streamlit for easy use

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

Set the following environment variables:

```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
```

Alternatively, create a `.env` file:

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

### 3. Run the Application

```bash
streamlit run chatbot_app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Configure Credentials**: Ensure Azure OpenAI credentials are set in environment variables
2. **Upload Paper**: Upload a research paper in JSON format
3. **Enter Paper Name**: Provide a name for the paper
4. **Generate Code**: Click "Generate Code" to start the process
5. **Download**: Once complete, download the generated code as a ZIP file

## Architecture

The chatbot integrates three main components:

1. **Planning Stage** (`1_planning_azure.py`): Creates implementation strategy
2. **Analysis Stage** (`2_analyzing_azure.py`): Performs detailed logic analysis
3. **Coding Stage** (`3_coding_azure.py`): Generates complete code repository

## Azure OpenAI Integration

The application uses Azure OpenAI API through a compatibility layer (`azure_openai_client.py`) that mimics the standard OpenAI client interface. This allows seamless integration with existing Paper2Code code.

### Supported Models

- gpt-4
- gpt-4-turbo
- gpt-35-turbo
- Custom Azure deployments

## File Structure

```
Paper2Code_testingapp/
├── chatbot_app.py              # Main Streamlit application
├── app_config.yaml             # Application configuration
├── codes/
│   ├── azure_openai_client.py  # Azure OpenAI wrapper
│   ├── 1_planning_azure.py     # Planning stage (Azure)
│   ├── 2_analyzing_azure.py    # Analysis stage (Azure)
│   ├── 3_coding_azure.py       # Coding stage (Azure)
│   └── utils.py                # Utility functions
├── outputs/                    # Generated outputs (git-ignored)
└── temp_uploads/               # Temporary uploads (git-ignored)
```

## Cost Considerations

- The code generation process makes multiple LLM API calls
- Costs depend on the model used and paper complexity
- Typical cost: $0.50-$2.00 per paper with gpt-4
- Monitor your Azure OpenAI usage dashboard

## Troubleshooting

### Missing Environment Variables

If you see an error about missing environment variables:
- Ensure all required Azure OpenAI variables are set
- Check spelling and formatting of variable names
- Restart the application after setting variables

### PDF Processing

The current version requires pre-processed JSON files. To process PDFs:

1. Install and run s2orc-doc2json service
2. Convert PDF to JSON using the process described in main README.md
3. Upload the generated JSON file

## Notes

- Generated code files are NOT displayed in the chat interface
- All outputs are made available via downloadable ZIP files
- Processing time varies based on paper complexity (typically 5-15 minutes)
- The application creates timestamped output directories to avoid conflicts

## Support

For issues or questions, please refer to the main [Paper2Code repository](https://github.com/pk210495/Paper2Code_testingapp).
