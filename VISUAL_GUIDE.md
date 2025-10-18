# Visual Guide: Using the Paper2Code Chatbot

This guide provides step-by-step visual instructions for using the Paper2Code chatbot application.

## Before You Start

Ensure you have:
- ✅ Python 3.8+ installed
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Azure OpenAI credentials configured
- ✅ A paper in JSON format ready to upload

## Step-by-Step Guide

### Step 1: Launch the Application

```bash
streamlit run chatbot_app.py
```

**What you'll see:**
- Browser opens automatically to `http://localhost:8501`
- Title: "📄 Paper2Code Chatbot"
- Description of the application
- Upload area on the left
- Empty "Generated Files" panel on the right

### Step 2: Check Credentials (Sidebar)

**Left sidebar shows:**
- ✓ Azure OpenAI credentials configured (green checkmark)
  - If not configured: Red error message with instructions
- Model selection dropdown
  - Options: gpt-4, gpt-4-turbo, gpt-35-turbo
- About section with pipeline description

**What to do:**
- Verify green checkmark appears
- Select your preferred model
- If error appears, set environment variables and refresh

### Step 3: Upload Your Paper

**Main area - Upload Section:**
- "Upload Paper" header
- File uploader widget: "Upload research paper (JSON format)"
- Browse button to select file

**What to do:**
1. Click "Browse files" button
2. Navigate to your JSON file (e.g., `examples/Transformer_cleaned.json`)
3. Select the file
4. File name appears below the uploader

### Step 4: Enter Paper Name

**After upload, you'll see:**
- Text input field: "Paper Name"
- Pre-filled with filename (without extension)
- Help text: "Enter a name for this paper (used for output folder)"

**What to do:**
1. Review the auto-filled name
2. Modify if desired (e.g., "Transformer" or "BERT_Implementation")
3. Use descriptive names (no spaces recommended)

### Step 5: Generate Code

**You'll see:**
- Large blue button: "🚀 Generate Code"
- Spans full width of the column

**What to do:**
1. Click "🚀 Generate Code" button
2. Button becomes disabled during processing
3. Processing begins immediately

### Step 6: Monitor Progress

**During processing, you'll see:**

**Progress Bar:**
- Shows 0% → 33% → 66% → 100%
- Current stage displayed above bar:
  - "Stage 1/3: Planning..."
  - "Stage 2/3: Analysis..."
  - "Stage 3/3: Generating Code..."

**Expandable Sections (below progress):**
- "Planning Stage Details" (collapsible)
  - Info message: "Creating implementation strategy..."
- "Analysis Stage Details" (collapsible)
  - Info message: "Performing detailed logic analysis..."
- "Coding Stage Details" (collapsible)
  - Info message: "Generating complete code repository..."

**Processing time:**
- Planning: ~2-5 minutes
- Analysis: ~3-7 minutes
- Coding: ~5-10 minutes
- **Total: 10-15 minutes** (varies by paper complexity)

### Step 7: View Generated Files (Right Panel)

**When complete, right panel shows:**

**Header:**
- "Generated Files"
- Green success message: "✓ 6 files generated" (number varies)

**File List (expandable):**
- "View Files" section (expanded by default)
- List of generated files:
  ```
  📄 main.py
  📄 model.py
  📄 dataset_loader.py
  📄 trainer.py
  📄 evaluation.py
  📄 config.yaml
  📄 README.md
  ```

**What this means:**
- All code has been generated
- Files are ready for download
- No code shown in chat (as requested)

### Step 8: Prepare Download

**You'll see:**
- Button: "📦 Prepare Download"
- Full width button in right panel

**What to do:**
1. Click "📦 Prepare Download"
2. Spinner appears: "Creating zip file..."
3. Success message: "Zip file created!"
4. Download button appears below

**Processing time:** ~2-5 seconds

### Step 9: Download Generated Code

**You'll see:**
- Button: "⬇️ Download Code"
- Full width button in right panel
- Below the "Prepare Download" button

**What to do:**
1. Click "⬇️ Download Code"
2. Browser download dialog appears
3. Save file to your desired location
4. File name: `{PaperName}_code.zip`

**What you get:**
- ZIP file containing complete repository
- All generated code files
- Configuration files
- Documentation

### Step 10: Extract and Use Code

**After download:**

```bash
# Extract the ZIP file
unzip Transformer_code.zip -d Transformer_code

# Navigate to the directory
cd Transformer_code

# View the contents
ls -la

# Expected structure:
# main.py
# model.py
# dataset_loader.py
# trainer.py
# evaluation.py
# config.yaml
# README.md
```

**Next steps:**
1. Read the generated README.md
2. Review config.yaml for hyperparameters
3. Install dependencies (if any mentioned)
4. Prepare your dataset
5. Run the code!

## Troubleshooting Visuals

### Error: Missing Credentials

**What you'll see:**
- Red error box in sidebar
- Message: "Missing required environment variables: ..."
- Info box with instructions

**How to fix:**
1. Set environment variables as shown
2. Close browser tab
3. Stop Streamlit (Ctrl+C in terminal)
4. Restart: `streamlit run chatbot_app.py`

### Error: Upload Failed

**What you'll see:**
- Red error message below upload button
- Error description

**Common causes:**
- Wrong file format (must be JSON)
- File too large
- Corrupted JSON

**How to fix:**
- Verify file is valid JSON
- Try a different file
- Check file size

### Error: Processing Failed

**What you'll see:**
- Red error box after progress bar
- Error message from specific stage
- Stack trace (if enabled)

**What to do:**
1. Check error message
2. Verify Azure credentials
3. Check deployment quota
4. Try again with simpler paper
5. Review logs in expandable sections

## Tips for Best Experience

### Visual Cues

✓ **Green checkmark** = Success
✗ **Red X** = Error
🔄 **Spinner** = Processing
📄 **Document icon** = File
📦 **Package icon** = Archive

### Color Coding

- **Blue buttons** = Primary actions
- **Green messages** = Success
- **Red messages** = Errors
- **Yellow messages** = Warnings
- **Gray text** = Helper text

### Progress Indicators

- **Progress bar** = Overall completion
- **Stage text** = Current operation
- **Expandable sections** = Detailed logs
- **File count** = Generation progress

## Keyboard Shortcuts

In Streamlit applications:
- `Ctrl+C` (in terminal) = Stop server
- `F5` or `Ctrl+R` = Refresh page
- Browser's download shortcut = Faster download

## Screen Layout

```
┌─────────────────────────────────────────────────────┐
│  📄 Paper2Code Chatbot                              │
│  Description text...                                │
├─────────────────────┬───────────────────────────────┤
│  Upload Paper       │  Generated Files              │
│                     │                               │
│  [Upload Widget]    │  [Empty or File List]         │
│                     │                               │
│  Paper Name: [...]  │  [Prepare Download Button]    │
│                     │                               │
│  [Generate Button]  │  [Download Button]            │
│                     │                               │
│  [Progress Bar]     │                               │
│  [Status Text]      │                               │
│  [Stage Details]    │                               │
└─────────────────────┴───────────────────────────────┘
│                                                     │
│  Sidebar:                                           │
│  - Settings                                         │
│  - Credentials check                                │
│  - Model selection                                  │
│  - About section                                    │
└─────────────────────────────────────────────────────┘
```

## Summary

The chatbot interface provides a streamlined, visual way to:
1. ✅ Upload papers with drag-and-drop
2. ✅ Monitor progress with visual feedback
3. ✅ Download complete code repositories
4. ✅ Avoid clutter (no code in chat)
5. ✅ Get organized output (ZIP files)

All without touching the command line! 🎉
