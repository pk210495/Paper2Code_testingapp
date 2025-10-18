"""
Paper2Code Chatbot Application
A web interface for uploading research papers and generating code implementations.
"""

import streamlit as st
import os
import sys
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
import yaml

# Add codes directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'codes'))

# Import paper2code modules
from codes.azure_openai_client import AzureOpenAIClient
from codes import utils


# Page configuration
st.set_page_config(
    page_title="Paper2Code Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_config():
    """Load application configuration."""
    config_path = os.path.join(os.path.dirname(__file__), 'app_config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def initialize_session_state():
    """Initialize session state variables."""
    if 'processing_stage' not in st.session_state:
        st.session_state.processing_stage = None
    if 'output_dir' not in st.session_state:
        st.session_state.output_dir = None
    if 'paper_name' not in st.session_state:
        st.session_state.paper_name = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []


def validate_azure_credentials():
    """Validate Azure OpenAI credentials."""
    required_vars = ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT']
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        st.error(f"Missing required environment variables: {', '.join(missing)}")
        st.info("""
        Please set the following environment variables:
        - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
        - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint (e.g., https://your-resource.openai.azure.com/)
        - AZURE_OPENAI_DEPLOYMENT: Your deployment name
        """)
        return False
    return True


def process_pdf_to_json(pdf_path, output_json_path):
    """
    Process PDF to JSON format.
    Note: This requires the s2orc-doc2json tool to be running.
    For simplicity, we'll skip this step and ask users to provide JSON.
    """
    # For now, we'll just indicate that this would normally process the PDF
    st.warning("PDF processing requires s2orc-doc2json service. Please upload pre-processed JSON file.")
    return None


def run_planning_stage(paper_name, pdf_json_path, output_dir, gpt_version="gpt-4"):
    """Run the planning stage of Paper2Code."""
    import subprocess
    
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'codes', '1_planning_azure.py'),
        '--paper_name', paper_name,
        '--gpt_version', gpt_version,
        '--pdf_json_path', pdf_json_path,
        '--output_dir', output_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def run_analysis_stage(paper_name, pdf_json_path, output_dir, gpt_version="gpt-4"):
    """Run the analysis stage of Paper2Code."""
    import subprocess
    
    # First extract config
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'codes', '1.1_extract_config.py'),
        '--paper_name', paper_name,
        '--output_dir', output_dir
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    
    # Run analysis
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'codes', '2_analyzing_azure.py'),
        '--paper_name', paper_name,
        '--gpt_version', gpt_version,
        '--pdf_json_path', pdf_json_path,
        '--output_dir', output_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def run_coding_stage(paper_name, pdf_json_path, output_dir, output_repo_dir, gpt_version="gpt-4"):
    """Run the coding stage of Paper2Code."""
    import subprocess
    
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'codes', '3_coding_azure.py'),
        '--paper_name', paper_name,
        '--gpt_version', gpt_version,
        '--pdf_json_path', pdf_json_path,
        '--output_dir', output_dir,
        '--output_repo_dir', output_repo_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def create_zip_file(source_dir, output_path):
    """Create a zip file of the generated repository."""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)


def main():
    """Main application function."""
    initialize_session_state()
    config = load_config()
    
    # Header
    st.title("📄 Paper2Code Chatbot")
    st.markdown("""
    Upload a research paper and let AI generate a complete code implementation.
    The generated code will be available for download as a zip file.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Check Azure credentials
        if not validate_azure_credentials():
            st.stop()
        
        st.success("✓ Azure OpenAI credentials configured")
        
        # Model selection
        model_name = st.selectbox(
            "Select Model",
            ["gpt-4", "gpt-4-turbo", "gpt-35-turbo"],
            help="Select the Azure OpenAI deployment model"
        )
        
        st.divider()
        
        st.header("About")
        st.markdown("""
        **Paper2Code** transforms research papers into working code through:
        1. **Planning**: Creates implementation strategy
        2. **Analysis**: Performs detailed logic analysis
        3. **Coding**: Generates complete code repository
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Upload Paper")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload research paper (JSON format)",
            type=['json'],
            help="Upload a preprocessed paper in JSON format (from s2orc-doc2json)"
        )
        
        if uploaded_file:
            # Paper name input
            paper_name = st.text_input(
                "Paper Name",
                value=uploaded_file.name.replace('.json', '').replace('_cleaned', ''),
                help="Enter a name for this paper (used for output folder)"
            )
            
            if st.button("🚀 Generate Code", type="primary", use_container_width=True):
                if not paper_name:
                    st.error("Please provide a paper name")
                else:
                    # Create temporary directories
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    base_output_dir = os.path.join("outputs", f"{paper_name}_{timestamp}")
                    output_dir = os.path.join(base_output_dir, "artifacts")
                    output_repo_dir = os.path.join(base_output_dir, "repo")
                    
                    os.makedirs(output_dir, exist_ok=True)
                    os.makedirs(output_repo_dir, exist_ok=True)
                    
                    # Save uploaded file
                    pdf_json_path = os.path.join(output_dir, f"{paper_name}_input.json")
                    with open(pdf_json_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    st.session_state.paper_name = paper_name
                    st.session_state.output_dir = output_dir
                    st.session_state.output_repo_dir = output_repo_dir
                    
                    # Processing stages
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Stage 1: Planning
                        status_text.text("Stage 1/3: Planning...")
                        progress_bar.progress(0.1)
                        
                        with st.expander("Planning Stage Details", expanded=False):
                            st.info("Creating implementation strategy...")
                        
                        success, stdout, stderr = run_planning_stage(
                            paper_name, pdf_json_path, output_dir, model_name
                        )
                        
                        if not success:
                            st.error(f"Planning stage failed: {stderr}")
                            st.stop()
                        
                        progress_bar.progress(0.33)
                        
                        # Stage 2: Analysis
                        status_text.text("Stage 2/3: Analysis...")
                        
                        with st.expander("Analysis Stage Details", expanded=False):
                            st.info("Performing detailed logic analysis...")
                        
                        success, stdout, stderr = run_analysis_stage(
                            paper_name, pdf_json_path, output_dir, model_name
                        )
                        
                        if not success:
                            st.error(f"Analysis stage failed: {stderr}")
                            st.stop()
                        
                        progress_bar.progress(0.66)
                        
                        # Stage 3: Coding
                        status_text.text("Stage 3/3: Generating Code...")
                        
                        with st.expander("Coding Stage Details", expanded=False):
                            st.info("Generating complete code repository...")
                        
                        success, stdout, stderr = run_coding_stage(
                            paper_name, pdf_json_path, output_dir, output_repo_dir, model_name
                        )
                        
                        if not success:
                            st.error(f"Coding stage failed: {stderr}")
                            st.stop()
                        
                        progress_bar.progress(1.0)
                        status_text.text("✓ Processing complete!")
                        
                        # Success message
                        st.success("🎉 Code generation complete!")
                        
                        # Store generated files
                        st.session_state.generated_files = []
                        for root, dirs, files in os.walk(output_repo_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                rel_path = os.path.relpath(file_path, output_repo_dir)
                                st.session_state.generated_files.append(rel_path)
                        
                    except Exception as e:
                        st.error(f"Error during processing: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
    
    with col2:
        st.header("Generated Files")
        
        if st.session_state.generated_files:
            st.success(f"✓ {len(st.session_state.generated_files)} files generated")
            
            # Show file list
            with st.expander("View Files", expanded=True):
                for file in st.session_state.generated_files:
                    st.text(f"📄 {file}")
            
            # Create download button
            if st.session_state.output_repo_dir:
                zip_path = os.path.join(
                    st.session_state.output_dir,
                    f"{st.session_state.paper_name}_code.zip"
                )
                
                if st.button("📦 Prepare Download", use_container_width=True):
                    with st.spinner("Creating zip file..."):
                        create_zip_file(st.session_state.output_repo_dir, zip_path)
                        st.success("Zip file created!")
                
                if os.path.exists(zip_path):
                    with open(zip_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Code",
                            data=f,
                            file_name=f"{st.session_state.paper_name}_code.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
        else:
            st.info("Upload a paper and generate code to see files here")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9em;">
    Powered by Azure OpenAI | Paper2Code Multi-Agent System
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
